# P7 execution-only resume record — 2026-09-20

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Verification Status: ANALYZED (procedural recovery only, not P7 scientific outcome)

At 2026-09-20 02:54 Asia/Shanghai, monitoring found that the Git-bound four-worker parent process PID11924 and all of its child workers were no longer present. The corresponding stderr log remained empty. The last stdout write was at 02:52, so this was treated as an unreported execution stop rather than a scientific, leakage, fairness, or hash failure.

Before resumption, `results/p7/execution_status.json` reported 70 of 240 trajectories complete. The raw directory contained exactly 70 trajectory CSVs and 70 matching integrity receipts; none were removed or rewritten. The status also continued to record `heldout_accessed=false`, `alibaba_accessed=false`, and `estimator_modified=false`. The seed-bound preflight reverified the original and supplemental execution hashes successfully.

An initial documentation attempt appended this event to the already hash-bound `docs/P7_EXECUTION_RECOVERY.md`. The seed-bound entry point correctly rejected that launch before trajectory execution with `supplemental execution hash mismatch: docs/P7_EXECUTION_RECOVERY.md`. The bound document was restored byte-for-byte, and this separate record was created instead. The rejected process generated no trajectory outcome and made no change to the 70 valid receipts.

Recovery uses the same command and concurrency already bound by `audits/P7_EXECUTION_RESOURCE_SCALING.json`:

```text
C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_seed_bound.py run --workers 4
```

Only a new timestamped stdout/stderr pair and a new operating-system process identifier are introduced. The runner must validate and skip the 70 complete receipt-bound trajectories, then continue the remaining frozen matrix. No generator, source bank, estimator, scaler, feature, response definition, center pool, scenario role, threshold, grid, update budget, seed, or scientific claim is changed.
