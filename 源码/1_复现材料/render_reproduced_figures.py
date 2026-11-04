"""Render original figure functions from newly verified reproduction tables."""
import argparse,ast,hashlib,json,os,runpy,sys,warnings
from pathlib import Path
B=Path(__file__).resolve().parent
SOURCE=B/'figures/corrected_batch20_final/generate_paper3_figures.py'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--statistics',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--site-packages',type=Path);a=p.parse_args()
    folder=a.statistics.resolve();out=a.output.resolve()
    if out.exists():raise RuntimeError('Fresh figure output required')
    receipt=read(folder/'STATISTICS_RECEIPT.json')
    if receipt['status']!='PASS':raise RuntimeError('Statistics comparison has not passed')
    if a.site_packages:sys.path.insert(0,str(a.site_packages.resolve()))
    out.mkdir(parents=True);os.environ['MPLCONFIGDIR']=str(out/'matplotlib_cache')
    env=runpy.run_path(str(SOURCE),run_name='frozen_plot_functions')
    tree=ast.parse(SOURCE.read_text('utf-8'));fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='load_data')
    # Replace only the old-machine authority-manifest loader. Everything from
    # method/center consistency checks through plotted quantities stays exact.
    start=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='methods' for t in n.targets))
    prefix=ast.parse("tables = _new_tables\nused = _new_bindings\n").body
    fn.body=prefix+fn.body[start:]
    tables={};bindings={};expected={r['file']:r['sha256'] for r in receipt['comparisons']}
    import csv
    for name in env['NAMES']:
        path=folder/name;digest=sha(path)
        if digest!=expected[name]:raise RuntimeError('New statistics changed: '+name)
        with path.open(encoding='utf-8-sig',newline='') as f:tables[name]=list(csv.DictReader(f))
        bindings[name]=digest
    env.update(_new_tables=tables,_new_bindings=bindings)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(SOURCE),'exec'),env)
    data=env['load_data'](folder,None);env['style']();checks={}
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        for name,creator in [('Fig2_Paired_Service_Loss','fig2'),('Fig3_Selective_Search','fig3')]:
            fig=env[creator](data);checks[name]=env['audit_layout'](fig)
            fig.savefig(out/(name+'.pdf'),metadata=env['PDF_METADATA'])
            fig.savefig(out/(name+'.png'),dpi=600)
            env['plt'].close(fig)
        missing=[str(w.message) for w in seen if 'Glyph' in str(w.message) and 'missing' in str(w.message)]
        if missing:raise RuntimeError(missing)
    (out/'PLOT_DATA.json').write_text(json.dumps(data,indent=2,sort_keys=True),'utf-8')
    result=dict(status='PASS',scope=receipt['scope'],source_sha256=sha(SOURCE),statistics_receipt_sha256=sha(folder/'STATISTICS_RECEIPT.json'),input_sha256=bindings,layout=checks,adaptation='Only historical authority-file loading replaced with current verified statistics receipt. Scientific extraction, consistency assertions and figure functions unchanged.')
    (out/'FIGURE_RECEIPT.json').write_text(json.dumps(result,indent=2),'utf-8')
    print(json.dumps(dict(status='PASS',scope=receipt['scope'],figures=2)))
if __name__=='__main__':main()
