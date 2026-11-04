# P7.4B finalization: audited vectorized-CPU recovery (2026-09-26)

## Scope and reason

The GPU execution-only path committed at `d79964a` stopped when a CUDA worker
crashed inside `nvcuda64.dll`, as recorded at `871931c` in
`P7_4B_GPU_FINALIZE_DRIVER_STOP_20260926.md`. The user has subsequently
explicitly authorized repairing the execution and continuing to completion.
This document is an execution-only, post-outcome recovery amendment, frozen
before its formal run. It is not a changed scientific protocol or a new
Validation opening. The original `scripts/run_p7_4b.py`, all raw Fit and
Validation receipts, representation/behavior paths, center assignment,
bootstrap seed 2904, 4,000 resamples, paired intervals, decision rules, and
claim boundary remain unchanged.

The new runner reuses only complete, provenance-checked, SHA-256-valid GPU
checkpoints: one main plus 17 leave-one-center-out (LOO) sets. The seven
missing LOO sets use the identical frozen NumPy RNG center draws and the
algebraically equivalent vectorized center-statistic aggregation on one
logical CPU. Each newly completed set receives a separate atomic JSON
checkpoint and SHA-256 sidecar under
`results/p7_4b/cpu_recovery_checkpoints/`. There is no CUDA use in this
recovery runner. It still calls the unmodified frozen `finalize()` for all
other computations, audits, report generation, verdict, and Git commit.
Any incomplete, mismatched, or duplicate-provenance checkpoint is a STOP.

Bound execution code:

| File | SHA-256 |
| --- | --- |
| `scripts/run_p7_4b_cpu_recovery.py` | `45f408fc3207787193b1ca356bf1be2380c6c0535b03801c89762d11063fc647` |
| `scripts/run_p7_4b_cpu_recovery_supervisor.py` | `619d4ad0678108f53a1cddee35669d0c6c745e45953567635ffd7cd0dc14a235` |

## Recovery integrity gate

The failed GPU finalizer had already rewritten exactly two previously
persisted intermediate files: `paired_a1_vs_a0.csv` and
`paired_bootstrap_samples.csv`. The other six paused intermediate file hashes
still matched `P7_4B_FINALIZE_USER_PAUSE_20260924.md`. The two rewritten
files were not treated as the old frozen bytes: their schema, all 4,000
sample values, paired point estimates, bootstrap seed/count, and confidence
intervals were checked against the complete, hash-valid GPU main checkpoint
and freshly regenerated frozen Validation predictions. All 288 Validation
trajectory/scales/integrity receipts and stagewise A0/A1 path equality were
reloaded by the frozen `load_pool()` during recovery verification.

The 2026-09-26 supervised verification passed before this amendment was
bound. The new CPU-vectorized 4,000-draw main output differed from the valid
GPU main checkpoint by at most `4.44e-16`; all 17 completed 4,000-draw LOO
GPU checkpoints were likewise compared replicate by replicate within the
predeclared `1e-12` tolerance. Each of the seven missing LOO cases passed an
eight-draw replicate comparison with the original serial CPU bootstrap.
The previous GPU verification had compared all 4,000 main draws to the
pre-GPU original serial CPU CSV, with maximum difference `5.27e-16`.
These checks establish numerical equivalence, not bitwise identity.
Verification log: `results/p7_4b/cpu_recovery_verify_20260926_225607_*`;
stderr was empty.

## Faulty-fan resource boundary

The user reports the fan is still faulty but authorizes a guarded run. The
runner pins itself to one logical CPU and below-normal priority. A separate
Windows Job Object supervisor monitors process liveness, available memory,
and the only accessible thermal sensor (GPU temperature) every two seconds.
It fails closed at GPU temperature 75 C or failed GPU sensor, at two memory
samples below 1.5 GiB, or at a 45-minute hard timeout. Launch requires two
memory readings at least ten seconds apart at or above 2.3 GiB. **CPU
temperature remains unobservable; this software monitor cannot guarantee
whole-machine thermal safety.** In the short recovery verification the GPU
temperature peaked at 52 C and available memory remained above 4.047 GiB.
If physical heat, smell, or fan behavior becomes concerning, stop the run.
No WeChat/Weixin, QQMusic, or any unrelated process may be altered.

## Exact command and terminal gate

After this amendment and both scripts are Git committed, verify no P7.4B
Python process is active and run only:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b_cpu_recovery_supervisor.py run --stop-c 75 --launch-memory-gib 2.3 --min-memory-gib 1.5 --interval-seconds 2 --timeout-minutes 45`

On scientific, pairing, scale, hash, or execution failure, STOP and preserve
evidence; do not silently retry or alter bound scientific files. On success,
verify every required output, final audit/manifest SHA-256, no heldout
centers 33000–33019/Alibaba/P8 access, final Git commit, and the honest
P7_4B_PASS or P7_4B_FAIL. Then stop for human scientific review.
