# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class FWSAV1Config:
    protocol_version: str = "fwsa_v1_future_winner_stability_audit_1_0"
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    audit_blocks: int = 6
    audit_windows: int = 40
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
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 210091
    epsilon: float = 1e-12
    output_root: str = "results/fwsa_v1"
    work_root: str = "tmp/fwsa_v1_work"
    mpv_manifest_path: str = "results/mpv_aux_v1/mpv_aux_manifest.json"
    mpv_spans_path: str = "results/mpv_aux_v1/mpv_aux_raw_spans.csv"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = FWSAV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
