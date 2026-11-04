# P7.4B Fit Execution Resource Adjustment 4

## Trigger

During the three-worker P7.4B Fit continuation, available physical memory was
1.47 GiB and 1.06 GiB on two consecutive scheduled checks. Workers remained
healthy, receipts continued to grow, and stderr was empty, but the predeclared
two-sample 1.5 GiB safety trigger requires a downscale.

## Procedure

Stop only the verified P7.4B Fit process tree rooted at PID 28964. Preserve and
hash-check every complete trajectory, scale, and integrity receipt, confirm no
orphan remains, and resume the identical seed-bound Phase A command with two
workers and new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 2`

The runner skips only complete hash-valid receipts. This is an execution-only
memory-safety adjustment and changes no scientific input, behavior path,
representation, scale construction, center, seed, scenario, training rule,
metric, threshold, or STOP condition.

Do not re-expand unless a later pair of stable samples again satisfies the
2.0 GiB predicted reserve and CPU limits with sufficient remaining runtime.
No Validation, final heldout, Alibaba, or P8 access is authorized here.
