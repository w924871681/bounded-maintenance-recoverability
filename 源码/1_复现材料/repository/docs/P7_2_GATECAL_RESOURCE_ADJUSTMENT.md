# P7.2 GateCal-v2 Execution Resource Adjustment

## Event

GateCal-v2 was launched at 2026-09-20 21:08:11 Asia/Shanghai from the Git-bound entry point `scripts/run_p7_2.py gatecal --workers 4` under parent PID 12124. Four child workers loaded concurrently. Available physical memory declined from 2.59 GiB before launch to 0.80 GiB and then 0.53 GiB. The parent and all five descendants were explicitly identified and stopped before an operating-system out-of-memory failure.

At stop time, exactly four complete trajectory CSVs and four matching integrity receipts existed in `results/p7_2/raw/gatecal`. No incomplete file is accepted by the runner, and no completed file was deleted. After the process tree stopped, available memory recovered to 2.25 GiB.

## Authorized procedural recovery

Execution resumes from the same frozen P7.2 entry point with `--workers 2`. The runner validates and skips only CSVs with matching integrity receipts. The change affects wall-clock parallelism only. It does not change center IDs, seeds, scenarios, P50 GateCal path, estimator/scaler/features, oracle target, delta candidates, selection metric, tie-break, stop criteria, generator, source/model bank or any scientific denominator. No held-out, Alibaba, ActionCal-v2 or P8 data were accessed.

