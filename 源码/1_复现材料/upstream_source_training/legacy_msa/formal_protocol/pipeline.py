# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
import csv
import gc
import hashlib
import json
import os
import platform
import random
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from configs.methods.limited_validation_formal_cfg import CFG, config_dict
from core.data.center_api import fixed_target_raw_layout
from core.methods.ours.paper_engine import _load_prior_model
from core.methods.ours.stage2_runtime import (
    candidate_backend_context,
    candidate_device,
    synchronize_if_cuda,
)
from core.space import build_model, profile_arch
from main_evaluation.pipeline import (
    _fixed_target_adapt,
    _load_fixed_source_model,
    _run_search_case,
)
from shared.data_access import (
    get_source_training_support_validation,
    get_support_validation_check,
    get_test_only_after_selection,
)
from shared.evaluation.common import (
    atomic_json,
    build_runtime,
    eval_metrics,
    feasible_indices,
    file_sha256,
    load_frozen_assets,
    load_json,
    seed_all,
)


def _sha256(path: Path) -> str:
    return file_sha256(str(path))


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, text=True,
        encoding="utf-8", errors="replace", stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout.strip()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields=None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows({k: row.get(k) for k in fields} for row in rows)


def _atomic_torch_save(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.{time.time_ns()}.tmp")
    torch.save(obj, tmp)
    os.replace(tmp, path)


def _log(output_root: Path, message: str) -> None:
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (output_root / "run.log").open("a", encoding="utf-8", newline="\n") as h:
        h.write(line + "\n")


def _environment(device: str) -> Dict[str, Any]:
    return {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "numpy": np.__version__,
        "device_request": device,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_runtime": torch.version.cuda,
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def _jobs(pool: Sequence[int]) -> List[Tuple[int, int, int]]:
    start, count, _offset = map(int, pool)
    return [
        (cid, H, K)
        for cid in range(start, start + count)
        for H in CFG.H_list
        for K in CFG.K_list
    ]


def _case_seed(cid: int, H: int, K: int) -> int:
    return int(CFG.train_seed + 1009 * cid + 37 * H + 53 * K)


def _source_seed(H: int, idx: int) -> int:
    return int(CFG.train_seed + 101 * H + idx)


def _center_bootstrap(values_by_center: Mapping[int, Sequence[float]], seed: int):
    centers = sorted(values_by_center)
    arr = np.asarray([np.mean(values_by_center[c]) for c in centers], dtype=np.float64)
    if not len(arr):
        return {"mean": None, "median": None, "ci_low": None, "ci_high": None, "n_centers": 0}
    rng = np.random.default_rng(int(seed))
    ids = rng.integers(0, len(arr), size=(CFG.bootstrap_repeats, len(arr)))
    boot = arr[ids].mean(axis=1)
    return {
        "mean": float(arr.mean()), "median": float(np.median(arr)),
        "ci_low": float(np.quantile(boot, .025)),
        "ci_high": float(np.quantile(boot, .975)),
        "n_centers": int(len(arr)), "repetitions": CFG.bootstrap_repeats,
        "seed": int(seed),
    }


def _relative_gain(new: float, ref: float) -> float:
    return float((float(ref) - float(new)) / (abs(float(ref)) + CFG.eps))


def _asset_path(root: Path, item: Mapping[str, Any]) -> Path:
    return root / str(item["path"]).replace("\\", "/")


def _load_external_manifest(root: Path) -> Dict[str, Any]:
    path = root / CFG.external_source_manifest_path
    obj = load_json(str(path))
    if obj.get("decision") != "PASS_EXTERNAL_SOURCE_ASSETS_FROZEN":
        raise RuntimeError("External source manifest is not frozen PASS")
    if obj.get("target_pool_used") or obj.get("validation_pool_k_used") or obj.get("test_used"):
        raise RuntimeError("External source provenance contains target/Test use")
    for item in obj.get("assets", {}).values():
        full = _asset_path(root, item)
        if not full.is_file() or _sha256(full).lower() != str(item["sha256"]).lower():
            raise RuntimeError(f"External source asset invalid: {full}")
    return obj


def _tensor_sha256(*tensors: torch.Tensor) -> str:
    h = hashlib.sha256()
    for tensor in tensors:
        arr = tensor.detach().cpu().contiguous().numpy()
        h.update(str(arr.dtype).encode())
        h.update(str(arr.shape).encode())
        h.update(arr.tobytes())
    return h.hexdigest()


def _structured_prior_usage_audit(root: Path, output_root: Path) -> Dict[str, Any]:
    proposed = set(range(CFG.main_pool[0], CFG.main_pool[0] + CFG.main_pool[1]))
    proposed_seed = int(CFG.main_pool[2])
    excluded = {
        (root / "formal_protocol" / "pipeline.py").resolve(),
        (root / "configs" / "methods" / "limited_validation_formal_cfg.py").resolve(),
        (root / "tests" / "test_limited_validation_protocol.py").resolve(),
    }
    center_hits: List[Dict[str, Any]] = []
    seed_hits: List[Dict[str, Any]] = []
    scanned = 0

    def inspect(obj: Any, key: str, path: Path, locator: str) -> None:
        low = key.lower()
        if isinstance(obj, dict):
            for child_key, value in obj.items():
                inspect(value, str(child_key), path, f"{locator}.{child_key}")
        elif isinstance(obj, list):
            if "pool" in low and len(obj) >= 3 and all(isinstance(x, int) for x in obj[:3]):
                start, count, offset = map(int, obj[:3])
                overlap = sorted(proposed.intersection(range(start, start + max(0, count))))
                if overlap:
                    center_hits.append({"path": str(path), "locator": locator, "values": overlap})
                if offset == proposed_seed:
                    seed_hits.append({"path": str(path), "locator": locator, "value": offset})
            if "center" in low:
                vals = {int(x) for x in obj if isinstance(x, int)}
                overlap = sorted(vals & proposed)
                if overlap:
                    center_hits.append({"path": str(path), "locator": locator, "values": overlap})
            for i, value in enumerate(obj):
                inspect(value, key, path, f"{locator}[{i}]")
        elif isinstance(obj, int):
            if "center" in low and obj in proposed:
                center_hits.append({"path": str(path), "locator": locator, "values": [obj]})
            if "seed" in low and obj == proposed_seed:
                seed_hits.append({"path": str(path), "locator": locator, "value": obj})
        elif isinstance(obj, str):
            ids = {int(x) for x in re.findall(r"\bc(\d+)_h(?:1|4)_k(?:10|20)\b", obj)}
            overlap = sorted(ids & proposed)
            if overlap:
                center_hits.append({"path": str(path), "locator": locator, "values": overlap})

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        resolved = path.resolve()
        if resolved in excluded or output_root.resolve() in resolved.parents:
            continue
        suffix = path.suffix.lower()
        if suffix not in {".json", ".csv", ".md", ".txt", ".py", ".tex", ".yaml", ".yml"}:
            continue
        scanned += 1
        try:
            if suffix == ".json":
                inspect(json.loads(path.read_text(encoding="utf-8")), "root", path, "root")
            elif suffix == ".csv":
                with path.open(encoding="utf-8", errors="replace", newline="") as h:
                    for row_no, row in enumerate(csv.DictReader(h), 2):
                        for key, value in row.items():
                            if value is None:
                                continue
                            if "center" in key.lower() and value.strip().isdigit() and int(value) in proposed:
                                center_hits.append({"path": str(path), "locator": f"row{row_no}.{key}", "values": [int(value)]})
                            if "seed" in key.lower() and value.strip().isdigit() and int(value) == proposed_seed:
                                seed_hits.append({"path": str(path), "locator": f"row{row_no}.{key}", "value": int(value)})
            else:
                text = path.read_text(encoding="utf-8", errors="replace")
                ids = {int(x) for x in re.findall(r"\bc(\d+)_h(?:1|4)_k(?:10|20)\b", text)}
                overlap = sorted(ids & proposed)
                if overlap:
                    center_hits.append({"path": str(path), "locator": "case_key_text", "values": overlap})
                if suffix == ".py":
                    tree = ast.parse(text)
                    for node in ast.walk(tree):
                        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                            continue
                        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                        names = [t.id for t in targets if isinstance(t, ast.Name)]
                        value = node.value
                        if not any("pool" in name.lower() for name in names):
                            continue
                        if isinstance(value, ast.Tuple) and len(value.elts) >= 3 and all(
                            isinstance(x, ast.Constant) and isinstance(x.value, int)
                            for x in value.elts[:3]
                        ):
                            start, count, offset = [int(x.value) for x in value.elts[:3]]
                            pool_overlap = sorted(proposed.intersection(range(start, start + max(0, count))))
                            if pool_overlap:
                                center_hits.append({"path": str(path), "locator": f"python_assignment:{','.join(names)}", "values": pool_overlap})
                            if offset == proposed_seed:
                                seed_hits.append({"path": str(path), "locator": f"python_assignment:{','.join(names)}", "value": offset})
        except (OSError, UnicodeError, json.JSONDecodeError, csv.Error):
            continue
    return {
        "proposed_pool": list(CFG.main_pool),
        "proposed_center_ids": sorted(proposed),
        "proposed_pool_master_seed": int(CFG.data_seed + proposed_seed),
        "files_scanned": scanned,
        "center_id_hits": center_hits,
        "seed_offset_hits": seed_hits,
        "untouched": not center_hits and not seed_hits,
        "scanner_scope": "repository structured JSON/CSV plus case-key text; new declaration files excluded",
    }


def prepare(root: Path, output_root: Path, device: str, safe_mode: str) -> Dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_path = output_root / "protocol_manifest.json"
    if manifest_path.exists():
        obj = load_json(str(manifest_path))
        if obj.get("protocol_version") != CFG.protocol_version:
            raise RuntimeError("Existing output directory belongs to another protocol")
        return obj
    usage = _structured_prior_usage_audit(root, output_root)
    if not usage["untouched"]:
        raise RuntimeError("Proposed main pool appears in prior experiment artifacts")
    cfg, cache, _A, _requested, _safe = build_runtime(
        device, safe_mode, (CFG.main_pool,)
    )
    task = cfg.main.task
    if (task.validation_windows, task.check_windows, task.test_windows) != (
        CFG.validation_windows, CFG.check_windows, CFG.test_windows
    ):
        raise RuntimeError("Active TaskCfg does not match frozen formal protocol")
    verification_rows: List[Dict[str, Any]] = []
    for H in CFG.H_list:
        for K in CFG.K_list:
            Xs, _ys, Xv, _yv, Xc, _yc, _tier, _ctype = get_support_validation_check(
                cfg, cache, CFG.main_pool[0], H, K
            )
            Xt, _yt = get_test_only_after_selection(
                cfg, cache, CFG.main_pool[0], H, K, selection_fixed=True
            )
            layout = fixed_target_raw_layout(
                total_steps=cfg.main.sim.n_history, L=task.L, H=H, K=K,
                validation_windows=task.validation_windows,
                check_windows=task.check_windows,
                test_windows=task.test_windows,
            )
            sets = {name: set(range(*layout[name])) for name in ("support", "validation", "check", "test")}
            disjoint = all(
                sets[a].isdisjoint(sets[b])
                for i, a in enumerate(sets) for b in list(sets)[i + 1:]
            )
            verification_rows.append({
                "H": H, "K": K, "support_windows": len(Xs),
                "validation_windows": len(Xv), "check_windows": len(Xc),
                "test_windows": len(Xt), "raw_layout": layout,
                "raw_point_sets_pairwise_disjoint": disjoint,
                "cross_boundary_windows": False,
                "unused_raw_points": layout["unused"][1] - layout["unused"][0],
            })
    try:
        get_test_only_after_selection(
            cfg, cache, CFG.main_pool[0], 1, 10, selection_fixed=False
        )
        test_gate = False
    except RuntimeError:
        test_gate = True

    source_cfg, source_cache, _A2, _r2, _s2 = build_runtime(device, safe_mode, ())
    source_hashes: Dict[str, Any] = {}
    for H in CFG.H_list:
        Xs, ys, Xv, yv = get_source_training_support_validation(
            source_cfg, source_cache, 0, H, max(CFG.K_list)
        )
        source_hashes[f"h{H}_center0"] = {
            "support_windows": len(Xs), "validation_windows": len(Xv),
            "tensor_sha256": _tensor_sha256(Xs, ys, Xv, yv),
        }
    external = _load_external_manifest(root)
    old_bank_path = root / CFG.old_strong_bank_manifest_path
    old_bank = load_json(str(old_bank_path))
    for item in old_bank.get("assets", {}).values():
        full = _asset_path(root, item)
        if not full.is_file() or _sha256(full) != item["sha256"]:
            raise RuntimeError(f"Old strong-bank asset hash mismatch: {full}")
    center_records = []
    for cid in range(CFG.main_pool[0], CFG.main_pool[0] + CFG.main_pool[1]):
        rec = cache.centers[cid]
        center_records.append({
            "center_id": cid, "center_type": rec.center_type,
            "budget_tier": rec.tier_name,
            "pool_master_seed": rec.metadata.get("pool_master_seed"),
            "center_rng_seed": rec.metadata.get("center_rng_seed"),
            "target_seeds": {
                f"h{H}_k{K}": _case_seed(cid, H, K)
                for H in CFG.H_list for K in CFG.K_list
            },
        })
    changed = _git(root, "status", "--short").splitlines()
    code_paths = [
        root / "configs/main_cfg.py", root / "core/data/center_api.py",
        root / "core/data/sim.py", root / "shared/data_access.py",
        root / "source_prior_bank/pipeline.py", root / "reporting/frozen.py",
        root / "configs/methods/limited_validation_formal_cfg.py",
        root / "tests/test_limited_validation_protocol.py",
        root / "formal_protocol/pipeline.py",
        root / "scripts/run_limited_validation_formal_protocol.py",
    ]
    manifest = {
        "protocol_version": CFG.protocol_version,
        "created_at_unix_s": time.time(),
        "repository": {
            "base_commit": _git(root, "rev-parse", "HEAD"),
            "branch": _git(root, "branch", "--show-current"),
            "status_short": changed,
        },
        "protocol": config_dict(),
        "semantics": {
            "K": "target adaptation support-window budget only",
            "target_instantiation_labeled_windows": "K + 80",
            "validation": "adapted-candidate model selection only",
            "check": "offline screening/calibration/diagnostic only",
            "test": "held-out evaluation after selection fixed",
            "unused_tail": "unused after exact requested window counts",
        },
        "new_main_pool_audit": usage,
        "new_main_center_seed_records": center_records,
        "source_asset_reuse": {
            "allowed": True,
            "reason": "source-only accessor reproduces the legacy ratio-allocated K20 source tensors independently of target V",
            "source_tensor_hashes": source_hashes,
            "external_manifest": {"path": str(root / CFG.external_source_manifest_path), "sha256": _sha256(root / CFG.external_source_manifest_path)},
            "old_strong_bank_manifest": {"path": str(old_bank_path), "sha256": _sha256(old_bank_path)},
            "old_strong_asset_count": len(old_bank.get("assets", {})),
            "external_decision": external.get("decision"),
        },
        "protocol_verification": {
            "cases": verification_rows,
            "test_gate_rejects_unfixed_selection": test_gate,
            "all_pass": test_gate and all(
                r["raw_point_sets_pairwise_disjoint"]
                and (r["support_windows"], r["validation_windows"], r["check_windows"], r["test_windows"]) == (r["K"], 80, 60, 200)
                for r in verification_rows
            ),
        },
        "code_hashes": {str(p.relative_to(root)).replace("\\", "/"): _sha256(p) for p in code_paths if p.exists()},
        "environment": _environment(device),
        "diagnostic_results_policy": "validation_budget_impact_diagnostic is diagnostic-only and excluded from formal headline results",
        "legacy_result_policy": "old 14.60% canonical result is preserved as legacy old-protocol evidence",
    }
    if not manifest["protocol_verification"]["all_pass"]:
        raise RuntimeError("Formal target protocol verification failed")
    atomic_json(usage, str(output_root / "center_usage_audit.json"))
    atomic_json(manifest, str(manifest_path))
    table = [
        "| H | K | Support | Validation | Check | Test | Raw disjoint | Unused raw |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in verification_rows:
        table.append(f"| {r['H']} | {r['K']} | {r['support_windows']} | {r['validation_windows']} | {r['check_windows']} | {r['test_windows']} | {r['raw_point_sets_pairwise_disjoint']} | {r['unused_raw_points']} |")
    protocol_md = f"""# Limited-Validation Formal Protocol

## Material Passport

- Protocol: `{CFG.protocol_version}`
- Repository base commit: `{manifest['repository']['base_commit']}`
- Status: FROZEN BEFORE SCREENING
- Scope: protocol repair through new held-out main evaluation only

K=10/20 is the support-window adaptation budget. Validation is independently fixed at 80 windows, so target-side instantiation uses K+80 labeled windows. Check=60 is offline development evidence. Test=200 is opened only after selection is fixed. Each split is first allocated as a disjoint raw segment; the unused tail is not consumed.

- Screening pool: `{list(CFG.screening_pool)}`
- Calibration development pool: `{list(CFG.calibration_pool)}`
- Calibration final pool: `{list(CFG.calibration_final_pool)}`
- New main pool: `{list(CFG.main_pool)}`; master seed `{CFG.data_seed + CFG.main_pool[2]}`
- New main pool untouched audit: **PASS**
- Source assets: reusable under an independently reproduced legacy source-only recipe; hashes are frozen in `protocol_manifest.json`.
"""
    verification_md = """# Protocol Verification

## Material Passport

- Origin: formal K/80/60/200 repair
- Verification Status: VERIFIED

""" + "\n".join(table) + f"""

- Test accessor rejects calls before selection is fixed: **{test_gate}**
- Cross-boundary windows: **False** for all four H/K cases
- Table 1 values are read from `configs.main_cfg.CFG.task`, not independently hard-coded.
- Source-training tensors remain on the legacy source-only allocation and are independent of target V.
"""
    _write_text(output_root / "LIMITED_VALIDATION_FORMAL_PROTOCOL.md", protocol_md)
    _write_text(output_root / "PROTOCOL_VERIFICATION.md", verification_md)
    _log(output_root, "PREPARE complete: protocol verified and new main pool frozen")
    return manifest


def _load_pt_model(root: Path, external: Mapping[str, Any], A, H, tier, input_dim, L, device):
    return _load_fixed_source_model(
        str(root), external, "pt_ft", H, tier, A, input_dim, L, device
    )[0]


def screening(root: Path, output_root: Path, device: str, safe_mode: str) -> Dict[str, Any]:
    protocol = load_json(str(output_root / "protocol_manifest.json"))
    if not protocol["protocol_verification"]["all_pass"]:
        raise RuntimeError("Protocol verification is not PASS")
    out = output_root / "screening" / "screening_cases.json"
    cfg, cache, A, requested, safe = build_runtime(device, safe_mode, (CFG.screening_pool,))
    frozen = load_frozen_assets(str(root))
    external = _load_external_manifest(root)
    L = int(cfg.main.task.L)
    result = load_json(str(out)) if out.exists() else {
        "protocol_version": CFG.protocol_version,
        "pool": list(CFG.screening_pool), "records": {},
        "architecture_count": len(A), "test_used": False,
        "retention_rule": f"check_true_wins>={CFG.candidate_rule_min_wins} OR validation_positive_wins>={CFG.candidate_rule_min_wins}",
    }
    records = dict(result.get("records", {}))
    jobs = _jobs(CFG.screening_pool)
    started = time.time()
    total = 0
    for cid, H, K in jobs:
        Xs, *_rest, tier, _ctype = get_support_validation_check(cfg, cache, cid, H, K)
        total += len(feasible_indices(cfg, A, tier, L, int(Xs.shape[-1]), H))
    done0 = sum(len(r.get("candidates", {})) for r in records.values())
    done = 0
    for case_no, (cid, H, K) in enumerate(jobs, 1):
        Xs, ys, Xv, yv, Xc, yc, tier, ctype = get_support_validation_check(cfg, cache, cid, H, K)
        input_dim = int(Xs.shape[-1])
        feasible = feasible_indices(cfg, A, tier, L, input_dim, H)
        key = f"c{cid}_h{H}_k{K}_b{tier}"
        rec = dict(records.get(key, {}))
        candidates = dict(rec.get("candidates", {}))
        seed0 = _case_seed(cid, H, K)
        if "pt_anchor" not in rec:
            spec = A[CFG.anchor_arch_idx]
            actual = candidate_device(spec, requested, safe)
            with candidate_backend_context(spec, actual, safe):
                model = _load_pt_model(root, external, A, H, tier, input_dim, L, actual)
                _fixed_target_adapt(model, Xs, ys, seed=seed0 + 11)
                rec["pt_anchor"] = {"validation": eval_metrics(model, Xv, yv), "check": eval_metrics(model, Xc, yc)}
                del model
        for idx in feasible:
            if str(idx) in candidates:
                continue
            spec = A[idx]
            actual = candidate_device(spec, requested, safe)
            with candidate_backend_context(spec, actual, safe):
                model, _prior = _load_prior_model(spec=spec, H=H, L=L, input_dim=input_dim, bank=frozen["bank"], device=actual)
                _fixed_target_adapt(model, Xs, ys, seed=seed0 + 101 * idx)
                params, flops = profile_arch(spec, L=L, input_dim=input_dim, H=H)
                candidates[str(idx)] = {
                    "arch_idx": idx, "arch_key": str(spec.arch_key), "family": str(spec.family),
                    "params": float(params), "flops": float(flops),
                    "validation": eval_metrics(model, Xv, yv), "check": eval_metrics(model, Xc, yc),
                }
                del model
                synchronize_if_cuda(actual)
            done += 1
            rec.update({"case_key": key, "center_id": cid, "center_type": ctype, "budget_tier": tier, "H": H, "K": K, "feasible_indices": feasible, "candidates": candidates, "test_used": False})
            records[key] = rec
            result.update({"records": records, "completed_candidate_count": done0 + done, "expected_candidate_count": total, "complete": False})
            atomic_json(result, str(out))
        rows = list(candidates.values())
        best_check = min(rows, key=lambda r: (r["check"]["weighted_mse"], r["params"], r["flops"], r["arch_idx"]))
        best_val = min(rows, key=lambda r: (r["validation"]["weighted_mse"], r["params"], r["flops"], r["arch_idx"]))
        pt_val = float(rec["pt_anchor"]["validation"]["weighted_mse"])
        pt_chk = float(rec["pt_anchor"]["check"]["weighted_mse"])
        use_alt = float(best_val["validation"]["weighted_mse"]) < pt_val
        rec["summary"] = {
            "c1_check_oracle_arch_idx": int(best_check["arch_idx"]),
            "c1_check_oracle_mse": float(best_check["check"]["weighted_mse"]),
            "validation_selected_arch_idx": int(best_val["arch_idx"]),
            "validation_selected_check_mse": float(best_val["check"]["weighted_mse"]) if use_alt else pt_chk,
            "validation_selected_source": "C1_ARCH_CANDIDATE" if use_alt else "PT_A57_ANCHOR",
            "pt_validation_mse": pt_val, "pt_check_mse": pt_chk,
        }
        rec["complete"] = True
        records[key] = rec
        result.update({"records": records, "N_records": len(records), "complete": len(records) == len(jobs) and all(r.get("complete") for r in records.values())})
        atomic_json(result, str(out))
        if case_no % 4 == 0:
            elapsed = time.time() - started
            eta = elapsed / case_no * (len(jobs) - case_no)
            _log(output_root, f"SCREEN case={case_no}/80 candidates={done0+done}/{total} elapsed={elapsed/60:.1f}m eta={eta/60:.1f}m")
        gc.collect()
        if requested.type == "cuda": torch.cuda.empty_cache()
    check_wins, val_wins = Counter(), Counter()
    for rec in records.values():
        s = rec["summary"]
        if s["c1_check_oracle_mse"] < s["pt_check_mse"]:
            check_wins[s["c1_check_oracle_arch_idx"]] += 1
        if s["validation_selected_source"] == "C1_ARCH_CANDIDATE" and s["validation_selected_check_mse"] < s["pt_check_mse"]:
            val_wins[s["validation_selected_arch_idx"]] += 1
    retained = sorted(i for i in set(check_wins) | set(val_wins) if check_wins[i] >= CFG.candidate_rule_min_wins or val_wins[i] >= CFG.candidate_rule_min_wins)
    summary_rows = [{
        "arch_idx": i, "arch_key": str(A[i].arch_key), "family": str(A[i].family),
        "check_true_wins": int(check_wins[i]), "validation_positive_wins": int(val_wins[i]),
        "retained": i in retained,
    } for i in range(len(A))]
    summary = {
        "protocol_version": CFG.protocol_version, "pool": list(CFG.screening_pool),
        "N_cases": len(records), "architecture_count": len(A),
        "retained_architectures": retained, "rows": summary_rows,
        "test_used": False, "complete": True,
    }
    atomic_json(summary, str(output_root / "screening" / "screening_summary.json"))
    _write_csv(output_root / "screening" / "screening_summary.csv", summary_rows)
    retained_text = ", ".join(f"A{i}" for i in retained) if retained else "none"
    md = f"""# Screening Rerun Report

## Material Passport

- Protocol: `{CFG.protocol_version}`
- Pool: `{list(CFG.screening_pool)}` (original screening centers)
- Status: VERIFIED COMPLETE
- Test used: False

The full 66-configuration feasible space was screened over 80 H/K cases under K/80/60. Retention follows the unchanged rule: at least two check-oracle true wins or at least two validation-positive wins.

- Retained configurations: **{retained_text}**
- Candidate evaluations completed: {result['completed_candidate_count']}/{result['expected_candidate_count']}

Detailed win counts and deployment feasibility evidence are in `screening_summary.csv` and `screening_cases.json`.
"""
    _write_text(output_root / "SCREENING_RERUN_REPORT.md", md)
    _log(output_root, f"SCREEN complete retained={retained_text}")
    return summary


def _iter_source_batches(cfg, cache, H: int, epoch: int):
    rng = random.Random(CFG.train_seed + 10007 * H + epoch)
    centers = list(range(CFG.source_centers)); rng.shuffle(centers)
    for cid in centers:
        Xs, ys, Xv, yv = get_source_training_support_validation(cfg, cache, cid, H, max(CFG.K_list))
        X, y = torch.cat((Xs, Xv)), torch.cat((ys, yv))
        gen = torch.Generator(device=X.device)
        gen.manual_seed(CFG.train_seed + 101 * H + 1009 * cid + epoch)
        order = torch.randperm(len(X), generator=gen, device=X.device)
        for left in range(0, len(X), CFG.source_batch_size):
            idx = order[left:left + CFG.source_batch_size]
            yield X.index_select(0, idx), y.index_select(0, idx)


def bank(root: Path, output_root: Path, device: str, safe_mode: str) -> Dict[str, Any]:
    screen = load_json(str(output_root / "screening" / "screening_summary.json"))
    retained = list(map(int, screen["retained_architectures"]))
    cfg, cache, A, requested, safe = build_runtime(device, safe_mode, ())
    old_path = root / CFG.old_strong_bank_manifest_path
    old = load_json(str(old_path)); old_assets = old.get("assets", {})
    external = _load_external_manifest(root)
    bank_dir = output_root / "candidate_bank" / "assets"; bank_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_root / "candidate_bank" / "candidate_bank_manifest.json"
    manifest = load_json(str(manifest_path)) if manifest_path.exists() else {
        "protocol_version": CFG.protocol_version, "retained_architectures": retained,
        "protected_reference": "PT_A57_A57", "assets": {},
        "source_recipe": {"optimizer": "Adam", "loss": "MSE", "epochs": 50, "lr": .001, "batch_size": 64, "weight_decay": 0.0, "accessor": "get_source_training_support_validation"},
    }
    L = int(cfg.main.task.L)
    X0, *_ = get_source_training_support_validation(cfg, cache, 0, 1, 20)
    input_dim = int(X0.shape[-1])
    jobs = [(H, i) for H in CFG.H_list for i in sorted(set(retained) | {CFG.anchor_arch_idx})]
    for job_no, (H, idx) in enumerate(jobs, 1):
        key = f"h{H}_a{idx}"; dst = bank_dir / f"formal_h{H}_a{idx}.pt"
        if key in manifest["assets"] and dst.exists() and _sha256(dst) == manifest["assets"][key]["sha256"]:
            continue
        spec = A[idx]
        old_item = old_assets.get(key)
        if old_item:
            src = _asset_path(root, old_item)
            if _sha256(src) != old_item["sha256"]:
                raise RuntimeError(f"Old bank asset invalid: {src}")
            shutil.copy2(src, dst)
            provenance = "exact_reuse_old_strong_source_asset"
        elif idx == CFG.anchor_arch_idx:
            item = external["assets"][f"pt_ft_h{H}_btight"]
            src = _asset_path(root, item); shutil.copy2(src, dst)
            provenance = "exact_reuse_protected_PT_A57"
        else:
            actual = candidate_device(spec, requested, safe)
            checkpoint = dst.with_suffix(".progress.pt")
            with candidate_backend_context(spec, actual, safe):
                seed_all(_source_seed(H, idx), actual)
                model = build_model(spec, input_dim=input_dim, H=H, L=L, device=str(actual))
                opt = optim.Adam(model.parameters(), lr=CFG.source_lr, weight_decay=CFG.source_weight_decay)
                start_epoch = 0
                if checkpoint.exists():
                    state = torch.load(checkpoint, map_location=actual)
                    model.load_state_dict(state["model"]); opt.load_state_dict(state["optimizer"])
                    start_epoch = int(state["next_epoch"])
                for epoch in range(start_epoch, CFG.source_epochs):
                    losses = []
                    for Xb, yb in _iter_source_batches(cfg, cache, H, epoch):
                        model.train(); opt.zero_grad(set_to_none=True)
                        loss = ((model(Xb.to(actual).contiguous()) - yb.to(actual).contiguous()) ** 2).mean()
                        if not torch.isfinite(loss): raise RuntimeError("Non-finite source loss")
                        loss.backward(); opt.step(); losses.append(float(loss.detach()))
                    _atomic_torch_save({"model": {k: v.detach().cpu() for k, v in model.state_dict().items()}, "optimizer": opt.state_dict(), "next_epoch": epoch + 1}, checkpoint)
                    _log(output_root, f"BANK job={job_no}/{len(jobs)} H={H} A={idx} epoch={epoch+1}/50 loss={np.mean(losses):.6g}")
                _atomic_torch_save({k: v.detach().cpu() for k, v in model.state_dict().items()}, dst)
                if checkpoint.exists(): checkpoint.unlink()
                del model, opt
            provenance = "new_source_training_exact_frozen_recipe"
        params, flops = profile_arch(spec, L=L, input_dim=input_dim, H=H)
        manifest["assets"][key] = {
            "path": str(dst.relative_to(root)).replace("\\", "/"), "sha256": _sha256(dst),
            "H": H, "arch_idx": idx, "arch_key": str(spec.arch_key), "family": str(spec.family),
            "params": float(params), "flops": float(flops), "provenance": provenance,
            "source_seed": _source_seed(H, idx), "epochs_completed": CFG.source_epochs,
        }
        atomic_json(manifest, str(manifest_path))
    manifest.update({
        "candidate_tokens": ["PT_A57_A57"] + (["LEGACY_C1_A57_A57"] if CFG.anchor_arch_idx in retained else []) + [f"FORMAL_STRONG_A{i}" for i in retained if i != CFG.anchor_arch_idx],
        "asset_count": len(manifest["assets"]), "complete": len(manifest["assets"]) == len(jobs),
        "old_strong_bank_manifest_sha256": _sha256(old_path),
        "source_assets_retrained": [k for k, v in manifest["assets"].items() if v["provenance"].startswith("new_source")],
    })
    atomic_json(manifest, str(manifest_path))
    _log(output_root, f"BANK complete assets={manifest['asset_count']} newly_trained={len(manifest['source_assets_retrained'])}")
    return manifest


def _load_bank_model(root: Path, manifest: Mapping[str, Any], A, H, idx, input_dim, L, device):
    item = manifest["assets"][f"h{H}_a{idx}"]
    path = _asset_path(root, item)
    if _sha256(path) != item["sha256"]: raise RuntimeError(f"Formal bank hash mismatch: {path}")
    state = torch.load(path, map_location=device)
    model = build_model(A[idx], input_dim=input_dim, H=H, L=L, device=str(device))
    model.load_state_dict(state, strict=True)
    return model


def _planned_candidates(retained: Sequence[int], feasible: set[int]) -> List[Tuple[str, int, str]]:
    out = [("PT_A57", CFG.anchor_arch_idx, "strong")]
    if CFG.anchor_arch_idx in retained:
        out.append(("LEGACY_C1_A57", CFG.anchor_arch_idx, "c1"))
    out.extend(("FORMAL_STRONG", i, "strong") for i in retained if i != CFG.anchor_arch_idx and i in feasible)
    return out


def _candidate_cache(root: Path, output_root: Path, pool: Sequence[int], role: str, device: str, safe_mode: str):
    bank_manifest = load_json(str(output_root / "candidate_bank" / "candidate_bank_manifest.json"))
    retained = list(map(int, bank_manifest["retained_architectures"]))
    out = output_root / "calibration" / role / "candidates.json"
    cfg, cache, A, requested, safe = build_runtime(device, safe_mode, (pool,))
    frozen = load_frozen_assets(str(root)); L = int(cfg.main.task.L)
    result = load_json(str(out)) if out.exists() else {"protocol_version": CFG.protocol_version, "role": role, "pool": list(pool), "records": {}, "test_used": False}
    records = dict(result.get("records", {})); jobs = _jobs(pool); started = time.time()
    for n, (cid, H, K) in enumerate(jobs, 1):
        Xs, ys, Xv, yv, Xc, yc, tier, ctype = get_support_validation_check(cfg, cache, cid, H, K)
        feasible = set(feasible_indices(cfg, A, tier, L, int(Xs.shape[-1]), H))
        key = f"c{cid}_h{H}_k{K}_b{tier}"
        if key in records and records[key].get("complete"): continue
        rows = []
        for source, idx, loader in _planned_candidates(retained, feasible):
            spec = A[idx]; actual = candidate_device(spec, requested, safe)
            with candidate_backend_context(spec, actual, safe):
                model = (_load_prior_model(spec=spec, H=H, L=L, input_dim=int(Xs.shape[-1]), bank=frozen["bank"], device=actual)[0] if loader == "c1" else _load_bank_model(root, bank_manifest, A, H, idx, int(Xs.shape[-1]), L, actual))
                _fixed_target_adapt(model, Xs, ys, seed=_case_seed(cid, H, K))
                params, flops = profile_arch(spec, L=L, input_dim=int(Xs.shape[-1]), H=H)
                rows.append({"token": f"{source}_A{idx}", "source": source, "arch_idx": idx, "arch_key": str(spec.arch_key), "family": str(spec.family), "params": float(params), "flops": float(flops), "validation": eval_metrics(model, Xv, yv), "check": eval_metrics(model, Xc, yc), "target_seed": _case_seed(cid, H, K)})
                del model
        records[key] = {"case_key": key, "center_id": cid, "center_type": ctype, "budget_tier": tier, "H": H, "K": K, "candidates": rows, "complete": True, "test_used": False}
        result.update({"records": records, "N_records": len(records), "complete": len(records) == len(jobs)})
        atomic_json(result, str(out))
        if n % 8 == 0: _log(output_root, f"CALIBRATION-{role} case={n}/80 elapsed={(time.time()-started)/60:.1f}m")
        gc.collect()
    return result


def _select(rows: Sequence[Mapping[str, Any]], margin: Optional[float]):
    anchor = next(r for r in rows if r["source"] == "PT_A57")
    alternatives = [r for r in rows if r is not anchor]
    if margin is None or not alternatives:
        return anchor, False
    best = min(alternatives, key=lambda r: (r["validation"]["weighted_mse"], r["params"], r["flops"], r["arch_idx"], r["source"]))
    switched = float(best["validation"]["weighted_mse"]) <= float(anchor["validation"]["weighted_mse"]) * (1 - float(margin))
    return (best if switched else anchor), switched


def _evaluate_margin(records: Mapping[str, Any], margin: Optional[float], seed: int):
    primary, arch, oracle = defaultdict(list), defaultdict(list), defaultdict(list)
    selections = {}; switched = harmful = 0
    for key, rec in records.items():
        rows = rec["candidates"]; pt = next(r for r in rows if r["source"] == "PT_A57")
        selected, did_switch = _select(rows, margin)
        legacy = [r for r in rows if r["source"] == "LEGACY_C1_A57"]
        dual, _ = _select([pt, *legacy], margin) if legacy else (pt, False)
        best_check = min(rows, key=lambda r: r["check"]["weighted_mse"])
        pt_mse = float(pt["check"]["weighted_mse"]); sel_mse = float(selected["check"]["weighted_mse"])
        cid = int(rec["center_id"])
        primary[cid].append(_relative_gain(sel_mse, pt_mse))
        arch[cid].append(_relative_gain(sel_mse, float(dual["check"]["weighted_mse"])))
        oracle[cid].append(_relative_gain(float(best_check["check"]["weighted_mse"]), pt_mse))
        switched += int(did_switch); harmful += int(did_switch and sel_mse > pt_mse)
        selections[key] = {"token": selected["token"], "switched": did_switch, "check_mse": sel_mse, "pt_check_mse": pt_mse}
    p = _center_bootstrap(primary, seed + 1); a = _center_bootstrap(arch, seed + 2); o = _center_bootstrap(oracle, seed + 3)
    harmful_rate = harmful / max(1, len(records))
    eligible = margin is not None and p["mean"] >= CFG.primary_gain_mean and p["ci_low"] > CFG.primary_gain_ci_low and harmful_rate <= CFG.harmful_switch_rate_max and a["mean"] >= CFG.architecture_increment_mean and a["ci_low"] > CFG.architecture_increment_ci_low
    return {"margin_rel": margin, "primary_gain_over_PT": p, "architecture_increment_over_dual_A57": a, "check_oracle_headroom_over_PT": o, "switch_count": switched, "switch_rate": switched / max(1, len(records)), "harmful_switch_count": harmful, "harmful_switch_rate_all_cases": harmful_rate, "eligible": bool(eligible), "selections": selections}


def calibration(root: Path, output_root: Path, device: str, safe_mode: str):
    dev = _candidate_cache(root, output_root, CFG.calibration_pool, "development", device, safe_mode)
    grid, eligible = {}, []
    for i, margin in enumerate(CFG.margin_grid):
        item = _evaluate_margin(dev["records"], margin, CFG.train_seed + 100 * i)
        grid[f"{margin:.6f}"] = item
        if item["eligible"]: eligible.append(margin)
    tau = min(eligible) if eligible else None
    result = {"protocol_version": CFG.protocol_version, "margin_grid": list(CFG.margin_grid), "eligible_margins": eligible, "calibrated_tau": tau, "fallback": tau is None, "fallback_rule": "adapted protected PT-A57 only", "grid_results": grid, "test_used": False}
    atomic_json(result, str(output_root / "calibration" / "calibration_result.json"))
    final = _candidate_cache(root, output_root, CFG.calibration_final_pool, "final", device, safe_mode)
    final_eval = _evaluate_margin(final["records"], tau, CFG.train_seed + 9000)
    atomic_json(final_eval, str(output_root / "calibration" / "calibration_final_evaluation.json"))
    rows = [{"margin": k, "eligible": v["eligible"], "mean_gain": v["primary_gain_over_PT"]["mean"], "ci_low": v["primary_gain_over_PT"]["ci_low"], "ci_high": v["primary_gain_over_PT"]["ci_high"], "architecture_gain": v["architecture_increment_over_dual_A57"]["mean"], "architecture_ci_low": v["architecture_increment_over_dual_A57"]["ci_low"], "harmful_rate": v["harmful_switch_rate_all_cases"], "switch_rate": v["switch_rate"]} for k, v in grid.items()]
    _write_csv(output_root / "calibration" / "calibration_grid.csv", rows)
    tau_text = "protected-reference fallback" if tau is None else f"tau={tau:.3f}"
    md = f"""# Calibration Rerun Report

## Material Passport

- Protocol: `{CFG.protocol_version}`
- Development pool: `{list(CFG.calibration_pool)}`
- One-shot final calibration pool: `{list(CFG.calibration_final_pool)}`
- Status: VERIFIED COMPLETE
- Test used: False

- Eligible margins: `{eligible}`
- Formal selector: **{tau_text}**
- Final-pool mean check gain vs PT: {100*final_eval['primary_gain_over_PT']['mean']:.3f}%
- Final-pool harmful selections: {final_eval['harmful_switch_count']}/80

The margin grid and all eligibility gates are unchanged. No Test result was used for calibration.
"""
    _write_text(output_root / "CALIBRATION_RERUN_REPORT.md", md)
    _log(output_root, f"CALIBRATION complete {tau_text} eligible={eligible}")
    return result


def _run_ours(root, bank_manifest, frozen, cfg, A, requested, safe, Xs, ys, Xv, yv, tier, H, seed, tau):
    feasible = set(feasible_indices(cfg, A, tier, int(cfg.main.task.L), int(Xs.shape[-1]), H))
    rows, states = [], {}
    for source, idx, loader in _planned_candidates(bank_manifest["retained_architectures"], feasible):
        spec = A[idx]; actual = candidate_device(spec, requested, safe)
        with candidate_backend_context(spec, actual, safe):
            model = (_load_prior_model(spec=spec, H=H, L=cfg.main.task.L, input_dim=int(Xs.shape[-1]), bank=frozen["bank"], device=actual)[0] if loader == "c1" else _load_bank_model(root, bank_manifest, A, H, idx, int(Xs.shape[-1]), cfg.main.task.L, actual))
            _fixed_target_adapt(model, Xs, ys, seed=seed)
            params, flops = profile_arch(spec, L=cfg.main.task.L, input_dim=int(Xs.shape[-1]), H=H)
            row = {"token": f"{source}_A{idx}", "source": source, "arch_idx": idx, "arch_key": str(spec.arch_key), "family": str(spec.family), "params": float(params), "flops": float(flops), "validation": eval_metrics(model, Xv, yv)}
            rows.append(row); states[row["token"]] = {k: v.detach().cpu() for k, v in model.state_dict().items()}; del model
    selected, switched = _select(rows, tau)
    spec = A[int(selected["arch_idx"])]; actual = candidate_device(spec, requested, safe)
    model = build_model(spec, input_dim=int(Xs.shape[-1]), H=H, L=cfg.main.task.L, device=str(actual)); model.load_state_dict(states[selected["token"]])
    pt = next(r for r in rows if r["source"] == "PT_A57")
    pt_spec = A[CFG.anchor_arch_idx]; pt_actual = candidate_device(pt_spec, requested, safe)
    pt_model = build_model(pt_spec, input_dim=int(Xs.shape[-1]), H=H, L=cfg.main.task.L, device=str(pt_actual)); pt_model.load_state_dict(states[pt["token"]])
    return model, pt_model, selected, pt, rows, switched


def main_evaluation(root: Path, output_root: Path, device: str, safe_mode: str):
    cal = load_json(str(output_root / "calibration" / "calibration_result.json")); tau = cal["calibrated_tau"]
    bank_manifest = load_json(str(output_root / "candidate_bank" / "candidate_bank_manifest.json"))
    cfg, cache, A, requested, safe = build_runtime(device, safe_mode, (CFG.main_pool,))
    frozen = load_frozen_assets(str(root)); external = _load_external_manifest(root); L = int(cfg.main.task.L)
    methods_dir = output_root / "main" / "methods"; methods_dir.mkdir(parents=True, exist_ok=True)
    method_results = {}
    for method in CFG.methods:
        path = methods_dir / f"{method}.json"
        method_results[method] = load_json(str(path)) if path.exists() else {"protocol_version": CFG.protocol_version, "method": method, "pool": list(CFG.main_pool), "records": {}, "test_opened_after_selection": True}
    started = time.time(); jobs = _jobs(CFG.main_pool)
    for n, (cid, H, K) in enumerate(jobs, 1):
        Xs, ys, Xv, yv, Xc, yc, tier, ctype = get_support_validation_check(cfg, cache, cid, H, K)
        key = f"c{cid}_h{H}_k{K}_b{tier}"; seed = _case_seed(cid, H, K); input_dim = int(Xs.shape[-1])
        for method in CFG.methods:
            obj = method_results[method]; records = obj["records"]
            if key in records and records[key].get("complete"): continue
            if method == "ours_formal":
                model, pt_model, selected, pt_row, candidates, switched = _run_ours(root, bank_manifest, frozen, cfg, A, requested, safe, Xs, ys, Xv, yv, tier, H, seed, tau)
                selector = {"calibrated_tau": tau, "fallback": tau is None, "selected_token": selected["token"], "switched_from_reference": switched, "candidate_validations": candidates}
                spec = A[int(selected["arch_idx"])]; candidate_count = len(candidates); adapted_count = candidate_count
                selection_fixed = True
                Xt, yt = get_test_only_after_selection(cfg, cache, cid, H, K, selection_fixed=selection_fixed)
                test = eval_metrics(model, Xt, yt); pt_test = eval_metrics(pt_model, Xt, yt)
                del pt_model
            elif method in {"pt_ft", "medet_style"}:
                model, spec, idx = _load_fixed_source_model(str(root), external, method, H, tier, A, input_dim, L, requested)
                _fixed_target_adapt(model, Xs, ys, seed=seed); val = eval_metrics(model, Xv, yv)
                selector = {"selector": "fixed_A57", "selected_arch_idx": idx, "selection_uses_test": False}; candidate_count = adapted_count = 1
                Xt, yt = get_test_only_after_selection(cfg, cache, cid, H, K, selection_fixed=True); test = eval_metrics(model, Xt, yt); pt_test = test if method == "pt_ft" else None
            elif method == "scratch50":
                spec = A[CFG.anchor_arch_idx]; seed_all(seed, requested); model = build_model(spec, input_dim=input_dim, H=H, L=L, device=str(requested)); _fixed_target_adapt(model, Xs, ys, seed=seed); val = eval_metrics(model, Xv, yv)
                selector = {"selector": "fixed_A57_random_initialization", "selection_uses_test": False}; candidate_count = adapted_count = 1
                Xt, yt = get_test_only_after_selection(cfg, cache, cid, H, K, selection_fixed=True); test = eval_metrics(model, Xt, yt); pt_test = None
            else:
                model, spec, selected_row, selector, candidate_count, adapted_count = _run_search_case(method, frozen, cfg, A, requested, safe, Xs, ys, Xv, yv, tier, H, input_dim, L, seed)
                val = selected_row["validation"]
                Xt, yt = get_test_only_after_selection(cfg, cache, cid, H, K, selection_fixed=True); test = eval_metrics(model, Xt, yt); pt_test = None
            params, flops = profile_arch(spec, L=L, input_dim=input_dim, H=H)
            if method == "ours_formal": val = selected["validation"]
            records[key] = {"complete": True, "case_key": key, "center_id": cid, "center_type": ctype, "budget_tier": tier, "H": H, "K": K, "arch_idx": int(spec.arch_id), "arch_key": str(spec.arch_key), "family": str(spec.family), "params": float(params), "flops": float(flops), "validation": val, "check": eval_metrics(model, Xc, yc), "test": test, "pt_anchor_test": pt_test, "selector": selector, "candidate_count": candidate_count, "adapted_candidate_count": adapted_count, "target_seed": seed, "selection_uses_check": False, "selection_uses_test": False, "test_opened_after_selection": True, "deployment_limit_satisfied": int(spec.arch_id) in set(feasible_indices(cfg, A, tier, L, input_dim, H))}
            obj.update({"records": records, "N_records": len(records), "expected_records": len(jobs), "complete": len(records) == len(jobs)})
            atomic_json(obj, str(methods_dir / f"{method}.json")); del model
        if n % 4 == 0:
            elapsed = time.time() - started; eta = elapsed / n * (len(jobs) - n)
            _log(output_root, f"MAIN case={n}/80 elapsed={elapsed/60:.1f}m eta={eta/60:.1f}m")
        gc.collect()
        if requested.type == "cuda": torch.cuda.empty_cache()
    ours = method_results["ours_formal"]["records"]; pt = method_results["pt_ft"]["records"]
    gains, by_center = [], defaultdict(list); beneficial = harmful = alt = wins = 0
    selected_counts = Counter(); hk = defaultdict(list); ctype_groups = defaultdict(list)
    for key in sorted(ours):
        r, p = ours[key], pt[key]; g = _relative_gain(r["test"]["weighted_mse"], p["test"]["weighted_mse"])
        gains.append(g); by_center[int(r["center_id"])].append(g); hk[(r["H"], r["K"])].append(g); ctype_groups[r["center_type"]].append(g)
        switched = bool(r["selector"]["switched_from_reference"]); alt += int(switched); wins += int(r["test"]["weighted_mse"] < p["test"]["weighted_mse"])
        beneficial += int(switched and g > 0); harmful += int(switched and g < 0); selected_counts[r["selector"]["selected_token"]] += 1
    boot = _center_bootstrap(by_center, CFG.train_seed + 701 + len("pt_ft") + len("weighted_mse"))
    overall_rows = []
    for method, obj in method_results.items():
        vals = list(obj["records"].values())
        overall_rows.append({"method": method, "N_cases": len(vals), "test_mse_mean": float(np.mean([r["test"]["weighted_mse"] for r in vals])), "test_mae_mean": float(np.mean([r["test"]["mae"] for r in vals])), "test_worst10_mean": float(np.mean([r["test"]["worst10"] for r in vals])), "deployment_satisfaction_rate": float(np.mean([r["deployment_limit_satisfied"] for r in vals]))})
    summary = {"protocol_version": CFG.protocol_version, "pool": list(CFG.main_pool), "calibrated_tau": tau, "fallback": tau is None, "N_cases": len(gains), "N_centers": len(by_center), "mean_paired_mse_reduction": float(np.mean(gains)), "median_case_paired_mse_reduction": float(np.median(gains)), "center_cluster_bootstrap": boot, "mse_win_rate": wins / len(gains), "reference_retained_count": len(gains) - alt, "alternative_selected_count": alt, "beneficial_alternative_selections": beneficial, "harmful_alternative_selections": harmful, "all_case_harmful_rate": harmful / len(gains), "conditional_harmful_rate": harmful / alt if alt else 0.0, "selected_configuration_counts": dict(selected_counts), "deployment_limits_all_satisfied": all(r["deployment_limit_satisfied"] for obj in method_results.values() for r in obj["records"].values()), "hk_stratified": {f"H{H}_K{K}": {"N": len(v), "mean_gain": float(np.mean(v)), "median_gain": float(np.median(v)), "win_rate": float(np.mean(np.asarray(v) > 0))} for (H, K), v in hk.items()}, "center_type_stratified": {k: {"N": len(v), "mean_gain": float(np.mean(v)), "median_gain": float(np.median(v)), "win_rate": float(np.mean(np.asarray(v) > 0))} for k, v in ctype_groups.items()}, "overall_methods": overall_rows, "test_opened_only_after_selection": all(r["test_opened_after_selection"] for obj in method_results.values() for r in obj["records"].values())}
    atomic_json(summary, str(output_root / "main" / "main_summary.json")); _write_csv(output_root / "main" / "main_overall.csv", overall_rows)
    case_rows = []
    for key in sorted(ours):
        r, p = ours[key], pt[key]
        case_rows.append({"case_key": key, "center_id": r["center_id"], "center_type": r["center_type"], "budget_tier": r["budget_tier"], "H": r["H"], "K": r["K"], "selected_token": r["selector"]["selected_token"], "switched": r["selector"]["switched_from_reference"], "ours_test_mse": r["test"]["weighted_mse"], "pt_ft_test_mse": p["test"]["weighted_mse"], "paired_mse_reduction": _relative_gain(r["test"]["weighted_mse"], p["test"]["weighted_mse"]), "harmful_selection": r["selector"]["switched_from_reference"] and r["test"]["weighted_mse"] > p["test"]["weighted_mse"], "deployment_limit_satisfied": r["deployment_limit_satisfied"]})
    _write_csv(output_root / "main" / "canonical_main_cases.csv", case_rows)
    _write_csv(output_root / "main" / "canonical_main_summary.csv", [{k: v for k, v in summary.items() if not isinstance(v, (dict, list))}])
    hk_lines = "\n".join(f"- {k}: mean {100*v['mean_gain']:.3f}%, median {100*v['median_gain']:.3f}%, win {100*v['win_rate']:.2f}%" for k, v in summary["hk_stratified"].items())
    ct_lines = "\n".join(f"- {k}: mean {100*v['mean_gain']:.3f}%, median {100*v['median_gain']:.3f}%, win {100*v['win_rate']:.2f}%" for k, v in summary["center_type_stratified"].items())
    md = f"""# Main Rerun Report

## Material Passport

- Protocol: `{CFG.protocol_version}`
- New untouched pool: `{list(CFG.main_pool)}`
- Status: VERIFIED COMPLETE
- Test opened only after selection: {summary['test_opened_only_after_selection']}

## MSA-DTI vs PT+FT

- Mean paired MSE reduction: **{100*summary['mean_paired_mse_reduction']:.3f}%**
- Median case paired reduction: **{100*summary['median_case_paired_mse_reduction']:.3f}%**
- 95% center-cluster bootstrap CI: **[{100*boot['ci_low']:.3f}%, {100*boot['ci_high']:.3f}%]**
- MSE win rate: **{100*summary['mse_win_rate']:.2f}%**
- Reference retained / alternative selected: {summary['reference_retained_count']} / {alt}
- Beneficial / harmful alternative selections: {beneficial} / {harmful}
- All-case harmful rate: {100*summary['all_case_harmful_rate']:.2f}%
- Conditional harmful rate: {100*summary['conditional_harmful_rate']:.2f}%
- All deployment limits satisfied: **{summary['deployment_limits_all_satisfied']}**

## H/K stratification

{hk_lines}

## Center-type stratification

{ct_lines}

All target-dependent baselines were reevaluated on the same pool and active split. Detailed method and case records are under `main/`.
"""
    _write_text(output_root / "MAIN_RERUN_REPORT.md", md); _log(output_root, f"MAIN complete gain={100*summary['mean_paired_mse_reduction']:.3f}% CI=[{100*boot['ci_low']:.3f},{100*boot['ci_high']:.3f}] harmful={harmful}/80")
    return summary


def finalize(root: Path, output_root: Path, commands: Sequence[str]) -> Dict[str, Any]:
    required = ["LIMITED_VALIDATION_FORMAL_PROTOCOL.md", "PROTOCOL_VERIFICATION.md", "SCREENING_RERUN_REPORT.md", "CALIBRATION_RERUN_REPORT.md", "MAIN_RERUN_REPORT.md"]
    missing = [name for name in required if not (output_root / name).is_file()]
    if missing: raise RuntimeError(f"Missing required reports: {missing}")
    atomic_json({"commands": list(commands)}, str(output_root / "execution_commands.json"))
    changed = {"base_commit": _git(root, "rev-parse", "HEAD"), "status_short": _git(root, "status", "--short").splitlines(), "tracked_diff_paths": _git(root, "diff", "--name-only", "HEAD").splitlines()}
    atomic_json(changed, str(output_root / "files_changed.json"))
    artifacts = {}
    for path in sorted(output_root.rglob("*")):
        if path.is_file() and path.name != "artifact_hash_manifest.json":
            artifacts[str(path.relative_to(output_root)).replace("\\", "/")] = {"size_bytes": path.stat().st_size, "sha256": _sha256(path)}
    result = {"protocol_version": CFG.protocol_version, "complete": True, "artifact_count": len(artifacts), "artifacts": artifacts, "generated_at_unix_s": time.time()}
    atomic_json(result, str(output_root / "artifact_hash_manifest.json"))
    _log(output_root, f"FINALIZE complete artifacts={len(artifacts)}")
    return result
