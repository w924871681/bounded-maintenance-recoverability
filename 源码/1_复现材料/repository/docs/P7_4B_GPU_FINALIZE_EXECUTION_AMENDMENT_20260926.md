# P7.4B GPU finalization — execution-only amendment (2026-09-26)

## Status and provenance

This is a post-outcome, execution-only optimization requested by the user
after the 2026-09-24 user pause. It is frozen **before** a new finalization
attempt. It is not a new scientific protocol, a new Validation opening, or a
claim that GPU and CPU implementations are bitwise identical. The existing
`scripts/run_p7_4b.py` and all P7.4B scientific inputs remain unchanged.
Fit and Validation materialization are each complete at 288/288. There is no
final report, final scientific audit, or P7.4B verdict yet. The prior
partially completed leave-one-center-out work lived only in RAM and cannot be
recovered. No process from that run remains.

The only permitted change is to compute the same frozen paired-bootstrap
statistics by precomputing each center's Spearman, TPR, and TNR once, drawing
the same 4,000 center-resample sequences with seed 2904, and performing the
per-resample center aggregation on the CUDA GPU. The frozen finalizer still
loads and audits the 288 raw Validation receipts, generates predictions and
other metrics, applies the same decision/STOP rules, writes the final report
and audit, and performs the final Git commit. Its `bootstrap` function is
replaced only in the new execution process. The 24 leave-one-center-out
calculations retain the frozen omitted-center order and each gets an atomic,
SHA-256-validated checkpoint. A checkpoint is reused only when its complete
center list, input hash, seed, draw count, schema, and receipt match; an
incomplete or mismatched checkpoint causes STOP, never silent recomputation.

Bound execution code:

| File | SHA-256 |
| --- | --- |
| `scripts/run_p7_4b_gpu_finalize.py` | `dd8569634e633a16cd4351ec9f84c028469edd973c087e362fb82041d65e7648` |
| `scripts/run_p7_4b_gpu_supervisor.py` | `1756b05d7e6227c54448fb2db7e71ce0077d3af22e64f80d6c9a1df3d668d913` |

The selected CUDA environment is
`C:/Users/92487/anaconda3/envs/tf-gpu/python.exe`, with CUDA-enabled PyTorch
2.5.1+cu121. The default scientific runner continues to use the previously
established CPU environment. The GPU worker has **no** CPU fallback. A first
CuPy-based dry test failed because its NVRTC builtins DLL was unavailable; no
experiment statistic or checkpoint was produced in that failed test. The
worker was replaced with CUDA PyTorch before this amendment was frozen.

## Pre-execution verification

The supervised short test completed on 2026-09-26 without creating any final
scientific output. Its 4,000 GPU main-bootstrap paired effects were compared
replicate by replicate against the already persisted serial CPU
`paired_bootstrap_samples.csv`; the maximum absolute discrepancy was
`5.27e-16`, below the predeclared `1e-12` numerical-equivalence tolerance.
Eight matching resample draws were also compared to the frozen serial
bootstrap for each of the first and last omitted Validation centers. This
test does not itself establish the final scientific verdict; any undefined
replicate, pairing mismatch, hash failure, or material numerical divergence
still causes STOP. Verification logs are under `results/p7_4b/` with prefix
`gpu_finalize_verify_20260926_204539`; the GPU temperature was 45–49 C and
available memory never fell below 5.543 GiB during this short test.

## Thermal/resource execution boundary

The user reported that the laptop fan remains faulty and explicitly chose a
GPU run with live temperature supervision. This does **not** prove the laptop
is safe: the host currently exposes a GPU temperature through `nvidia-smi`
but no reliable CPU temperature. The new supervisor uses a Windows Job Object
that kills its own experiment process tree if the supervisor exits; it does
not stop or alter any other application. It samples GPU temperature and
available physical memory at most every two seconds. It stops its experiment
tree immediately at **75 C GPU temperature**, on any missing/failed GPU
temperature reading, or after two available-memory samples below **1.5 GiB**.
Before launch it requires two readings at least ten seconds apart with at
least **2.3 GiB** available and GPU temperature below 75 C. A short transient
between samples and unobserved CPU overheating cannot be ruled out. If the
user observes abnormal heat, fan behavior, smell, or thermal shutdown signs,
they should stop the run rather than relying on this software guard.

No WeChat/Weixin, QQMusic, or other application may be closed, suspended, or
modified. Never access centers 33000–33019, Alibaba, or P8; never modify
the behavior path, representation, folds, models, seeds, resample count,
bootstrap intervals, proceed checks, or scientific claim boundary.

## Exact execution and terminal gate

Run the supervised command only after this amendment and both scripts are
Git committed, no matching P7.4B process exists, the frozen preflight passes,
all 288 Validation receipts and stagewise A0/A1 path equality pass, and the
eight persisted intermediate-file hashes match the 2026-09-24 pause record:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b_gpu_supervisor.py run --gpu-python C:/Users/92487/anaconda3/envs/tf-gpu/python.exe --stop-c 75 --launch-memory-gib 2.3 --min-memory-gib 1.5 --interval-seconds 2`

The supervisor must run its equivalence check before the frozen finalizer
continues. On any execution or scientific failure, STOP and preserve the
checkpoint/logs for audit; do not silently retry. On successful exit, verify
the full final report, scientific audit and SHA-256 manifest, all required
outputs, Git commit, and no heldout/Alibaba/P8 access. Report the actual
P7_4B_PASS or P7_4B_FAIL and stop for human scientific review.
