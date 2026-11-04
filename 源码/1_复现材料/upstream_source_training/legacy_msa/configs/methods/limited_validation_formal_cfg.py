# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class LimitedValidationFormalConfig:
    """Prospectively frozen first-stage K/80/60/200 repair protocol."""

    protocol_version: str = "limited_validation_formal_k80_60_200_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    source_centers: int = 20
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    architecture_count: int = 66
    anchor_arch_idx: int = 57

    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200

    # Original development pools, recovered from the retained C3 source
    # workspace and frozen before this rerun.
    screening_pool: Tuple[int, int, int] = (900, 20, 180000)
    calibration_pool: Tuple[int, int, int] = (940, 20, 200000)
    calibration_final_pool: Tuple[int, int, int] = (960, 20, 210000)

    # New untouched headline pool. The preparation stage must prove that these
    # IDs and this seed offset are absent from all prior experiment artifacts.
    main_pool: Tuple[int, int, int] = (1400, 20, 420000)

    output_root: str = "results/limited_validation_formal_protocol"
    candidate_rule_min_wins: int = 2

    c1_bank_path: str = (
        "outputs/formal_c1_seed2904/shared_artifacts/"
        "ours_weight_bank_source_pooled_c1_v1_src20.pt"
    )
    c1_bank_sha256: str = (
        "bb3a655606af3b554a8f088bb1d2f3f8d9f190b0911a812fd3755d3de3216b9d"
    )
    external_source_manifest_path: str = (
        "outputs/shared.evaluation_external_d2904_t2904/"
        "source_assets/source_assets_manifest.json"
    )
    old_strong_bank_manifest_path: str = (
        "outputs/source_prior_bank_d2904_t2904/strong_bank/"
        "c31_strong_bank_manifest.json"
    )

    source_epochs: int = 50
    source_lr: float = 1e-3
    source_batch_size: int = 64
    source_weight_decay: float = 0.0
    target_steps: int = 50
    target_lr: float = 1e-2
    target_grad_clip: float = 1.0

    margin_grid: Tuple[float, ...] = (0.05, 0.075, 0.10, 0.125, 0.15, 0.20)
    primary_gain_mean: float = 0.03
    primary_gain_ci_low: float = 0.0
    harmful_switch_rate_max: float = 0.05
    architecture_increment_mean: float = 0.03
    architecture_increment_ci_low: float = 0.0

    bootstrap_repeats: int = 4000
    eps: float = 1e-12
    methods: Tuple[str, ...] = (
        "ours_formal",
        "pt_ft",
        "medet_style",
        "scratch50",
        "meta_nas_lite",
        "zero_nas",
        "zero_nas_ft",
    )


CFG = LimitedValidationFormalConfig()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
