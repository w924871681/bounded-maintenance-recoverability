# P7.5A claim boundary — literature/theory audit only

Date: 2026-09-27 (Asia/Shanghai). Decision: `LEVEL_C_RECOMMENDED`. This file is a prospective writing boundary, not a change to any previous experiment or protocol. Evidence and source limitations are in [`P7_5A_MAINTENANCE_EXHAUSTION_NOVELTY_AUDIT.md`](../reports/P7_5A_MAINTENANCE_EXHAUSTION_NOVELTY_AUDIT.md).

## Immutable prior scientific state

- C1 bounded fixed-identity maintenance recoverability: human-reviewed `SUPPORTED` **as the current core problem formulation**.
- A1 fixed deployment-reference representation: `A1_DIRECTIONALLY_SUPPORTED_BUT_NOT_ROBUST`.
- P7.4B: formal `P7_4B_FAIL`, unchanged.
- P7.4B.1: `F2_UNCERTAINTY_BOUNDARY_SENSITIVITY`; 24/24 positive LOO paired point effects, 15/24 failed frozen paired uncertainty rule, no single-center aggregate reversal. This does not turn formal FAIL into PASS.

## Claims the evidence permits

1. The *question* “can this deployed model identity regain acceptable service over horizon \(H\) through some admissible fixed-identity maintenance policy with budget \(B\)?” differs from current error, drift, and benefit from one update. This is a conditional operational estimand, not a priority claim.
2. Under nested admissible policy sets and fixed loss/threshold/state, \(R(B)\) is nondecreasing. \(R(0)\), crossing budget when attained, and \(R(B_{max})\) can label service adequacy and bounded recoverability states. This monotonicity is elementary; a budget curve is not in itself new.
3. Exact \(R(B_{max})<0\) means **bounded fixed-identity maintenance unrecoverability relative to the explicitly named class, horizon, threshold, budget, and objective**. A failed finite policy search gives only *evidence within the tested class*, not universal exhaustion.
4. Evidence of bounded unrecoverability can **admit** model-level candidates for evaluation. It neither requires a switch nor proves a better feasible alternative exists.
5. A1 direction is encouraging but its fresh-center robustness remains unestablished. The next experiment recommendation is only a recommendation pending new authorization.

## Claims forbidden without new evidence

- “First DT to update, re-instantiate, switch, retrain, or use utility/uncertainty/cost gates.” These are established in [DiTEC](https://link.springer.com/chapter/10.1007/978-3-031-75390-9_5), [Vlachas et al.](https://doi.org/10.1016/j.ymssp.2026.114717), and related prior art.
- “First recoverability analysis” or “first budget/performance profile.” Earlier [recovery analysis](https://doi.org/10.1016/j.neucom.2014.09.076) and [budget learning curves](https://doi.org/10.1016/j.patrec.2024.08.010) invalidate those broad claims.
- “P7.4B passed,” “A1 transport robust,” “A1 improves every center,” or “uncertainty failure is merely technical.” The frozen failure and center heterogeneity remain.
- “Negative approximate \(\widehat R\) proves all fixed-identity maintenance impossible,” “plasticity is exhausted,” or “model obsolete” without a class-wide certificate.
- “Oracle recoverability is known online.” An oracle can be an offline target only; deployed estimates require causal data, calibration and explicit abstention.
- “Maintenance exhaustion mandates replacement,” or “every exhausted identity has a better bank candidate.” Model-level admission and candidate benefit are separate.
- A1 normalization, generic confidence intervals, generic utility thresholds, generic drift detection, and the \(R(B)\) curve as standalone independent novelties.
- A stronger-conference-level claim, three independent technical contributions, or a new algorithmic module justified solely by this audit.

## Terminology and mathematics to preserve

Preferred formal phrase: **bounded fixed-identity maintenance unrecoverability**. “Maintenance exhaustion” may be shorthand only after stating all qualifiers. Define identity/version lineage and which parameter, adapter, architecture, initialization, and bank changes remain within the admissible class **before** using the term. Do not silently move the boundary to obtain positive results.

With exact nested \(\Pi(B_1)\subseteq\Pi(B_2)\), \(R(B_2)\ge R(B_1)\). If \(\widehat\Pi\subseteq\Pi\), then \(\widehat R\le R\); negative \(\widehat R\) is not an exhaustion certificate. A valid interval \([L_R,U_R]\) for true \(R\) may support recoverability when \(L_R\ge0\), bounded unrecoverability when \(U_R<0\), or indeterminacy otherwise; a finite-search bootstrap alone does not guarantee such coverage.

## Contribution posture and stop-loss

- C1: `MODERATE_METHOD_NOVELTY` as operational problem formulation; not an independent mathematical theorem.
- C2: `SUPPORTING_MECHANISM`, not a robust empirical novelty claim.
- C3: `SUPPORTING_MECHANISM` now; utility-based and repair/replace approaches already overlap, so independent method novelty requires future evidence.
- Recommended structure: one core conceptual/operational contribution + supporting evidence mechanism + future validation contribution.
- Research level: `LEVEL_C_RECOMMENDED`. Freeze method scope; do not add a major module solely to chase level B.
- **One next step only:** a separately pre-registered larger fresh-center A1 replication, only after explicit new human authorization. No experiment is authorized by P7.5A.

No new experiment, heldout evaluation, Alibaba evaluation, or P8 execution was performed.
