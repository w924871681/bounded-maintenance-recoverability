"""Re-execute the six original non-anchor MSA source-training branches.

The four compact-bank identities and two new formal-bank identities retain
their distinct original AST statement bodies. No protected-anchor copying
branch is executed. Selection/NAS provenance is a separate acceptance gate.
"""
import argparse,ast,hashlib,importlib,json,os,subprocess,sys,traceback
from pathlib import Path
from retrain_external_sources import install_read_guard
B=Path(__file__).resolve().parent
SOURCE=B/'upstream_source_training/legacy_msa'
IDENTITIES=(1,6,46,55,56,62)

def read(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2),'utf-8')

def original_branch(index):
    compact=index in (1,6,55,56)
    rel='source_prior_bank/pipeline.py' if compact else 'formal_protocol/pipeline.py'
    path=SOURCE/rel;tree=ast.parse(path.read_text('utf-8-sig'),filename=str(path))
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==('build_strong_bank' if compact else 'bank'))
    choices=[n for n in ast.walk(function) if isinstance(n,ast.If) and ast.unparse(n.test)=='idx == CFG.anchor_arch_idx']
    if len(choices)!=1 or not choices[0].orelse:raise RuntimeError('Original training branch is ambiguous')
    body=choices[0].orelse
    if any(isinstance(n,(ast.Break,ast.Continue,ast.Return)) for x in body for n in ast.walk(x)):
        raise RuntimeError('Training branch depends on outer control flow')
    module=ast.Module(body=body,type_ignores=[])
    return rel,module,dict(source_file=rel,source_sha256=sha(path),
        branch_ast_sha256=hashlib.sha256(ast.dump(module,include_attributes=False).encode()).hexdigest(),
        first_line=body[0].lineno,last_line=body[-1].end_lineno,ast_statements_edited=False)

def verify_sources():
    for row in read(SOURCE/'SOURCE_COLLECTION.json')['files']:
        path=(SOURCE/row['file']).resolve()
        if not path.is_relative_to(SOURCE) or sha(path)!=row['sha256']:
            raise RuntimeError('Frozen collected source changed: '+row['file'])
    audit=read(B/'upstream_source_training/SOURCE_RECIPE_AUDIT.json')
    bound={r['identity']:r for r in audit['imported_identities']}
    checks=[]
    for index in IDENTITIES:
        target=bound[f'msa_a{index}_pt']
        if sha(B/target['checkpoint'])!=target['sha256']:raise RuntimeError('Frozen target model changed')
        _,body,provenance=original_branch(index)
        compile(body,str(SOURCE/provenance['source_file']),'exec')
        checks.append(dict(architecture=index,expected_sha256=target['sha256'],**provenance))
    return checks

def environment(out):
    sys.dont_write_bytecode=True
    roots=[Path(sys.base_prefix).resolve(),Path(sys.prefix).resolve()]
    sys.path[:]=[str(SOURCE)]+[p for p in sys.path if p and any(Path(p).resolve().is_relative_to(r) for r in roots)]
    for key in ('TEMP','TMP','TORCH_HOME','CUDA_CACHE_PATH','MPLCONFIGDIR'):
        path=out/'cache'/key;path.mkdir(parents=True,exist_ok=True);os.environ[key]=str(path)
    os.chdir(out);install_read_guard(out)

def main():
    parser=argparse.ArgumentParser(__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mode',choices=('verify','preflight','train'),required=True)
    parser.add_argument('--device',choices=('cpu','cuda'),default='cuda')
    parser.add_argument('--safe-mode',choices=('default','gru-native','gru-cpu'),default='gru-native')
    parser.add_argument('--worker-architecture',type=int,choices=IDENTITIES,help=argparse.SUPPRESS)
    args=parser.parse_args();out=args.output.resolve()
    if out.exists() or out.is_relative_to(B) or B.is_relative_to(out):raise RuntimeError('New output outside package required')
    out.mkdir(parents=True)
    try:
        bindings=verify_sources();write(out/'SOURCE_BINDINGS.json',bindings)
        if args.mode=='verify':
            write(out/'RECEIPT.json',dict(status='PASS_SIX_SOURCE_BRANCH_STATIC_BINDINGS_ONLY',source_models_retrained=False));return
        if args.mode=='train' and args.worker_architecture is None:
            checks=[]
            for index in IDENTITIES:
                target=out/f'a{index}'
                cmd=[sys.executable,'-X','utf8','-B',str(Path(__file__).resolve()),'--mode','train','--worker-architecture',str(index),
                     '--output',str(target),'--device',args.device,'--safe-mode',args.safe_mode]
                with (out/f'a{index}.log').open('x',encoding='utf-8') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
                receipt=read(target/'RECEIPT.json')
                if receipt['status']!='PASS_ORIGINAL_MSA_SOURCE_BRANCH_EXACT':raise RuntimeError('Source branch comparison did not pass')
                checks.append(receipt)
            write(out/'RECEIPT.json',dict(status='PASS_SIX_MSA_SOURCE_MODELS',checks=checks,source_models_retrained=True,
                architecture_selection_reproduced=False,full_package_accepted=False));return
        environment(out)
        import torch
        modules={name:importlib.import_module(name+'.pipeline') for name in ('source_prior_bank','formal_protocol')}
        for name,m in modules.items():
            if (m.CFG.train_seed,m.CFG.source_centers,m.CFG.source_epochs,m.CFG.source_lr,m.CFG.source_batch_size,m.CFG.source_weight_decay)!=(2904,20,50,.001,64,0.0):
                raise RuntimeError('Unexpected frozen source recipe: '+name)
        if args.mode=='preflight':
            write(out/'RECEIPT.json',dict(status='PASS_SIX_SOURCE_IMPORTS_AND_FROZEN_RECIPE_ONLY',python=sys.version,
                torch=str(torch.__version__),source_models_retrained=False));return
        index=args.worker_architecture;rel,body,provenance=original_branch(index)
        m=modules[rel.split('/')[0]]
        cfg,cache,A,requested,safe=m.build_runtime(args.device,args.safe_mode,())
        X0,*_=m.get_source_training_support_validation(cfg,cache,0,1,20)
        target=out/f'formal_h1_a{index}.pt'
        ns=dict(m.__dict__)
        ns.update(cfg=cfg,cache=cache,A=A,requested=requested,safe=safe,H=1,idx=index,spec=A[index],
                  L=int(cfg.main.task.L),input_dim=int(X0.shape[-1]),epochs=m.CFG.source_epochs,
                  out_file=str(target),dst=target,output_root=out,jobs=[(1,index)],job_no=1,
                  root=str(out),manifest={'assets':{}},key=f'h1_a{index}')
        # Only the previously hash-verified original else-body is compiled;
        # optimizer, batches, seeds, backend context and all epochs unchanged.
        exec(compile(body,str(SOURCE/rel),'exec'),ns,ns)
        reference=B/f'repository/imported/msa_dti/bank/formal_h1_a{index}.pt'
        left=torch.load(reference,map_location='cpu',weights_only=True);right=torch.load(target,map_location='cpu',weights_only=True)
        exact=left.keys()==right.keys() and all(left[k].shape==right[k].shape and left[k].dtype==right[k].dtype and torch.equal(left[k],right[k]) for k in left)
        receipt=dict(status='PASS_ORIGINAL_MSA_SOURCE_BRANCH_EXACT' if exact else 'FAIL_SOURCE_STATE_DIFFERENCE',
                     architecture=index,state_tensors_exact=exact,tolerance=0,new_sha256=sha(target),original_sha256=sha(reference),
                     source_models_retrained=True,source_branch=provenance,device=args.device,safe_mode=args.safe_mode,
                     python=sys.version,torch=str(torch.__version__),full_package_accepted=False)
        write(out/'SOURCE_COMPARISON.json',receipt)
        if not exact:raise RuntimeError('Source state differs; preserve outputs and diagnose')
        write(out/'RECEIPT.json',receipt)
    except BaseException:
        write(out/'FAILURE.json',dict(status='FAIL',traceback=traceback.format_exc(),mode=args.mode,full_package_accepted=False));raise

if __name__=='__main__':main()
