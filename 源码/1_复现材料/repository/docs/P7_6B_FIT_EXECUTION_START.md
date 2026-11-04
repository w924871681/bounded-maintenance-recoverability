# P7.6B formal ReplicationFit execution-only start record

This record is prospective: it is committed **before the first real P7.6B trajectory**. The human review authorizes **Fit only**, accepts the documented CPU/CUDA float32 differences on the tested qualification envelope and accepts the unrepaired cooling-fan risk as an operational decision, not as scientific evidence. Historical P7.6A/P7.4B verdicts and all frozen scientific criteria remain unchanged. ReplicationValidation, final heldout 33000–33019, Alibaba and P8 remain prohibited.

## Frozen bindings

| Object | SHA-256 / commit |
| --- | --- |
| P7.6B frozen protocol | `86272adb9a335ff72030cc4ba5c1fbc5f52e543eacd58ba032433e590251ee23` |
| 72-center frozen assignment | `172c694057fea9926fecabe800538a5f8ff5bddf8880c078dd457b705b53fb95` |
| CUDA-2 execution configuration | `cb4141fda8284a7e98b64187609e5af893e665f960afeef8853a8307fe1e9da3`; freeze commit `272c38671b34b2b99edaf152dcf00323d9a39184` |
| Fit-only human authorization | `cd24060fce17d01b09be9d7e9b9e558745bfb3d464693d7fad72da7e1d39f020`; authorization commit `b9675e7c4c2a06264628476a39294e9b93c842af` |
| CUDA qualification | commit `9622819cf6a4132810f3833dea3b4f510734bee7` |
| Fit supervisor | `7527b1344be4613ca80cc52c17ca18c41dd40a590466d070e0a66d1a0f101c3a` |

The exact scientific driver command run by the supervisor is:

`C:/Users/92487/anaconda3/envs/tf-gpu/python.exe -u scripts/run_p7_6b.py --phase fit --workers 2 --device cuda --resume`

One primary task is one `(center, seed, scenario)` complete 24-stage trajectory; there are exactly 36 × 3 × 4 = 432 shared A0/A1 Fit tasks. Windows `ProcessPoolExecutor` uses explicit `spawn`. `CUDA_VISIBLE_DEVICES=0`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`; frozen per-operation `torch.manual_seed` also calls `torch.cuda.manual_seed_all` under PyTorch 2.5.1. Float32 only; no AMP, changed update order, changed batch or changed RNG semantics.

The separate supervisor records parent/child PIDs, completed count, throughput, ETA, GPU temperature/utilization/clock/power/VRAM and available host RAM every five seconds. It may stop **only its verified P7.6B process tree** after two readings at or above GPU 82°C, two readings below 1.5 GiB available RAM, two lost GPU telemetry readings or three active thermal-slowdown readings. These are procedural safety boundaries and cannot change scientific decisions. CPU package and GPU hotspot temperatures are unavailable, so the human cooling-risk acceptance must not be called proof of sustained thermal safety. Worker failure, CUDA OOM/device loss or invalid receipt causes an un-retried interruption. Complete hash-valid receipts are preserved. The supervisor does not inspect partial scientific metrics to decide whether to continue.

Pre-launch read-only checks: Git-bound protocol/assignment/config/authorization; 432 deterministic Fit tasks; `--phase preflight` PASS; Fit `--dry-run` enumerated 432 tasks with no outcomes; Validation `--dry-run` denied due missing committed Fit freeze. The scientific `results/p7_6b` directory did not exist at this record's creation.

Upon 432/432 validated receipts, evaluate the frozen four Fit OOF conditions. On any failure record `P7_6B_FIT_GATE_FAIL` and stop without final pipelines or Validation. Only on all-pass, fit/freeze the final A0/A1 Fit pipelines and Fit manifest. Validation remains locked in either case pending separate human review.
