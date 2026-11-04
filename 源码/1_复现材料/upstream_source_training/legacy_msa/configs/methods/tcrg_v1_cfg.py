# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class TCRGV1Config:
    protocol_version: str = "tcrg_v1_train_calibrate_confirm_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    validation_blocks: Tuple[Tuple[int, int], ...] = ((0, 20), (20, 40), (40, 60), (60, 80))
    epsilon: float = 1e-12
    c_grid: Tuple[float, ...] = (0.01, 0.1, 1.0, 10.0)
    cv_folds: int = 5
    cv_seed: int = 26904
    p0_grid: Tuple[float, ...] = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95)
    primary_gain_mean: float = 0.03
    harmful_switch_rate_max: float = 0.05
    architecture_increment_mean: float = 0.03
    bootstrap_repeats: int = 4000
    calibration_bootstrap_seed: int = 27904
    confirmation_bootstrap_seed: int = 28904
    reliability_training_pool: Tuple[int, int, int] = (1740, 80, 670000)
    p0_calibration_pool: Tuple[int, int, int] = (1820, 20, 680000)
    conditional_confirmation_pool: Tuple[int, int, int] = (1840, 20, 690000)
    control_tau: float = 0.35
    output_root: str = "results/tcrg_v1_train_calibrate_confirm"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = TCRGV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
