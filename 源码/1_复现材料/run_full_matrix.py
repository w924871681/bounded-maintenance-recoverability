"""Execute every frozen task, collect complete shard receipts, and reject omissions.

Workers are separate processes so recorded Torch RNG states cannot interfere.
The original source/causal checks and exact per-case numerical comparisons run
inside each worker. No failed trajectory is silently rerun.
"""
import argparse,itertools,json,os,subprocess,sys,time,datetime
from pathlib import Path
B=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def write(p,x):
    path=Path(p);temp=path.with_suffix(path.suffix+'.new')
    temp.write_text(json.dumps(x,ensure_ascii=False,indent=2),'utf-8');temp.replace(path)

def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--output',required=True,type=Path);p.add_argument('--python',default=sys.executable)
    p.add_argument('--workers',type=int,default=1);p.add_argument('--site-packages',type=Path)
    p.add_argument('--batches',type=int,default=120,help='Recycle processes between bounded batches; scientific tasks/RNG remain unchanged')
    p.add_argument('--min-available-gib',type=float,default=2.5)
    p.add_argument('--resume-from',type=Path,help='Audited externally interrupted run; recheck and copy only fully passed shards')
    a=p.parse_args();out=a.output.resolve()
    batches=a.batches or a.workers
    if not 1<=a.workers<=batches<=1200:raise ValueError('Invalid worker/batch count')
    if out.exists():raise RuntimeError('Use a new full-run output directory')
    out.mkdir(parents=True);children=[];handles=[];started=time.monotonic()
    cfg=read(B/'repository/configs/P7_7_FINAL_LIFECYCLE_PROTOCOL.json');pop=cfg['final_population']
    expected=set(itertools.product(pop['centers'],pop['seeds'],pop['scenarios'],[m['method'] for m in cfg['comparators']]))
    try:
        carried=[]
        if a.resume_from:
            from resume_verified_shards import carry
            carried=carry(a.resume_from,out,B,batches)
        carried_indices={read(w/'MATRIX_RECEIPT.json')['shard_index'] for w in carried}
        carried_count=sum(read(w/'MATRIX_RECEIPT.json')['completed'] for w in carried)
        pending=[i for i in range(batches) if i not in carried_indices];launches=[]
        def launch(i):
            worker=out/f'worker_{i:03}';cmd=[a.python,'-X','utf8','-B',str(B/'reproduce.py'),'matrix','--shards',str(batches),'--shard-index',str(i),'--output',str(worker)]
            if a.site_packages:cmd[3:3]=['-I','-S'];cmd.extend(['--site-packages',str(a.site_packages.resolve())])
            log=(out/f'worker_{i:02}.log').open('w',encoding='utf-8');handles.append(log)
            proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));children.append((proc,worker))
            launches.append({'pid':proc.pid,'output':str(worker),'launched_at':datetime.datetime.now().isoformat(),'command':cmd})
            write(out/'LAUNCH.json',{'parent_pid':os.getpid(),'workers':launches,'expected':len(expected),'max_concurrent_workers':a.workers,'batches':batches,'scientific_inputs':'packaged canonical F1 arrays, frozen source/estimator checkpoints and recorded RNG states'})
        while pending or any(proc.poll() is None for proc,w in children):
            bad=[(p.pid,p.returncode) for p,w in children if p.poll() not in (None,0)]
            if bad:raise RuntimeError('Worker failed; inspect preserved log/FAILURE.json: '+str(bad))
            available=None
            if a.min_available_gib:
                import psutil
                available=psutil.virtual_memory().available/1024**3
            active=sum(proc.poll() is None for proc,w in children)
            if pending and active<a.workers and (available is None or available>=a.min_available_gib):
                launch(pending.pop(0))
            progress=[]
            for proc,w in children:
                try:item=read(w/'PROGRESS.json')
                except (OSError,ValueError):item={'completed':0}
                progress.append({'pid':proc.pid,'exit_code':proc.poll(),**item})
            write(out/'PROGRESS.json',{'completed':carried_count+sum(x['completed'] for x in progress),'carried_complete_trajectories':carried_count,'expected':len(expected),'elapsed_seconds':time.monotonic()-started,'workers':progress,'pending_batches':len(pending),'available_memory_gib':available,'resource_gate':'WAITING_FOR_MEMORY' if pending and active==0 and available is not None and available<a.min_available_gib else 'RUNNING'})
            time.sleep(5)
        actual=[]
        for proc,w in children:
            if proc.returncode!=0:raise RuntimeError('Worker failed')
        for w in carried+[w for proc,w in children]:
            receipt=read(w/'MATRIX_RECEIPT.json')
            if receipt['status']!='PASS_SHARD':raise RuntimeError('Incomplete shard')
            for entry in receipt['records']:
                task=entry['task'];key=tuple(task[k] for k in ('center','seed','scenario','method'))
                if entry['status']!='PASS_SINGLE_LIFECYCLE':raise RuntimeError('Failed comparison')
                actual.append(key)
        if len(actual)!=len(expected) or set(actual)!=expected:raise RuntimeError('Matrix omissions or duplicates')
        write(out/'FULL_MATRIX_RECEIPT.json',{'status':'PASS_1200_CANONICAL_LIFECYCLE_REPLAYS','trajectories':len(actual),'stages':len(actual)*24,'exact_scientific_table_equality':True,'wall_times_excluded':True,'source_bank_retrained':False,'statistics_regeneration':'PENDING_SEPARATE_STEP','elapsed_seconds':time.monotonic()-started})
    except BaseException as error:
        write(out/'FAILURE.json',{'error':repr(error),'elapsed_seconds':time.monotonic()-started,'no_automatic_retry':True})
        for proc,w in children:
            if proc.poll() is None:proc.terminate()
        for proc,w in children:
            try:proc.wait(timeout=30)
            except subprocess.TimeoutExpired:proc.kill()
        raise
    finally:
        for h in handles:h.close()

if __name__=='__main__':main()
