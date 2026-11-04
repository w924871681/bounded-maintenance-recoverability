# P7.2 Adaptive Worker Scaling Protocol

Date: 2026-09-20 (Asia/Shanghai)

## Scope

This is an execution-only resource controller for the already frozen P7.2 GateCal-v2 and, only after P7.2a PASS and gate freeze, ActionCal-v2. It changes process parallelism and wall-clock duration only. It does not change scientific inputs, outputs, denominators, seed binding, receipt validation, or any frozen decision rule.

## Current GateCal observation

After the user-authorized termination of QQ Music and Weixin/WeChat processes, GateCal-v2 ran stably with four workers:

- 14 physical cores and 20 logical processors;
- 5.04-5.06 GiB available physical memory across three samples;
- 44-48% total CPU utilization;
- five Python processes (one parent plus four workers);
- 2.04 GiB aggregate Python private memory;
- approximately 0.44-0.45 GiB private memory per worker;
- empty stderr;
- 63 complete hash-valid receipts at the observation endpoint.

Each worker had accumulated CPU time at about 1.8 times wall time, indicating that numerical-library threading makes CPU capacity, rather than memory, the first expected saturation constraint.

## Adaptive computation

For a healthy multi-worker run, estimate:

- `m_worker`: upper observed per-worker private memory, rounded upward;
- `c_worker`: observed per-worker CPU-core demand;
- `M_available`: current available physical memory;
- `C_physical`: physical CPU-core count;
- memory reserve: 2.0 GiB;
- target CPU occupancy: at most 90% of physical-core capacity.

The next worker count is the largest positive integer satisfying both:

1. predicted available memory after expansion remains at least 2.0 GiB; and
2. predicted aggregate worker CPU demand remains at most 90% of physical-core capacity.

Scale upward only when stderr is empty, valid receipts are growing, no worker has failed, and the expected remaining runtime exceeds the restart cost. Resize by stopping only the verified phase process tree and resuming the same seed-bound entry point; complete hash-valid receipts are retained and skipped.

Scale downward when available memory remains below 1.5 GiB on two consecutive checks, stderr shows a resource/worker failure, or valid receipt growth stalls while workers are unhealthy. Every resize requires a new separate Git-bound execution record; no previously bound file may be modified.

## Current derived decision

At four workers, the memory constraint permits approximately ten workers while retaining the reserve, but the CPU constraint permits approximately seven to eight workers. Therefore GateCal-v2 will be resumed with eight workers. Counts above eight are not justified by the current hardware measurements and are expected to increase scheduling and numerical-thread contention.

For ActionCal-v2, the controller must re-measure its own worker memory and CPU demand after initial valid receipt production; it must not assume GateCal's per-worker footprint. ActionCal may scale to a different count if its measured resource profile warrants it.

## Scientific boundary

No final heldout centers, Alibaba data, or P8 are authorized. P7 PASS, P7.1, the P7.2 prospective amendment, center pools, estimator/scaler, feature set, generator and bank, gate grid, tie-breaks, lifecycle costs, and stop rules remain immutable.
