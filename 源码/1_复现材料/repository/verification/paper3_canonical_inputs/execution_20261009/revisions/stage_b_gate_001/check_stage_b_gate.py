"""Input-only scientific gate; no model, loss, statistics or generator access."""
from __future__ import annotations
import csv
import hashlib
import json
import sys
from pathlib import Path

RUN=Path(sys.argv[1]).resolve(strict=True)
OUT=Path(sys.argv[2]).resolve(strict=True)
def read(name):return json.loads((RUN/name).read_text(encoding="utf-8"))
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def publish(name,obj):
    with (OUT/name).open("xb") as f:f.write((json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode())

receipt=read("execution_receipt.json")
inventory=read("outputs_inventory.json")["files"]
hash_errors=[name for name,digest in inventory.items() if sha(RUN/name)!=digest]
if sha(RUN/"run_manifest.json")!=receipt["run_manifest_sha256"]:hash_errors.append("receipt->run_manifest")
if sha(RUN/"outputs_inventory.json")!=receipt["outputs_inventory_sha256"]:hash_errors.append("receipt->outputs_inventory")
with (RUN/"existing_input_match_inventory.csv").open(encoding="utf-8",newline="") as f:records=list(csv.DictReader(f))
cohorts={"LEGACY_SERIAL":{"count":0,"matched_expected":0,"unmatched":[]},
         "SINGLETON_PARALLEL":{"count":0,"matched_expected":0,"unmatched":[]}}
for row in records:
    name=row["cohort"]
    if name not in cohorts:continue
    context="F" if name=="LEGACY_SERIAL" else "S"
    cohort=cohorts[name];cohort["count"]+=1
    if row["r0_qualified"]=="True" and row[f"{context}_r1_qualified"]=="True":cohort["matched_expected"]+=1
    else:cohort["unmatched"].append({k:row[k] for k in ("center_id","seed","scenario","method","config_id","r0_qualified","F_r1_qualified","S_r1_qualified","errors")})
mismatches=[]
with (RUN/"existing_input_field_match_inventory.csv").open(encoding="utf-8",newline="") as f:
    for row in csv.DictReader(f):
        if row["status"] in ("OBSERVED_MISMATCH","NOT_VERIFIABLE","NOT_RECORDED"):
            mismatches.append(row)
with (OUT/"stage_b_saved_field_nonmatches.jsonl").open("xb") as f:
    for row in mismatches:f.write((json.dumps(row,sort_keys=True,ensure_ascii=False)+"\n").encode())
summary=read("existing_input_mapping_summary.json")
cert=read("validation_certificate.json")
execution_pass=receipt["exit_code"]==0 and receipt["status"]=="INPUT_ONLY_CHECKS_COMPLETED" and receipt["originals_unchanged"] is True and not hash_errors and cert["checks_completed"] is True
historical_correspondence=(len(records)==1200 and cohorts["LEGACY_SERIAL"]["count"]==cohorts["LEGACY_SERIAL"]["matched_expected"]==239 and cohorts["SINGLETON_PARALLEL"]["count"]==cohorts["SINGLETON_PARALLEL"]["matched_expected"]==961)
result={"schema":"paper3-stage-b-scientific-gate-v1","input_verification_root":str(RUN),"execution_receipt_sha256":sha(RUN/"execution_receipt.json"),
    "execution_pass":execution_pass,"output_hash_errors":hash_errors,"expected_historical_cohort_correspondence_pass":historical_correspondence,
    "cohorts":cohorts,"existing_group_summary":summary,"full_vs_singleton_comparison":"REPORTED_WITH_EXACT_CRITERIA_NOT_A_REQUIREMENT_TO_MATCH",
    "historical_environment_reproduced":False,"initial_state_verified":False,"R2":"PENDING_STAGE_C_INITIAL_MODEL_AND_CAUSAL_CERTIFICATION", "R3":"PENDING_FULL_REPLICATION",
    "stage_c_allowed":execution_pass and historical_correspondence,"decisions_based_on_model_results":False}
publish("stage_b_scientific_gate.json",result)
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result["stage_c_allowed"] else 2)
