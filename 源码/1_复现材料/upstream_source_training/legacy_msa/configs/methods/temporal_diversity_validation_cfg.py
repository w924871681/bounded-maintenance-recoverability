# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class TemporalDiversityValidationConfig:
    protocol_version: str = "temporal_diversity_validation_development_only_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_label_budget: int = 80
    validation_observation_span_raw: int = 416
    check_windows: int = 60
    test_windows: int = 200
    strategies: Tuple[str, ...] = ("D0_CONSECUTIVE_80_CONTROL", "D1_TEMPORALLY_DIVERSE_80")
    margin_grid: Tuple[float, ...] = (
        0.05, 0.075, 0.10, 0.125, 0.15, 0.20,
        0.225, 0.25, 0.275, 0.30, 0.325, 0.35,
        0.375, 0.40, 0.425, 0.45, 0.475, 0.50,
    )
    primary_gain_mean: float = 0.03
    primary_gain_ci_low: float = 0.0
    harmful_switch_rate_max: float = 0.05
    architecture_increment_mean: float = 0.03
    architecture_increment_ci_low: float = 0.0
    bootstrap_repeats: int = 4000
    development_bootstrap_seed: int = 24904
    confirmation_bootstrap_seed: int = 25904
    development_pool: Tuple[int, int, int] = (1700, 20, 650000)
    conditional_confirmation_pool: Tuple[int, int, int] = (1720, 20, 660000)
    output_root: str = "results/temporal_diversity_validation_study"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = TemporalDiversityValidationConfig()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
