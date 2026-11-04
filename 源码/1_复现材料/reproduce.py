"""Portable replay of the frozen canonical-input lifecycle; historical files stay unchanged.

The author workstation authorization is replaced by explicit package verification,
new runtime provenance, an output-only write guard and the original generation
guard. All scientific adapters, source pins, input fingerprints and causal checks
are the original code. Recorded RNG is replayed as published experiment input,
not represented as a failed-task retry or an independent random realization.
"""
import argparse, hashlib, importlib.metadata, json, os, platform, sys, sysconfig, time
from pathlib import Path

B=Path(__file__).resolve().parent
REPO=B/'repository'
CAN=REPO/'verification/paper3_canonical_inputs'
INPUT=CAN/'P7_7_CANONICAL_INPUT_VERIFICATION_V1/CIV_INPUT_V1_AUTHORIZED_20261009_RUN003'
EXPECTED=REPO/'results/p7_7_integrity_replication_batch20_env_v3'

def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False),'utf-8')

def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('mode',choices=['verify','initial','case','matrix'])
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--center',type=int,default=33000)
    ap.add_argument('--seed',type=int,default=7311)
    ap.add_argument('--scenario',choices=['C0','C1','C3','C4'],default='C0')
    ap.add_argument('--method',choices=['B0','B1','B2','B8','P7.7'],default='B0')
    ap.add_argument('--site-packages',type=Path,help='Explicit Python 3.11 environment site-packages for -I -S execution')
    ap.add_argument('--shards',type=int,default=1)
    ap.add_argument('--shard-index',type=int,default=0)
    ap.add_argument('--limit',type=int,help='Limited entry check; never full acceptance')
    a=ap.parse_args()
    if a.shards<1 or not 0<=a.shard_index<a.shards:raise ValueError('Invalid shard selection')
    out=a.output.resolve()
    if out.exists() and any(out.iterdir()):raise RuntimeError('Fresh output directory required')
    if out==B or out.is_relative_to(REPO):raise RuntimeError('Outputs must not overwrite packaged evidence')
    out.mkdir(parents=True,exist_ok=True)
    sys.dont_write_bytecode=True
    if a.site_packages:sys.path.insert(0,str(a.site_packages.resolve(strict=True)))
    dependency_roots={Path(sysconfig.get_path(k)).resolve() for k in ('purelib','platlib')}
    if a.site_packages:dependency_roots.add(a.site_packages.resolve(strict=True))
    sys.path.insert(0,str(REPO))
    for key in ['TEMP','TMP','TORCH_HOME','CUDA_CACHE_PATH','MPLCONFIGDIR']:
        p=out/'runtime_cache'/key;p.mkdir(parents=True,exist_ok=True);os.environ[key]=str(p)
    from verification.paper3_canonical_inputs.replication_executor_batch20_env_v3 import provenance as p, science_adapter as s
    from verification.paper3_canonical_inputs.replication_executor_batch20_env_v3.fixed_inputs import FixedInputStore
    # Only old repository-root identifiers in historical JSON are relocated.
    # No historical manifest bytes or numeric/source dependencies are rewritten.
    native_regular=p.regular_path
    old='D:/dt-talk/DT_LIFECYCLE_ESCALATION'
    def relocated(path,**kw):
        value=str(path).replace('\\','/')
        if value.casefold()==old.casefold() or value.casefold().startswith(old.casefold()+'/'):
            path=REPO/value[len(old):].lstrip('/')
        return native_regular(path,**kw)
    p.regular_path=relocated
    verified=p.verify_stage_b(REPO,INPUT)
    source_pins=s._check_sources(REPO,None)
    cfg=read(REPO/'configs/P7_7_FINAL_LIFECYCLE_PROTOCOL.json');s._check_cfg(REPO,cfg)
    env={'python':sys.version,'platform':platform.platform(),'packages':{k:importlib.metadata.version(k) for k in p.EXPECTED_MODEL_VERSIONS}}
    if env['packages']!=p.EXPECTED_MODEL_VERSIONS:raise RuntimeError({'environment_mismatch':env,'expected':p.EXPECTED_MODEL_VERSIONS})
    if sys.version_info[:2]!=(3,11):raise RuntimeError('Python 3.11 required for the frozen model environment')
    authorization={'environment':env,'source_bindings':source_pins,'stage_b':verified['binding_sha256'],
                   'scope':'New portable replay authorization; original workstation authorization is retained as historical evidence'}
    write(out/'PORTABLE_PROVENANCE.json',authorization)
    def require(repo,inputs):
        if Path(repo).resolve()!=REPO or Path(inputs).resolve()!=INPUT:raise RuntimeError('Foreign repository/input root')
        if s._check_sources(REPO,None)!=source_pins:raise RuntimeError('Scientific source changed')
        return authorization
    p.require_authorized_execution=require
    store=FixedInputStore(REPO,INPUT)
    # Audit Python IO: every mutation is confined to this new output directory;
    # project reads outside the portable package are forbidden.
    def guard(event,args):
        if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
            path=Path(os.fsdecode(args[0])).resolve();mode=args[1];flags=args[2]
            mut=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
            if mut and not path.is_relative_to(out):raise PermissionError('Write outside declared output: '+str(path))
            lower=str(path).replace('\\','/').casefold()
            if (lower.startswith('d:/dt-talk/') or lower.startswith('d:/审稿/') or lower.startswith('d:/毕业论文/') or lower.startswith('e:/')) and not (path.is_relative_to(B) or path.is_relative_to(out)):
                # Explicit dependency environment is allowed; no old scientific files.
                if not any(path.is_relative_to(root) for root in dependency_roots):raise PermissionError('Read outside package: '+str(path))
        elif event in {'os.remove','os.rmdir','os.mkdir','os.chmod','os.utime','os.truncate'}:
            if isinstance(args[0],(str,bytes,os.PathLike)) and not Path(os.fsdecode(args[0])).resolve().is_relative_to(out):raise PermissionError('Mutation outside output')
        elif event in {'os.rename','os.link'}:
            for value in args[:2]:
                if not Path(value).resolve().is_relative_to(out):raise PermissionError('Mutation outside output')
    sys.addaudithook(guard)
    p.install_generator_guard(REPO)
    if a.mode=='verify':
        for c in s.CENTERS:
            for scenario in s.SCENARIOS:store.load(c,scenario)
        write(out/'VERIFICATION.json',{'status':'PASS_FROZEN_INPUTS_SOURCES_ENVIRONMENT','optimizer_steps':0,'full_reproduction':False});return
    runner=s._runner(REPO,None)
    initial=next(r for r in read(EXPECTED/'initial_state_manifest.json')['states'] if r['center_id']==a.center and r['seed']==a.seed)
    if a.mode=='initial':
        result=s.initial_preflight(REPO,INPUT,a.center,a.seed,cfg,original_runner=runner,input_store=store)
        result['matches_frozen_initial_state']=result['initial_state_hash']==initial['initial_state_hash']
        write(out/'INITIAL.json',result)
        if not result['matches_frozen_initial_state']:raise RuntimeError('Initial-state mismatch')
        return
    if a.mode=='matrix':
        population=cfg['final_population'];tasks=[]
        for center in population['centers']:
            for seed in population['seeds']:
                for scenario in population['scenarios']:
                    for method in cfg['comparators']:
                        tasks.append(dict(center=center,seed=seed,scenario=scenario,method=method['method']))
        tasks=tasks[a.shard_index::a.shards];expected_count=len(tasks)
        if a.limit is not None:tasks=tasks[:a.limit]
        states={(x['center_id'],x['seed']):x for x in read(EXPECTED/'initial_state_manifest.json')['states']}
        done=[];began=time.monotonic()
        for task in tasks:
            case=argparse.Namespace(**task)
            stem='_'.join(str(task[k]) for k in ('center','seed','scenario','method'))
            case_out=out/'cases'/stem;case_out.mkdir(parents=True)
            try:
                verdict=execute_case(case,case_out,p,s,store,runner,cfg,env,states[task['center'],task['seed']])
                done.append(dict(task=task,status=verdict['status'],directory=case_out.relative_to(out).as_posix()))
                write(out/'PROGRESS.json',dict(completed=len(done),expected=expected_count,elapsed_seconds=time.monotonic()-began,last=task))
            except Exception as error:
                write(out/'FAILURE.json',dict(task=task,error=repr(error),completed=len(done),expected=expected_count));raise
        write(out/'MATRIX_RECEIPT.json',dict(status='PASS_SHARD' if len(done)==expected_count and a.limit is None else 'PARTIAL_ENTRY_CHECK',shard_index=a.shard_index,shards=a.shards,completed=len(done),expected=expected_count,source_bank_retrained=False,records=done))
    else:
        execute_case(a,out,p,s,store,runner,cfg,env,initial)


def execute_case(a,out,p,s,store,runner,cfg,env,initial):
    method_cfg=next(x for x in cfg['comparators'] if x['method']==a.method)
    task=dict(center_id=a.center,seed=a.seed,scenario=a.scenario,method=a.method,config_id=method_cfg['config_id'])
    stem=f"{task['config_id']}_{a.center}_{a.seed}_{a.scenario}"
    integrity=read(EXPECTED/'raw'/f'{stem}.integrity.json')
    rngpath=EXPECTED/integrity['rng_relative']
    if sha(rngpath)!=integrity['rng_file_sha256']:raise RuntimeError('Recorded RNG file changed')
    rng=read(rngpath)
    body={k:v for k,v in rng.items() if k!='state_digest'}
    if rng['state_digest']!=p.canonical_hash(body):raise RuntimeError('Recorded RNG digest changed')
    if rng['bindings']['task']!=task or rng['bindings']['input_bundle_digest']!=store.bundle['input_bundle_digest']:raise RuntimeError('Recorded RNG belongs to another task/input')
    if rng['torch_version']!=str(runner.torch.__version__) or rng['cuda_runtime']!=runner.torch.version.cuda:raise RuntimeError('Recorded RNG runtime differs')
    torch=runner.torch
    if len(rng['cuda'])!=torch.cuda.device_count():raise RuntimeError('Recorded RNG device count differs')
    torch.set_rng_state(s._decode_rng(torch,rng['cpu']))
    if rng['cuda']:torch.cuda.set_rng_state_all([s._decode_rng(torch,x['state']) for x in rng['cuda']])
    def captured(current):
        if current['cpu']!=rng['cpu'] or current['cuda']!=rng['cuda']:raise RuntimeError('Replay setup altered original pre-task RNG')
        write(out/'RNG_REPLAY.json',{'historical_file_sha256':sha(rngpath),'historical_state_digest':rng['state_digest'],
                                  'current_state':current,'same_recorded_random_realization':True,'independent_random_replication':False})
    started=time.monotonic()
    frame,audit=s.run_task(REPO,INPUT,task,cfg,expected_initial_state_hash=initial['initial_state_hash'],
                           environment_binding=p.canonical_hash(env),original_runner=runner,input_store=store,rng_capture_sink=captured)
    frame.to_csv(out/'trajectory.csv',index=False);write(out/'AUDIT.json',audit)
    # Scientific table equality; timing columns are reported separately.
    import pandas as pd
    import numpy as np
    expected=pd.read_csv(EXPECTED/'raw'/f'{stem}.csv');actual=pd.read_csv(out/'trajectory.csv')
    differences=[];excluded=[]
    if list(expected.columns)!=list(actual.columns) or len(expected)!=len(actual):raise RuntimeError('Output shape/schema differs')
    for col in expected:
        if col in {'decision_runtime_actual_s','decision_runtime_standalone_estimate_s'} or any(x in col.lower() for x in ('seconds','wall_time','elapsed','peak_memory')):excluded.append(col);continue
        if pd.api.types.is_numeric_dtype(expected[col]) and not pd.api.types.is_bool_dtype(expected[col]):
            match=np.isclose(expected[col],actual[col],atol=0,rtol=0,equal_nan=True)
        else:match=(expected[col].fillna('<NA>')==actual[col].fillna('<NA>')).to_numpy()
        if not bool(match.all()):differences.append({'column':col,'rows':np.where(~match)[0].tolist()})
    result={'status':'PASS_SINGLE_LIFECYCLE' if not differences else 'FAIL','task':task,'stages':len(frame),
            'absolute_tolerance':0,'comparison_policy':'Exact scientific equality; no unapproved tolerance introduced','differences':differences,'excluded_timing_columns':excluded,
            'elapsed_seconds':time.monotonic()-started,'full_matrix_reproduced':False,'source_bank_retrained':False}
    write(out/'COMPARISON.json',result);print(json.dumps(result))
    if differences:raise RuntimeError('Scientific comparison failed')
    return result

if __name__=='__main__':main()
