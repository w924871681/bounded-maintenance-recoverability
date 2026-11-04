# P7.4B Fit Execution Resource Adjustment

## Scope

This is an execution-only adjustment made during P7.4B Phase A. It does not
change any scientific input, center, seed, scenario, behavior path,
representation, scale rule, estimator, metric, threshold, or STOP condition.

## Observed state before adjustment

- Original command: `C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 2`
- Parent PID: `16696`
- Launch time: 2026-09-21 19:18:14 Asia/Shanghai
- Complete hash-valid Fit trajectories: 12 of 288
- Matching trajectory, scale, and integrity receipts: 12 each
- Parent private memory: approximately 0.42 GiB
- Worker private memory: approximately 0.45 and 0.47 GiB
- Available physical memory: 2.46 GiB at the decision check
- Both workers were CPU-active and stderr was empty.

At the observed mean worker footprint, a third worker predicts approximately
2.00 GiB remaining available memory. Three workers remain well below the
frozen execution controller's 90% limit for 14 physical cores. With 276
trajectories remaining, the expected runtime reduction exceeds restart cost.

## Authorized procedure

Stop only the verified P7.4B Fit process tree rooted at PID 16696. Preserve all
complete CSV, scale, and integrity receipts. Confirm that no process from that
tree remains. Resume the identical seed-bound Phase A entry point as:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 3`

with new timestamped stdout and stderr logs. The runner may skip only complete
hash-valid receipts. It must recompute any interrupted, receipt-less task.

Scale down if available memory remains below 1.5 GiB on two consecutive
checks or a resource/worker failure repeats. No further expansion is justified
without new stable measurements satisfying the same reserve and CPU limits.

No Validation, final heldout, Alibaba, or P8 access is authorized by this
record.
