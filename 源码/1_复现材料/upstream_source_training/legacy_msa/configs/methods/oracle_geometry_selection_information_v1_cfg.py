# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class OracleGeometrySelectionInformationV1Config:
    protocol_version: str = "oracle_geometry_selection_information_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
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
    tau: float = 0.35
    target_steps: int = 50
    target_lr: float = 0.01
    target_grad_clip: float = 1.0
    epsilon: float = 1e-12
    near_deltas: Tuple[float, ...] = (0.01, 0.03, 0.05)
    alpha_grid: Tuple[float, ...] = (0.01, 0.1, 1.0, 10.0, 100.0)
    threshold_grid: Tuple[float, ...] = (-0.05, 0.0, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20)
    outer_folds: int = 5
    inner_folds: int = 5
    cv_seed: int = 82904
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 92904
    output_root: str = "results/oracle_geometry_selection_information_v1"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"
    protected_reference: str = "PT_A57_A57"


CFG = OracleGeometrySelectionInformationV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
