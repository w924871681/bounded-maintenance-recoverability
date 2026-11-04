# P7.4B Fit Execution Resource Adjustment 3

## Trigger and scope

This is an execution-only rescaling during P7.4B Phase A. After the prior
low-memory condition cleared, two consecutive monitoring samples measured
2.64 GiB and 3.10 GiB available physical memory with two healthy workers,
empty stderr, and growing hash-valid receipts. Each active worker used about
0.46--0.47 GiB private memory.

Adding one worker predicts at least approximately 2.17 GiB available memory
across the two samples and remains well below 90% occupancy of 14 physical
cores. Adding two workers does not satisfy the reserve on both samples.
Therefore three workers is the largest currently authorized count. With 222
of 288 Fit trajectories remaining, the expected saved runtime exceeds restart
cost.

## Procedure

Stop only the verified P7.4B Fit process tree rooted at PID 3608, preserve and
hash-check all complete trajectory, scale, and integrity receipts, confirm no
orphan remains, and resume the identical seed-bound command with new logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 3`

The runner skips only complete hash-valid receipts. This adjustment changes
wall-clock execution only and does not change any scientific degree of
freedom. Downscale again if available memory is below 1.5 GiB on two
consecutive checks or resource failure repeats. No Validation, final heldout,
Alibaba, or P8 access is authorized by this record.
