"""Portable P6 and P7.6B full estimator generation, fitting and comparison.

Original scientific modules remain byte-identical. Git bookkeeping is replaced
by explicit SHA256 seals in a fresh private workspace, not by unconditional
success. Historical reference outputs are never copied into target namespaces.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

PACKAGE=Path(__file__).resolve().parent
REPO=PACKAGE/'repository'
STAGES=('p6_materialize','p6_cv','p6_tests','p6_finalize','p6_compare',
        'p7_fit','p7_fit_freeze','p7_open_validation','p7_validation','p7_finalize','p7_compare')
RESET_PREFIXES=('results/p6/','results/p7_6b/','verification/',
                'artifacts/p6_recoverability','artifacts/p7_6b_A')
RESET_STEMS=('configs/p6_selected_estimator','audits/P6_ESTIMATOR_FREEZE',
             'audits/P6_SCIENTIFIC_AUDIT','audits/P7_6B_FIT_FREEZE',
             'audits/P7_6B_VALIDATION_OPENING','audits/P7_6B_FINAL_SCIENTIFIC_AUDIT',
             'audits/P7_6B_FIT_SCIENTIFIC_STOP','reports/P6_ESTIMATOR_FITTING_AND_SELECTION',
             'reports/P6_FIGURE_VISUAL_QA',
             'reports/P7_6B_DESIGN_BASED_REPLICATION')


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    temp=p.with_suffix(p.suffix+'.portable.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(temp,p)


def prepare(out):
    out.mkdir(parents=True,exist_ok=False);work=out/'workspace';work.mkdir()
    assembly=read(PACKAGE/'ASSEMBLY_MANIFEST.json')['files'];files={};excluded=[]
    for src in sorted(REPO.rglob('*')):
        if src.is_symlink() or getattr(src.lstat(),'st_file_attributes',0)&0x400:raise RuntimeError('Linked input is not portable: '+str(src))
        if not src.is_file():continue
        rel=src.relative_to(REPO).as_posix()
        if '__pycache__' in src.parts or '.git' in src.parts or src.suffix=='.pyc':continue
        if rel.startswith(RESET_PREFIXES+RESET_STEMS):excluded.append(rel);continue
        digest=sha(src);expected=assembly.get('repository/'+rel,{}).get('sha256')
        if expected is None:
            if rel.startswith(('core/','scripts/','configs/','imported/','tests/','vendor/')):raise RuntimeError('Unregistered scientific input: '+rel)
            excluded.append(rel);continue
        if expected!=digest:raise RuntimeError('Changed registered repository input: '+rel)
        dst=work/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        if sha(dst)!=digest:raise RuntimeError('Private input copy mismatch: '+rel)
        files[rel]=digest
    for folder in ('results/p6','results/p7_6b','artifacts','audits','reports','configs'):(work/folder).mkdir(parents=True,exist_ok=True)
    write(out/'INPUT_IDENTITY.json',dict(files=files,excluded_reference_outputs=excluded,
          scientific_implementations_modified=False,reference_root_is_package_local=True))
    write(out/'PORTABLE_SEALS.json',dict(files=files,events=[]))
    write(out/'PREPARATION_RECEIPT.json',dict(status='PASS_FRESH_ESTIMATOR_WORKSPACE_ONLY',files=len(files),
          copied_bytes=sum((work/r).stat().st_size for r in files),training_performed=False,
          expected_p6_trajectories=360,expected_p7_fit_trajectories=432,expected_p7_validation_trajectories=432,
          output_namespaces_empty=not any((work/'results/p6').iterdir()) and not any((work/'results/p7_6b').iterdir())))


def runtime(out):
    work=out/'workspace';sys.dont_write_bytecode=True
    for key in ('TEMP','TMP','MPLCONFIGDIR','TORCH_HOME','CUDA_CACHE_PATH'):
        target=out/'cache'/key;target.mkdir(parents=True,exist_ok=True);os.environ[key]=str(target)
    os.environ['MPLBACKEND']='Agg';os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
    os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
    roots=[Path(sys.prefix).resolve(),Path(sys.base_prefix).resolve()]
    sys.path[:]=[str(work),str(PACKAGE)]+[p for p in sys.path if p and any(Path(p).resolve().is_relative_to(r) for r in roots)]
    os.chdir(work)
    def guard(event,args):
        if event=='subprocess.Popen':
            command=args[1]
            if isinstance(command,(list,tuple)) and any(str(x).lower() in ('git','git.exe') for x in command[:1]):
                raise RuntimeError('Git execution prohibited in portable estimator run')
        if event!='open' or not args or isinstance(args[0],int):return
        raw=os.fsdecode(args[0])
        if raw.casefold()==os.devnull.casefold():return
        p=Path(raw).resolve();mode=args[1];flags=args[2] if len(args)>2 else 0
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT))
        if writing and not p.is_relative_to(out):raise RuntimeError('Write outside private estimator output: '+str(p))
        if not any(p.is_relative_to(r) for r in [out,PACKAGE,*roots]):raise RuntimeError('External read rejected: '+str(p))
    sys.addaudithook(guard)
    import torch
    from scripts import run_p6 as p6
    from scripts import run_p7_6b as runner
    from scripts import p7_6b_science as science
    for module in (p6,runner,science):
        if not Path(module.__file__).resolve().is_relative_to(work):raise RuntimeError('Imported wrong scientific source')
    def bound(path):
        path=Path(path).resolve()
        if not path.is_relative_to(work):return False
        expected=read(out/'PORTABLE_SEALS.json')['files'].get(path.relative_to(work).as_posix())
        return path.is_file() and expected is not None and sha(path)==expected
    def seal(paths,message):
        ledger=read(out/'PORTABLE_SEALS.json');entries={}
        for p in paths:
            p=Path(p).resolve()
            if not p.is_relative_to(work):raise RuntimeError('Seal outside workspace')
            rel=p.relative_to(work).as_posix();digest=sha(p)
            if rel in ledger['files'] and ledger['files'][rel]!=digest:raise RuntimeError('Previously sealed input changed: '+rel)
            entries[rel]=digest
        ledger['files'].update(entries);ledger['events'].append(dict(message=message,files=entries))
        write(out/'PORTABLE_SEALS.json',ledger)
        return 'portable-sha256:'+sha(out/'PORTABLE_SEALS.json')
    runner.git_bound=bound;science._commit=seal
    def attributes():
        expected=read(work/'audits/P6_ESTIMATOR_FREEZE.json')['files']['.gitattributes']
        if sha(work/'.gitattributes')!=expected:raise RuntimeError('P6 original attributes bytes changed')
    runner.install_p6_attribute_provenance_compatibility=attributes
    # Only replace Git commit metadata lookup in original P6 freeze function.
    module=ast.parse((work/'scripts/run_p6.py').read_text(encoding='utf-8'))
    fn=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='freeze_artifacts')
    class ProvenanceLookup(ast.NodeTransformer):
        count=0
        def visit_Call(self,node):
            if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='subprocess' and node.func.attr=='check_output':
                self.count+=1
                return ast.copy_location(ast.Constant('portable-sha256:'+sha(out/'INPUT_IDENTITY.json')),node)
            return self.generic_visit(node)
    adapter=ProvenanceLookup();fn=adapter.visit(fn)
    if adapter.count!=1:raise RuntimeError('P6 provenance adaptation no longer matches original source')
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(work/'scripts/run_p6.py'),'exec'),p6.__dict__)
    # Relocate only the original figure-helper path constants. Functions and
    # export/visual-review gates otherwise retain their original AST statements.
    class FigurePath(ast.NodeTransformer):
        count=0
        def visit_Constant(self,node):
            if node.value=='C:/Users/92487/.codex/skills/scipilot-figure-skill/scripts':
                self.count+=1
                return ast.copy_location(ast.Constant(str(work/'vendor/figure_helpers')),node)
            return node
    paths=FigurePath()
    for original in ast.parse((work/'scripts/run_p6.py').read_text(encoding='utf-8')).body:
        if isinstance(original,ast.FunctionDef) and any(isinstance(n,ast.Constant) and n.value=='C:/Users/92487/.codex/skills/scipilot-figure-skill/scripts' for n in ast.walk(original)):
            relocated=paths.visit(original)
            exec(compile(ast.fix_missing_locations(ast.Module(body=[relocated],type_ignores=[])),str(work/'scripts/run_p6.py'),'exec'),p6.__dict__)
    if paths.count!=2:raise RuntimeError('Original P6 figure dependency locations changed')
    write(out/'PORTABILITY_RECEIPT.json',dict(scientific_code_files_unchanged=True,
          original_p6_source_sha256=sha(work/'scripts/run_p6.py'),
          git_binding_replacement='SHA256 checked immutable input/output seal ledger',
          p6_git_metadata_replacement='portable-sha256 identity, explicitly not a Git commit',
          attributes_replacement='original exact historical bytes; no hash spoofing',
          numerical_functions_replaced=False,figure_helper_path_constants_relocated=paths.count,
          execution_worker_policy='Serial full trajectories; original CUDA/float32/deterministic seeds and torch threads unchanged',torch=str(torch.__version__),python=sys.version))
    return p6,runner,science,seal


def exact_payload(left,right,torch):
    if isinstance(left,torch.Tensor):
        return isinstance(right,torch.Tensor) and left.dtype==right.dtype and left.shape==right.shape and torch.equal(left,right)
    if isinstance(left,dict):return isinstance(right,dict) and left.keys()==right.keys() and all(exact_payload(left[k],right[k],torch) for k in left)
    if isinstance(left,(list,tuple)):return type(left)==type(right) and len(left)==len(right) and all(exact_payload(x,y,torch) for x,y in zip(left,right))
    return left==right


def compare_csv(a,b):
    import pandas as pd
    left=pd.read_csv(a);right=pd.read_csv(b)
    # core/p7.py records wall-clock telemetry with perf_counter; neither field
    # enters estimator features, labels, selection or scientific pass criteria.
    runtime_fields=['decision_runtime_actual_s','decision_runtime_standalone_estimate_s']
    omitted=[x for x in runtime_fields if x in left.columns]
    if set(left.columns)!=set(right.columns):raise RuntimeError('CSV schema differs: '+a.name)
    if omitted:
        import numpy as np
        for frame in (left,right):
            if not np.isfinite(frame[omitted].to_numpy()).all() or (frame[omitted]<0).any().any():raise RuntimeError('Invalid runtime telemetry')
        left=left.drop(columns=omitted);right=right.drop(columns=omitted)
    pd.testing.assert_frame_equal(left,right,check_exact=True)
    return dict(file=a.name,rows=len(left),columns=len(left.columns),runtime_telemetry_excluded=omitted,comparison='exact parsed scientific values; no tolerance relaxation')


def compare_p6(out):
    import torch
    work=out/'workspace';checks=[]
    for name in ('stage_records.csv','candidate_cv_summary.csv','selected_feature_matrix.csv','cv_predictions.csv','metrics_by_center.csv','metrics_by_scenario.csv','fold_metrics.csv'):
        checks.append(compare_csv(work/'results/p6'/name,REPO/'results/p6'/name))
    actual=read(work/'configs/p6_selected_estimator.json');original=read(REPO/'configs/p6_selected_estimator.json')
    for field in ('selected_config_id','selected_model_family','K_S','K_L','ridge_alpha','pass_gate'):
        if actual[field]!=original[field]:raise RuntimeError('P6 selection differs: '+field)
    if not actual.get('final_refit_performed'):raise RuntimeError('P6 final fit did not happen')
    if read(work/actual['scaler_artifact'])!=read(REPO/original['scaler_artifact']):raise RuntimeError('P6 scaler differs')
    if actual['selected_model_family']!='MLP':raise RuntimeError('Historical MLP selection changed')
    if not exact_payload(torch.load(work/actual['estimator_artifact'],weights_only=True,map_location='cpu'),torch.load(REPO/original['estimator_artifact'],weights_only=True,map_location='cpu'),torch):raise RuntimeError('P6 model tensor or metadata differs')
    write(out/'P6_COMPARISON.json',dict(status='PASS_FULL_P6_GENERATION_CV_TESTS_REFIT_EXACT',tables=checks,trajectories=360,model_state_tolerance=0))


def compare_p7(out):
    import torch
    work=out/'workspace';refs=PACKAGE/'upstream_source_training/estimator_references';checks=[]
    for rep in ('A0','A1'):
        name=f'artifacts/p7_6b_{rep}_estimator.pt'
        if not exact_payload(torch.load(work/name,weights_only=True,map_location='cpu'),torch.load(refs/name,weights_only=True,map_location='cpu'),torch):raise RuntimeError('P7.6B state differs: '+rep)
        name=f'artifacts/p7_6b_{rep}_scaler.json'
        if read(work/name)!=read(refs/name):raise RuntimeError('P7.6B scaler differs: '+rep)
    for name in ('fit_oof_predictions.csv','fit_metrics.csv','validation_predictions.csv','validation_metrics.csv','paired_bootstrap_samples.csv','paired_a1_vs_a0.csv','leave_one_center_out.csv'):
        checks.append(compare_csv(work/'results/p7_6b'/name,refs/'results/p7_6b'/name))
    actual=read(work/'audits/P7_6B_FINAL_SCIENTIFIC_AUDIT.json');old=read(REPO/'audits/P7_6B_FINAL_SCIENTIFIC_AUDIT.json')
    for key in ('verdict','fit_absolute_checks','validation_checks','paired_point_estimates','paired_intervals','transport_deterioration_stop','leave_one_center_all_pass'):
        if actual[key]!=old[key]:raise RuntimeError('P7.6B final scientific audit differs: '+key)
    write(out/'P7_COMPARISON.json',dict(status='PASS_FULL_P7_6B_GENERATION_FITTING_VALIDATION_EXACT',fit_trajectories=432,validation_trajectories=432,tables=checks,model_state_tolerance=0,verdict=actual['verdict']))


def stage(out,name):
    work=out/'workspace';receipts=out/'stages';receipts.mkdir(exist_ok=True)
    index=STAGES.index(name)
    if not (out/'SOURCE_TRAINING_EVIDENCE.json').exists():raise RuntimeError('Upstream source training evidence required before estimator execution')
    if index and not (receipts/(STAGES[index-1]+'.json')).exists():raise RuntimeError('Previous stage not complete')
    if (receipts/(name+'.json')).exists():raise RuntimeError('Stage already complete; no duplicate execution')
    p6,runner,science,seal=runtime(out)
    if name=='p6_materialize':p6.materialize()
    elif name=='p6_cv':
        import pandas as pd
        selection=p6.cross_validate(pd.read_csv(p6.RESULTS/'stage_records.csv'))
        if not selection['pass_gate']['pass']:raise RuntimeError('Original P6 scientific gate failed')
    elif name=='p6_tests':
        if not p6.run_tests()['passed']:raise RuntimeError('Original P6 tests failed')
    elif name=='p6_finalize':
        selection=p6.finalize()
        if not selection.get('final_refit_performed'):raise RuntimeError('P6 final refit not performed')
        freeze=read(p6.FREEZE)
        seal([work/rel for rel in freeze['files']]+[p6.FREEZE,p6.FREEZE_SHA],'P6 fresh numerical freeze')
    elif name=='p6_compare':compare_p6(out)
    elif name in ('p7_fit','p7_validation'):
        phase='fit' if name=='p7_fit' else 'validation'
        assignment,_=runner.preflight(phase=phase,require_opening=phase=='validation')
        runner.require_execution_authorization(phase)
        if phase=='fit':runner.require_r0_fit_release()
        config=read(runner.EXECUTION_CONFIG);runner._worker_init(config['EXECUTION_DEVICE'],config['TORCH_NUM_THREADS'])
        tasks=runner.canonical_tasks(assignment,phase)
        if len(tasks)!=432:raise RuntimeError('Original full phase coverage differs')
        started=time.monotonic()
        for number,task in enumerate(tasks,1):
            runner._trajectory_worker(phase,task,sha(runner.EXECUTION_CONFIG))
            write(out/'PROGRESS.json',dict(stage=name,completed=number,expected=432,elapsed_seconds=time.monotonic()-started,
                  execution_workers=1,frozen_device=config['EXECUTION_DEVICE'],scientific_settings_changed=False))
    elif name=='p7_fit_freeze':science.fit_freeze()
    elif name=='p7_open_validation':science.open_validation()
    elif name=='p7_finalize':science.finalize()
    elif name=='p7_compare':compare_p7(out)
    write(receipts/(name+'.json'),dict(status='PASS_STAGE',stage=name,wrapper_sha256=sha(Path(__file__)),full_pipeline=False))


def source_evidence(out,runs):
    definitions=(('external','retrain_external_sources.py','RECEIPT.json','PASS_TWO_EXTERNAL_H1_SOURCE_MODELS',2),
                 ('r3','retrain_source_pair.py','SOURCE_COMPARISON.json','PASS_THREE_SOURCE_REGIME_MODELS',3),
                 ('msa','retrain_msa_sources.py','RECEIPT.json','PASS_SIX_MSA_SOURCE_MODELS',6))
    evidence=[];folders=[]
    for i,(label,script,receipt_name,expected,count) in enumerate(definitions):
        folder=Path(runs[i]).resolve() if runs else out/'source_training'/label
        if not runs:
            log=out/(label+'_source_training.log')
            with log.open('x',encoding='utf-8') as stream:
                subprocess.run([sys.executable,'-X','utf8','-B',str(PACKAGE/script),'--mode','train','--output',str(folder)],stdout=stream,stderr=subprocess.STDOUT,check=True)
        folders.append(folder)
    import torch
    for (label,script,receipt_name,expected,count),folder in zip(definitions,folders):
        receipt=read(folder/receipt_name)
        if receipt['status']!=expected or len(receipt['checks'])!=count:raise RuntimeError('Source training evidence incomplete: '+label)
        checks=receipt['checks']
        if not all(x.get('state_tensors_exact') is True for x in checks):raise RuntimeError('Source state equality not proven')
        available={sha(p):p for p in folder.rglob('*.pt') if p.is_file()}
        references={sha(p):p for p in REPO.rglob('*.pt') if p.is_file() and 'verification' not in p.parts}
        for check in checks:
            new=available.get(check.get('new_sha256'));old=references.get(check.get('original_sha256'))
            if new is None or old is None:raise RuntimeError('New or reference source checkpoint bytes missing')
            if not exact_payload(torch.load(new,map_location='cpu',weights_only=True),torch.load(old,map_location='cpu',weights_only=True),torch):raise RuntimeError('Independent source tensor comparison failed')
        evidence.append(dict(kind=label,receipt=str(folder/receipt_name),receipt_sha256=sha(folder/receipt_name),new_model_hashes=[x['new_sha256'] for x in checks]))
    write(out/'SOURCE_TRAINING_EVIDENCE.json',dict(status='PASS_ELEVEN_SOURCE_IDENTITY_TRAINING_RECEIPTS_AND_BYTES',evidence=evidence,
          storage_identity_policy='Use package checkpoint serialization only after exact newly trained tensor equality; frozen byte identities required by original manifests remain intact.',source_selection_reproduced=False))


def main():
    parser=argparse.ArgumentParser(__doc__);parser.add_argument('--mode',choices=('prepare','preflight','full'),default='full')
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--internal-stage',choices=STAGES)
    parser.add_argument('--check-portability',action='store_true',help='Test hash seals and unopened-validation guards in an existing prepared workspace, without training')
    parser.add_argument('--internal-sources',action='store_true')
    parser.add_argument('--source-runs',nargs=3,type=Path,metavar=('EXTERNAL','R3','MSA'))
    args=parser.parse_args();out=args.output.resolve()
    if out.is_relative_to(PACKAGE) or PACKAGE.is_relative_to(out):raise RuntimeError('Use separate fresh output')
    try:
        if args.internal_sources:source_evidence(out,args.source_runs);return
        if args.check_portability:
            _,runner,science,seal=runtime(out)
            test=out/'workspace/audits/PORTABLE_BINDING_NEGATIVE_CONTROL.txt';test.write_text('original',encoding='utf-8')
            seal([test],'Portability negative control only')
            if not runner.git_bound(test):raise RuntimeError('Fresh seal not recognized')
            test.write_text('changed',encoding='utf-8')
            if runner.git_bound(test):raise RuntimeError('Changed file incorrectly accepted')
            test.write_text('original',encoding='utf-8')
            rejected=False
            try:science.open_validation()
            except RuntimeError:rejected=True
            if not rejected:raise RuntimeError('Validation opened without a newly fitted freeze')
            rejected=False
            try:(PACKAGE/'PORTABILITY_WRITE_GUARD_NEGATIVE_CONTROL').write_text('must not be written',encoding='utf-8')
            except RuntimeError:rejected=True
            if not rejected:raise RuntimeError('Package write guard failed')
            write(out/'PORTABILITY_CHECKS.json',dict(status='PASS_SEAL_MUTATION_VALIDATION_LOCK_AND_PACKAGE_WRITE_GUARDS',training_performed=False))
            return
        if args.internal_stage:stage(out,args.internal_stage);return
        prepare(out)
        if args.mode=='prepare':return
        if args.mode=='preflight':
            p6,runner,_,_=runtime(out);p6.validate_preflight();assignment,_=runner.preflight()
            write(out/'PREFLIGHT_RECEIPT.json',dict(status='PASS_PORTABLE_ESTIMATOR_INPUTS_AND_PHASE_PLAN_ONLY',p6_trajectories=360,
                  fit_tasks=len(runner.canonical_tasks(assignment,'fit')),validation_tasks=len(runner.canonical_tasks(assignment,'validation')),
                  full_training_performed=False,phases=list(STAGES)))
            return
        command=[sys.executable,'-X','utf8','-B',str(Path(__file__).resolve()),'--output',str(out),'--internal-sources']
        if args.source_runs:command+=['--source-runs',*[str(p) for p in args.source_runs]]
        with (out/'source_training_validation.log').open('x',encoding='utf-8') as log:
            subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
        for name in STAGES:
            write(out/'PROGRESS.json',dict(stage=name,status='RUNNING'))
            with (out/(name+'.log')).open('x',encoding='utf-8') as log:
                subprocess.run([sys.executable,'-X','utf8','-B',str(Path(__file__).resolve()),'--output',str(out),'--internal-stage',name],stdout=log,stderr=subprocess.STDOUT,check=True)
        write(out/'RECEIPT.json',dict(status='PASS_FULL_P6_P7_6B_ESTIMATOR_CHAIN_EXACT',source_models_retrained_or_verified_current_runs=True,
             p6_trajectories=360,p7_fit_trajectories=432,p7_validation_trajectories=432,source_selection_reproduced=False,
             final_lifecycle_linkage_revalidated=False,full_package_acceptance=False))
    except BaseException:
        if out.exists():write(out/('FAILURE_'+(args.internal_stage or args.mode)+'.json'),dict(status='FAIL',traceback=traceback.format_exc(),scientific_tolerances_changed=False))
        raise


if __name__=='__main__':main()
