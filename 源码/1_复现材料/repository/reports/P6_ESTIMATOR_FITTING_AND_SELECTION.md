# P6 Recoverability Estimator Fitting and Selection

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent; figures follow scipilot-figure-skill
- Origin Mode: run + validate
- Origin Date: 2026-09-16
- Verification Status: ANALYZED (execution and leakage tests passed; no independent stochastic reproduction rerun)
- Version Label: p6_estimator_fitting_selection_v1
- Overall Verdict: **PASS**

## 1. Boundary and preregistration

Only the P4-frozen fitting centers 31200–31229 were generated and used. Five center-group folds, all window pairs, Ridge alphas, the single 6→16→8→1 MLP, the one-standard-error rule, deterministic tie-break and explicit CV pass gate were SHA-bound and Git-committed before outcomes. Calibration centers 32000–32019, heldout centers 33000–33019, Alibaba and prior-paper heldout outcomes were not accessed. The frozen P3.2 r3 generator/source assets were not modified. C4 is **Nonlinear Dependency-Shift Stress**, not architecture-level mismatch.

The dataset contains 8,640 stage events (30 centers × 3 seeds × 4 scenarios × 24 stages). Every center's seeds, scenarios and stages remain in one fold. The target is frozen H_R=4, eta=0.25, B50 continuous `R_B50`; future service is offline-label-only. Estimator inputs are exactly six same-identity causal history values from `[gain,residual]`: short/long means and their coverages. No effort proxy, scenario/center/type/tier/architecture metadata, oracle quantity or future service value enters the features.

The fixed MLP optimization uses the preregistered target multiplier 1,000 and divides predictions by 1,000; this is a fixed unit conversion, not a fitted target scaler. The fold-training-mean reference is an estimator-development diagnostic only; no lifecycle baseline comparison has been run.

## 2. Selection outcome

Selected configuration: **mlp_ks2_kl6** (`MLP`, K_S=2, K_L=6). Best observed configuration: `mlp_ks2_kl18`. Best macro-center MAE = 0.00114741; one-SE = 0.00008119; eligibility threshold = 0.00122860. The simpler Ridge family was preferred only if eligible under the predeclared threshold.

| Selected OOF metric | Value |
|---|---:|
| Macro-center MAE | 0.00116204 |
| Macro-center RMSE | 0.00208386 |
| Pooled Spearman | 0.4103 |
| Mean / median center Spearman | 0.2761 / 0.2738 |
| Sign accuracy | 0.7464 |
| Balanced accuracy (`R<0`) | 0.7117 |
| Relative macro-MAE improvement over fold-training-mean baseline | 29.04% |

## 3. Fold and center generalization

|   fold | validation_centers                  |    n |      mae |     rmse |   spearman |   sign_accuracy |   balanced_accuracy |   negative_prevalence |   macro_center_mae |   macro_center_rmse |   macro_center_spearman_mean |   centers_positive_spearman |
|-------:|:------------------------------------|-----:|---------:|---------:|-----------:|----------------:|--------------------:|----------------------:|-------------------:|--------------------:|-----------------------------:|----------------------------:|
|      0 | 31200,31201,31202,31203,31204,31205 | 1728 | 0.001087 | 0.002127 |   0.502541 |        0.707755 |            0.705568 |              0.334491 |           0.001087 |            0.002061 |                     0.321331 |                           6 |
|      1 | 31206,31207,31208,31209,31210,31211 | 1728 | 0.001013 | 0.002107 |   0.366198 |        0.822338 |            0.728609 |              0.270255 |           0.001013 |            0.001949 |                     0.246346 |                           5 |
|      2 | 31212,31213,31214,31215,31216,31217 | 1728 | 0.001525 | 0.002622 |   0.407452 |        0.711806 |            0.717927 |              0.269097 |           0.001525 |            0.002492 |                     0.309634 |                           6 |
|      3 | 31218,31219,31220,31221,31222,31223 | 1728 | 0.000909 | 0.001725 |   0.421039 |        0.787616 |            0.704837 |              0.293981 |           0.000909 |            0.001663 |                     0.336825 |                           6 |
|      4 | 31224,31225,31226,31227,31228,31229 | 1728 | 0.001276 | 0.002309 |   0.337094 |        0.702546 |            0.693464 |              0.295718 |           0.001276 |            0.002255 |                     0.166361 |                           5 |

Across 30 unseen validation centers, 28 have positive and 2 negative center-level Spearman. Leave-one-center-out pooled Spearman ranges 0.3960 to 0.4372; leave-one-fold-out ranges 0.3806 to 0.4306. The complete center table is `results/p6/metrics_by_center.csv`.

An additional descriptive removal of every pair of centers (435 combinations, no refitting) gives pooled Spearman 0.3808 to 0.4455. This supplements the requested one/two-center dominance inspection; it was not added to selection or scientific gate criteria after outcomes. Positive leave-out association does not prove absence of all center or scenario confounding.

## 4. Scenario and C3-dominance diagnostics

| scenario   |    n |      mae |     rmse |   spearman |   sign_accuracy |   balanced_accuracy |   negative_prevalence |   macro_center_mae |   macro_center_rmse |   macro_center_spearman_mean |   macro_center_spearman_median |
|:-----------|-----:|---------:|---------:|-----------:|----------------:|--------------------:|----------------------:|-------------------:|--------------------:|-----------------------------:|-------------------------------:|
| C0         | 2160 | 0.000733 | 0.001072 |   0.148061 |        0.804630 |            0.404186 |              0.004630 |           0.000733 |            0.000831 |                    -0.161976 |                      -0.141778 |
| C1         | 2160 | 0.000818 | 0.001252 |   0.202525 |        0.759259 |            0.655350 |              0.081944 |           0.000818 |            0.000970 |                    -0.065951 |                       0.029809 |
| C3         | 2160 | 0.002346 | 0.003916 |   0.542364 |        0.705556 |            0.738289 |              0.730556 |           0.002346 |            0.003749 |                     0.600386 |                       0.613721 |
| C4         | 2160 | 0.000752 | 0.001125 |   0.420431 |        0.716204 |            0.684744 |              0.353704 |           0.000752 |            0.000950 |                     0.227725 |                       0.328462 |

All-scenario pooled Spearman is 0.4103. Excluding C3 it is 0.2806, with balanced accuracy 0.6783. C3 alone has Spearman 0.5424 and C4 separately has Spearman 0.4204. C3 is intentionally severe, so pooled performance is not treated as sufficient: the predeclared non-C3 and leave-out checks determine whether scale separation dominates. C4 remains a heterogeneous secondary stress condition regardless of its estimator metrics.

**Caution:** C0/C1 pooled correlations are weak, and their mean within-center correlations are negative. The all-scenario center result therefore does not establish reliable within-scenario ranking for either maintainable reference. C0 has only 10 negative events out of 2,160, so its sign diagnostic is highly imbalanced. C3 errors have a long tail and predictions compress severe negative margins toward zero. These limitations remain in the record despite the operational CV PASS. Selection and reporting on the same grouped CV are development diagnostics, not an unbiased final heldout estimate.

## 5. Predicted-versus-oracle, errors, sign and continuous calibration

- `results/p6/figures/predicted_vs_oracle.png`: scenario-faceted OOF scatter with identity line; transparency exposes density rather than hiding it behind means.
- `results/p6/figures/residual_distribution.png`: scenario-specific OOF error densities.
- `results/p6/figures/sign_confusion_matrix.png`: count matrix for the diagnostic `R=0` sign split.
- `results/p6/figures/continuous_margin_calibration.png`: predicted-margin deciles versus oracle means; bars are center-cluster bootstrap 95% intervals (1,000 resamples, 30 centers).

These plots diagnose a continuous estimator. They do not calibrate `delta_R`, a lifecycle gate or a binary decision threshold.

Scatter axes are scenario-specific and explicitly tick-labeled to reveal local patterns; do not infer equal severity from equal visual distance across panels. All original events and long error tails are retained. Visual and grayscale review is recorded separately in `reports/P6_FIGURE_VISUAL_QA.md` and `results/p6/visual_qa.json`; vector export requires current approved PNG and prediction hashes.

## 6. Predeclared stop gate

| Check | Pass |
|---|---|
| `selected_pooled_spearman` | PASS |
| `selected_macro_center_spearman_median` | PASS |
| `selected_balanced_accuracy` | PASS |
| `positive_fold_spearman_count` | PASS |
| `relative_macro_mae_improvement` | PASS |
| `non_c3_pooled_spearman` | PASS |
| `non_c3_balanced_accuracy` | PASS |
| `leave_one_center_out_positive` | PASS |
| `leave_one_fold_out_positive` | PASS |

Failed checks: none. Scientific/leakage test suite: **PASS** (`...............                                                          [100%]
15 passed in 3.26s`).

## 7. Statistical interpretation and fallacy scan

All metrics are out-of-fold by unseen center. Correlated seeds/scenarios/stages are not represented as independent centers in the primary macro-center MAE, and center-level direction/leave-out analyses expose heterogeneity. Scenario metrics and binary sign statistics are secondary diagnostics; no multiplicity-adjusted confirmatory claims are made. The continuous calibration plot is descriptive. Coverage: **11/11 fallacy types checked** — aggregation reversal/Simpson risk is addressed with scenario and center tables; ecological inference is avoided; selected-sample/Berkson and collider risks are noted; sign base rates are reported; no extreme-center preselection or survivor deletion occurred; all candidates are reported to limit look-elsewhere and forking-path bias; no causal claim is made from prediction association; and temporal precedence plus offline-label isolation is audited without claiming that it removes all generator confounding.

## 8. Freeze and next boundary

Final all-fitting-center refit performed: **True**. Scaler and estimator were fit only on the 30 fitting centers and frozen with hashes. No calibration data were used. Do not begin P7, gate calibration, Proposed, baselines, robustness, Alibaba or heldout evaluation.

## 9. Execution changes and provenance

Procedural fixes and authorized checkpoint recovery are recorded in `docs/P6_EXECUTION_CHANGELOG.md`. Frozen generator, centers, response definition, candidate grid, selection rule and scientific stop criteria remain unchanged. Numerical P6 development stop checks were agent-operationalized and committed before fitting outcomes; they are not newly attributed to the original human protocol and are not lifecycle gate calibration. Figure PNGs require a separately recorded visual QA review before final vector export.

**PASS: Maintenance-response features provide useful out-of-center prediction of the continuous recoverability margin, and a frozen estimator is ready for calibration.**
