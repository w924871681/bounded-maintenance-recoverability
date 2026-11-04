# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class PPCRV1Config:
    protocol_version: str = "ppcr_v1_exposed_development_nested_cv_1_0"
    data_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    exposed_pools: Tuple[Tuple[int, int, int], ...] = (
        (1980, 40, 730000),
        (2020, 40, 760000),
        (2100, 40, 800000),
        (2140, 40, 810000),
    )
    protected_reference: str = "PT_A57_A57"
    formal_tau: float = 0.35
    ordinary_steps: int = 50
    ordinary_lr: float = 0.01
    ordinary_grad_clip: float = 1.0
    epsilon: float = 1e-12
    topk_grid: Tuple[int, ...] = (1, 2, 3, 4)
    near_deltas: Tuple[float, ...] = (0.01, 0.03, 0.05)
    C_grid: Tuple[float, ...] = (0.01, 0.1, 1.0, 10.0, 100.0)
    eta_grid: Tuple[float, ...] = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95)
    outer_folds: int = 5
    inner_folds: int = 5
    cv_seed: int = 83905
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 93905
    output_root: str = "results/ppcr_v1"
    prior_candidate_artifact: str = "results/oracle_geometry_selection_information_v1/selection_oof_candidate_predictions.csv"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = PPCRV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
