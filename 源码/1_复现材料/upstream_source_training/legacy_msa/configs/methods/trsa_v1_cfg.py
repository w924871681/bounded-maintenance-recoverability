# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class TRSAV1Config:
    protocol_version: str = "trsa_v1_target_regime_stable_suitability_1_0"
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
    alpha_grid: Tuple[float, ...] = (0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0)
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 230111
    epsilon: float = 1e-12
    formula_epsilon: float = 1e-8
    output_root: str = "results/trsa_v1"
    crss_manifest_path: str = "results/crss_v1/crss_manifest.json"
    crss_schema_path: str = "results/crss_v1/crss_feature_schema.json"
    crss_candidates_path: str = "results/crss_v1/crss_candidate_row_predictions.csv"
    crss_cases_path: str = "results/crss_v1/crss_outer_case_predictions.csv"
    crss_inner_path: str = "results/crss_v1/crss_inner_cv_manifest.json"
    fwsa_manifest_path: str = "tmp/fwsa_v1_work/fwsa_manifest.json"
    fwsa_spans_path: str = "tmp/fwsa_v1_work/fwsa_raw_spans.csv"
    fwsa_candidates_path: str = "tmp/fwsa_v1_work/fwsa_candidate_metrics.csv"
    bank_manifest_path: str = "results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json"


CFG = TRSAV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
