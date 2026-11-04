# P7.2 ActionCal-v2 Initial Resource Launch

Date: 2026-09-20 (Asia/Shanghai)

## Gate prerequisite

GateCal-v2 completed all 144 trajectory/receipt pairs. `gate-finalize` returned `PASS`, selected `delta_2` with `delta_R = -0.000272181217042075`, generated a matching SHA-256 gate freeze, and committed the freeze as `afe84e45e008de79495ea46e370469c4de12243a`. Heldout, Alibaba, and ActionCal data had not been accessed at gate finalization.

## Initial ActionCal execution decision

Available physical memory after GateCal completion was approximately 6.8 GiB and CPU utilization was approximately idle. ActionCal-v2 will begin with four workers as a conservative measurement launch. GateCal's per-worker footprint is not assumed to apply to ActionCal.

After initial complete hash-valid ActionCal receipts are produced, the monitor will measure ActionCal-specific per-worker private memory, CPU-core demand, total CPU utilization, stderr, worker health, and receipt throughput. It will then apply `docs/P7_2_ADAPTIVE_WORKER_SCALING.md` to decide whether a restart at a higher or lower worker count is justified by remaining runtime.

The command is:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_2.py actioncal --workers 4`

This is an execution-only decision. It does not alter the selected gate, action grid, lifecycle costs, estimator/scaler, feature set, generator, bank, center/seed/scenario pool, tie-breaks, or scientific stop criteria. Final heldout centers, Alibaba data, and P8 remain prohibited.
