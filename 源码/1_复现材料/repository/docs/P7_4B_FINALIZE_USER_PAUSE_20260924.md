# P7.4B User-Requested Finalize Pause — 2026-09-24

## State at interruption

At the user's explicit request, the fifteen-minute P7.4B monitor was paused
and only the verified `python.exe` process PID 24780, whose command was
`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py finalize`, was
stopped. A post-stop check at approximately 11:13 Asia/Shanghai found no
matching P7.4B Python process. No other application or process was stopped.

Fit and Validation materialization each completed 288/288 trajectories. Before
finalize began, all 288 Validation trajectory/scales/integrity receipts passed
SHA-256 and every-stage A0/A1 parent-state hash, action, post-action identity,
and path-hash equality checks. The Fit freeze remains at commit
`024e6e1c36ad06737dcaa5e6ec0bc406b5239c54`, and the one-time Validation
opening at `f291127`. The Validation materialization status is
`MATERIALIZATION_COMPLETE`. No scientific configuration was changed.

The frozen finalize command had written the following eight intermediate files
before the interruption. Their SHA-256 digests were measured after the process
stopped; the files remain on disk under `results/p7_4b/`.

| File | SHA-256 |
| --- | --- |
| `validation_predictions.csv` | `8005857261909602aee7e928e96b514c46f907e131649944f6d5d8f5c3db9aac` |
| `validation_metrics.csv` | `9ec2a260d7a6e8b0fdbb8ba310fa82badd9f1d7f48989cce3005f1459dc20cdb` |
| `metrics_by_center.csv` | `9c5790fdba4c924e31be081e12369d748f274448964e495863ab16ea9ff3e585` |
| `metrics_by_scenario.csv` | `da726b35da3b5e0fb8d84e4e7f5a0d5c56523296e2c7e8ce714a5efc3428a5d5` |
| `metrics_by_stratum.csv` | `e445bf5def66dfde42580d6c254717430b2204d89016fbe4c1d37dda3a530044` |
| `reference_scale_audit.csv` | `d22deba235437c938322199b1f38a817697310902cecd6d79cdaa1437112787f` |
| `paired_a1_vs_a0.csv` | `fcc7df5b92fbab9f596625bab8d4c60786f39f4aa738c40a0cf02a937e2ad444` |
| `paired_bootstrap_samples.csv` | `ea2e8b6a91c46646c977ade35758d62bede91096598d72601703564ea2ce8c3f` |

The frozen script had not yet written `leave_one_center_out.csv`, the final
report, or the final scientific audit. The leave-one-center-out bootstrap state
was held only in process memory and is not recoverable from these files. This
record makes no P7.4B PASS/FAIL claim. The intermediate outcome files are
intentionally left as produced by the frozen command; this execution record
does not commit them as a completed scientific result.

## Resume boundary

Do not restart finalization or monitoring until the user explicitly says to
continue. Before any authorized restart, verify that no P7.4B process is
active, revalidate all frozen inputs and 288 complete Validation receipts,
and compare the persisted intermediate-file hashes with this record. The
frozen finalize command may need to recompute the in-memory bootstrap work;
do not infer that partial bootstrap work can be resumed. Do not change the
behavior path, estimator, representation, grids, centers, seeds, stop rules,
or scientific outputs. No heldout, Alibaba, or P8 access is authorized.
