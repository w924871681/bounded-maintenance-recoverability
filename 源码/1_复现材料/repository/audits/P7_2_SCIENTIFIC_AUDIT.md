# P7.2 Scientific Audit

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Verification Status: ANALYZED
- Final verdict: **FAIL**

All 20 required scientific/leakage/fairness checks passed at runtime and the prospective pytest suite returned code `0`. Check map:

```json
{
  "test_p7_2_amendment_committed_before_outcomes": true,
  "test_p7_2_fresh_centers_unused": true,
  "test_p7_2_gatecal_actioncal_disjoint": true,
  "test_p7_2_no_final_heldout_access": true,
  "test_p7_2_no_alibaba_access": true,
  "test_p7_2_p6_estimator_hash_unchanged": true,
  "test_p7_2_scaler_hash_unchanged": true,
  "test_p7_2_feature_spec_unchanged": true,
  "test_p7_2_window_pair_unchanged": true,
  "test_p7_2_delta_grid_identical_to_p7": true,
  "test_p7_2_gate_selection_uses_only_gatecal": true,
  "test_p7_2_actioncal_never_changes_delta": true,
  "test_p7_2_scenario_not_used_as_gate_feature": true,
  "test_p7_2_no_future_service_in_online_decision": true,
  "test_p7_2_assessment_not_used_for_gradients": true,
  "test_p7_2_same_bank_budget_across_methods": true,
  "test_p7_2_history_reset_on_identity_change": true,
  "test_p7_2_baseline_grids_not_expanded": true,
  "test_p7_2_b8_always_open_exact": true,
  "test_p7_2_all_selected_params_frozen_before_heldout": true
}
```

GateCal-v2 and ActionCal-v2 are disjoint center clusters. The gate grid is byte-derived from the original seven P7 values; the P6 estimator/scaler, six-feature `[gain,residual]` definition, K_S=2/K_L=6, generator and bank hashes are unchanged. Scenario is not an estimator feature. D_assess causes no gradient update, service begins after the decision timestamp, and future service is offline-label-only. Every method has the same bank/filter/update budget; B8 gate-open is exactly one; RI resets the response history.

11/11 fallacy scan: subgroup tables address Simpson risk without replacing the primary pooled center statistic; no individual inference is made from center aggregates; selected synthetic pools may not represent natural prevalence (Berkson/selection caution); no collider adjustment is introduced; oracle class prevalence accompanies TPR/TNR (base-rate check); no regression-to-mean improvement claim is made; all frozen centers and keys are retained (no survivorship filtering); every threshold and baseline grid result is exported (look-elsewhere); pre-outcome grids/ties/stops constrain forking paths; calibration associations are not causal superiority claims; temporal ordering does not prove causal direction. ActionCal is a disjoint validation pool for admission semantics, not final heldout evidence.

No `33000–33019`, Alibaba or P8 access occurred. Existing P7 PASS and P7.1 effectively-Always-Open verdict remain preserved. C4 remains secondary Nonlinear Dependency-Shift Stress only.
