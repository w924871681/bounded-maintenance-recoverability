# P7.4B Validation Execution Resource Adjustment 2

## Trigger

The three-worker P7.4B Validation continuation crossed the frozen low-memory
trigger. Available physical memory first fell to 0.56 GiB. Weixin/WeChat had
reopened and was stopped under the user's standing authorization; no other
application was touched. Two subsequent samples still measured only 1.02 GiB
and 0.93 GiB, both below the 1.5 GiB contraction threshold. All three workers
remained CPU-active and stderr was empty, so this is an execution-only resource
condition rather than a scientific failure.

## Procedure

Stop only the verified P7.4B Validation process tree rooted at PID 6616.
Preserve and hash-check all complete trajectory, scale, and integrity receipts,
and confirm that no matching parent or orphan worker remains. Resume the
identical seed-bound command conservatively with one worker and new timestamped
logs only when fresh post-stop memory measurements support safe execution:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py validation-materialize --workers 1`

The runner skips only complete hash-valid receipts. This adjustment changes
wall-clock execution only and modifies no frozen behavior path, A0/A1
representation, center, seed, scenario, Fit pipeline, scale, metric, threshold,
or STOP rule. Any later resize requires another separate Git-bound execution
record. No final heldout, Alibaba, or P8 access is authorized.
