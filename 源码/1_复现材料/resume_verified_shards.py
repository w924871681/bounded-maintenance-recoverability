"""Carry only complete, rechecked shards from an externally interrupted matrix.

This is never a retry of a recorded scientific failure. Partial shards remain in
the original directory; their tasks execute in new output directories. Completed
shards are copied byte-for-byte with a per-file provenance ledger.
"""
import hashlib,json,shutil
from pathlib import Path

def read(path):return json.loads(path.read_text('utf-8-sig'))
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def carry(previous,out,package,batches):
    import pandas as pd
    import numpy as np
    previous=previous.resolve(strict=True)
    interruption=read(previous/'INTERRUPTION_RECEIPT.json')
    if interruption['status']!='INTERRUPTED_NO_LIVE_TASK_PROCESSES':raise RuntimeError('Audited interruption required')
    if list(previous.rglob('FAILURE.json')):raise RuntimeError('Recorded failure must be diagnosed; cannot resume automatically')
    cfg=read(package/'repository/configs/P7_7_FINAL_LIFECYCLE_PROTOCOL.json');pop=cfg['final_population']
    keys=[(c,s,sc,m['method']) for c in pop['centers'] for s in pop['seeds'] for sc in pop['scenarios'] for m in cfg['comparators']]
    expected_root=package/'repository/results/p7_7_integrity_replication_batch20_env_v3/raw'
    ledger=[];completed=[]
    for i in range(batches):
        source=previous/f'worker_{i:03}'
        receipt=source/'MATRIX_RECEIPT.json'
        if not receipt.exists():continue
        value=read(receipt)
        if value['status']!='PASS_SHARD' or value['shards']!=batches or value['shard_index']!=i:raise RuntimeError('Invalid shard identity')
        observed=[]
        for entry in value['records']:
            task=entry['task'];key=tuple(task[k] for k in ('center','seed','scenario','method'));observed.append(key)
            folder=(source/entry['directory']).resolve(strict=True)
            if not folder.is_relative_to(source):raise RuntimeError('Escaping case path')
            comparison=read(folder/'COMPARISON.json')
            if entry['status']!='PASS_SINGLE_LIFECYCLE' or comparison['status']!='PASS_SINGLE_LIFECYCLE' or comparison['differences'] or comparison['absolute_tolerance']!=0:raise RuntimeError('Invalid comparison')
            config=next(m['config_id'] for m in cfg['comparators'] if m['method']==task['method'])
            stem=f"{config}_{task['center']}_{task['seed']}_{task['scenario']}"
            actual=pd.read_csv(folder/'trajectory.csv');expected=pd.read_csv(expected_root/(stem+'.csv'))
            if len(actual)!=24 or len(expected)!=24 or list(actual.columns)!=list(expected.columns):raise RuntimeError('Schema mismatch')
            for col in expected:
                if col in {'decision_runtime_actual_s','decision_runtime_standalone_estimate_s'} or any(x in col.lower() for x in ('seconds','wall_time','elapsed','peak_memory')):continue
                match=np.isclose(expected[col],actual[col],atol=0,rtol=0,equal_nan=True) if pd.api.types.is_numeric_dtype(expected[col]) and not pd.api.types.is_bool_dtype(expected[col]) else (expected[col].fillna('<NA>')==actual[col].fillna('<NA>')).to_numpy()
                if not bool(match.all()):raise RuntimeError(f'Changed scientific output {folder}: {col}')
        if observed!=keys[i::batches] or value['completed']!=len(observed):raise RuntimeError('Shard omissions/order mismatch')
        target=out/source.name
        for path in sorted(source.rglob('*')):
            if path.lstat().st_file_attributes & 1024:raise RuntimeError('Links are forbidden in resumed evidence')
            if not path.is_file():continue
            relative=path.relative_to(source);dest=target/relative;dest.parent.mkdir(parents=True,exist_ok=True)
            digest=sha(path);shutil.copy2(path,dest)
            if sha(dest)!=digest or sha(path)!=digest:raise RuntimeError('Copy identity mismatch')
            ledger.append(dict(source=str(path),destination=dest.relative_to(out).as_posix(),sha256=digest))
        completed.append(target)
    (out/'RESUMPTION_RECEIPT.json').write_text(json.dumps(dict(status='PASS_COMPLETE_SHARDS_RECHECKED_AND_COPIED',previous=str(previous),carried_shards=len(completed),carried_trajectories=sum(len(read(w/'MATRIX_RECEIPT.json')['records']) for w in completed),partial_shards_reused=False,scientific_tolerance=0,files=ledger),indent=2),'utf-8')
    return completed
