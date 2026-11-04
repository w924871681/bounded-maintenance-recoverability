# -*- coding: utf-8 -*-
from __future__ import annotations

import copy
import gc
import hashlib
import json
import math
import os
import random
import time
from collections import defaultdict
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from cfg.methods.final_e2e_c23_external_cfg import CFG, config_dict
from core.methods.ours.adapt import adapt_steps
from core.methods.ours.paper_engine import _load_prior_model
from core.methods.ours.stage2_runtime import (
    candidate_backend_context,
    candidate_device,
    synchronize_if_cuda,
)
from core.space import build_model, profile_arch
from final_e2e.data_access import get_support_validation_check, get_test_only
from final_e2e_c23.common import (
    atomic_json,
    build_runtime,
    eval_metrics,
    feasible_indices,
    file_sha256,
    load_frozen_assets,
    load_json,
    seed_all,
)


def _atomic_torch_save_obj(obj: Any, path: str) -> None:
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.{time.time_ns()}.tmp"
    torch.save(obj, tmp)
    os.replace(tmp, path)


def _atomic_torch_save(state: Mapping[str, torch.Tensor], path: str) -> None:
    _atomic_torch_save_obj({k: v.detach().cpu() for k, v in state.items()}, path)


def _rank_score(values: Mapping[int, float], larger_is_better: bool = True) -> Dict[int, float]:
    items = sorted(values.items(), key=lambda kv: kv[1], reverse=larger_is_better)
    n = len(items)
    if n <= 1:
        return {int(k): 1.0 for k, _ in items}
    return {int(k): 1.0 - float(r) / float(n - 1) for r, (k, _v) in enumerate(items)}


def _sample_proxy_batch(
    X: torch.Tensor,
    y: torch.Tensor,
    *,
    points: int,
    batch_size: int,
    seed: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    n = int(X.shape[0])
    take = min(max(1, int(points)), n)
    gen = torch.Generator(device=X.device)
    gen.manual_seed(int(seed))
    idx = torch.randperm(n, generator=gen, device=X.device)[:take]
    Xp, yp = X.index_select(0, idx), y.index_select(0, idx)
    if int(batch_size) > 0 and int(Xp.shape[0]) > int(batch_size):
        idx2 = torch.randperm(int(Xp.shape[0]), generator=gen, device=X.device)[: int(batch_size)]
        Xp, yp = Xp.index_select(0, idx2), yp.index_select(0, idx2)
    return Xp, yp


def _entropy_proxy(model: nn.Module, X: torch.Tensor, y: torch.Tensor) -> float:
    model.train()
    model.zero_grad(set_to_none=True)
    pred = model(X)
    loss = ((pred - y) ** 2).mean()
    params = [p for p in model.parameters() if p.requires_grad]
    grads = torch.autograd.grad(loss, params, retain_graph=False, create_graph=False, allow_unused=True)
    chunks = [g.detach().reshape(-1).abs() for g in grads if g is not None]
    if not chunks:
        return float("-inf")
    flat = torch.cat(chunks)
    total = flat.sum()
    if (not torch.isfinite(total)) or float(total.item()) <= 0.0:
        return float("-inf")
    prob = (flat / (total + 1e-12)).clamp_min(1e-12)
    return float((-(prob * prob.log()).sum()).item())


def _fixed_target_adapt(
    model: nn.Module,
    Xs: torch.Tensor,
    ys: torch.Tensor,
    *,
    steps: int,
    lr: float,
    seed: int,
) -> None:
    dev = next(model.parameters()).device
    seed_all(seed, dev)
    model.train()
    opt = optim.SGD(model.parameters(), lr=float(lr))
    Xd, yd = Xs.to(dev).contiguous(), ys.to(dev).contiguous()
    for _ in range(int(steps)):
        opt.zero_grad(set_to_none=True)
        loss = ((model(Xd) - yd) ** 2).mean()
        if not torch.isfinite(loss):
            raise RuntimeError("Non-finite fixed-backbone target loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), CFG.fixed_target_grad_clip)
        opt.step()


def _search_target_adapt(
    model: nn.Module,
    Xs: torch.Tensor,
    ys: torch.Tensor,
    *,
    seed: int,
) -> None:
    dev = next(model.parameters()).device
    adapt_steps(
        model,
        Xs.to(dev).contiguous(),
        ys.to(dev).contiguous(),
        steps=CFG.search_target_steps,
        lr=CFG.search_target_lr,
        weight_decay=0.0,
        robust_loss_type="huber",
        huber_delta=CFG.search_target_huber_delta,
        cvar_lambda=0.0,
        prior_state=None,
        prior_group_lambdas=None,
        batch_size=0,
        use_amp=False,
        oom_to_cpu=False,
        seed=int(seed),
        max_grad_norm=CFG.search_target_grad_clip,
    )


def _source_case(cfg, cache, cid: int, H: int, K: int):
    return get_support_validation_check(cfg, cache, int(cid), int(H), int(K))


def _iter_source_batches(cfg, cache, H: int, batch_size: int, epoch: int):
    rng = random.Random(CFG.train_seed + 10007 * int(H) + int(epoch))
    centers = list(range(CFG.source_centers))
    rng.shuffle(centers)
    for cid in centers:
        Xs, ys, Xv, yv, *_ = _source_case(cfg, cache, cid, H, max(CFG.K_list))
        X = torch.cat([Xs, Xv], dim=0)
        y = torch.cat([ys, yv], dim=0)
        gen = torch.Generator(device=X.device)
        gen.manual_seed(CFG.train_seed + 101 * H + 1009 * cid + epoch)
        order = torch.randperm(int(X.shape[0]), generator=gen, device=X.device)
        for left in range(0, int(X.shape[0]), int(batch_size)):
            idx = order[left : left + int(batch_size)]
            yield X.index_select(0, idx), y.index_select(0, idx)


def _source_fixed_backbones(cfg, A: Sequence[Any], pi50: Sequence[float], L: int, input_dim: int) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for H in CFG.H_list:
        for tier in ("tight", "medium", "loose"):
            feasible = feasible_indices(cfg, A, tier, L, input_dim, H)
            if not feasible:
                raise RuntimeError(f"No source-fixed feasible backbone for H={H}, tier={tier}")
            idx = max(feasible, key=lambda i: (float(pi50[i]), -int(i)))
            spec = A[idx]
            params, flops = profile_arch(spec, L=L, input_dim=input_dim, H=H)
            out[f"h{H}_b{tier}"] = {
                "arch_idx": int(idx),
                "arch_key": str(spec.arch_key),
                "family": str(spec.family),
                "source_prior_score": float(pi50[idx]),
                "params": float(params),
                "flops": float(flops),
                "selection_data": "source_only_pi50",
            }
    return out


def prepare_source_assets(project_root: str, out_dir: str, device: str, safe_mode: str, smoke: bool = False) -> Dict[str, Any]:
    os.makedirs(out_dir, exist_ok=True)
    cfg, cache, A, requested, _safe = build_runtime(device, safe_mode, ())
    frozen = load_frozen_assets(project_root)
    L = int(cfg.main.task.L)
    X0, _y0, *_ = _source_case(cfg, cache, 0, CFG.H_list[0], max(CFG.K_list))
    input_dim = int(X0.shape[-1])
    backbones = _source_fixed_backbones(cfg, A, frozen["pi50"], L, input_dim)
    pt_epochs = 1 if smoke else CFG.pt_epochs
    meta_iters = 4 if smoke else CFG.medet_meta_iters

    unique_plan = sorted({(int(H), int(backbones[f"h{H}_b{tier}"]["arch_idx"])) for H in CFG.H_list for tier in ("tight", "medium", "loose")})
    print(json.dumps({
        "event": "external_source_asset_plan",
        "fixed_backbones": backbones,
        "unique_H_arch_jobs": unique_plan,
        "unique_pt_models": len(unique_plan),
        "unique_medet_models": len(unique_plan),
        "pt_epochs": pt_epochs,
        "medet_meta_iters": meta_iters,
        "source_centers": CFG.source_centers,
        "target_or_test_used": False,
    }, ensure_ascii=False, indent=2), flush=True)

    manifest: Dict[str, Any] = {
        "study": "final_e2e_c23_external_source_assets",
        "decision": "SOURCE_ASSETS_IN_PROGRESS",
        "protocol": config_dict(),
        "source_centers": list(range(CFG.source_centers)),
        "fixed_backbones": backbones,
        "assets": {},
        "frozen_asset_hashes": frozen["hashes"],
        "selection_data": "source_only_pi50",
        "target_pool_used": False,
        "validation_pool_k_used": False,
        "check_pool_k_used": False,
        "test_used": False,
    }
    trained: Dict[Tuple[str, int, int], Dict[str, Any]] = {}

    for H in CFG.H_list:
        for tier in ("tight", "medium", "loose"):
            bb = backbones[f"h{H}_b{tier}"]
            idx = int(bb["arch_idx"])
            spec = A[idx]

            pt_key = ("pt_ft", H, idx)
            pt_file = os.path.join(out_dir, f"pt_ft_h{H}_a{idx}.pt")
            if pt_key not in trained:
                started = time.perf_counter()
                if not os.path.isfile(pt_file):
                    seed_all(CFG.train_seed + 101 * H + idx, requested)
                    model = build_model(spec, input_dim=input_dim, H=H, L=L, device=str(requested))
                    opt = optim.Adam(model.parameters(), lr=CFG.pt_lr)
                    progress_file = pt_file + ".progress.pt"
                    start_epoch = 0
                    if os.path.isfile(progress_file):
                        checkpoint = torch.load(progress_file, map_location=requested)
                        model.load_state_dict(checkpoint["model"], strict=True)
                        opt.load_state_dict(checkpoint["optimizer"])
                        start_epoch = int(checkpoint.get("next_epoch", 0))
                        print(f"[External:Source:PT] resume H={H} arch={idx} next_epoch={start_epoch}", flush=True)
                    pt_started = time.perf_counter()
                    for epoch in range(start_epoch, pt_epochs):
                        losses = []
                        for Xb, yb in _iter_source_batches(cfg, cache, H, CFG.pt_batch_size, epoch):
                            model.train()
                            opt.zero_grad(set_to_none=True)
                            loss = ((model(Xb.to(requested)) - yb.to(requested)) ** 2).mean()
                            if not torch.isfinite(loss):
                                raise RuntimeError("Non-finite PT source loss")
                            loss.backward()
                            opt.step()
                            losses.append(float(loss.detach().item()))
                        pt_elapsed = time.perf_counter() - pt_started
                        pt_eta = pt_elapsed / max(1, epoch - start_epoch + 1) * max(0, pt_epochs - epoch - 1)
                        _atomic_torch_save_obj({
                            "model": {k: v.detach().cpu() for k, v in model.state_dict().items()},
                            "optimizer": opt.state_dict(),
                            "next_epoch": int(epoch + 1),
                        }, progress_file)
                        print(
                            f"[External:Source:PT] H={H} tier={tier} arch={idx} epoch={epoch+1}/{pt_epochs} loss={np.mean(losses):.6g} elapsed={pt_elapsed/3600:.2f}h eta={pt_eta/3600:.2f}h",
                            flush=True,
                        )
                    synchronize_if_cuda(requested)
                    _atomic_torch_save(model.state_dict(), pt_file)
                    if os.path.isfile(progress_file): os.remove(progress_file)
                    del model
                    if requested.type == "cuda":
                        torch.cuda.empty_cache()
                trained[pt_key] = {
                    "path": os.path.relpath(pt_file, project_root),
                    "sha256": file_sha256(pt_file),
                    "train_seconds_current_run": float(time.perf_counter() - started),
                }
            manifest["assets"][f"pt_ft_h{H}_b{tier}"] = trained[pt_key]
            atomic_json(manifest, os.path.join(out_dir, "source_assets_manifest.json"))

            medet_key = ("medet_style", H, idx)
            medet_file = os.path.join(out_dir, f"medet_style_h{H}_a{idx}.pt")
            if medet_key not in trained:
                started = time.perf_counter()
                if not os.path.isfile(medet_file):
                    seed_all(CFG.train_seed + 211 * H + idx, requested)
                    meta = build_model(spec, input_dim=input_dim, H=H, L=L, device=str(requested))
                    outer = optim.Adam(meta.parameters(), lr=CFG.medet_outer_lr)
                    rng = random.Random(CFG.train_seed + 211 * H + idx)
                    progress_file = medet_file + ".progress.pt"
                    start_iter = 0
                    if os.path.isfile(progress_file):
                        checkpoint = torch.load(progress_file, map_location=requested)
                        meta.load_state_dict(checkpoint["model"], strict=True)
                        outer.load_state_dict(checkpoint["optimizer"])
                        start_iter = int(checkpoint.get("next_iter", 0))
                        if "rng_state" in checkpoint: rng.setstate(checkpoint["rng_state"])
                        print(f"[External:Source:MeDeT] resume H={H} arch={idx} next_iter={start_iter}", flush=True)
                    medet_started = time.perf_counter()
                    for it in range(start_iter, meta_iters):
                        outer.zero_grad(set_to_none=True)
                        grad_acc = [torch.zeros_like(p) for p in meta.parameters()]
                        task_ids = rng.sample(
                            list(range(CFG.source_centers)),
                            k=min(CFG.medet_meta_batch, CFG.source_centers),
                        )
                        val_losses = []
                        for cid in task_ids:
                            K = CFG.K_list[(it + cid) % len(CFG.K_list)]
                            Xs, ys, Xv, yv, *_ = _source_case(cfg, cache, cid, H, K)
                            fast = copy.deepcopy(meta)
                            _fixed_target_adapt(
                                fast,
                                Xs,
                                ys,
                                steps=CFG.medet_inner_steps,
                                lr=CFG.medet_inner_lr,
                                seed=CFG.train_seed + 1009 * cid + 37 * H + it,
                            )
                            dev = next(fast.parameters()).device
                            lv = ((fast(Xv.to(dev)) - yv.to(dev)) ** 2).mean()
                            grads = torch.autograd.grad(lv, tuple(fast.parameters()))
                            for acc, grad in zip(grad_acc, grads):
                                acc.add_(grad.detach())
                            val_losses.append(float(lv.detach().item()))
                            del fast
                        for p, g in zip(meta.parameters(), grad_acc):
                            p.grad = g / max(1, len(task_ids))
                        torch.nn.utils.clip_grad_norm_(meta.parameters(), CFG.medet_grad_clip)
                        outer.step()
                        if (it + 1) == meta_iters or (it + 1) % 10 == 0:
                            _atomic_torch_save_obj({
                                "model": {k: v.detach().cpu() for k, v in meta.state_dict().items()},
                                "optimizer": outer.state_dict(),
                                "next_iter": int(it + 1),
                                "rng_state": rng.getstate(),
                            }, progress_file)
                            medet_elapsed = time.perf_counter() - medet_started
                            completed_now = max(1, it - start_iter + 1)
                            medet_eta = medet_elapsed / completed_now * max(0, meta_iters - it - 1)
                            inner_updates = (it + 1) * min(CFG.medet_meta_batch, CFG.source_centers) * CFG.medet_inner_steps
                            print(
                                f"[External:Source:MeDeT] H={H} tier={tier} arch={idx} iter={it+1}/{meta_iters} inner_updates={inner_updates} meta_val={np.mean(val_losses):.6g} elapsed={medet_elapsed/3600:.2f}h eta={medet_eta/3600:.2f}h",
                                flush=True,
                            )
                    synchronize_if_cuda(requested)
                    _atomic_torch_save(meta.state_dict(), medet_file)
                    if os.path.isfile(progress_file): os.remove(progress_file)
                    del meta
                    if requested.type == "cuda":
                        torch.cuda.empty_cache()
                trained[medet_key] = {
                    "path": os.path.relpath(medet_file, project_root),
                    "sha256": file_sha256(medet_file),
                    "train_seconds_current_run": float(time.perf_counter() - started),
                }
            manifest["assets"][f"medet_style_h{H}_b{tier}"] = trained[medet_key]
            atomic_json(manifest, os.path.join(out_dir, "source_assets_manifest.json"))

    manifest["decision"] = "PASS_EXTERNAL_SOURCE_ASSETS_FROZEN"
    manifest["asset_count"] = len(manifest["assets"])
    manifest["unique_asset_count"] = len({x["sha256"] for x in manifest["assets"].values()})
    atomic_json(manifest, os.path.join(out_dir, "source_assets_manifest.json"))
    return manifest


def _load_source_manifest(project_root: str, source_dir: str) -> Dict[str, Any]:
    path = os.path.join(source_dir, "source_assets_manifest.json")
    obj = load_json(path)
    if obj.get("decision") != "PASS_EXTERNAL_SOURCE_ASSETS_FROZEN":
        raise RuntimeError("External source assets are not frozen PASS")
    if obj.get("test_used") or obj.get("target_pool_used"):
        raise RuntimeError("External source assets used target/test data")
    for item in obj["assets"].values():
        full = os.path.join(project_root, item["path"])
        if not os.path.isfile(full) or file_sha256(full) != item["sha256"]:
            raise RuntimeError(f"External source asset hash mismatch: {full}")
    return obj


def _load_fixed_source_model(
    project_root: str,
    manifest: Mapping[str, Any],
    method: str,
    H: int,
    tier: str,
    A: Sequence[Any],
    input_dim: int,
    L: int,
    device: torch.device,
):
    bb = manifest["fixed_backbones"][f"h{H}_b{tier}"]
    idx = int(bb["arch_idx"])
    spec = A[idx]
    asset = manifest["assets"][f"{method}_h{H}_b{tier}"]
    state = torch.load(os.path.join(project_root, asset["path"]), map_location=device)
    model = build_model(spec, input_dim=input_dim, H=H, L=L, device=str(device))
    model.load_state_dict(state, strict=True)
    return model, spec, idx


def _case_jobs(smoke: bool = False):
    start, count, _offset = CFG.final_pool_k
    jobs = [(cid, H, K) for cid in range(start, start + count) for H in CFG.H_list for K in CFG.K_list]
    return jobs[:2] if smoke else jobs


def _new_result(method: str, source_manifest: Mapping[str, Any], frozen_hashes: Mapping[str, str]) -> Dict[str, Any]:
    return {
        "study": "final_e2e_c23_external_pool_k",
        "method": method,
        "protocol": config_dict(),
        "source_manifest_sha256": hashlib.sha256(
            json.dumps(source_manifest, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest(),
        "frozen_asset_hashes": dict(frozen_hashes),
        "records": {},
        "selection_uses_check": False,
        "selection_uses_test": False,
        "test_opened_only_after_final_twin_fixed": True,
    }


def run_external_method(
    project_root: str,
    method: str,
    out_path: str,
    source_dir: str,
    device: str,
    safe_mode: str,
    smoke: bool = False,
) -> Dict[str, Any]:
    if method not in CFG.methods:
        raise ValueError(f"Unknown external method: {method}")
    start, count, offset = CFG.final_pool_k
    cfg, cache, A, requested, safe = build_runtime(device, safe_mode, ((start, count, offset),))
    frozen = load_frozen_assets(project_root)
    source_manifest = _load_source_manifest(project_root, source_dir)
    L = int(cfg.main.task.L)
    jobs = _case_jobs(smoke)
    out_path = os.path.abspath(out_path)
    result = load_json(out_path) if os.path.isfile(out_path) else _new_result(method, source_manifest, frozen["hashes"])
    if result.get("method") != method:
        raise RuntimeError("External result method mismatch")
    records = dict(result.get("records", {}))
    started = time.perf_counter()
    new_count = 0
    cumulative_adaptations = sum(int(r.get("adapted_candidate_count", 0)) for r in records.values())

    for case_no, (cid, H, K) in enumerate(jobs, 1):
        Xs, ys, Xv, yv, _Xc, _yc, tier, ctype = get_support_validation_check(cfg, cache, cid, H, K)
        case_key = f"c{cid}_h{H}_k{K}_b{tier}"
        if case_key in records:
            continue
        input_dim = int(Xs.shape[-1])
        seed = CFG.train_seed + 1009 * cid + 37 * H + 53 * K
        online_started = time.perf_counter()
        selected_model: Optional[nn.Module] = None
        selected_spec = None
        candidate_count = 0
        adapted_count = 0
        selector: Dict[str, Any] = {}
        max_steps = 0

        if method in ("pt_ft", "medet_style"):
            selected_model, selected_spec, selected_idx = _load_fixed_source_model(
                project_root, source_manifest, method, H, tier, A, input_dim, L, requested
            )
            feasible = selected_idx in feasible_indices(cfg, A, tier, L, input_dim, H)
            if not feasible:
                raise RuntimeError(f"Frozen fixed backbone is infeasible: {method} {case_key}")
            _fixed_target_adapt(
                selected_model,
                Xs,
                ys,
                steps=CFG.fixed_target_steps,
                lr=CFG.fixed_target_lr,
                seed=seed,
            )
            candidate_count = 1
            adapted_count = 1
            max_steps = CFG.fixed_target_steps
            selector = {
                "selector": "source_only_budget_matched_fixed_backbone",
                "arch_idx": int(selected_idx),
                "validation": eval_metrics(selected_model, Xv, yv),
                "selection_data": "source_only_pi50",
                "uses_target_architecture_search": False,
            }

        else:
            feasible = feasible_indices(cfg, A, tier, L, input_dim, H)
            if not feasible:
                raise RuntimeError(f"No feasible architecture: {case_key}")
            Xp, yp = _sample_proxy_batch(
                Xs.to(requested), ys.to(requested), points=CFG.proxy_support_points,
                batch_size=CFG.proxy_batch_size, seed=seed,
            )
            proxy_raw: Dict[int, float] = {}
            for pos, idx in enumerate(feasible, 1):
                spec = A[idx]
                actual = candidate_device(spec, requested, safe)
                with candidate_backend_context(spec, actual, safe):
                    seed_all(seed + idx, actual)
                    proxy_model = build_model(spec, input_dim=input_dim, H=H, L=L, device=str(actual))
                    proxy_raw[idx] = _entropy_proxy(proxy_model, Xp.to(actual), yp.to(actual))
                    del proxy_model
                    synchronize_if_cuda(actual)
                if pos == len(feasible) or pos % 12 == 0:
                    print(
                        f"[External:{method}:proxy] case={case_no}/{len(jobs)} {case_key} arch={pos}/{len(feasible)}",
                        flush=True,
                    )
            proxy_rank = _rank_score(proxy_raw, larger_is_better=True)

            if method == "meta_nas_lite":
                source_rank = _rank_score({i: float(frozen["pi50"][i]) for i in feasible}, larger_is_better=True)
                fused = {
                    i: CFG.meta_prior_weight * source_rank[i] + CFG.meta_proxy_weight * proxy_rank[i]
                    for i in feasible
                }
                shortlist = sorted(feasible, key=lambda i: (-fused[i], i))[: CFG.candidate_budget]
                adapt = True
                selector_name = "source_prior_plus_target_proxy_top12_valbest"
            elif method == "zero_nas":
                shortlist = sorted(feasible, key=lambda i: (-proxy_rank[i], i))[:1]
                adapt = False
                selector_name = "zero_cost_proxy_top1_no_target_ft"
            else:
                shortlist = sorted(feasible, key=lambda i: (-proxy_rank[i], i))[: CFG.candidate_budget]
                adapt = True
                selector_name = "zero_cost_proxy_top12_standard_ft50_valbest"

            candidate_count = len(shortlist)
            best_lex = None
            best_idx = None
            best_val = None
            for pos, idx in enumerate(shortlist, 1):
                spec = A[idx]
                actual = candidate_device(spec, requested, safe)
                with candidate_backend_context(spec, actual, safe):
                    model, _prior_state = _load_prior_model(
                        spec=spec, H=H, L=L, input_dim=input_dim,
                        bank=frozen["bank"], device=actual,
                    )
                    if adapt:
                        _search_target_adapt(model, Xs, ys, seed=seed + idx)
                        adapted_count += 1
                        max_steps = CFG.search_target_steps
                    val = eval_metrics(model, Xv, yv)
                    params, flops = profile_arch(spec, L=L, input_dim=input_dim, H=H)
                    lex = (float(val["weighted_mse"]), float(params), float(flops), int(idx))
                    if best_lex is None or lex < best_lex:
                        if selected_model is not None:
                            del selected_model
                        selected_model, selected_spec, best_idx, best_lex, best_val = model, spec, idx, lex, val
                    else:
                        del model
                    synchronize_if_cuda(actual)
                print(
                    f"[External:{method}:candidate] case={case_no}/{len(jobs)} {case_key} cand={pos}/{len(shortlist)} arch={idx}",
                    flush=True,
                )
            selector = {
                "selector": selector_name,
                "shortlist": [int(x) for x in shortlist],
                "selected_arch_idx": int(best_idx),
                "validation": best_val,
                "hard_feasible_prefilter": True,
                "shared_c1_source_initialization": True,
                "uses_target_condition_profile": False,
                "uses_c23_mode_or_fallback": False,
            }

        if selected_model is None or selected_spec is None:
            raise RuntimeError(f"External method did not return a model: {method} {case_key}")

        online_seconds = float(time.perf_counter() - online_started)
        params, flops = profile_arch(selected_spec, L=L, input_dim=input_dim, H=H)
        # Architecture and parameters are fixed before Check/Test are opened.
        _Xs2, _ys2, _Xv2, _yv2, Xc, yc, _tier2, _ctype2 = get_support_validation_check(cfg, cache, cid, H, K)
        check = eval_metrics(selected_model, Xc, yc)
        Xt, yt = get_test_only(cfg, cache, cid, H, K)
        test = eval_metrics(selected_model, Xt, yt)

        record = {
            "method": method,
            "case_key": case_key,
            "center_id": int(cid),
            "center_type": str(ctype),
            "budget_tier": str(tier),
            "H": int(H),
            "K": int(K),
            "feasible": True,
            "candidate_count": int(candidate_count),
            "adapted_candidate_count": int(adapted_count),
            "arch_idx": int(selected_spec.arch_id),
            "arch_key": str(selected_spec.arch_key),
            "family": str(selected_spec.family),
            "params": float(params),
            "flops": float(flops),
            "selector": selector,
            "check": check,
            "test": test,
            "online_seconds": online_seconds,
            "selection_uses_check": False,
            "selection_uses_test": False,
            "test_opened_after_selection": True,
            "hard_feasible": True,
            "max_online_gradient_steps_per_candidate": int(max_steps),
        }
        cumulative_adaptations += int(adapted_count)
        records[case_key] = record
        result["records"] = records
        result["N_records"] = len(records)
        result["expected_records"] = len(jobs)
        result["complete"] = len(records) == len(jobs)
        atomic_json(result, out_path)
        new_count += 1
        elapsed = time.perf_counter() - started
        eta = elapsed / max(1, new_count) * max(0, len(jobs) - case_no)
        print(
            f"[External:{method}] case={case_no}/{len(jobs)} {case_key} candidates={candidate_count} cumulative_adaptations={cumulative_adaptations} cumulative_gradient_steps={cumulative_adaptations*50} selected=A{record['arch_idx']} test_mse={test['weighted_mse']:.6g} elapsed={elapsed/3600:.2f}h eta={eta/3600:.2f}h",
            flush=True,
        )
        del selected_model
        gc.collect()
        if requested.type == "cuda":
            torch.cuda.empty_cache()

    return result


def _mean(values: Iterable[float]) -> Optional[float]:
    arr = list(values)
    return float(np.mean(arr)) if arr else None


def _cvar90(values: Iterable[float]) -> Optional[float]:
    arr = np.sort(np.asarray(list(values), dtype=float))
    if arr.size == 0:
        return None
    k = max(1, int(math.ceil(0.1 * arr.size)))
    return float(arr[-k:].mean())


def _center_bootstrap(values_by_center: Mapping[int, Sequence[float]], seed: int) -> Dict[str, Any]:
    arr = np.asarray([np.mean(values_by_center[c]) for c in sorted(values_by_center)], dtype=float)
    if arr.size == 0:
        return {"mean": None, "median": None, "ci_low": None, "ci_high": None, "n_centers": 0}
    rng = np.random.default_rng(int(seed))
    ids = rng.integers(0, len(arr), size=(CFG.bootstrap_repeats, len(arr)))
    boot = arr[ids].mean(axis=1)
    return {
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "ci_low": float(np.quantile(boot, 0.025)),
        "ci_high": float(np.quantile(boot, 0.975)),
        "n_centers": int(len(arr)),
    }


def _relative_gain(new: float, ref: float) -> float:
    return float((float(ref) - float(new)) / (abs(float(ref)) + CFG.eps))


def analyze_external(project_root: str, root: str) -> Dict[str, Any]:
    root = os.path.abspath(root)
    method_dir = os.path.join(root, "methods")
    ours_path = os.path.join(project_root, CFG.ours_result_path)
    ours = load_json(ours_path)
    payloads = {"ours_c23": ours}
    for method in CFG.methods:
        path = os.path.join(method_dir, f"{method}.json")
        if os.path.isfile(path):
            payloads[method] = load_json(path)

    def rows(obj):
        rec = obj.get("records", {})
        return rec if isinstance(rec, dict) else {}

    all_rows = {m: rows(p) for m, p in payloads.items()}
    overall = []
    for method, mapping in all_rows.items():
        vals = [r for r in mapping.values() if bool(r.get("feasible"))]
        overall.append({
            "method": method,
            "N_total": len(mapping),
            "N_feasible": len(vals),
            "feasible_rate": float(len(vals) / max(1, len(mapping))),
            "test_mse_mean": _mean(r["test"]["weighted_mse"] for r in vals),
            "test_mae_mean": _mean(r["test"]["mae"] for r in vals),
            "test_worst10_mean": _mean(r["test"]["worst10"] for r in vals),
            "case_cvar90_mse": _cvar90(r["test"]["weighted_mse"] for r in vals),
            "online_seconds_mean": _mean(r.get("online_seconds", 0.0) for r in vals),
            "params_mean": _mean(r.get("params", 0.0) for r in vals),
            "flops_mean": _mean(r.get("flops", 0.0) for r in vals),
        })

    paired = {}
    ours_rows = all_rows["ours_c23"]
    for method in CFG.methods:
        if method not in all_rows:
            continue
        base = all_rows[method]
        common = sorted(set(ours_rows) & set(base))
        gains_by_center: Dict[int, list[float]] = defaultdict(list)
        wins = 0
        n = 0
        for key in common:
            ro, rb = ours_rows[key], base[key]
            if not bool(ro.get("feasible")) or not bool(rb.get("feasible")):
                continue
            go = float(ro["test"]["weighted_mse"])
            gb = float(rb["test"]["weighted_mse"])
            gains_by_center[int(ro["center_id"])].append(_relative_gain(go, gb))
            wins += int(go < gb)
            n += 1
        paired[method] = {
            "N_common_feasible": n,
            "mse_win_rate": float(wins / max(1, n)),
            "mse_gain": _center_bootstrap(gains_by_center, CFG.train_seed + 701 + len(method)),
        }

    source_manifest_path = os.path.join(root, "source_assets", "source_assets_manifest.json")
    source_manifest = load_json(source_manifest_path) if os.path.isfile(source_manifest_path) else None
    summary = {
        "decision": "FINAL_E2E_C23_EXTERNAL_ANALYSIS_COMPLETE",
        "protocol": config_dict(),
        "overall": overall,
        "paired_ours_vs_external": paired,
        "primary_methods": ["ours_c23", *CFG.primary_methods],
        "diagnostic_methods": ["zero_nas"],
        "source_manifest": source_manifest,
        "test_used_only_after_each_final_twin_was_fixed": all(
            bool(p.get("test_opened_only_after_final_twin_fixed")) for p in payloads.values()
        ),
        "methods_present": list(all_rows),
    }
    out_dir = os.path.join(root, "analysis")
    os.makedirs(out_dir, exist_ok=True)
    atomic_json(summary, os.path.join(out_dir, "external_comparison_summary.json"))

    csv_path = os.path.join(out_dir, "external_comparison_overall.csv")
    import csv
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        fields = list(overall[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(overall)

    report = [
        "# C2.3 External Baseline Comparison",
        "",
        "Primary table: Ours, PT+FT, MeDeT-style, Meta+NAS-lite, Zero-NAS+FT.",
        "Zero-NAS without target adaptation is retained as a diagnostic baseline.",
        "",
        "| Method | Feasible | MSE | MAE | Worst-10% | CVaR90 | Online s | Params | FLOPs |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in overall:
        report.append(
            "| {method} | {feasible_rate:.1%} | {test_mse_mean:.8f} | {test_mae_mean:.8f} | {test_worst10_mean:.8f} | {case_cvar90_mse:.8f} | {online_seconds_mean:.3f} | {params_mean:.1f} | {flops_mean:.1f} |".format(**row)
        )
    report.extend(["", "## Paired Ours comparisons", ""])
    for method, comp in paired.items():
        gain = comp["mse_gain"]
        report.append(
            f"- Ours vs {method}: N={comp['N_common_feasible']}, win={comp['mse_win_rate']:.3f}, "
            f"gain={100*gain['mean']:.3f}% (95% CI {100*gain['ci_low']:.3f}%, {100*gain['ci_high']:.3f}%)."
        )
    with open(os.path.join(out_dir, "external_comparison_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    return summary


def audit_external(project_root: str, root: str) -> Dict[str, Any]:
    root = os.path.abspath(root)
    final_audit_path = os.path.join(project_root, CFG.final_audit_path)
    ours_path = os.path.join(project_root, CFG.ours_result_path)
    identity_path = os.path.join(root, "preflight", "external_baseline_identity.json")
    source_manifest_path = os.path.join(root, "source_assets", "source_assets_manifest.json")
    analysis_path = os.path.join(root, "analysis", "external_comparison_summary.json")
    paths_present = all(os.path.isfile(x) for x in [final_audit_path, ours_path, identity_path, source_manifest_path, analysis_path])
    final_audit = load_json(final_audit_path) if os.path.isfile(final_audit_path) else {}
    identity = load_json(identity_path) if os.path.isfile(identity_path) else {}
    source_manifest = load_json(source_manifest_path) if os.path.isfile(source_manifest_path) else {}
    ours = load_json(ours_path) if os.path.isfile(ours_path) else {}
    ours_keys = set(ours.get("records", {}))

    expected_counts = {
        "pt_ft": (1, 1, 50),
        "medet_style": (1, 1, 50),
        "meta_nas_lite": (12, 12, 50),
        "zero_nas": (1, 0, 0),
        "zero_nas_ft": (12, 12, 50),
    }
    method_present = {}
    method_complete = {}
    per_method_protocol = {}
    same_case_keys = {}
    total_records = 0

    for method in CFG.methods:
        path = os.path.join(root, "methods", f"{method}.json")
        method_present[method] = os.path.isfile(path)
        if not os.path.isfile(path):
            method_complete[method] = False
            per_method_protocol[method] = False
            same_case_keys[method] = False
            continue
        obj = load_json(path)
        rows = obj.get("records", {})
        method_complete[method] = bool(obj.get("complete")) and len(rows) == 200
        same_case_keys[method] = set(rows) == ours_keys
        exp_cand, exp_adapt, exp_steps = expected_counts[method]
        checks = []
        for row in rows.values():
            checks.append(
                bool(row.get("hard_feasible"))
                and not bool(row.get("selection_uses_check"))
                and not bool(row.get("selection_uses_test"))
                and bool(row.get("test_opened_after_selection"))
                and int(row.get("candidate_count", -1)) == exp_cand
                and int(row.get("adapted_candidate_count", -1)) == exp_adapt
                and int(row.get("max_online_gradient_steps_per_candidate", -1)) == exp_steps
            )
        per_method_protocol[method] = bool(checks) and all(checks)
        total_records += len(rows)

    checks = {
        "required_files_present": paths_present,
        "current_final_audit_pass": final_audit.get("decision") == CFG.expected_final_audit_decision,
        "external_identity_frozen": identity.get("decision") == "PASS_EXTERNAL_BASELINE_PROTOCOL_FROZEN",
        "external_identity_test_unused": identity.get("test_used") is False,
        "source_assets_pass": source_manifest.get("decision") == "PASS_EXTERNAL_SOURCE_ASSETS_FROZEN",
        "source_assets_source_only": source_manifest.get("target_pool_used") is False,
        "source_assets_test_unused": source_manifest.get("test_used") is False,
        "all_methods_present": all(method_present.values()),
        "all_methods_complete": all(method_complete.values()),
        "all_methods_same_pool_k_cases": all(same_case_keys.values()),
        "all_method_protocols": all(per_method_protocol.values()),
        "analysis_complete": load_json(analysis_path).get("decision") == "FINAL_E2E_C23_EXTERNAL_ANALYSIS_COMPLETE" if os.path.isfile(analysis_path) else False,
    }
    decision = "PASS_FINAL_E2E_C23_EXTERNAL_BASELINES_COMPLETE_AND_AUDITED" if all(checks.values()) else "FAIL_FINAL_E2E_C23_EXTERNAL_BASELINE_AUDIT_STOP"
    out = {
        "study": "final_e2e_c23_external_baseline_audit",
        "decision": decision,
        "protocol": config_dict(),
        "checks": checks,
        "method_present": method_present,
        "method_complete": method_complete,
        "same_case_keys": same_case_keys,
        "per_method_protocol": per_method_protocol,
        "N_external_records": total_records,
        "expected_external_records": 1000,
        "test_used_for_selection": False,
        "pool_k_did_not_tune_baseline_hyperparameters": True,
    }
    out_dir = os.path.join(root, "audit")
    os.makedirs(out_dir, exist_ok=True)
    atomic_json(out, os.path.join(out_dir, "external_baseline_audit.json"))
    return out
