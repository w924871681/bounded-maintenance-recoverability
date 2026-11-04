# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class NewFormalMainConfig:
    """Prospectively frozen held-out main-only protocol after tau repair."""

    protocol_version: str = "new_formal_main_tau035_k80_60_200_v1_0"
    calibration_protocol_version: str = "limited_validation_calibration_repair_v1_0"
    parent_protocol_version: str = "limited_validation_formal_k80_60_200_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    check_windows: int = 60
    test_windows: int = 200
    calibrated_tau: float = 0.35
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 3622

    main_pool: Tuple[int, int, int] = (1640, 20, 620000)
    output_root: str = "results/new_formal_main_evaluation"
    calibration_repair_root: str = "results/limited_validation_calibration_repair"
    bank_manifest_path: str = (
        "results/limited_validation_formal_protocol/candidate_bank/"
        "candidate_bank_manifest.json"
    )
    bank_manifest_sha256: str = (
        "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"
    )
    screening_summary_path: str = (
        "results/limited_validation_formal_protocol/screening/screening_summary.json"
    )


CFG = NewFormalMainConfig()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
