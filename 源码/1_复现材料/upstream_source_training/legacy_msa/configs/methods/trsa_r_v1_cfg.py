# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class TRSARV1Config:
    protocol_version: str = "trsa_r_v1_minimal_numerical_sanity_repair_1_0"
    alpha_grid: Tuple[float, ...] = (0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0)
    bootstrap_repeats: int = 4000
    bootstrap_seed: int = 230111
    epsilon: float = 1e-12
    output_root: str = "results/trsa_r_v1"
    trsa_manifest_path: str = "results/trsa_v1/trsa_manifest.json"
    trsa_schema_path: str = "results/trsa_v1/trsa_regime_feature_schema.json"
    trsa_candidates_path: str = "results/trsa_v1/trsa_candidate_predictions.csv"
    trsa_inner_path: str = "results/trsa_v1/trsa_inner_cv_manifest.json"
    trsa_summary_path: str = "results/trsa_v1/TRSA_V1_SUMMARY.md"
    trsa_pool_summary_path: str = "results/trsa_v1/trsa_pool_summary.csv"
    fwsa_candidates_path: str = "tmp/fwsa_v1_work/fwsa_candidate_metrics.csv"


CFG = TRSARV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
