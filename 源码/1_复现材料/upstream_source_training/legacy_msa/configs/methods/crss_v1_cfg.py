# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class CRSSV1Config:
    protocol_version: str = "crss_v1_candidate_response_stable_suitability_1_0"
    L: int = 96
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    top_k: int = 3
    exposed_pools: Tuple[Tuple[int, int, int], ...] = (
        (1980, 40, 730000),
        (2020, 40, 760000),
        (2100, 40, 800000),
        (2140, 40, 810000),
    )
    protected_reference: str = "PT_A57_A57"
    ordinary_steps: int = 50
    ordinary_lr: float = 0.01
    ordinary_grad_clip: float = 1.0
    alpha_grid: Tuple[float, ...] = (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 230111
    epsilon: float = 1e-12
    output_root: str = "results/crss_v1"
    fwsa_manifest_path: str = "tmp/fwsa_v1_work/fwsa_manifest.json"
    fwsa_spans_path: str = "tmp/fwsa_v1_work/fwsa_raw_spans.csv"
    fwsa_candidates_path: str = "tmp/fwsa_v1_work/fwsa_candidate_metrics.csv"
    fwsa_report_path: str = "results/fwsa_v1/FWSA_V1_SUMMARY.md"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"
    bank_manifest_sha256: str = "3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283"


CFG = CRSSV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
