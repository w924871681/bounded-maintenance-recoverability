# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class OracleCeilingAuditConfig:
    protocol_version: str = "oracle_ceiling_bottleneck_development_audit_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    epsilon: float = 1e-12
    tau: float = 0.35
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 32904
    diagnostic_pool: Tuple[int, int, int] = (1980, 40, 730000)
    output_root: str = "results/oracle_ceiling_bottleneck_audit"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = OracleCeilingAuditConfig()


def config_dict() -> Dict[str, object]: return asdict(CFG)
