# P7.4B Validation Execution Resource Adjustment 4

## Prospective execution decision

The resumed, seed-bound P7.4B Validation materialization was running with one
worker under parent PID 5708 on 2026-09-23 (Asia/Shanghai). Its stderr was empty,
the parent and one child were healthy, and complete receipts continued to grow.
At least 33 of 288 Validation trajectories had complete receipts at the time of
this decision. No scientific configuration is changed by this adjustment.

Two fresh stable in-phase samples, 12 seconds apart, measured 5.182 GiB and
5.162 GiB available physical memory. The resident parent used 0.319 GiB
private memory and the worker used 0.462 GiB. The worker consumed 24.02 CPU
seconds in 12 seconds, approximately two physical cores. Conservatively
charging 0.6 GiB for each added worker, five additional workers predict
5.162 - 5(0.6) = 2.162 GiB available memory. Six workers predict about
12 occupied physical cores, below 90% of 14 physical cores (12.6). A seventh
would exceed the CPU limit. With more than 250 trajectories remaining, the
expected runtime saving exceeds one restart. Six is therefore the derived
execution count, conditional on final process and receipt checks.

## Required procedure

Stop only the verified P7.4B Validation tree rooted at PID 5708. Preserve and
SHA-256-check every completed trajectory/scales/integrity receipt and verify
the stagewise A0/A1 parent-state hash, action, post-action identity, and path
hash equality. Confirm no matching parent or orphan worker remains. Then
resume the identical seed-bound command with six workers and new timestamped
stdout/stderr logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py validation-materialize --workers 6`

The runner may skip only complete hash-valid receipts. Check process health,
stderr, CPU and available memory immediately after restart. Stop only the
P7.4B tree if available memory is below 1.5 GiB on two consecutive checks,
or if resource/worker failure repeats. Never terminate, close, or otherwise
interfere with WeChat, QQMusic, or another application. Any further resize
requires its own separate Git-bound execution record.

This adjustment is wall-clock execution only. The frozen P7.2 Proposed
behavior path, A0/A1 observational representations, centers, seeds, scenarios,
Fit pipelines, scales, metrics, thresholds, stop criteria, and output scope
remain unchanged. No final heldout, Alibaba, or P8 access is authorized.
