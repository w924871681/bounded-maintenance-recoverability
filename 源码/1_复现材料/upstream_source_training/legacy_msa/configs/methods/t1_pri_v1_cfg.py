# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class T1PRIV1Config:
    protocol_version: str = "t1_pri_v1_protected_reference_integration_1_0"
    pools: Tuple[str, ...] = (
        "oracle_1980_2019",
        "saa_2020_2059",
        "trajectory_2100_2139",
        "divergence_2140_2179",
    )
    lambda_grid: Tuple[float, ...] = (
        0.000, 0.025, 0.050, 0.075, 0.100,
        0.125, 0.150, 0.175, 0.200, 0.225,
        0.250, 0.300, 0.350, 0.400, 0.500,
    )
    harmful_limit: float = 0.05
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 210105
    epsilon: float = 1e-12
    output_root: str = "results/t1_pri_v1"
    crss_manifest_path: str = "results/crss_v1/crss_manifest.json"
    crss_schema_path: str = "results/crss_v1/crss_feature_schema.json"
    crss_candidates_path: str = "results/crss_v1/crss_candidate_row_predictions.csv"
    crss_cases_path: str = "results/crss_v1/crss_outer_case_predictions.csv"
    crss_inner_path: str = "results/crss_v1/crss_inner_cv_manifest.json"
    trsa_r_manifest_path: str = "results/trsa_r_v1/trsa_r_manifest.json"
    trsa_r_candidates_path: str = "results/trsa_r_v1/trsa_r_candidate_predictions.csv"
    fwsa_manifest_path: str = "tmp/fwsa_v1_work/fwsa_manifest.json"
    fwsa_candidates_path: str = "tmp/fwsa_v1_work/fwsa_candidate_metrics.csv"
    fwsa_cases_path: str = "tmp/fwsa_v1_work/fwsa_case_metrics.csv"
    fwsa_analysis_path: str = "tmp/fwsa_v1_work/fwsa_analysis.json"


CFG = T1PRIV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
