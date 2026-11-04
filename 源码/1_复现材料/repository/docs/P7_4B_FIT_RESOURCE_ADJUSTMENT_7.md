# P7.4B Fit Execution Resource Adjustment 7

## Trigger and derived count

With four healthy P7.4B Fit workers, two consecutive checks measured 4.95 GiB
and 4.83 GiB available physical memory. Worker private memory was 0.45--0.53
GiB, receipts grew normally, and stderr was empty.

Six total workers are the largest count allowed by the CPU controller: at an
observed demand of roughly two physical cores per worker, six workers predict
about 12 occupied cores, below 90% of 14 physical cores. Adding two workers
also predicts more than 3.7 GiB available memory using the conservative
sample, above the 2.0 GiB reserve. With 112 Fit trajectories remaining, the
expected runtime saving exceeds restart cost.

## Procedure

Stop only the verified P7.4B Fit process tree rooted at PID 25564. Preserve
and hash-check all complete trajectory, scale, and integrity receipts, confirm
no orphan remains, and resume the identical seed-bound command with six
workers and new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 6`

The runner skips only complete hash-valid receipts. This changes wall-clock
execution only and leaves every scientific degree of freedom unchanged.
Downscale if two consecutive samples fall below 1.5 GiB or resource failure
repeats. No Validation, final heldout, Alibaba, or P8 access is authorized.
