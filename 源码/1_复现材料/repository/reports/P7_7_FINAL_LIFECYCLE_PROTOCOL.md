# P7.7 Final Lifecycle Protocol

Status: P7.7A-2 integration-frozen, development-qualified, final-heldout execution not authorized.

This document is the executable protocol companion to `configs/P7_7_FINAL_LIFECYCLE_PROTOCOL.json`. It does not authorize access to centers 33000–33019, Alibaba, or P8.

## Frozen authority

The older generic P7 material is retained as development/calibration vocabulary and lifecycle machinery. P7.2 GateCal-v2/ActionCal-v2 remains the frozen behavior/data-generation lineage with `delta_R=-0.000272181217042075` and cost ratio `10`; its ActionCal admission failure is preserved at its exact historical scope. P7.6B is preserved as `P7_6B_REPLICATION_PASS`; its A1 estimator/scaler are immutable recoverability-inference artifacts. The integrated P7.7 policy uses the A1 output at its exact zero boundary to open RI admission. The P7.2 `delta_R` is not reused as an A1 threshold. Runtime metadata is not a scientific parameter source.

## State and causal order

The deployed lifecycle state is `Z_t=(m_t, theta_t)`. Fixed-identity maintenance changes only `theta_t`; RI changes `m_t` only by committing an identity from the frozen eleven-identity bank. For each stage, the runner executes exactly:

1. read `D_upd` and `D_assess` only;
2. construct the 50-update fixed-identity probe and assess its loss;
3. append the causal response event to the operational same-identity history and apply the immutable P7.6B A1 estimator after identity-held `S_m` normalization;
4. use the exact formal zero boundary: A1 < 0 opens RI admission, while A1 >= 0 keeps RI search closed;
5. if the A1 gate is open, generate the frozen bank candidates, remove the current identity, and apply the unchanged deployment limits;
6. adapt every feasible candidate for exactly 50 updates and evaluate all on the same `D_assess`;
7. compare `retain`, `local + 0.1*unit`, and `candidate + 10*0.1*unit` with exact tie order `retain > local > bank order`;
8. commit the selected action, seal the decision, and only then read `D_srv`;
9. if RI was accepted, reset identity history and construct the new identity's A1 reference scale from the last 200 raw `D_assess` observations, yielding exactly 104 finite point errors; hold that scale fixed for the identity lifetime;
10. continue to the next stage.

No branch is implicit: a negative A1 online estimate makes RI admissible but never forces RI; an empty or unacceptable candidate set falls back to the same fixed-identity comparison and retains the incumbent when it wins.

## A1 and oracle boundaries

The P7.6B A1 artifact is loaded read-only. The runner uses the frozen A1 inference for the P7.7 RI-admission boundary and records the same prediction and `S_m` diagnostics with each development trajectory. `S_m` is `max(median(e_1,...,e_104),1e-12)` from the frozen 200-observation deployment reference. A1 < 0 only opens model-level alternatives; it never forces RI. Oracle bounded recoverability labels are generated only after decisions are sealed and are evaluation-only.

## Methods and population

The exact comparator set is compact and semantically diverse:

- B0 Frozen (no adaptation);
- B1 unconditional fixed-identity P50 maintenance;
- B2 verification-guided RAVM maintenance;
- B8 always-open model-level search;
- P7.7 Recoverability-Guided Lifecycle (internal method key `P7.7`), using P7.2 as historical behavior/data-generation lineage and P7.6B A1 for RI admission.

The named historical methods Always-FT, ER, EWC, SI, Huber-FT, SinglePath, and LegacyFull are excluded because no exact implementation/configuration is recoverable without invention. The final population is metadata-frozen as centers 33000–33019, seeds 7311/7312/7313, scenarios C0/C1/C3/C4: `20*3*4*5 = 1200` method trajectories. These outcomes have not been accessed.

After actions diverge, each method maintains its own parent model, identity, history, scale, and subsequent service path. Only exogenous fixed-seed generator randomness is common. Paired inference is at the center level and never forces a shared post-action trajectory.

## Endpoints and statistics

Primary endpoint: mean lifecycle service loss, defined as stage-mean service MSE followed by seed/scenario aggregation within center and arithmetic mean across centers. Secondary endpoints report maintenance count, RI count, maintenance cost, RI cost, total action cost, retain rate, gate-open rate, and RI rate separately. The historical ratio 10 remains a behavior-path parameter, not a new weighted primary objective.

Decision-quality diagnostics are correct retain, unnecessary RI, correct escalation, and missed escalation, using offline oracle labels only. The statistical unit is center; paired Proposed-versus-baseline contrasts use center-level pairing where valid, 4000 center bootstrap replicates with seed 2904 and percentile 95% intervals, scenario-stratified reporting, and leave-one-center-out sensitivity. No winner ranking is defined.

## Qualification and access guard

`scripts/run_p7_7_final.py --qualification` is the only enabled execution mode. It qualifies all five methods end-to-end on authorized development IDs, tests the P7.7 A1 gate closed branch, A1 gate open without RI commitment, RI commitment and identity/A1 reset, deterministic replay, receipt resume, method-specific paths, and no-future-leakage. `--final-heldout` is a hard error. The qualification audit and guard are:

- `audits/P7_7A2_BRANCH_B_IMPLEMENTATION_QUALIFICATION.json`
- `audits/P7_7A2_FINAL_HELDOUT_ACCESS_GUARD.json`

Final-heldout execution requires a separate human authorization and a later, explicit runner-opening step. This integration freeze itself reads no final-heldout values and produces no final lifecycle scientific verdict.
