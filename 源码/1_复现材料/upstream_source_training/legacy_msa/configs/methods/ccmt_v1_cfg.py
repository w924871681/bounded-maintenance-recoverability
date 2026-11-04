# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class CCMTV1Config:
    protocol_version: str = "ccmt_v1_exposed_development_lopo_1_0"
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    exposed_pools: Tuple[Tuple[int, int, int], ...] = (
        (1980, 40, 730000), (2020, 40, 760000),
        (2100, 40, 800000), (2140, 40, 810000),
    )
    protected_reference: str = "PT_A57_A57"
    candidate_vocabulary: Tuple[str, ...] = (
        "PT_A57_A57", "LEGACY_C1_A57_A57", "FORMAL_STRONG_A1",
        "FORMAL_STRONG_A6", "FORMAL_STRONG_A46", "FORMAL_STRONG_A55",
        "FORMAL_STRONG_A56", "FORMAL_STRONG_A62",
    )
    formal_tau: float = 0.35
    ordinary_steps: int = 50
    epsilon: float = 1e-12
    top_k: int = 3
    min_rows_per_candidate: int = 80
    tau_u_grid: Tuple[float, ...] = (-0.05, 0.00, 0.02, 0.05, 0.075, 0.10, 0.15, 0.20)
    reliability_bins: Tuple[str, ...] = ("(-inf,0]", "(0,0.10]", "(0.10,0.20]", "(0.20,0.35]", "(0.35,inf)")
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 181019
    output_root: str = "results/ccmt_v1"
    prior_candidate_artifact: str = "results/oracle_geometry_selection_information_v1/selection_oof_candidate_predictions.csv"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = CCMTV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
