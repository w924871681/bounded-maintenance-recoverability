# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

import torch

from core.data.center_api import (
    MetaDatasetCache,
    _allocate_raw_segments,
    _normalize_value_channels_from_support,
    build_feature_matrix,
    fixed_target_raw_layout,
    make_windows,
)


def _series(cfg, cache: MetaDatasetCache, center_id: int, H: int, K: int):
    rec = cache.centers[int(center_id)]
    if rec.y is None:
        raise ValueError("CenterRecord.y is None")
    L, H, K = int(cfg.main.task.L), int(H), int(K)
    return rec, build_feature_matrix(cfg, rec), rec.y, L, H, K


def _target_layout(cfg, X_series: torch.Tensor, L: int, H: int, K: int):
    return fixed_target_raw_layout(
        total_steps=int(X_series.shape[0]),
        L=L,
        H=H,
        K=K,
        validation_windows=int(cfg.main.task.validation_windows),
        check_windows=int(cfg.main.task.check_windows),
        test_windows=int(cfg.main.task.test_windows),
    )


def _window_segment(X_series, y_series, bounds, *, L: int, H: int):
    left, right = bounds
    return make_windows(X_series[left:right], y_series[left:right], L=L, H=H)


def get_support_validation_check(
    cfg,
    cache: MetaDatasetCache,
    center_id: int,
    H: int,
    K: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, str, str]:
    """Return the active K/80/60 target instantiation/development splits."""
    rec, X_series, y_series, L, H, K = _series(cfg, cache, center_id, H, K)
    layout = _target_layout(cfg, X_series, L, H, K)
    Xs, ys = _window_segment(X_series, y_series, layout["support"], L=L, H=H)
    Xv, yv = _window_segment(X_series, y_series, layout["validation"], L=L, H=H)
    Xc, yc = _window_segment(X_series, y_series, layout["check"], L=L, H=H)
    expected = (K, int(cfg.main.task.validation_windows), int(cfg.main.task.check_windows))
    actual = (int(Xs.shape[0]), int(Xv.shape[0]), int(Xc.shape[0]))
    if actual != expected:
        raise RuntimeError(f"Target split count mismatch: {actual} != {expected}")
    if bool(getattr(cfg.main.task, "normalize_values_from_support", False)):
        Xs, Xv, Xc = _normalize_value_channels_from_support(
            (Xs, Xv, Xc),
            k_max=int(cfg.main.sim.k_max),
            include_mask=bool(cfg.main.task.include_mask),
        )
    return Xs, ys, Xv, yv, Xc, yc, rec.tier_name, rec.center_type


def get_test_only_after_selection(
    cfg,
    cache: MetaDatasetCache,
    center_id: int,
    H: int,
    K: int,
    *,
    selection_fixed: bool,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Materialize the active 200-window Test split after selection is fixed."""
    if selection_fixed is not True:
        raise RuntimeError("Test access denied until target-side selection is fixed")
    _rec, X_series, y_series, L, H, K = _series(cfg, cache, center_id, H, K)
    layout = _target_layout(cfg, X_series, L, H, K)
    Xt, yt = _window_segment(X_series, y_series, layout["test"], L=L, H=H)
    expected = int(cfg.main.task.test_windows)
    if int(Xt.shape[0]) != expected:
        raise RuntimeError(f"Test count mismatch: {Xt.shape[0]} != {expected}")
    if bool(getattr(cfg.main.task, "normalize_values_from_support", False)):
        Xsup, _ys = _window_segment(
            X_series, y_series, layout["support"], L=L, H=H
        )
        Xsup, Xt = _normalize_value_channels_from_support(
            (Xsup, Xt),
            k_max=int(cfg.main.sim.k_max),
            include_mask=bool(cfg.main.task.include_mask),
        )
    return Xt, yt


def get_test_only(
    cfg,
    cache: MetaDatasetCache,
    center_id: int,
    H: int,
    K: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Legacy compatibility accessor for archived experiment reproduction.

    New formal runners must call :func:`get_test_only_after_selection`, whose
    explicit gate is covered by deterministic protocol tests.
    """
    return get_test_only_after_selection(
        cfg, cache, center_id, H, K, selection_fixed=True
    )


def get_source_training_support_validation(
    cfg,
    cache: MetaDatasetCache,
    center_id: int,
    H: int,
    K: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Reproduce the frozen source-training recipe independently of target V.

    The legacy source recipe trained on the old ratio-allocated support plus
    validation tensors at K=20. Keeping that allocation behind a source-only
    accessor allows its frozen weights to remain valid while the target-side
    protocol moves to K/80/60/200.
    """
    _rec, X_series, y_series, L, H, K = _series(cfg, cache, center_id, H, K)
    support_steps = L + H + K - 1
    n_sup, n_val, _n_chk, _n_test = _allocate_raw_segments(
        total_steps=int(X_series.shape[0]),
        support_steps=support_steps,
        min_eval_steps=L + H,
        val_ratio=float(cfg.main.task.val_ratio),
        chk_ratio=float(cfg.main.task.chk_ratio),
        test_ratio=float(cfg.main.task.test_ratio),
    )
    Xs, ys = make_windows(X_series[:n_sup], y_series[:n_sup], L=L, H=H)
    Xv, yv = make_windows(
        X_series[n_sup:n_sup + n_val],
        y_series[n_sup:n_sup + n_val],
        L=L,
        H=H,
    )
    if int(Xs.shape[0]) != K:
        raise RuntimeError(f"Source support count mismatch: {Xs.shape[0]} != {K}")
    if bool(getattr(cfg.main.task, "normalize_values_from_support", False)):
        Xs, Xv = _normalize_value_channels_from_support(
            (Xs, Xv),
            k_max=int(cfg.main.sim.k_max),
            include_mask=bool(cfg.main.task.include_mask),
        )
    return Xs, ys, Xv, yv
