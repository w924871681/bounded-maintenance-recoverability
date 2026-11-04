# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json, os, sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
from cfg.methods.final_e2e_c23_external_cfg import CFG
from external_e2e_c23.pipeline import prepare_source_assets
from final_e2e_c23.common import load_json

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--device",default="cuda"); ap.add_argument("--safe_mode",default="gru-native"); ap.add_argument("--smoke",action="store_true"); args=ap.parse_args()
    identity=os.path.join(ROOT,CFG.output_root,"preflight","external_baseline_identity.json")
    if not os.path.isfile(identity) or load_json(identity).get("decision")!="PASS_EXTERNAL_BASELINE_PROTOCOL_FROZEN": raise RuntimeError("External preflight is not PASS")
    out_dir=os.path.join(ROOT,CFG.output_root,"source_assets")
    result=prepare_source_assets(ROOT,out_dir,args.device,args.safe_mode,args.smoke)
    print(json.dumps({"decision":result.get("decision"),"asset_count":result.get("asset_count"),"out":os.path.join(out_dir,"source_assets_manifest.json")},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
