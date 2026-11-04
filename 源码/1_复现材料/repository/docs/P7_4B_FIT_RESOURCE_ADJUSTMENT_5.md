# P7.4B Fit Execution Resource Adjustment 5

## Trigger

After the required downscale to two workers, available physical memory was
only 0.38 GiB and 0.48 GiB on two consecutive checks. This is materially below
the 1.5 GiB safety threshold. Stderr remained empty, but continuing with two
workers would violate the frozen adaptive execution controller.

## Procedure

Stop only the verified P7.4B Fit process tree rooted at PID 32196. Preserve
and hash-check all complete trajectory, scale, and integrity receipts, confirm
no orphan remains, and resume the identical seed-bound command with one worker
and new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 1`

The runner skips only complete hash-valid receipts. This is an execution-only
memory-safety change. It modifies no scientific input, behavior path,
representation, center, seed, scenario, scale, training, metric, threshold,
or STOP rule.

Do not expand until at least two later stable samples satisfy the 2.0 GiB
predicted post-expansion reserve. No Validation, final heldout, Alibaba, or P8
access is authorized here.
