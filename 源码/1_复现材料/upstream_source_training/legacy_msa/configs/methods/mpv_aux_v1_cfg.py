# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class MPVAuxV1Config:
    protocol_version: str = "mpv_aux_v1_raw_disjoint_development_lopo_1_0"
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    formal_validation_windows: int = 80
    formal_check_windows: int = 60
    formal_test_windows: int = 200
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
    aux_validation_windows: int = 80
    aux_probe_windows: int = 20
    aux_audit_windows: int = 40
    q_grid: Tuple[int, ...] = (5, 10, 20)
    beta_grid: Tuple[float, ...] = (0.25, 0.50, 0.75, 1.00)
    tau_grid: Tuple[float, ...] = (-0.05, 0.00, 0.02, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.35)
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 190071
    epsilon: float = 1e-12
    output_root: str = "results/mpv_aux_v1"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = MPVAuxV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
