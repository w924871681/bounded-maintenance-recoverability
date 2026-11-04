# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class FinalE2EC23ExternalCfg:
    """Frozen external-baseline migration for the audited C2.3 Pool-K protocol.

    Hyperparameters are inherited from the pre-existing final_e2e baseline branch.
    They are not tuned on Pool K.
    """

    protocol_version: str = "final_e2e_c23_external_baselines_migrated_v1_0"
    data_seed: int = 2904
    train_seed: int = 2904
    source_centers: int = 20

    final_pool_k: Tuple[int, int, int] = (720, 50, 150000)
    H_list: Tuple[int, ...] = (1, 4)
    K_list: Tuple[int, ...] = (10, 20)
    architecture_count: int = 66
    candidate_budget: int = 12

    methods: Tuple[str, ...] = (
        "pt_ft",
        "medet_style",
        "meta_nas_lite",
        "zero_nas",
        "zero_nas_ft",
    )
    primary_methods: Tuple[str, ...] = (
        "pt_ft",
        "medet_style",
        "meta_nas_lite",
        "zero_nas_ft",
    )

    output_root: str = "outputs/final_e2e_c23_external_d2904_t2904"
    ours_result_path: str = "outputs/final_e2e_c23_d2904_t2904/final/methods/ours_c23.json"
    final_audit_path: str = "outputs/final_e2e_c23_d2904_t2904/final/audit/final_e2e_c23_audit.json"
    expected_final_audit_decision: str = "PASS_FINAL_E2E_C23_COMPLETE_AND_AUDITED"

    c1_bank_path: str = "outputs/formal_c1_seed2904/shared_artifacts/ours_weight_bank_source_pooled_c1_v1_src20.pt"
    c1_bank_sha256: str = "bb3a655606af3b554a8f088bb1d2f3f8d9f190b0911a812fd3755d3de3216b9d"
    source_pi50_path: str = "outputs/c1r_rebase_d2904_t2904/stage2/source_teacher_pi50.json"

    # Fixed-backbone source training (pre-existing protocol).
    pt_epochs: int = 50
    pt_lr: float = 1e-3
    pt_batch_size: int = 64

    medet_meta_iters: int = 400
    medet_meta_batch: int = 8
    medet_inner_steps: int = 5
    medet_inner_lr: float = 1e-2
    medet_outer_lr: float = 1e-3
    medet_grad_clip: float = 1.0

    # Target adaptation for fixed-backbone methods.
    fixed_target_steps: int = 50
    fixed_target_lr: float = 1e-2
    fixed_target_optimizer: str = "sgd"
    fixed_target_loss: str = "mse"
    fixed_target_grad_clip: float = 1.0

    # Search baselines: same hard-feasible 66-space and Top-12/50-step budget.
    meta_prior_weight: float = 0.60
    meta_proxy_weight: float = 0.40
    proxy_batch_size: int = 16
    proxy_support_points: int = 6
    search_target_steps: int = 50
    search_target_lr: float = 3e-4
    search_target_huber_delta: float = 0.2
    search_target_grad_clip: float = 5.0

    bootstrap_repeats: int = 4000
    eps: float = 1e-12


CFG = FinalE2EC23ExternalCfg()


def config_dict() -> Dict[str, object]:
    return asdict(CFG)
