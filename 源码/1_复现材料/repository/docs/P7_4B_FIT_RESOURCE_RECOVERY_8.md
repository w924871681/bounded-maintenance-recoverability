# P7.4B Fit Execution Resource Recovery 8

## Trigger

The six-worker P7.4B Fit continuation rooted at PID 9980 stopped on
2026-09-22 after materializing 272 of 288 trajectories. Its stderr recorded a
`concurrent.futures.process.BrokenProcessPool` failure: one worker process was
terminated abruptly while work was running or pending. No matching P7.4B
parent or child process remained when recovery was assessed on 2026-09-23.

This is treated as a resource/worker failure, not as a scientific result. The
existing frozen behavior path, A0/A1 representations, center assignment,
seeds, scenarios, scales, models, metrics, thresholds, and STOP rules remain
unchanged.

## Preserved state and recovery checks

Exactly 272 trajectory CSVs, 272 scale CSVs, and 272 integrity receipts were
present under `results/p7_4b/raw/fit`. A read-only audit verified all 272
trajectory and scale SHA-256 values against their receipts, 24 stages per
trajectory, the receipt path-pairing flag, and stagewise equality of A0/A1
parent-state hash, action, post-action identity, and post-action path hash.
There were zero failures. The seed-bound entry-point preflight also passed.

No P7.4B Fit freeze, Validation opening, Validation outcome, final heldout,
Alibaba, or P8 access occurred.

## Resource gate and authorized continuation

Available physical memory was 0.78 GiB at recovery assessment. Under the
user's standing authorization, only Weixin/WeChat-related processes were
stopped; no other application was touched. Available memory then measured
1.20 GiB, still below the 1.5 GiB stop threshold and insufficient for a safe
one-worker restart while retaining the required reserve.

Therefore no process is launched by this record. Once fresh stable
measurements support the required memory reserve, resume the identical
seed-bound command conservatively with one worker and new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 1`

Before launch, confirm that no P7.4B process or orphan worker is active and
that all 272 preserved receipts remain hash-valid. The runner may skip only
complete hash-valid receipts. Any later resize requires a new, separate
Git-bound execution record. No scientific file is modified by this recovery.
