# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class SAAV1Config:
    protocol_version: str = "saa_v1_source_anchored_calibrate_confirm_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    epsilon: float = 1e-12
    epsilon_theta: float = 1e-12
    tau_diagnostic: float = 0.35
    gamma_grid: Tuple[float, ...] = (0.0, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0)
    target_steps: int = 50
    target_lr: float = 1e-2
    target_grad_clip: float = 1.0
    criterion_mean: float = 0.03
    criterion_ci_low: float = 0.0
    bootstrap_repeats: int = 4000
    calibration_bootstrap_seed: int = 42904
    confirmation_bootstrap_seed: int = 52904
    calibration_pool: Tuple[int, int, int] = (2020, 40, 760000)
    confirmation_pool: Tuple[int, int, int] = (2060, 20, 780000)
    output_root: str = "results/saa_v1_calibrate_confirm"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"
    protected_reference: str = "PT_A57_A57"
    canonical_adaptation_path: str = "main_evaluation/pipeline.py"


CFG = SAAV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
