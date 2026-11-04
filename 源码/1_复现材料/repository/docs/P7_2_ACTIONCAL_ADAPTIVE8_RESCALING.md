# P7.2 ActionCal-v2 Adaptive Eight-Worker Re-Scaling

Date: 2026-09-20 (Asia/Shanghai)

## Observation

ActionCal-v2 was launched with four workers under parent PID 36308. After causal-prefix/reference construction, all four workers were active with:

- approximately 0.404 GiB private memory per worker;
- approximately 1.61 GiB aggregate worker private memory;
- approximately 3.88 GiB available physical memory;
- approximately 44% total CPU utilization;
- empty stderr and healthy worker processes;
- zero complete ActionCal trajectory receipts at the measurement point.

## Derived decision

Adding four workers predicts approximately 1.62 GiB additional private memory, leaving approximately 2.26 GiB available, above the 2.0 GiB reserve. Linear CPU projection is approximately 88%, below the 90% target. With 144 trajectories still incomplete, expected remaining runtime justifies the process-pool restart cost.

The verified four-worker ActionCal process tree will therefore be stopped and the same Git-bound entry point resumed with:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_2.py actioncal --workers 8`

Only complete hash-valid receipts are resumable. No complete receipt existed at the decision point; any in-flight partial computation is discarded and deterministically recomputed by the same frozen runner.

## Guard

Monitor eight child workers, stderr, valid receipt growth, CPU utilization, and available memory. If available memory remains below 1.5 GiB on two consecutive checks, or worker/resource failure repeats, stop only the verified ActionCal process tree, preserve complete receipts, create a new separate Git-bound recovery record, and resume at a lower derived worker count.

This changes wall-clock parallelism only. The selected gate, action grid, lifecycle costs, estimator/scaler, feature set, generator, bank, center/seed/scenario pool, tie-breaks, denominators, and scientific stop criteria remain frozen. Final heldout centers, Alibaba data, and P8 remain prohibited.
