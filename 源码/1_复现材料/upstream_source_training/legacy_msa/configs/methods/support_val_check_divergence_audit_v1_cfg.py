# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class SupportValCheckDivergenceAuditV1Config:
    protocol_version: str = "support_val_check_divergence_audit_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    diagnostic_pool: Tuple[int, int, int] = (2140, 40, 810000)
    t_grid: Tuple[int, ...] = (0, 1, 5, 10, 20, 50)
    primary_contrast: Tuple[int, int] = (20, 50)
    target_lr: float = 0.01
    target_grad_clip: float = 1.0
    tau_record_only: float = 0.35
    epsilon: float = 1e-12
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 72904
    support_material_threshold: float = 0.03
    check_material_threshold: float = 0.03
    output_root: str = "results/support_val_check_divergence_audit_v1"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"
    protected_reference: str = "PT_A57_A57"


CFG = SupportValCheckDivergenceAuditV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
