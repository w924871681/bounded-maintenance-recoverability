# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class BestFixedFTFormalBaselineV1Config:
    protocol_version: str = "best_fixed_ft_formal_baseline_v1_0"
    canonical_main_protocol: str = "new_formal_main_tau035_k80_60_200_v1_0"
    candidate_bank_architectures: Tuple[int, ...] = (1, 6, 46, 55, 56, 57, 62)
    protected_reference_token: str = "PT_A57_A57"
    development_pool: Tuple[int, int, int] = (1600, 20, 600000)
    confirmation_pool: Tuple[int, int, int] = (1620, 20, 610000)
    main_pool: Tuple[int, int, int] = (1640, 20, 620000)
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    adaptation_steps: int = 50
    adaptation_optimizer: str = "SGD"
    adaptation_lr: float = 0.01
    adaptation_momentum: float = 0.0
    adaptation_weight_decay: float = 0.0
    adaptation_gradient_clip: float = 1.0
    adaptation_loss: str = "full-support mean MSE"
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 3622
    tie_tolerance: float = 1e-12
    output_root: str = "results/best_fixed_ft_formal_baseline_v1"
    calibration_repair_root: str = "results/limited_validation_calibration_repair"
    canonical_main_root: str = "results/new_formal_main_evaluation"
    bank_manifest_path: str = (
        "results/limited_validation_formal_protocol/candidate_bank/"
        "candidate_bank_manifest.json"
    )
    bank_manifest_sha256: str = (
        "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"
    )


CFG = BestFixedFTFormalBaselineV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
