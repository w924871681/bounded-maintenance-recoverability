"""Execute the original r3 source-regime training in a new output directory.

This covers the three extra regime identities, not the eight imported MSA
identities or the offline recoverability estimator. No frozen file is replaced.
"""
import argparse,hashlib,json,os,sys,traceback
from pathlib import Path
B=Path(__file__).resolve().parent;REPO=B/'repository'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def config(path):
    value=read(path)
    if 'base_config' not in value:return value
    result=config(REPO/value.pop('base_config'))
    for key,item in value.items():result[key]={**result[key],**item} if key=='c3_regime_b' else item
    return result
def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--site-packages',type=Path);p.add_argument('--mode',choices=('preflight','train'),default='train');a=p.parse_args()
    out=a.output.resolve()
    if out.exists():raise RuntimeError('New source-training output required')
    if out.is_relative_to(B) or B.is_relative_to(out):raise RuntimeError('Output overlaps source package')
    out.mkdir(parents=True)
    try:
        execute(a,out)
    except BaseException:
        (out/'FAILURE.json').write_text(json.dumps(dict(status='FAIL',mode=a.mode,traceback=traceback.format_exc()),indent=2),'utf-8')
        raise
def execute(a,out):
    if a.site_packages:sys.path.insert(0,str(a.site_packages.resolve()))
    sys.path.insert(0,str(REPO));sys.dont_write_bytecode=True
    for key in ['TEMP','TMP','TORCH_HOME','CUDA_CACHE_PATH']:
        dst=out/'cache'/key;dst.mkdir(parents=True,exist_ok=True);os.environ[key]=str(dst)
    from retrain_external_sources import install_read_guard
    install_read_guard(out)
    import torch
    from core import p3_2_models as m
    frozen=read(REPO/'configs/p3_mismatch_v2_frozen.json')
    original=read(REPO/frozen['source_training_manifest_path'])
    cfg=config(REPO/'configs/p3_2_protocol_r3.json')
    if cfg['generator_revision']!=original['generator_revision']:raise RuntimeError('Wrong frozen source revision')
    expected={r['identity_id']:r for r in original['assets']}
    if len(expected)!=3:raise RuntimeError('Frozen source manifest must cover exactly three identities')
    for row in expected.values():
        if sha(REPO/row['checkpoint'])!=row['checkpoint_sha256']:raise RuntimeError('Original source checkpoint hash differs')
    assembly=read(B/'ASSEMBLY_MANIFEST.json')['files']
    for rel in ['repository/core/p3_2_models.py','repository/core/p3_2_data.py','repository/core/models.py','repository/configs/p3_2_protocol_r3.json']:
        if sha(B/rel)!=assembly[rel]['sha256']:raise RuntimeError('Frozen source implementation changed: '+rel)
    preflight=dict(status='PASS_R3_SOURCE_INPUTS_AND_IMPORTS_ONLY',python=sys.version,torch=str(torch.__version__),source_models_retrained=False,implementation_sha256=sha(Path(m.__file__)),expected_identities=sorted(expected))
    (out/'PREFLIGHT_RECEIPT.json').write_text(json.dumps(preflight,indent=2),'utf-8')
    if a.mode=='preflight':
        print(json.dumps(preflight));return
    m.ROOT=out
    actual=m.train_source_assets(cfg)
    if {r['identity_id'] for r in actual['assets']}!=set(expected) or len(actual['assets'])!=3:raise RuntimeError('New source output identity coverage differs')
    checks=[]
    for row in actual['assets']:
        old=expected[row['identity_id']];new_path=out/row['checkpoint'];old_path=REPO/old['checkpoint']
        left=torch.load(old_path,map_location='cpu',weights_only=True);right=torch.load(new_path,map_location='cpu',weights_only=True)
        equal=left.keys()==right.keys() and all(left[k].dtype==right[k].dtype and left[k].shape==right[k].shape and torch.equal(left[k],right[k]) for k in left)
        checks.append(dict(identity=row['identity_id'],state_tensors_exact=equal,source_data_digest_equal=row['source_regime_sha256']==old['source_regime_sha256'],new_sha256=sha(new_path),original_sha256=sha(old_path)))
    result=dict(status='PASS_THREE_SOURCE_REGIME_MODELS' if all(c['state_tensors_exact'] and c['source_data_digest_equal'] for c in checks) else 'FAIL',checks=checks,implementation_sha256=sha(Path(m.__file__)),python=sys.version,torch=str(torch.__version__),imported_eight_identities_retrained=False,estimator_retrained=False)
    (out/'SOURCE_COMPARISON.json').write_text(json.dumps(result,indent=2),'utf-8')
    print(json.dumps(result))
    if result['status']=='FAIL':raise RuntimeError('Source training differs; preserve outputs for diagnosis')
if __name__=='__main__':main()
