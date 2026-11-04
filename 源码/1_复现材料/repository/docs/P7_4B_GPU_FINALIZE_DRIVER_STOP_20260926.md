# P7.4B GPU finalization: driver-crash STOP (2026-09-26)

The post-outcome, execution-only GPU runner was committed before launch at
`d79964ac178781b69966c3e2b4424d1dbe335c88`. The supervised command from
`P7_4B_GPU_FINALIZE_EXECUTION_AMENDMENT_20260926.md` launched once at
2026-09-26 20:50:13 Asia/Shanghai. Supervisor logs are under
`results/p7_4b/gpu_finalize_run_20260926_205013_*`.

The frozen main 4,000-draw bootstrap passed replicate-level numerical
comparison against the earlier CPU output (maximum absolute difference
`5.27e-16`). The main and 17 of 24 leave-one-center-out GPU bootstrap jobs
completed. Their 18 JSON checkpoint files and 18 SHA-256 sidecars all
validated. The next CUDA worker exited abnormally with no Python stderr.
Windows Application Error event 1000 at 20:53:08 identifies
`C:/Users/92487/anaconda3/envs/tf-gpu/python.exe` crashing in `nvcuda64.dll`
with exception `0xc0000409` (WER event 1001 at 20:53:38). The supervisor then
exited nonzero; no matching P7.4B Python process remained. This is an
execution/driver failure, not evidence for a scientific PASS or FAIL.

During the supervised run, the observed GPU temperature was 50–56 C and
available physical memory was at least 4.87 GiB. Neither the 75 C GPU stop
threshold nor the 1.5 GiB memory threshold was reached. The faulty fan
remains a safety concern, and CPU temperature was not measurable. No other
application or process was stopped.

`results/p7_4b/leave_one_center_out.csv`,
`reports/P7_4B_REPRESENTATION_TRANSPORT.md`, and
`audits/P7_4B_FINAL_SCIENTIFIC_AUDIT.json` are absent. The 288 Fit and 288
Validation receipts and frozen scientific inputs remain unchanged. No
heldout centers 33000–33019, Alibaba, or P8 were accessed. No automatic GPU
retry is authorized under the execution amendment. Resume requires a new
explicit decision and a separately audited recovery method; incomplete or
hash-invalid checkpoints must never be silently reused.
