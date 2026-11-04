# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class SelectorImprovementStudyConfig:
    protocol_version: str = "selector_improvement_development_only_v1_0"
    parent_protocol_version: str = "limited_validation_formal_k80_60_200_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    validation_blocks: Tuple[Tuple[int, int], ...] = ((0, 20), (20, 40), (40, 60), (60, 80))
    selectors: Tuple[str, ...] = (
        "S0_CURRENT_GLOBAL_MARGIN",
        "S1_BLOCK_MEDIAN_MARGIN",
        "S2_BLOCK_CONSENSUS_MARGIN",
    )
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
    development_bootstrap_seed: int = 22904
    confirmation_bootstrap_seed: int = 23904
    development_pool: Tuple[int, int, int] = (1660, 20, 630000)
    conditional_confirmation_pool: Tuple[int, int, int] = (1680, 20, 640000)
    output_root: str = "results/selector_improvement_study"
    bank_manifest_path: str = (
        "results/limited_validation_formal_protocol/candidate_bank/"
        "candidate_bank_manifest.json"
    )
    bank_manifest_sha256: str = (
        "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"
    )


CFG = SelectorImprovementStudyConfig()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
