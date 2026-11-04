# P7.7A-2 Recoverability-to-Escalation Integration Audit

Status: development-only integration audit; final-heldout execution remains prohibited.

## Scope and access boundary

This audit uses only existing repository code, reports, configurations, manifests, frozen artifacts, and development qualification records. It does not read, materialize, preprocess, summarize, or execute final-heldout centers 33000–33019. Alibaba and P8 remain untouched. Historical verdicts are preserved exactly: P7.2 formal FAIL, P7.4B FAIL, P7.4B.1 `F2_UNCERTAINTY_BOUNDARY_SENSITIVITY`, P7.6B `P7_6B_REPLICATION_PASS`, P7.7A `P7_7A_PROTOCOL_NOT_READY`, and P7.7A-1 `P7_7A1_DESIGN_FREEZE_PASS`.

## Scientific role reconstruction

| Component | Estimated quantity / role | Causal and online? | Calibration-only? | Behavior-generating? | Observational? | Prospectively replicated? | Final action role after this audit | Superseded role? |
|---|---|---|---|---|---|---|---|---|
| P6 FrozenEstimator | Absolute recoverability estimate from same-identity response history | Yes | No | Yes in P7.2/P7.7A-1 | No | P7.2 lineage only | Historical gate lineage; not the A-2 RI-admission evidence | Not performance-superseded; replaced only for the integrated P7.7 policy boundary |
| P7.2 gate | Thresholded P6 prediction with frozen `delta_R=-0.000272181217042075` | Yes | Gate calibration used GateCal; ActionCal validated action admission | Yes | No | Calibrated/validated on P7.2 pools | Preserved historical artifact and failure scope; not reused as the A1 threshold | No |
| P7.2 `delta_R` | Frozen action-gate margin | Online threshold parameter | Selected before ActionCal outcomes | Yes in P7.2 | No | Yes as a frozen P7.2 parameter | Historical lineage only; never an A1 threshold | No |
| P7.2 cost ratio 10 | RI action-cost term | Online decision cost | Frozen action parameter | Yes | No | Yes | Unchanged candidate comparison cost | No |
| P7.6B A0 | Absolute representation target `R_B50` | Representation comparator | Fit/Validation scientific representation | No | No | Yes | Comparator only | No |
| P7.6B A1 estimator | `R_B50/S_m` prediction from same-identity gain/residual history | Yes, when fed causal history | Refit once under frozen Fit protocol | No in P7.6B | Initially observational | Yes (`P7_6B_REPLICATION_PASS`) | Frozen online evidence for RI admission | No |
| P7.6B A1 scaler | Fold/final feature scaler for A1 features | Applied online to frozen features | Fit-only artifact | No | Initially observational | Yes | Immutable A1 preprocessing | No |
| Formal recoverability zero boundary | `R>=0` recoverable, `R<0` unrecoverable | Decision semantics | No | Boundary only | No | Explicit in P7.6B protocol | Exact A1 admission boundary; no margin | No |
| RI candidate search | Frozen eleven-identity bank, feasibility filters, 50 updates, `D_assess` evaluation | Yes | No | Yes | No | Development-qualified | Unchanged | No |
| RI acceptance/fallback | Retain/local/RI comparison, exact tie order; no forced RI | Yes | No | Yes | No | Development-qualified | Unchanged | No |

P7.6B establishes reproducible A1 representation and zero-boundary classification evidence under its evaluated synthetic protocol. It does not establish final P7.7 lifecycle superiority and did not run the final lifecycle experiment.

## Branch A coherence test

Retaining P7.2/P6 as the action gate while keeping A1 diagnostic-only is internally executable, but C2 evidence would not affect the C3 decisions. C2 and C3 could only be stated as separate contributions: C2 is an auxiliary recoverability-representation result and C3 is a P7.2/P6 gate-based lifecycle policy. The paper would have to avoid claiming that A1 drives RI admission, and the phrase “recoverability-guided lifecycle escalation” would be inaccurate. This branch is scientifically conservative but leaves the stated C2→C3 contribution chain open.

## Branch B coherence test

Branch B is eligible without refit, retuning, a new margin, outcome-dependent redesign, or a changed candidate policy. The existing P7.6B A1 target is exactly `R_B50/S_m`; `S_m` is the identity-held median of exactly 104 finite point errors from a permitted 200-observation causal deployment reference, with a `1e-12` floor. Multiplication by the positive `S_m` preserves the sign, so zero has the same formal meaning: nonnegative is recoverable and negative is unrecoverable. The P7.6B protocol defines zero as the boundary and its audited metrics use negative recoverability as the admission class.

At stage `t`, A1 receives only the current same-identity response history plus the current probe event. `D_srv(t)` is read only after the decision is sealed. On RI, the selected identity is committed, the old response history is discarded, and `S_m` is reconstructed from the last 200 raw `D_assess` observations before the next decision; the new scale is then held fixed for that identity lifetime. No future RI outcome, maintenance outcome, service tensor, or post-decision observation is an A1 input.

The integrated rule is therefore:

1. Build the frozen A1 input from causal same-identity history.
2. Compute the immutable A1 prediction.
3. Use the exact zero boundary only.
4. If A1 is nonnegative, keep RI search closed and compare retain/local.
5. If A1 is negative, open the unchanged candidate search, feasibility filters, adaptation, and retain/local/RI comparison.
6. Commit RI only if it wins the frozen comparison; otherwise apply retain/local fallback.
7. After RI, reset identity, response history, and `S_m` prospectively.

A1 < 0 is admissibility evidence, never a forced RI action. The P7.2 `delta_R` is not reused as an A1 threshold.

## Historical P7.2 FAIL scope

The P7.2 formal FAIL is specifically the ActionCal-v2 admission-gate criterion: overall and non-C3 macro balanced admission accuracy were not strictly above 0.55. GateCal-v2 itself selected and froze the delta, and P7.2 did not fail because of an estimator hash, temporal leakage, service-outcome corruption, or a changed lifecycle cost. The P7.2 FAIL therefore remains a preserved historical failure of the absolute P6/P7.2 action-admission calibration under that preregistered criterion. It is not erased or relabeled. Using the P7.2 gate unchanged as the sole final operational gate would not support the intended integrated C2→C3 claim; the integrated policy instead uses the separately replicated A1 zero-boundary evidence.

## Claim-to-algorithm closure

| Formal concept | Online observable | Estimator | Threshold | Action implication | Algorithm location | Final metric |
|---|---|---|---|---|---|---|
| Bounded recoverability | Same-identity probe gain/residual history and identity-held `S_m` | Frozen P7.6B A1 | Exact zero | Negative evidence opens RI search; nonnegative keeps it closed | `FrozenA1Observer` plus `DecisionExecutor` Proposed branch | Mean lifecycle service loss and secondary action/RI metrics |
| Maintenance-unrecoverability | Same causal A1 output `<0` | Same frozen A1 | `0.0` only | RI candidates become admissible, not mandatory | Integrated Proposed gate | Center-level paired lifecycle outcomes |
| Candidate decision | Frozen bank, unchanged feasibility/adaptation and `D_assess` losses | No new estimator | Existing comparison | Retain/local/RI minimum with frozen ties | `DecisionExecutor` | Lifecycle service loss, RI/action cost |

The closure is complete only after the development-only Branch B qualification below passes. No final-heldout conclusion is made here.

## Consistency audit

The design resolution, protocol Markdown, machine-readable protocol, P7.6B frozen protocol, implementation, and historical audits were cross-checked for the following 20 items: P7.2 lineage; delta value; cost ratio; A1 target; `S_m` definition; zero boundary; same-identity history; `D_srv` ordering; RI reset; candidate bank; 50-update adaptation; feasibility; comparison; tie order; fallback; comparator set; center metadata; seeds/scenarios; bootstrap plan; and final-heldout guard. No disagreement was found in the frozen inputs or historical verdicts. The only intentional change is the prospective Branch B role switch: A1 becomes the online RI-admission evidence source, P7.2 `delta_R` becomes historical lineage, and the primary endpoint terminology is corrected to “mean lifecycle service loss” while the computation is unchanged.

## Branch selection and freeze condition

Branch B is selected from provenance, formal quantity compatibility, causal availability, and absence of post-hoc freedom—not from development performance. The final method identifier is `P7.7 Recoverability-Guided Lifecycle`. P7.2 remains historical behavior/calibration lineage; P7.6B A1 remains the frozen recoverability inference component; P7.7 is the integrated lifecycle policy. Final-heldout metadata remain 20 centers, three seeds, four scenarios, five methods, and 1200 expected trajectories. Final-heldout execution remains separately unauthorized.

The development-only Branch B qualification verified closed/open/non-committed/committed RI branches (67/27/2 rows), causal ordering, exact zero semantics, identity/A1 reset, deterministic replay, receipt/resume identity, and no-future leakage on authorized development IDs. The comparator and statistical plan remain unchanged, and no final-heldout, Alibaba or P8 access occurred.

## Final audit verdict

`P7_7A2_INTEGRATION_FREEZE_PASS` — Branch B is frozen prospectively as P7.7 Recoverability-Guided Lifecycle. This is an integration/design and development-qualification verdict only; it is not a final-heldout scientific result and does not authorize opening centers 33000–33019.
