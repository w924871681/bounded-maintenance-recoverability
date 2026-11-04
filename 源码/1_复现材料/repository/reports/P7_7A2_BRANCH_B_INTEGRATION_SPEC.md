# P7.7A-2 Branch-B Integration Specification

Status: frozen for development qualification; final-heldout execution is not authorized.

## Frozen lineage and roles

- P7.2 Proposed remains the historical behavior/data-generation lineage (`delta_R=-0.000272181217042075`, cost ratio `10`). Its formal ActionCal FAIL is preserved and is not reinterpreted.
- P7.6B A1 is the immutable recoverability-inference component. Its frozen scaler, features, estimator, `S_m` construction and zero boundary are unchanged.
- P7.7 is the integrated lifecycle policy identifier: `P7.7 Recoverability-Guided Lifecycle`.

## Operational rule

At each stage, after the fixed-identity 50-update probe and before service data are read, construct the A1 features from the current same-identity causal response history. Normalize the residual component by the identity-held `S_m = max(median(exactly 104 finite point errors from the permitted 200-observation reference), 1e-12)`. Apply the frozen A1 estimator and the exact formal boundary `0.0`:

- A1 `>= 0`: RI search remains closed; compare retain and local maintenance under the existing frozen costs and tie order.
- A1 `< 0`: RI search becomes admissible; generate the unchanged frozen bank candidates, remove the current identity, apply unchanged feasibility limits, adapt each feasible candidate for exactly 50 updates, and compare retain/local/RI with the existing comparison and tie order.

A1 `< 0` never forces RI. If no acceptable candidate exists or RI does not win, the existing retain/local fallback applies. After a committed RI, commit the selected identity, discard the old response history, reconstruct `S_m` from the last 200 raw `D_assess` observations before the next decision, and hold the new scale fixed for that identity lifetime.

## Preserved components

No refit, recalibration, new margin, threshold tuning, feature change, history change, candidate-bank change, adaptation-budget change, deployment-feasibility change, service-loss change, comparator change, or statistical-plan change is introduced. The P7.2 `delta_R` is not used as an A1 threshold. The primary endpoint is named “mean lifecycle service loss”; its existing stage → seed/scenario within center → center mean computation is unchanged.

## Causal and access guards

The decision path reads only `D_upd` and `D_assess` before action selection. `D_srv` is read after the decision is sealed. Oracle labels are post-decision diagnostics only. A1 history and `S_m` reset after RI. Final-heldout centers 33000–33019, Alibaba and P8 remain hard-blocked; `--final-heldout` remains a hard error.

## Development qualification evidence

The Branch-B qualification is development-only and uses the authorized development pool. It passed:

- all five methods end-to-end;
- A1 gate-closed rows: 67;
- A1 gate-open/non-committed rows: 27;
- committed RI rows: 2;
- identity/A1 reset fields;
- deterministic replay;
- receipt/resume identity;
- no-future-service leakage;
- method-specific paths;
- final-heldout, Alibaba and P8 access guards.

The machine-readable qualification record is `audits/P7_7A2_BRANCH_B_IMPLEMENTATION_QUALIFICATION.json`; the access guard is `audits/P7_7A2_FINAL_HELDOUT_ACCESS_GUARD.json`.
