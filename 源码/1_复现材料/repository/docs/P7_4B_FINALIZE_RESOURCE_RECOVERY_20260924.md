# P7.4B Finalize Resource Recovery — 2026-09-24

## Trigger

After the user explicitly resumed P7.4B, the eight intermediate output files
matched the SHA-256 values in `P7_4B_FINALIZE_USER_PAUSE_20260924.md` exactly.
There was no matching P7.4B process; all 288 Validation
trajectory/scales/integrity receipts passed SHA-256 and every-stage A0/A1
parent-state hash, action, post-action identity, and path-hash equality checks;
the frozen preflight passed. Available physical memory was approximately
3.13 GiB before launch.

The exact frozen `scripts/run_p7_4b.py finalize` command was started with PID
22056 at 2026-09-24 14:28:27 Asia/Shanghai. Its stderr remained empty and
CPU work continued, but available physical memory measured 1.479 GiB,
1.499 GiB, then 0.995 GiB on successive checks. This crossed the established
two-sample 1.5 GiB resource stop threshold. Only the verified finalize process
PID 22056 was stopped; no matching P7.4B process remained. No other
application was touched. Available memory remained about 1.08–1.20 GiB after
the stop, showing that the low-memory condition was not solely the finalize
process's footprint.

The 288 Fit and 288 Validation complete receipts remain on disk. All eight
intermediate output file hashes still match the prior pause record. The frozen
script had not produced `leave_one_center_out.csv`, the final report, or the
final scientific audit. There is no P7.4B scientific PASS/FAIL verdict yet.
Any in-memory leave-one-center-out bootstrap work was lost at the process
stop; this record does not claim an intermediate scientific result.

## Deferred execution-only recovery

Keep P7.4B finalization stopped while memory is low. Monitor available memory
without closing WeChat/Weixin, QQMusic, or any other application. The observed
pre-to-post-launch decline was about 2.1 GiB. Conservatively reserve 0.8 GiB
for the finalize process, this observed external fluctuation, and at least
1.5 GiB remaining: require two stable pre-launch samples, separated by at
least one fifteen-minute heartbeat, of **at least 4.5 GiB available memory**
before another launch. This margin is an execution resource condition only;
it does not change any scientific input or STOP rule.

Before relaunch, verify no matching P7.4B process or orphan, all 288 complete
Validation receipts and stagewise path equality, frozen preflight, and the
intermediate-file hashes in the prior pause record. Relaunch only the exact
frozen `C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py finalize`
command with new timestamped logs. Monitor memory and stderr immediately
after launch and stop only the verified P7.4B process if the resource stop
threshold recurs. Do not silently retry scientific, leakage, pairing, scale,
or hash failures. Do not access final heldout centers 33000–33019, Alibaba,
or P8. The frozen P7.2 Proposed behavior path and all scientific parameters
remain unchanged.
