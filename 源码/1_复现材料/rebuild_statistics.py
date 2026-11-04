"""Apply the unchanged frozen arithmetic/bootstrap functions to a complete matrix."""
import argparse,csv,hashlib,io,json,sys
from pathlib import Path
B=Path(__file__).resolve().parent;REPO=B/'repository'
EXPECTED=REPO/'results/p7_7_integrity_replication_batch20_env_v3'
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(__doc__);ap.add_argument('--matrix',type=Path);ap.add_argument('--saved-results-check',action='store_true');ap.add_argument('--output',type=Path,required=True);ap.add_argument('--site-packages',type=Path);a=ap.parse_args()
    if bool(a.matrix)==bool(a.saved_results_check):raise ValueError('Choose one complete new matrix or explicit saved-results check')
    out=a.output.resolve()
    if out.exists():raise RuntimeError('New output path required')
    out.mkdir(parents=True)
    if a.site_packages:sys.path.insert(0,str(a.site_packages.resolve()))
    sys.path.insert(0,str(REPO))
    from verification.paper3_canonical_inputs.replication_statistics_batch20_env_v3 import statistics as s
    if a.matrix:
        root=a.matrix.resolve();receipt=read(root/'FULL_MATRIX_RECEIPT.json')
        if receipt['status']!='PASS_1200_CANONICAL_LIFECYCLE_REPLAYS':raise RuntimeError('Full code execution has not passed')
        paths=[]
        for worker in sorted(root.glob('worker_*')):
            if not worker.is_dir():continue
            for record in read(worker/'MATRIX_RECEIPT.json')['records']:
                folder=worker/record['directory']
                if read(folder/'COMPARISON.json')['status']!='PASS_SINGLE_LIFECYCLE':raise RuntimeError('Comparison failed')
                paths.append(folder/'trajectory.csv')
    else:paths=sorted((EXPECTED/'raw').glob('*.csv'))
    if len(paths)!=1200:raise RuntimeError('Complete 1200-trajectory input required')
    rows=[];bindings={}
    for path in paths:
        bindings[str(path)]=sha(path)
        with path.open(encoding='utf-8-sig',newline='') as f:incoming=list(csv.DictReader(f))
        if len(incoming)!=24:raise RuntimeError('Incomplete trajectory')
        rows.extend(incoming)
    cfg=read(REPO/'configs/P7_7_FINAL_LIFECYCLE_PROTOCOL.json')
    agg=s.aggregate_rows(rows,service_unit=float(cfg['service_unit']));tables=s.joint_center_tables(agg);runtime=s.execution_cost_tables(rows)
    mapping={'final_metrics_by_trajectory.csv':agg['trajectory'],'final_metrics_by_center.csv':agg['center'],
             'final_metrics_by_scenario_center.csv':agg['scenario_center'],'final_metrics_by_method.csv':tables['method'],
             'final_metrics_by_scenario.csv':tables['scenario'],'final_paired_contrasts.csv':tables['contrasts'],
             'final_method_bootstrap.csv':tables['method_bootstrap'],'final_paired_bootstrap.csv':tables['bootstrap'],
             'final_loo.csv':tables['loo'],'final_decision_diagnostics.csv':agg['diagnostics'],
             'final_execution_cost_by_trajectory.csv':runtime['trajectory'],'final_execution_cost_by_method.csv':runtime['method']}
    import numpy as np
    np.save(out/'joint_center_resample_indices.npy',tables['indices'],allow_pickle=False)
    comparisons=[]
    for name,data in mapping.items():
        payload=s._csv_bytes(data);(out/name).write_bytes(payload)
        expected=EXPECTED/'statistics_batch20_env_v3'/name
        comparisons.append({'file':name,'sha256':hashlib.sha256(payload).hexdigest(),'matches_expected_bytes':payload==expected.read_bytes(),'timing_table':name.startswith('final_execution_cost_')})
    failed=[r for r in comparisons if not r['matches_expected_bytes'] and (a.saved_results_check or not r['timing_table'])]
    for filename,digest in bindings.items():
        if sha(filename)!=digest:raise RuntimeError('Input mutated during aggregation')
    result={'status':'PASS' if not failed else 'FAIL','scope':'SAVED_OUTPUTS_REAGGREGATION_ONLY' if a.saved_results_check else 'FULL_NEW_MATRIX_TO_FROZEN_SCIENTIFIC_TABLES','raw_trajectories':len(paths),'stage_rows':len(rows),'source_bank_retrained':False,'implementation_sha256':sha(Path(s.__file__)),'comparisons':comparisons,'failed':failed,'input_sha256':bindings}
    (out/'STATISTICS_RECEIPT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'},ensure_ascii=False))
    if failed:raise RuntimeError('Statistical output differs')
if __name__=='__main__':main()
