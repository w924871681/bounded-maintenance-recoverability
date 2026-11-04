# P7.6B design-based independent replication — pre-outcome protocol freeze

## Material Passport

- Stage: P7.6A-1 protocol resolution; no new scientific outcomes.
- Source: human P7.6A review and frozen P7.4B method/decision artifacts.
- Verification status: protocol and metadata assignment frozen; P7.6B execution **not authorized**.
- Prior verdict preserved: P7.6A **STOP**, not PASS or FAIL; P7.4B **P7_4B_FAIL**; contribution level **LEVEL_C_RECOMMENDED**.

## Scientific target and center count

**R-A, representation-principle replication.** Refit A0 and A1 independently under the same frozen learning procedure on new ReplicationFit, then assess the frozen new pipelines exactly once on disjoint new ReplicationValidation. The exact old fitted P7.4B weights are not the target.

The total is **72 fresh centers**, split **36 Fit + 36 Validation**. This is a **pre-specified design-based replication size**, not power- or assurance-derived. It increases each P7.4B pool from 24 to 36 (50%) and permits exactly four centers per each of nine type × tier strata in each pool. It does not assert 80% power, 80% assurance, statistical optimality, or guaranteed CI exclusion.

## Provenance and deterministic metadata assignment

The metadata stream was fixed before inspection at commit `0975a14f56260fdc2ed28f631831ebbb1339c086`: IDs 32248–32631, batch length 384, seed 7311, and the frozen generator's type schedule and per-slot RNG semantics. The metadata-only RNG replay matched **all 48 frozen P7.4B center type/tier records** without generating labels, workload traces, predictions, oracle R, or trajectories. A repository-wide current-worktree identity-token/filename screen found no prior center-identity use in this range: its only non-new-document matches were the old P7.4B exclusive range upper bound `32248` and a historical process PID `32552`. The old P7.4B centers 32200–32247 and final heldout 33000–33019 are excluded. Candidate strata all contain at least eight eligible centers.

The exact 72 selected IDs are noncontiguous, span **32248–32448**, and are bound in `configs/P7_6B_CENTER_ASSIGNMENT.json` (SHA-256 `172c694057fea9926fecabe800538a5f8ff5bddf8880c078dd457b705b53fb95`). For each stratum below, these are the first eight unused IDs in ascending candidate-stream order. Odd positions go to Fit, even positions to Validation:

| Type / tier | Eight selected IDs, ascending |
| --- | --- |
| A / loose | 32253, 32256, 32262, 32285, 32293, 32307, 32313, 32319 |
| A / medium | 32251, 32264, 32273, 32283, 32289, 32295, 32299, 32304 |
| A / tight | 32258, 32268, 32275, 32280, 32310, 32311, 32328, 32336 |
| B / loose | 32261, 32269, 32271, 32315, 32344, 32352, 32353, 32365 |
| B / medium | 32248, 32254, 32255, 32265, 32274, 32276, 32278, 32279 |
| B / tight | 32249, 32266, 32267, 32281, 32303, 32323, 32327, 32329 |
| C / loose | 32260, 32290, 32306, 32343, 32362, 32381, 32407, 32448 |
| C / medium | 32250, 32257, 32277, 32286, 32287, 32291, 32296, 32300 |
| C / tight | 32252, 32259, 32263, 32270, 32272, 32282, 32318, 32322 |

Each pool has four IDs in every stratum. Within each stratum, the four sorted Fit IDs go to OOF folds 0, 1, 2, 3 respectively. Every held-out fold therefore has 9 centers (one per stratum) and every training fold has 27. All seeds/scenarios/stages from a center stay together. Neither pool nor fold is selected from outcome information.

**Fit (36):** 32248, 32249, 32250, 32251, 32252, 32253, 32255, 32258, 32260, 32261, 32262, 32263, 32267, 32271, 32272, 32273, 32274, 32275, 32277, 32278, 32287, 32289, 32293, 32296, 32299, 32303, 32306, 32310, 32313, 32318, 32327, 32328, 32344, 32353, 32362, 32407.
**Validation (36):** 32254, 32256, 32257, 32259, 32264, 32265, 32266, 32268, 32269, 32270, 32276, 32279, 32280, 32281, 32282, 32283, 32285, 32286, 32290, 32291, 32295, 32300, 32304, 32307, 32311, 32315, 32319, 32322, 32323, 32329, 32336, 32343, 32352, 32365, 32381, 32448.

## Immutable scientific procedure

The sole shared behavior path is frozen **P7.2 Proposed**, `delta_R=-0.000272181217042075`, cost ratio 10. P7.2's FAIL is unchanged. A0/A1 remain observational; neither may affect selected action, parent state, RI, identity, or lifecycle evolution. Every `(center, seed, scenario, stage)` must match between A0 and A1 on parent identity/state hash, selected action, post-action identity, and behavior-path hash; any mismatch is STOP.

A0: target `R_B50`, response `[gain, post_assessment_mse]`, fixed optimization multiplier 1000, predictions divided by 1000 before metrics and zero-boundary use. A1: `S_m=max(median(e_1,…,e_104),1e-12)` using exactly 104 squared errors from the causal 200-observation deployment reference; target `R_B50/S_m`, response `[gain,post_assessment_mse/S_m]`, multiplier 1. `S_m` is fixed during one identity lifetime; after RI discard the old scale/history and reconstruct from the identical rule. No new representation, feature, reference, floor, uncertainty module, or decision boundary is allowed.

Common factors: model seeds 7311/7312/7313; scenarios C0/C1/C3/C4; 24 stages; window 96; `D_upd=400`, `D_assess=240`, `D_srv=400`; `H_R=4`, `eta=0.25`, B50 and P0/P10/P20/P50; unchanged tau-service rule, generator, bank, deployment filters; `K_S=2`, `K_L=6`, six features. A0/A1 each use separate fold-specific StandardScaler fitted only on 27 training centers (mean/population SD, zero SD→1), then final separate scalers on all 36 Fit centers. MLP `6→16→8→1`, ReLU, identity output, float32, full-fold Adam/MSE, lr 0.001, weight decay 0.0001, 400 epochs, no shuffle, early stop or checkpoint choice. Paired initialization seeds are **9632–9635** for folds 0–3 and **19631** for all-Fit final models.

For every A1 identity birth audit scale source, 200-reference/104-error count, initial-vs-RI birth, center/type/tier, finite value, and floor activation. Nonfinite scale, non-104 count, or >1% floor activation within either pool is STOP.

## Frozen order and decision

After separate authorization: generate **Fit only**; produce paired records; run four group OOF fits; evaluate all Fit absolute conditions; fit two final pipelines on all 36 Fit centers; hash/Git-freeze scalers, estimators, formulas, Fit OOF metrics and implementation/configuration; commit a machine-readable one-time Validation-opening manifest; only then materialize the 36 Validation centers; apply pipelines once without refitting or reselection; calculate the complete original decision and stop for human scientific review.

Both Fit OOF and Validation require A1 macro-center Spearman >0, positive-center fraction >0.5, zero-boundary balanced admission accuracy >0.5, and non-C3 macro-center Spearman >0. Validation also requires paired `A1−A0` macro Spearman >0 and balanced admission accuracy >0. The **4000** paired center bootstrap uses prospectively frozen seed **7601**, identical A0/A1 resamples, linear-quantile percentile 95% intervals: at least one lower bound >0 and the other upper bound not <0. Undefined or fewer replicates cause STOP. Fit→Validation deterioration is Fit OOF minus Validation; if A1 deteriorates strictly more than A0 on **both** macro Spearman and BA, FAIL. Remove each of 36 Validation centers in turn without refit and recompute all Validation absolute, paired-point and paired-uncertainty conditions; **one failure is FAIL**. Integrity, leakage, pairing, scale or path failures also prevent PASS. Final labels are exactly `P7_6B_REPLICATION_PASS` or `P7_6B_REPLICATION_FAIL`; no partial PASS or tolerance.

Only the 72 new centers determine the primary verdict; old P7.4B centers cannot rescue a failure. A PASS supports only bounded reproducibility under this evaluated synthetic lifecycle protocol, not universal DT/recoverability claims, lifecycle superiority, C3 novelty, final-heldout success or Alibaba generality. A FAIL ends further A1 redesign under the LEVEL_C_RECOMMENDED stop-loss decision.

## Bindings, readiness and prohibition

The complete machine-readable protocol is `configs/P7_6B_FROZEN_PROTOCOL.json` (SHA-256 `86272adb9a335ff72030cc4ba5c1fbc5f52e543eacd58ba032433e590251ee23`). This file-level hash binds formulas, scale construction, behavior path, estimator/fitting and preprocessing, all seeds, and every decision condition; the resolution audit carries component-level hashes and the center-assignment hash. The original P7.4B protocol/generator/behavior-source hashes are recorded there as upstream bindings.

**P7.6B is protocol-resolved but not executable yet.** The current P7.4B runner hard-codes 24/24 centers and the 32200–32247 range. A separate future implementation must reproduce the frozen 384-slot metadata schedule for selected noncontiguous IDs and pass pre-outcome code/hash/path preflight; P7.6B also needs separate human authorization. No P7.6B trajectory or scientific outcome may be created by this phase.

The eventual 72-center design implies **864** shared center×seed×scenario trajectories and **20,736** stages (72×3×4×24), not double-counted for observational A0/A1. No final-heldout, Alibaba, or P8 execution is authorized.
