# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class LRSSV1Config:
    protocol_version: str = "lrss_v1_learned_raw_stable_suitability_probe_1_0"
    pools: Tuple[Tuple[str, int, int, int], ...] = (
        ("oracle_1980_2019", 1980, 40, 730000),
        ("saa_2020_2059", 2020, 40, 760000),
        ("trajectory_2100_2139", 2100, 40, 800000),
        ("divergence_2140_2179", 2140, 40, 810000),
    )
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    validation_windows: int = 80
    top_k: int = 3
    conv_channels: int = 8
    kernel_size: int = 5
    latent_dim: int = 8
    epochs: Tuple[int, ...] = (25, 50, 100, 200)
    seeds: Tuple[int, ...] = (2904, 2905, 2906)
    optimizer: str = "AdamW"
    learning_rate: float = 1e-3
    weight_decay: float = 1e-3
    gradient_clip: float = 1.0
    center_batch_size: int = 16
    normalization_epsilon: float = 1e-6
    low_std_threshold: float = 1e-8
    bootstrap_repeats: int = 4000
    # Chosen so pooled/pool L0 resampling exactly reuses verified TRSA-R T1 seeds.
    bootstrap_seed: int = 230112
    epsilon: float = 1e-12
    output_root: str = "results/lrss_v1"
    trsa_r_manifest_path: str = "results/trsa_r_v1/trsa_r_manifest.json"
    trsa_r_candidates_path: str = "results/trsa_r_v1/trsa_r_candidate_predictions.csv"
    trsa_r_pool_summary_path: str = "results/trsa_r_v1/trsa_r_pool_summary.csv"
    crss_schema_path: str = "results/crss_v1/crss_feature_schema.json"
    crss_manifest_path: str = "results/crss_v1/crss_manifest.json"
    fwsa_manifest_path: str = "tmp/fwsa_v1_work/fwsa_manifest.json"
    fwsa_spans_path: str = "tmp/fwsa_v1_work/fwsa_raw_spans.csv"
    fwsa_candidates_path: str = "tmp/fwsa_v1_work/fwsa_candidate_metrics.csv"


CFG = LRSSV1Config()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
