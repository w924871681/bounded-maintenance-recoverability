# P7.4B Fit Execution Resource Adjustment 2

## Trigger

This is an execution-only safety correction during P7.4B Phase A. The
three-worker continuation remained scientifically healthy and produced
matching trajectory, scale, and integrity receipts with empty stderr, but
available physical memory measured 1.10 GiB and 1.20 GiB on two consecutive
checks. This crosses the predeclared 1.5 GiB downscale trigger.

## Procedure

Stop only the verified P7.4B Fit process tree rooted at PID 29416. Preserve and
hash-check every complete receipt. Resume the identical seed-bound command at
two workers with new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 2`

The runner skips only complete hash-valid receipts and recomputes interrupted
receipt-less work. This change affects wall-clock execution only. It does not
change the frozen behavior path, representations, scale construction, centers,
seeds, scenarios, training, metrics, thresholds, or STOP rules.

Do not re-expand while the current external-memory condition persists. No
Validation, final heldout, Alibaba, or P8 access is authorized by this record.
