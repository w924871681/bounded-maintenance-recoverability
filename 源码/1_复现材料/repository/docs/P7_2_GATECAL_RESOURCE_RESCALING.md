# P7.2 GateCal-v2 Resource Re-Scaling Record

Date: 2026-09-20 (Asia/Shanghai)

## User-authorized host cleanup

The user explicitly authorized termination of QQ Music and Weixin/WeChat-related processes and prohibited termination of other applications. Only processes with the exact names `QQMusic`, `Weixin`, and `WeChatAppEx` were stopped. No other application process was terminated.

Immediately before that cleanup, available physical memory was 4.72 GiB. Five seconds after the authorized processes ended, available physical memory was 6.47 GiB. GateCal-v2 remained healthy and had 30 complete CSV/integrity receipt pairs.

## Execution-only re-scaling decision

Because available physical memory now exceeds the prospectively recorded 6.0 GiB four-worker threshold, GateCal-v2 may be re-scaled from one worker to four workers. The current verified GateCal process tree will be stopped, all complete hash-valid receipts will be retained, and the same Git-bound entry point will be resumed with:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_2.py gatecal --workers 4`

The resumed runner validates and skips only complete receipt pairs. This operation changes wall-clock parallelism only. It does not change any center, seed, scenario, estimator, scaler, feature, target, generator, bank, threshold candidate, selection rule, cost, tie-break, denominator, or scientific stop criterion.

## Runtime guard

Monitor the parent, four children, stderr, receipt growth, and available physical memory. If available memory remains below 1.5 GiB on two consecutive checks, or worker failure repeats, stop only the verified GateCal process tree, preserve complete receipts, create another separate Git-bound recovery record, and resume at the next lower worker tier. Do not modify any previously bound file.

No ActionCal-v2, final heldout center, Alibaba data, or P8 access is authorized by this record.
