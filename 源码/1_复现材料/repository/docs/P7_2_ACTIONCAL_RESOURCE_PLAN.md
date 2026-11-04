# P7.2 ActionCal-v2 Execution Resource Plan

Date: 2026-09-20 (Asia/Shanghai)

## Purpose

This record corrects an overly conservative wall-clock estimate for P7.2 and prospectively records an execution-only resource plan for ActionCal-v2. It does not modify the scientific protocol, any frozen parameter, the estimator, the scaler, the feature set, the generator, the model/source bank, the center pools, the seven-point gate grid, tie-break rules, lifecycle costs, or stop criteria.

## Evidence-based workload comparison

- The completed original P7 materialized 240 trajectories and evaluated 120 action configurations, for 28,800 trajectory-configuration units.
- P7.2 ActionCal-v2 is specified to materialize 144 trajectories and evaluate 102 action configurations, for 14,688 trajectory-configuration units.
- The nominal ActionCal-v2 workload is therefore 14,688 / 28,800 = 0.51 of original P7.
- The original P7 receipt span was approximately 21.08 hours and was executed predominantly with four workers, with interruptions and recovery overhead.
- A one-worker ActionCal-v2 projection of roughly 35-45 hours is plausible, but a 50-70 hour projection is not supported by this workload-normalized comparison.
- At two workers, the workload-normalized projection is approximately 21.5 hours before machine-state variation; the operational planning interval is 18-26 hours.

## GateCal-v2 disposition

GateCal-v2 remains on the current one-worker run. It is already progressing with hash-valid receipts, and another interruption would provide limited benefit relative to its remaining duration.

## Prospective ActionCal-v2 resource rule

If and only if P7.2a passes, the gate selection is frozen and Git-bound, and no scientific, leakage, fairness, or hash check fails:

1. Start ActionCal-v2 with two workers only when available physical memory is at least 2.5 GiB immediately before launch.
2. Preserve per-task deterministic seed binding and the existing complete-receipt resume behavior.
3. Monitor the parent, two children, stderr, valid receipt growth, and available memory.
4. If available physical memory remains below 1.0 GiB on two consecutive checks, or a worker failure repeats, stop the verified ActionCal process tree, preserve all complete hash-valid receipts, create a new separate Git-bound recovery record, and resume with one worker.
5. Do not alter or append to any already hash-bound file.

## Corrected wall-clock expectation

- GateCal-v2 from the 2026-09-20 21:51 checkpoint: approximately 5 hours remaining, followed by roughly 5-15 minutes for gate finalization and audit.
- If P7.2a fails: P7.2 stops after that finalization.
- If P7.2a passes and ActionCal-v2 can use two workers: approximately 18-26 additional hours.
- Corrected end-to-end expectation from the checkpoint: approximately 23-31 hours, not two to three days.
- If memory forces a one-worker fallback, the honest contingency becomes approximately 40-50 hours total from the checkpoint.

## Scientific boundary

This plan changes wall-clock parallelism only. It does not authorize final heldout centers 33000-33019, Alibaba data, P8, parameter reselection, new thresholds, new trajectories outside the frozen P7.2 pools, or any modification of the P7/P7.1 verdicts.
