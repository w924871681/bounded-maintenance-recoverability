# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class SAAV1MagnitudeAuditConfig:
    protocol_version: str = "saa_v1_optimization_scale_magnitude_audit_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    calibration_pool: Tuple[int, int, int] = (2020, 40, 760000)
    gamma_grid: Tuple[float, ...] = (0.0, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0)
    steps: int = 50
    lr: float = 0.01
    grad_clip: float = 1.0
    epsilon_theta: float = 1e-12
    mandatory_steps: Tuple[int, ...] = (0, 1, 2, 5, 10, 20, 30, 40, 49)
    output_root: str = "results/saa_v1_magnitude_audit"
    parent_result_root: str = "results/saa_v1_calibrate_confirm"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = SAAV1MagnitudeAuditConfig()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
