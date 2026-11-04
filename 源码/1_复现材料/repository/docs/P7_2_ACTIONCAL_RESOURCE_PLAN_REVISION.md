# P7.2 ActionCal-v2 Resource Plan Revision

Date: 2026-09-20 (Asia/Shanghai)

This execution-only record supersedes only the ActionCal-v2 launch-memory rule in `docs/P7_2_ACTIONCAL_RESOURCE_PLAN.md`. All scientific boundaries and frozen inputs remain unchanged.

## Reason for revision

GateCal-v2 demonstrated that worker count is constrained by current host memory rather than by the scientific protocol:

- Four workers launched with about 2.59 GiB available memory and reduced availability to 0.53 GiB.
- Two workers resumed after memory recovery and reduced availability to about 0.42 GiB before another receipt completed.
- One worker has remained stable, with empty stderr and continuing valid receipt growth.

Therefore, the earlier 2.5 GiB threshold for a two-worker ActionCal launch did not retain enough demonstrated headroom and is replaced by the tiered rule below.

## Revised prospective ActionCal-v2 launch rule

If and only if P7.2a passes and the gate freeze is Git-bound:

- Available memory >= 6.0 GiB: launch ActionCal-v2 with four workers.
- Available memory >= 4.0 GiB and < 6.0 GiB: launch with two workers.
- Available memory < 4.0 GiB: launch with one worker.

During a multi-worker run, if available physical memory remains below 1.5 GiB on two consecutive monitoring checks, or worker failure repeats, stop only the verified ActionCal process tree, retain all complete hash-valid receipts, create a new separate Git-bound recovery record, and resume at the next lower worker tier. No already bound file may be modified.

This rule changes wall-clock parallelism only. Per-task deterministic seeds, receipt validation, centers, scenarios, configurations, thresholds, estimators, costs, tie-breaks, and denominators remain identical.
