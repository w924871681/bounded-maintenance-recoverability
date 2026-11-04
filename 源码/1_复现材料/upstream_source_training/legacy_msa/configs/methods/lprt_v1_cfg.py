# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class LPRTV1Config:
    protocol_version: str = "lprt_v1_exposed_development_lopo_1_0"
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
    epsilon: float = 1e-12
    distance_epsilon: float = 1e-6
    minimum_neighbors: int = 5
    top_k: int = 3
    k_grid: Tuple[int, ...] = (5, 10, 20)
    tau_u_grid: Tuple[float, ...] = (-0.05, 0.00, 0.02, 0.05, 0.075, 0.10, 0.15, 0.20)
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 151007
    output_root: str = "results/lprt_v1"
    prior_candidate_artifact: str = "results/oracle_geometry_selection_information_v1/selection_oof_candidate_predictions.csv"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = LPRTV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
