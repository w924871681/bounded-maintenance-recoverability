# P7 execution-only resource scaling record

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run and monitor
- Verification Status: ANALYZED (execution environment only)
- Date: 2026-09-19 Asia/Shanghai

## Reason for the change

The seed-bound P7 run used one trajectory worker. The first trajectory reached stage 14 after 870.3 seconds, with 11 distinct deployed-parent states, implying roughly 22–25 minutes per 24-stage trajectory and approximately 3.7–4.2 days for all 240 trajectories. This was a wall-clock execution bottleneck, not an inherent requirement of the frozen scientific design.

At the decision point, no complete closed-loop trajectory CSV or integrity receipt existed. Only the already-completed common calibration reference and numeric B4 threshold artifacts had been persisted. The one-worker parent PID 27372 and its worker PID 32552 were stopped before any formal trajectory result was committed. No completed outcome was deleted, selected, filtered, or inspected to choose the scaling factor.

The host exposed 20 logical processors and approximately 5.79 GiB free physical memory. One P7 worker used two Torch threads and approximately 0.45 GiB working/private model memory. Four independent trajectory workers therefore remain below half of the logical-CPU capacity and within the observed memory margin. The execution command is changed only from `--workers 1` to `--workers 4`.

## Scientific invariants

This is an execution-only parallelization change. It does not alter:

- calibration centers 32000–32019, the three model seeds, or C0/C1/C3/C4;
- any P6 estimator/scaler weights, KS2/KL6 features, response event, H_R=4, eta=.25, or B50;
- the seven delta candidates, lifecycle-cost grid, baseline grids, false-escalation cap, fallback, or selection criterion;
- generator, eleven-identity bank, deployment filter, candidate count, SGD operator, update count, assessment visibility, action semantics, or tie-breaking;
- Torch/NumPy seed binding, state/history reset semantics, causal data roles, offline-oracle isolation, or source-candidate hashes;
- P3.2b FAIL history or the secondary-only interpretation of C4;
- heldout/Alibaba/P8 prohibition.

Each trajectory is deterministic and isolated by center, seed and scenario. The seed-bound wrapper restores Torch RNG state per adaptation call, so task scheduling order cannot change model states or actions. Each output path belongs to exactly one trajectory; the runner writes a CSV and integrity receipt only after all 24 stages complete. Existing common reference/threshold files are immutable and shared read-only by workers.

## Runtime interpretation

All formal trajectory records after this point are produced under a four-worker environment; none was completed under the earlier one-worker attempt. `decision_runtime_actual_s` is actual elapsed executor time under this concurrent calibration environment and must be reported with that context. It is suitable for within-run descriptive burden comparisons, not an exclusive-core hardware benchmark. Deterministic search-candidate/update counts and the separately charged standalone-operation estimate remain the primary cross-method computational-burden measures.

Expected wall-clock duration is approximately 24–36 hours, subject to scenario-dependent parent branching and host contention. The ETA must be recalibrated from completed four-worker trajectory receipts rather than asserted from the abandoned one-worker partial trajectory.

This document and its supplemental manifest are Git-bound before restarting closed-loop materialization. The original P7 preregistration and RNG-binding manifests remain unchanged.
