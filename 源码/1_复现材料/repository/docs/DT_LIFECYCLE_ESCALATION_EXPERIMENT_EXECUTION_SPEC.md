# DT Lifecycle Escalation — Section 5 Experimental Plan and Codex Execution Specification

**Purpose:** Freeze the experimental questions, protocol, baselines, fairness rules, execution phases, required artifacts, and audit conditions for the third DT-lifecycle paper.

**Core problem:** Determine when fixed-identity local maintenance remains sufficient and when lifecycle control should escalate to model-level re-instantiation.

**Repository rule:** The first-paper MSA-DTI repository and second-paper RAVM-DT repository are read-only sources. The third paper must use an independent workspace. Reused code must be copied or wrapped and its source path, commit/hash, and modifications recorded.

---

## 1. Experimental questions

### Q1 — Does the recoverability problem actually exist?

Before testing the online gate, establish that the controlled lifecycle benchmark contains both:

1. **maintenance-recoverable stages**, where bounded fixed-identity maintenance can satisfy the service criterion; and
2. **maintenance-insufficient stages**, where bounded fixed-identity maintenance cannot satisfy the criterion but at least one deployment-feasible alternative identity can provide a persistent service benefit after target adaptation.

Required evidence:
- finite-policy oracle approximation `R_oracle_approx`;
- recoverability margin by scenario/stage;
- best-local horizon loss versus best feasible re-instantiation horizon loss;
- persistence of re-instantiation benefit;
- center-level variability and 95% center-cluster bootstrap intervals.

**STOP rule:** If the development pool does not show a stable recoverable/insufficient distinction, do not launch large held-out experiments. Return a diagnostic report instead of tuning the gate until it wins.

### Q2 — Does Proposed improve lifecycle decisions?

Evaluate service–intervention trade-off relative to fixed, maintenance-only, periodic, drift-triggered, reject-count, recent-gap, and always-open model-level baselines.

Primary outcomes:
- lifecycle MSE/MAE;
- normalized lifecycle objective;
- local-maintenance rate;
- model-level search rate;
- re-instantiation rate;
- target-side runtime and peak memory.

### Q3 — Does it distinguish maintainable change from re-instantiation-worthy change?

Measure:
- false-escalation rate on oracle-recoverable stages;
- missed-escalation rate on oracle-insufficient stages;
- escalation delay from the first persistent oracle-insufficient stage;
- re-instantiation precision;
- post-escalation horizon gain;
- immediate reversal rate.

### Q4 — Is escalation robust to unreliable/transient monitoring evidence?

Test transient and persistent telemetry corruption while keeping service evaluation clean.

### Q5 — Which mechanisms matter, and is behavior stable?

Ablate current probing, multi-timescale response evidence, coverage information, and the recoverability gate. Evaluate window/gate/cost sensitivity, estimator simplicity, architecture/horizon generality, deployment limits, runtime and memory.

### Q6 — Does the frozen method transfer to an external production trace?

Reuse the Alibaba Cluster Trace v2018 pipeline. Primary external evidence must be **direct transfer with the synthetic-domain configuration frozen**. Any Alibaba-specific recalibration is a separate diagnostic.

---

## 2. Proposed Section 5 structure

```text
5. Experimental Evaluation

5.1 Experimental Setup
    5.1.1 Reusable Model Bank and Lifecycle Protocol
    5.1.2 Controlled Evolution, Recoverability Oracle, and Data Roles
    5.1.3 Baselines, Metrics, and Calibration
    5.1.4 Implementation, Statistics, and Reproducibility

5.2 Oracle Recoverability and the Need for Re-instantiation
5.3 Overall Lifecycle Escalation Performance
5.4 Escalation Specificity and Timeliness Across Change Types
5.5 Robustness to Unreliable Monitoring Evidence
5.6 Mechanism, Sensitivity, Generality, and Cost
5.7 External Production-Trace Evaluation
```

---

## 3. Reusable assets

### 3.1 MSA-DTI read-only assets

Reuse where available:
- reusable source-trained model bank;
- MLP/TCN/GRU definitions;
- source checkpoints and source-training metadata;
- model identity metadata `(architecture, source-trained initialization)`;
- operation-count and parameter-count measurement;
- hard deployment-limit filtering;
- target adaptation operator;
- candidate assessment utilities;
- synthetic-center generator components;
- center-cluster bootstrap utilities;
- checkpoint/config hashing utilities.

Reference settings from the first paper:
```text
input length L = 96
source training = Adam / MSE / 50 epochs / lr 1e-3 / batch 64
target adaptation = SGD / MSE / 50 updates / lr 0.01 / grad clip 1.0
operation limits = 1.5e6 / 5e6 / 2e7
parameter limits = 3e4 / 1e5 / 5e5
bootstrap = 4000 center-cluster repetitions
```

Do not use first-paper held-out outcomes for third-paper tuning.

### 3.2 RAVM-DT read-only assets

Reuse where available:
- lifecycle engine;
- raw-first causal stage split;
- update / assessment / service role separation;
- 24-stage trajectory infrastructure;
- stationary/gradual/abrupt/recurring generators;
- corruption generators;
- clean service evaluation;
- runtime/memory instrumentation;
- center-level bootstrap;
- Alibaba preprocessing;
- leakage/reproducibility audits;
- deterministic seed utilities.

Reference final protocol:
```text
T = 24
seeds = {7311, 7312, 7313}
main model = GRU-32
L = 96
prediction horizon = 1
per stage:
    D_upd = 400 raw observations
    D_assess = 240 raw observations
    D_srv = 400 raw observations
local adaptation:
    SGD / MSE / 50 updates
    lr = 0.01
    grad clip = 1.0
batch = 64
statistical unit = center
bootstrap = 4000
hardware reference = NVIDIA RTX 3060 Laptop GPU
```

Rename prior “verification” role to **assessment** where needed to match the third-paper notation.

---

## 4. New repository

Recommended:

```text
DT_LIFECYCLE_ESCALATION/
├── docs/
├── configs/
├── core/
├── imported/
│   ├── msa_dti/
│   └── ravm_dt/
├── scripts/
├── experiments/
├── results/
├── audits/
├── reports/
└── paper/
```

Rules:
1. MSA-DTI repo: read-only.
2. RAVM-DT repo: read-only.
3. Do not modify prior frozen artifacts.
4. Record imported file source path, commit if available, SHA-256, destination, and modifications.
5. Produce `audits/REUSE_PROVENANCE.md`.

---

## 5. Main lifecycle protocol

Default main protocol:

```text
T = 24
L = 96
main prediction horizon = 1
model seeds = 7311, 7312, 7313

per stage:
    D_upd: 400
    D_assess: 240
    D_srv: 400

D_upd, D_assess, D_srv are pairwise disjoint.
D_srv is unavailable until after the stage-t action is fixed.
```

Execution order:

```text
decision-time information
→ local-maintenance probe on candidate copy using D_upd
→ paired pre/post assessment on D_assess
→ current probe response
→ same-identity bounded response history
→ recoverability estimate
→ gate model-level action space
→ if gate open: adapt feasible alternatives using D_upd
→ compare admissible actions on D_assess
→ select/deploy action
→ evaluate clean D_srv
→ update/reset response history
```

No future service observation may enter the online decision.

---

## 6. Initial deployed identity

All methods in a paired run must start from exactly the same initial state.

Preferred construction:
1. use the first-paper source-trained bank and hard deployment filtering;
2. use only an initial warm-up segment;
3. choose the initial identity with a frozen procedure;
4. save the initial state hash and reuse it for every method in the same center/seed/scenario.

The initial identity must be suitable for the initial regime and must not use future post-shift data.

---

## 7. Controlled lifecycle conditions

Use common stage boundaries across paired methods.

### C0 Stationary
No meaningful regime change. Tests unnecessary escalation.

### C1 Parameter-level gradual drift
Gradually vary parameters within the same generating family while preserving the underlying dependency structure. Expected to remain mostly maintainable.

### C2 Parameter-level abrupt drift
Abrupt parameter change at a fixed boundary, preferably stage 9, while preserving the generating family. Tests rapid adaptation without automatic identity escalation.

### C3 Source-identity mismatch / prior-family replacement
After the shift, change the target regime so that another source-trained initialization in the bank is substantially closer under the same bounded adaptation budget. Include at least one same-architecture version to show that model identity is not only architecture.

### C4 Architecture-level mismatch
Change temporal dependency structure so that a different architecture family in the reusable bank has a persistent post-adaptation advantage. Development-only generator knobs may include:
- short-memory → long-memory dependence;
- weak temporal dependence → recurrent/periodic dependence;
- nonlinear temporal interaction change;
- masked-variable dependence change.

Do not freeze the generator until Q1 diagnostics confirm the intended recoverability distinction on development centers.

### C5 Persistent regime replacement
Switch to a new regime and stay there. This may be represented by C3/C4 subtypes if the main matrix must remain smaller.

### C6 Recurring regime
Recommended schedule:
```text
stages 1–8: A
stages 9–16: B
stages 17–24: A
```
Tests identity-tenure reset and stale-history behavior.

### C7 Transient corruption
Underlying service regime remains recoverable; corrupt decision-time maintenance information briefly. Tests spurious escalation.

### C8 Persistent mismatch + unreliable monitoring
Overlay corruption on a true maintenance-insufficient regime. Tests whether noisy evidence suppresses needed escalation.

### Full-baseline main matrix
Use:
```text
C0, C1, C2, C3, C4, C6
```
Use C7/C8 mainly in robustness experiments.

---

## 8. Mandatory development phenomenon gate

Before fitting the final online estimator, run an oracle diagnostic.

For each development center/seed/stage:
1. compute finite-policy local-maintenance oracle approximation;
2. compute best deployment-feasible re-instantiation horizon outcome;
3. compare continued fixed-identity maintenance with re-instantiation.

Required outputs:
- recoverability margin by condition/stage;
- fraction `R_oracle_approx < 0`;
- re-instantiation horizon gain conditional on negative recoverability;
- re-instantiation gain conditional on nonnegative recoverability;
- center-wise paired distributions;
- identity/architecture chosen after model-level escalation.

Required qualitative pattern:
```text
maintainable conditions:
    predominantly nonnegative recoverability
    little persistent re-instantiation advantage

mismatch conditions:
    meaningful post-shift negative recoverability
    persistent advantage from at least one feasible alternative

transient corruption:
    no persistent re-instantiation advantage after corruption ends
```

If absent: **STOP** and write `reports/P3_PHENOMENON_DIAGNOSTIC.md`.

---

## 9. Finite-policy oracle approximation

Experiments must not claim the ideal infimum is exactly observable.

Recommended initial finite policy set:
```text
P0  = retain only
P10 = 10 optimizer updates per stage
P20 = 20 optimizer updates per stage
P50 = 50 optimizer updates per stage
```

All preserve incumbent identity, use causal data, and satisfy the maintenance budget.

Define a finite-policy oracle approximation:
```text
R_oracle_approx = tau_svc - min_horizon_service_loss_over_prespecified_local_policies
```

Report it as an approximation, not exact ground truth.

Recoverability horizon development grid:
```text
H_R ∈ {2, 4, 6}
```
Choose on development-only stability/identifiability criteria and freeze before heldout.

---

## 10. Service threshold

Do not set `tau_svc` from held-out outcomes.

Preferred development definition:
```text
tau_svc = (1 + eta_svc) * L_ref
```
where `L_ref` is a development-only initial-regime reference loss and `eta_svc` is chosen on a prespecified development grid.

Freeze the rule before calibration/heldout.

---

## 11. Local probe and effort-feature audit

Primary implementation should reuse the fixed 50-update local adaptation operator for maximum compatibility.

This may make optimizer-update effort constant.

Mandatory audit:
- compute variance of `e_t`;
- if constant or non-informative, remove it from the estimator input and manuscript before heldout;
- do not manufacture artificial variability.

Default response if effort is constant:
```text
xi_t = [gain_t, residual_t]
gain_t = (pre_assess_loss - post_assess_loss) / (pre_assess_loss + eps)
residual_t = post_assess_loss
```

---

## 12. Recoverability estimator

Estimator architecture is not the novelty.

Mandatory candidates:
```text
Ridge / linear regression
small 2-layer MLP
```

Optional development diagnostic:
```text
small gradient-boosted regressor
```

Target:
```text
continuous finite-policy recoverability margin
```

Fit loss:
```text
MSE
```

Standardize continuous inputs using fitting-pool statistics only.

---

## 13. Center pools

Use disjoint pools.

Recommended:
```text
method development / estimator fitting: 30 centers
decision/gate calibration:              20 centers
final synthetic heldout:                20 centers
```

Three fixed model seeds per center.

Create new deterministic center IDs for the third paper and store them in `configs/center_splits.json`.

No held-out center may be used for:
- feature design;
- estimator selection;
- threshold selection;
- scenario-generator tuning;
- cost-weight selection.

---

## 14. Core baselines

All baselines use the same paired center/seed/scenario realization, same initial state, same online data visibility, same bank where applicable, same hard deployment filtering, and same per-candidate adaptation operator.

### B0 Frozen
Never maintain, never re-instantiate.

### B1 Always-Maintain
Fixed-identity local maintenance every stage; never re-instantiate.

### B2 RAVM-DT Only
Use frozen RAVM-DT local state-transition control; disable model-level re-instantiation.

### B3 Periodic Re-instantiation
Trigger every `K` stages.
Development grid:
```text
K ∈ {4, 6, 8, 12}
```

### B4 Error-Threshold Re-instantiation
Open model-level actions when current decision-time assessment loss exceeds a calibrated threshold, optionally with persistence.
Development grid:
```text
threshold quantiles = {0.80, 0.90, 0.95}
persistence = {1, 2, 3}
```

### B5 ADWIN Re-instantiation
Feed a causal decision-time error/loss stream into ADWIN; signal → open model-level action space.
Never use future service error online.

### B6 Reject-Count Re-instantiation
Use frozen RAVM-DT accept/reject decisions; re-instantiate after `K` consecutive local-candidate rejections.
Development grid:
```text
K ∈ {2, 3, 4, 6}
```
Tests the naive “RAVM-DT + hard-coded trigger” route.

### B7 KEEP-Style Recent-Gap Switching
Task-matched recent-window comparison:
- compare best candidate versus incumbent on recent decision-time evidence;
- switch only when gap exceeds calibrated threshold;
- same bank, limits, update/assessment data, and adaptation operator.

Call this a **KEEP-style task-matched baseline**, not an exact DiTEC reproduction unless implementation assumptions truly match.

### B8 Always-Open Model-Level Selection
Every stage, evaluate the same feasible alternatives Proposed would evaluate after gate opening and select using the same decision-time surrogate. No recoverability gate.
This isolates the value of the gate.

### B9 Proposed
Current bounded maintenance probe + same-identity multi-timescale response history + recoverability estimator + calibrated gate + deployment-feasible re-instantiation.

### Diagnostic upper bounds (not deployable baselines)

**O1 Oracle Recoverability Gate:** use the finite-policy future-service oracle approximation for gate state.

**O2 Retrospective Best Action:** use future service outcomes to choose the best action retrospectively.

Never present O1/O2 as deployable methods.

---

## 15. Literature comparisons to discuss

Do not force incompatible methods into a neural workload-regression benchmark and then call the port exact.

At minimum discuss:
- Mahadevan & Mathioudakis, **Cost-Aware Retraining for Machine Learning**, KBS 2024, DOI 10.1016/j.knosys.2024.111610.
- Regol et al., **When to retrain a machine learning model**, ICML/PMLR 2025.
- Dittler et al., **Illustrating the benefits of efficient creation and adaption of behavior models in intelligent Digital Twins over the machine life cycle**, JMS 2024, DOI 10.1016/j.jmsy.2024.08.016.
- DiTEC / KEEP adaptive model selection.
- Vlachas et al., **Utility-driven adaptive model selection for digital twinning**, MSSP 258, 114717, 2026, DOI 10.1016/j.ymssp.2026.114717.

If official code enables a scientifically faithful regression-compatible port, add it as an extended baseline. Otherwise clearly label controlled task-matched analogues.

---

## 16. Fairness rules

Mandatory:
1. same center/seed/scenario realization;
2. same initial deployed-state hash;
3. same stage boundaries;
4. same raw indices for `D_upd`, `D_assess`, `D_srv`;
5. same reusable bank/hash;
6. same hard deployment limits;
7. same per-candidate target adaptation operator for re-instantiation methods;
8. same max optimizer-update budget per candidate;
9. same assessment set for candidate comparison;
10. no service data in online decisions;
11. baseline hyperparameters selected only on development/calibration pools;
12. heldout untouched until configs frozen;
13. runtime reflects actual work; do not claim equal compute when search frequencies differ;
14. report decision quality and search/runtime cost;
15. list any method-specific extra information explicitly.

---

## 17. Metrics

### Service
- lifecycle MSE (primary);
- lifecycle MAE.

### Lifecycle objective
Report:
```text
J_life = mean_service_loss + lambda_M * maintenance_cost + lambda_R * reinstantiation_cost
```
Always report components separately.

Cost-ratio sensitivity:
```text
lambda_R / lambda_M ∈ {2, 5, 10}
```
or another prespecified three-point range after development-only scale audit.

### Recoverability estimation
- MAE;
- RMSE;
- Spearman correlation;
- sign accuracy;
- AUROC/AUPRC for `R_oracle_approx < 0` as diagnostics.

### Escalation
- gate-open rate;
- re-instantiation rate;
- false-escalation rate;
- missed-escalation rate;
- escalation delay;
- re-instantiation precision;
- immediate reversal rate;
- post-escalation horizon gain.

### Deployment
- operation-limit satisfaction;
- parameter-limit satisfaction;
- number of feasible alternatives.

### Runtime/cost
- local-probe time;
- recoverability inference time;
- model-bank search/adaptation time;
- total decision time;
- peak GPU memory;
- persistent history memory;
- model-level search frequency.

---

## 18. Calibration

Use separate fitting and calibration centers.

Estimator fit: fitting centers only.

Gate margin `delta_R`: calibration centers only.

Preferred gate calibration:
```text
minimize empirical lifecycle objective
subject to a prespecified maximum false-escalation rate
```

Initial false-escalation caps:
```text
{0.05, 0.10}
```

Each threshold-based baseline receives its own fair calibration on the same calibration pool.

No heldout tuning.

---

## 19. Main held-out matrix

Recommended:
```text
centers = 20
seeds = 3
stages = 24
main conditions = 6
methods = 10 (B0–B9)
```

Trajectories:
```text
20 × 3 × 6 × 10 = 3600
```

Stage-method records:
```text
3600 × 24 = 86,400
```

If runtime is excessive, decide and freeze a smaller matrix from development throughput **before** heldout execution.

---

## 20. Section 5.2 — Q1

Report:
1. oracle recoverability margin by condition/stage;
2. recoverable vs insufficient stage fraction;
3. best bounded-local horizon loss;
4. best feasible re-instantiation horizon loss;
5. re-instantiation benefit conditional on oracle insufficiency;
6. stages where local maintenance is insufficient but no feasible alternative is better.

Claim boundary:
`R_oracle_approx < 0` means bounded local maintenance is insufficient under the finite-policy approximation; it does not guarantee beneficial re-instantiation.

---

## 21. Section 5.3 — Q2

Compare B0–B9 on six main conditions.

Primary table:
```text
Method
Lifecycle MSE
Lifecycle MAE
J_life
Local-maintenance rate
Gate/search rate
Re-instantiation rate
Decision time
Peak GPU memory
Deployment-limit satisfaction
```

Use paired center differences and 4000 center-cluster bootstrap repetitions.

A CI crossing zero is inconclusive, not equivalence.

---

## 22. Section 5.4 — Q3

Break down C0/C1/C2/C3/C4/C6.

Report:
- false escalation;
- missed escalation;
- delay;
- re-instantiation precision;
- horizon gain;
- selected identity;
- reversal count.

Representative lifecycle figure should show:
```text
oracle recoverability
estimated recoverability
gate state
deployed identity
service loss
```

Aggregate conclusions must remain center-level, not anecdotal.

---

## 23. Section 5.5 — Q4 corruption robustness

Reuse RAVM-DT corruption generators.

Keep `D_srv` clean.

Families:
```text
random noise
persistent bias
burst
replay
mixed
```

Fractions:
```text
alpha ∈ {0.05, 0.10, 0.20}
```

Use at least:
```text
one maintainable physical regime
one true persistent identity-mismatch regime
```

This tests both false escalation and missed necessary escalation.

If full matrix is too large, preregister a robustness subset:
```text
Proposed
RAVM-DT Only
ADWIN-RI
KEEP-style
Always-Open
```

---

## 24. Section 5.6 — Q5

### Ablation
Use fixed diagnostic heldout slice, no per-ablation retuning:
```text
A Full
B CurrentProbeOnly
C ShortOnly
D LongOnly
E NoCoverage
F CurrentLossOnly
G NoRecoverabilityGate / Always-Open
```

If `e_t` is removed, do not create a NoEffort ablation.

### Estimator simplicity
```text
Ridge
small 2-layer MLP
```

### Window sensitivity
```text
K_S ∈ {2, 4, 6}
K_L ∈ {6, 12, 18}
K_S < K_L
```
Use a prespecified local slice rather than unnecessary full Cartesian search.

### Gate sensitivity
Frozen `delta_R ± one calibration grid step`.

### Recoverability horizon
```text
H_R ∈ {2, 4, 6}
```

### Cost ratio
At least three `lambda_R / lambda_M` values.

### Architecture/horizon generality
```text
backbone ∈ {MLP, TCN, GRU-32}
prediction horizon ∈ {1, 4}
```

### Deployment limits
Reuse matched tight/medium/loose pairs:
```text
operations = 1.5e6 / 5e6 / 2e7
parameters = 3e4 / 1e5 / 5e5
```

Report feasible-bank size, blocked escalation opportunities, MSE/objective, re-instantiation rate, runtime/memory.

---

## 25. Section 5.7 — Alibaba

Preferred new split:
```text
source/init = 20 machines
development = 20
calibration = 20
heldout = 40
```

Use machine IDs/hashes disjoint from prior heldout machines where possible.

Primary:
```text
direct transfer
```
with synthetic-frozen estimator/gate/window/cost configuration.

Secondary:
```text
domain-specific calibration diagnostic
```
using Alibaba calibration machines only.

If the natural trace contains few oracle-insufficient opportunities, report the limitation instead of manufacturing a strong claim.

---

## 26. Stage-level raw schema

```text
run_id
center_id
center_pool
seed
scenario
scenario_subtype
stage
method

incumbent_identity_id
incumbent_architecture
incumbent_source_init_id
incumbent_state_hash

D_upd_hash
D_assess_hash
D_srv_hash

probe_state_hash
probe_update_count
probe_pre_assess_loss
probe_post_assess_loss
probe_gain
probe_residual
probe_effort

history_size
K_S
K_L
coverage_S
coverage_L
feature_vector_hash

recoverability_hat
recoverability_oracle_approx
oracle_recoverable

gate_margin
gate_open
num_bank_candidates
num_feasible_alternatives

selected_action
selected_identity_id
reinstantiated
selected_assess_loss

service_mse
service_mae

maintenance_cost
reinstantiation_cost
lifecycle_objective_stage

local_probe_time_s
recoverability_inference_time_s
model_level_search_time_s
decision_total_time_s
peak_gpu_memory_bytes
persistent_history_bytes

operation_count
parameter_count
operation_limit
parameter_limit
deployment_feasible

update_start_ts
assessment_ts
decision_ts
service_start_ts
service_end_ts
```

Candidate-level table:
```text
run_id
stage
candidate_identity_id
candidate_architecture
candidate_source_init_id
feasible
adapted_state_hash
adaptation_updates
assessment_loss
candidate_cost
surrogate_objective
adaptation_time_s
```

---

## 27. Mandatory audits

```text
test_no_future_service_leakage.py
test_raw_role_disjointness.py
test_window_no_cross_role_boundary.py
test_same_initial_state_across_methods.py
test_same_stage_data_across_methods.py
test_same_bank_hash_across_methods.py
test_deployment_filter_identical.py
test_candidate_adaptation_budget.py
test_assessment_not_used_for_gradients.py
test_service_data_immutable.py
test_current_probe_before_gate.py
test_gate_before_model_level_search.py
test_probe_does_not_modify_deployed_state.py
test_history_contains_probe_responses_only.py
test_history_reset_after_reinstantiation.py
test_history_bounded_by_KL.py
test_recoverability_feature_causal.py
test_oracle_future_data_offline_only.py
test_fit_calibration_heldout_disjoint_centers.py
test_baseline_calibration_heldout_disjoint.py
test_final_config_hash_frozen_before_heldout.py
test_bootstrap_clusters_by_center.py
test_all_deployed_models_meet_limits.py
test_effort_feature_variance.py
```

Any scientific/leakage/fairness audit failure:
```text
STOP
```

---

## 28. Codex execution phases

### P0 Repository discovery
Locate the first-paper GitHub/local repository and the local final RAVM-DT workspace. Record commits/hashes/status. Do not modify them.

Output:
```text
reports/P0_REPOSITORY_DISCOVERY.md
audits/REUSE_PROVENANCE.md
```

### P1 New third-paper workspace
Create independent repo/environment lock.

### P2 Reuse integration + causal audits
Integrate only necessary components. Run smoke/leakage/role tests. No large experiment.

### P3 Controlled-shift generator + Q1 phenomenon diagnostic
Run small development diagnostics for C0–C8.

If recoverable/insufficient states and re-instantiation benefit do not stably exist:
```text
STOP
```

Output:
```text
reports/P3_PHENOMENON_DIAGNOSTIC.md
```

### P4 Freeze scenario generator
Output:
```text
configs/scenario_frozen.yaml
audits/scenario_frozen.sha256
```

### P5 Probe/feature audit
Audit effort variance, response distributions, window coverage, leakage. Remove `e_t` if non-informative.

Output:
```text
reports/P5_RESPONSE_FEATURE_AUDIT.md
```

### P6 Recoverability-estimator fitting
Fit Ridge and small MLP on fitting centers.

Output:
```text
artifacts/recoverability_estimator.*
reports/P6_ESTIMATOR_SELECTION.md
```

### P7 Calibration and final freeze
Calibrate Proposed and all baseline thresholds on calibration centers only.

Output:
```text
configs/final_method_config.yaml
configs/final_baseline_configs.yaml
audits/FINAL_FREEZE_MANIFEST.json
audits/FINAL_FREEZE_SHA256.txt
```

### P8 Heldout Q1 confirmatory oracle diagnostic

### P9 Heldout Q2 main comparison

### P10 Q3 specificity/timeliness

### P11 Q4 corruption robustness

### P12 Q5 ablation/sensitivity

### P13 Q5 generality/deployment/cost

### P14 Q6 Alibaba direct transfer, then separate recalibration diagnostic

### P15 Statistics/figures
Use 4000 center-cluster bootstrap repetitions.

### P16 Final reproducibility audit

---

## 29. Runtime protocol

Separate:
```text
local probe
recoverability inference
model-level search/adaptation
final comparison
total decision time
```

Exclude service evaluation from online decision runtime.

Use identical warm-up rules.

Do not state “same computational budget” unless exactly true. Prefer:
- same per-candidate optimizer-update budget;
- same candidate adaptation operator;
- same data visibility.

---

## 30. Statistics

Primary unit = center.

For each center:
1. average fixed seeds within matched method/condition;
2. compute paired differences;
3. bootstrap centers with replacement while keeping stages/scenarios belonging to a center together.

```text
4000 bootstrap repetitions
```

For delay:
- report conditional delay among escalated cases;
- report missed-escalation rate separately;
- do not assign arbitrary finite delay to never-escalated runs.

---

## 31. Required manuscript outputs

**Table 1:** main configuration.

**Figure 3:** oracle recoverability phenomenon + local-vs-reinstantiation horizon gap.

**Main performance table/figure:** lifecycle MSE, lifecycle objective, re-instantiation/search rate, decision time.

**Specificity/timeliness figure:** false escalation, missed escalation, delay, precision.

**Representative trajectory:** oracle recoverability, estimated recoverability, gate state, deployed identity, service loss.

**Robustness figure:** false/missed escalation and lifecycle MSE/objective across corruption.

**Ablation table:** Full, CurrentProbeOnly, ShortOnly, LongOnly, NoCoverage, CurrentLossOnly, NoGate.

**Sensitivity/generality/cost:** windows, cost ratio, architecture/horizon, deployment limits, runtime/memory.

**External table/figure:** Alibaba direct transfer; recalibration shown separately.

---

## 32. Claim boundaries

Do not claim:
- perfect structural-mismatch identification;
- optimal escalation guarantee;
- universally reduced compute;
- universal generalization;
- exact reproduction of task-incompatible literature methods.

Preferred:
- “within the evaluated controlled lifecycle conditions”;
- “the estimated recoverability was associated with…”;
- “the gate changed/reduced model-level search frequency…”;
- “the trend was consistent across the tested architectures/horizons”;
- “external-trace results provide additional evidence, with the following boundary…”

---

## 33. Scientific success criteria

The third-paper experiment is convincing only if held-out evidence jointly shows:

1. recoverable and insufficient lifecycle states both exist under the controlled protocol;
2. the estimator contains useful information about the finite-policy recoverability margin;
3. Proposed avoids unnecessary re-instantiation under maintainable drift;
4. Proposed escalates with acceptable delay under persistent identity/architecture mismatch;
5. service–intervention trade-off is better than periodic, threshold, drift, reject-count, recent-gap, and always-open baselines over a meaningful cost range;
6. temporary corruption does not cause uncontrolled escalation;
7. behavior is not confined to one backbone/horizon;
8. all deployed identities satisfy hard deployment limits;
9. no future-service leakage or held-out tuning occurs.

If only raw MSE improves while recoverability evidence, specificity, or intervention cost fails, the central claim is not sufficiently supported.

---

## 34. First instruction to Codex

Start with **P0–P3 only**.

Do not launch the full held-out matrix.

First deliver:
```text
reports/P0_REPOSITORY_DISCOVERY.md
audits/REUSE_PROVENANCE.md
reports/P3_PHENOMENON_DIAGNOSTIC.md
```

Human/research review must approve Q1 before P4–P16 continue.
