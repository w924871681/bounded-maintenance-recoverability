"""Create a fresh Python 3.11 environment using the official package indexes."""
import argparse,os,subprocess,sys
from pathlib import Path
B=Path(__file__).resolve().parent
p=argparse.ArgumentParser(__doc__);p.add_argument('--python',default=sys.executable);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
out=a.output.resolve()
if out.exists():raise RuntimeError('Use a new environment directory')
version=subprocess.check_output([a.python,'-c','import sys;print(".".join(map(str,sys.version_info[:2])))'],text=True).strip()
if version!='3.11':raise RuntimeError('Supply Python 3.11 with --python')
cache=out.parent/(out.name+'_installation_tmp');cache.mkdir(parents=True,exist_ok=True);env=dict(os.environ,TEMP=str(cache),TMP=str(cache))
subprocess.run([a.python,'-m','venv','--copies',str(out)],check=True,env=env)
python=out/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
for args in [
 ['install','--no-cache-dir','torch==2.5.1+cu121','--index-url','https://download.pytorch.org/whl/cu121'],
 ['install','--no-cache-dir','-r',str(B/'requirements.txt'),'--index-url','https://pypi.org/simple'],
 ['check'],
]:subprocess.run([str(python),'-m','pip',*args],check=True,env=env)
print('Environment created:',python)
