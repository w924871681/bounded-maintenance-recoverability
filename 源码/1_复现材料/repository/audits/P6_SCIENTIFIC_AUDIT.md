# P6 Scientific and Leakage Audit

## Material Passport

- Origin: P6 frozen fitting-pool execution
- Date: 2026-09-16
- Verification Status: ANALYZED; required execution/leakage tests validated, no independent stochastic reproduction rerun
- Overall: **PASS**

## Required checks

| Check | Result |
|---|---|
| `test_p6_fit_pool_matches_p4_freeze` | PASS |
| `test_p6_no_calibration_or_heldout_access` | PASS |
| `test_p6_group_split_by_center` | PASS |
| `test_p6_no_center_overlap_between_folds` | PASS |
| `test_p6_fold_local_scaler` | PASS |
| `test_p6_feature_exactly_six_dimensions` | PASS |
| `test_p6_no_scenario_or_center_metadata_feature` | PASS |
| `test_p6_no_future_service_input` | PASS |
| `test_p6_current_probe_is_causal` | PASS |
| `test_p6_history_reset_on_identity_change` | PASS |
| `test_p6_window_never_crosses_identity_boundary` | PASS |
| `test_p6_window_never_uses_future_response` | PASS |
| `test_p6_oracle_target_offline_only` | PASS |
| `test_p6_cv_predictions_complete` | PASS |
| `test_p6_model_selection_rule_predeclared` | PASS |

Pytest command: `python -m pytest -q tests/test_p6.py`

```text
...............                                                          [100%]
15 passed in 3.26s
```

No calibration, heldout, Alibaba, Proposed, baseline or P7 access occurred. The C4 architecture-level claim remains prohibited.
