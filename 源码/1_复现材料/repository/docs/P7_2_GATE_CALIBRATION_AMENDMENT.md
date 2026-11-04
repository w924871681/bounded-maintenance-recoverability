# P7.2 Prospective Gate-Calibration Semantics Amendment

## Material Passport

- Origin: human scientific review after P7 and the read-only P7.1 forensic audit
- Date: 2026-09-20 (Asia/Shanghai)
- Status: prospective, binding calibration-semantics amendment
- Scope: C3 Recoverability-Gated Lifecycle Escalation only
- Integrity: the SHA-256 of this complete file is recorded externally in `docs/P7_2_GATE_CALIBRATION_AMENDMENT.sha256`; the file cannot contain its own complete digest without self-reference.

## 1. Preserved scientific history

The original P7 protocol, pre-outcome freeze, calibration artifacts, report and formal **PASS** remain immutable historical records. P7 selected `delta_R=+0.0010887248681683`, the `+2s` endpoint and largest positive member of the pre-frozen seven-candidate grid. Nothing in P7.2 deletes, overwrites, relabels or retrospectively reevaluates that decision under a criterion that did not govern P7.

The read-only P7.1 audit is also preserved. Its verdict is **`GATE_IS_EFFECTIVELY_ALWAYS_OPEN_ON_CALIBRATION`**. At the P7 selection, the model-level search/gate-open rate was `96.4236%`, final-action agreement with frozen B8 Always-Open was `98.6979%`, and deterministic search-work reduction was only `3.715%`. The old selection was therefore a boundary optimum with a near-Always-Open action path on the original calibration pool. P7.1 did not refit the estimator, alter any parameter or access held-out data.

P3.2b remains a formal FAIL. C3 remains the primary controlled model-identity mismatch condition. C4 remains only the secondary **Nonlinear Dependency-Shift Stress** / heterogeneous dependency-shift stress condition and cannot support an architecture-family replacement or architecture-failure claim.

## 2. Scientific correction and semantic separation

The recoverability gate decides whether model-level alternatives are **admitted** to the feasible online action space. Gate calibration must therefore evaluate admission correctness directly against the frozen finite-local-policy oracle target `R_B50 < 0`.

The original P7 quantity named false escalation used actual downstream RI among `R_B50 >= 0` stages. That quantity measures the result of both gate admission and the downstream assessment-based action selector. It does not penalize opening the model-level action space when RI is later rejected. P7.2 corrects this calibration semantics prospectively:

- **True admission:** `R_B50 < 0` and the gate opens.
- **Missed admission:** `R_B50 < 0` and the gate stays closed.
- **Correct closure:** `R_B50 >= 0` and the gate stays closed.
- **False admission:** `R_B50 >= 0` and the gate opens.
- **Unnecessary/harmful RI:** a downstream RI outcome after gate opening; this remains an action-layer diagnostic and is not a gate-threshold selection target.

P7.2a calibrates `delta_R` **only for admission quality**. No lifecycle objective, downstream RI choice, scenario label, search-cost penalty or model-bank action result may influence threshold selection. P7.2b, if unlocked, evaluates the separate downstream controller layer with the P7.2a threshold held immutable.

The old P7 and P7.1 results are not deleted and are not reinterpreted as PASS under the new criterion. P7.2 is a fresh prospective calibration on disjoint unused centers.

## 3. Unchanged representation, estimator and experiment scope

P7.2 cannot modify:

- the C1 recoverability formulation;
- the P6 estimator, scaler, MLP architecture or weights;
- the response event `xi_t=[gain_t,residual_t]^T`;
- `K_S=2`, `K_L=6`, or the six-feature order;
- the generator, scenario definitions, source/model bank or deployment filters;
- `H_R=4`, `eta=0.25`, or `B50={P0,P10,P20,P50}`;
- the adaptation operator, per-candidate 50-update budget, assessment no-gradient rule or action tie-break;
- the original seven-point threshold grid `{-2s,-s,-0.5s,0,+0.5s,+s,+2s}`;
- the original baseline grids or cost-ratio grid `{2,5,10}`.

No generator, estimator, feature, window, local-policy, service-threshold or source-bank tuning is permitted. Final held-out centers `33000–33019`, Alibaba/external outcomes and P8 remain inaccessible throughout P7.2.

## 4. Fresh pools and nonreplacement rule

Twenty-four completely unused synthetic center IDs will be selected before any P7.2 trajectory outcome is written. Their identities, deterministic metadata-only stratification, GateCal-v2/ActionCal-v2 assignment and nonoverlap audit will be recorded in `configs/p7_2_fresh_center_pools.json` and SHA-256 bound before execution.

The pools contain 12 GateCal-v2 centers and 12 distinct ActionCal-v2 centers. Assignment may use only generator-known center type and deployment tier, never losses, labels, predictions, scenario outcomes or trajectory summaries. Once bound, no center may be replaced because of failure, class prevalence, runtime, metric value or scientific result. A procedural retry may only resume the same center/seed/scenario key from a validated complete receipt.

## 5. P7.2a threshold-independent GateCal trajectory

GateCal-v2 uses the same causal trajectory semantics on which the P6 estimator was developed. For each fresh center, model seed and frozen scenario, the deployed incumbent starts from the frozen native identity and, at every stage, is advanced by the copied 50-update local probe `P50` trained only on `D_upd`. The probe is evaluated on same-stage `D_assess`; `[gain,residual]` is appended to the same-identity causal history; the frozen P6 estimator produces continuous `R_hat_t`; then the current local-policy H=4 oracle label `R_B50` is computed offline. The P50 probe becomes the next-stage parent, exactly as in the P6 fitting trajectory construction.

This path is independent of every candidate `delta_R`: it loads no RI alternatives, performs no model-bank search, and runs no downstream retain/local/RI action selector. Thus all seven candidates are evaluated on exactly the same prediction/label records and threshold choice cannot change its own future state path. Future service is restricted to offline oracle labeling after causal decision-time features are fixed; it never enters the estimator input or online gate calculation.

The gate rule is `open iff R_hat_t < delta_R`. The only target is `R_B50 < 0`. Scenario identity is a reporting stratum, never a gate feature or truth label.

## 6. Frozen primary gate-selection rule

For each center and threshold candidate:

- `TPR = P(gate open | R_B50 < 0)` when the negative denominator is nonzero;
- `TNR = P(gate closed | R_B50 >= 0)` when the nonnegative denominator is nonzero.

Undefined center-components remain null. `macro_TPR` and `macro_TNR` are means over centers where their respective components are defined. The primary score is

`macro_balanced_admission_accuracy = 0.5 * (macro_TPR + macro_TNR)`.

Select the candidate with the highest score. Exact-score ties are broken by: (1) lower overall gate-open rate; (2) smaller absolute `delta_R`; (3) lower numeric `delta_R`. Lifecycle loss and action outcomes are prohibited selection inputs. No search penalty lambda is introduced.

Literal Always-Open and Always-Closed are admission-only comparators. When both oracle classes are represented, each has balanced admission accuracy 0.5; all class counts and undefined components remain explicit.

## 7. Pre-outcome P7.2a stop rules

P7.2a passes only if all integrity checks pass and all the following prospective scientific conditions hold:

1. The selected overall macro-center balanced admission accuracy is **strictly greater than 0.55**. A value `<=0.55` is treated as near-random / not meaningfully better than the literal admission baselines.
2. The same selected threshold, without subgroup reselection, has non-C3 macro-center balanced admission accuracy **strictly greater than 0.55**. Otherwise performance is judged C3-driven and collapsed outside C3.
3. If the selected threshold opens at least `90%` of all GateCal-v2 stages, there must not exist another frozen candidate whose gate-open rate is at least `10` percentage points lower and whose overall macro balanced admission accuracy is within `0.01` of the selected score. If such a candidate exists, the near-Always-Open selection has no material admission advantage and P7.2 stops.
4. The P6 estimator/scaler hashes, feature specification, window pair, seven-point grid, causal ordering, no-future-service boundary and pool isolation must all pass.

C3, C4, non-C3 and per-scenario metrics are mandatory diagnostics but do not introduce post-outcome alternative thresholds. A P7.2a FAIL freezes the failure evidence, leaves ActionCal-v2 untouched, and returns for human scientific review.

## 8. P7.2b boundary if P7.2a passes

Only a P7.2a PASS authorizes ActionCal-v2. The newly selected `delta_R` is frozen immediately and cannot change in P7.2b. On the disjoint 12-center ActionCal-v2 pool, the actual controller follows gate → admissible actions → assessment-based selector → retain/local/RI.

The downstream cost ratio is selected from the already-predeclared `{2,5,10}` grid by macro-center lifecycle objective, with service and intervention components reported separately. Exact ties use lower RI rate, then lower search rate, then lower numeric ratio. All tunable baselines B3–B7 are recalibrated only on ActionCal-v2 using their original P7 grids; B0/B1/B2/B8 remain fixed definitions. No baseline grid may be enlarged. B8 Always-Open remains the mandatory paired mechanism comparator.

P7.2b calibration is descriptive and cannot support a superiority claim. Its purpose is to determine whether the prospectively corrected gate remains nondegenerate and scientifically distinct from Always-Open before any later, separately authorized final held-out evaluation.

The final P7.2 PASS is not granted merely because the GateCal-v2 selection criterion passed. Without changing or reselecting `delta_R`, the frozen gate must also satisfy all of the following on the disjoint ActionCal-v2 records: (1) overall macro-center balanced admission accuracy strictly greater than `0.55`; (2) non-C3 macro-center balanced admission accuracy strictly greater than `0.55`; and (3) overall gate-open rate strictly below `90%`, equivalent to more than 10 percentage points of model-level search reduction relative to literal Always-Open. These are validation conditions, not tuning objectives. Lifecycle MSE, lifecycle objective, RI rate and action agreement are reported but cannot rescue or overturn an admission-gate failure. All scientific, leakage, fairness and hash audits must also pass.

## 9. Verdict and claim boundary

P7.2 ends with exactly one formal verdict:

- **PASS:** the GateCal-selected threshold satisfies the predeclared admission criteria again on disjoint ActionCal-v2, opens fewer than 90% of stages there, and downstream lifecycle/baseline parameters are frozen for possible later final held-out evaluation; or
- **FAIL:** the frozen recoverability estimator does not support a scientifically useful model-level admission gate under the frozen representation.

A FAIL cannot authorize representation, estimator, generator or threshold-grid redesign. A PASS does not authorize P8 by itself. After P7.2 the workflow stops for human scientific review, with no access to `33000–33019` or Alibaba.
