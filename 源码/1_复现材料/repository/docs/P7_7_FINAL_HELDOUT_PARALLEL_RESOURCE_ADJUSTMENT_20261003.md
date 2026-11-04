# P7.7 Final-heldout Controlled Parallel Resource Adjustment

Status: execution-only adjustment; scientific protocol and all frozen parameters unchanged.

## Prior execution stop

- Prior attempt: `p7_7_final_20261003_142433`.
- Command: `python -u scripts/run_p7_7_final.py --final-heldout`.
- Stop reason: user-authorized controlled worker parallelization because serial throughput was too slow; this was not a scientific, integrity, leakage, or resource failure.
- Verified process tree: only the P7.7 final-heldout Python process was stopped; no other application was touched.
- Valid completed trajectories preserved: `239/1200`.
- Valid-failure count at stop: `0`.
- One incomplete P7.7 claim was preserved under `results/p7_7/interrupted_claims/attempt_p7_7_final_20261003_142433/`.
- All completed trajectory CSVs and integrity receipts remain unchanged and are resumed only after hash validation.
- The 239 preserved receipts retain the prior serial execution binding pair
  (`protocol_hash=8785dc1e…d15838d`, `runner_hash=20c0a354…e43ec5`); this exact pair is
  explicitly compatibility-allowlisted for this recovery. All method, center, seed,
  scenario, implementation, output, row-count, and access-guard fields remain mandatory.

## Controlled resume

- The resume command is `python -u scripts/run_p7_7_final.py --final-heldout --workers auto`.
- `auto` takes two fresh host-memory samples 10 seconds apart, reserves 2 GiB for the host,
  budgets 1 GiB per worker, and caps occupancy at 90% of physical cores (2 cores/worker).
  It resolves one fixed worker count for this execution; it does not resize live.
- If a later resource adjustment is justified, stop only the verified P7.7 tree, preserve and
  validate receipts, add a new Git-bound execution record, and launch a new phase-level count.
- Each worker uses the exact same `run_one(..., allow_final=True)` scientific implementation, frozen model artifacts, centers, seeds, scenarios, methods, thresholds, candidate bank, endpoint, and statistical plan.
- Tasks are independent by `(method, center, seed, scenario)`; outputs are written to unique atomic receipt paths.
- Existing valid receipts are never rerun. Missing tasks are restarted canonically; no partial claim is treated as a completed trajectory.
- The parent process alone updates `results/p7_7/execution_status.json` and writes receipts after validating returned 24-stage output.
- No final-heldout center outside `33000–33019`, Alibaba, or P8 is accessed.

## Safety and scientific invariants

- This is a procedural execution adjustment only; no scientific branch, threshold, A1 scaler, A1 estimator, candidate bank, cost, endpoint, comparator, or statistical parameter changes.
- The final authorization manifest remains the authority for the exact final population and frozen source hashes.
- The adjustment does not add trajectories: the final population remains exactly `20*3*4*5 = 1200`.
- On any worker or integrity failure, preserve evidence and stop; do not silently retry a corrupted result.
