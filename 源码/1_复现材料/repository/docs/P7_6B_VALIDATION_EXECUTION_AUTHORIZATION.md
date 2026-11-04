# P7.6B ReplicationValidation execution authorization

This is an execution-only authorization amendment. It does not change any scientific input, estimator, scaler, threshold, seed, assignment, behavior path, or evaluation criterion.

- Scope: frozen P7.6B ReplicationValidation only, followed by the frozen finalize command.
- User authorization: the user explicitly instructed: “开始 Validation”.
- Backend: CUDA, two workers, float32, spawn, exact frozen runner `scripts/run_p7_6b.py`.
- Fit status: 432/432 completed and Fit freeze is committed at `168494e099de7a60ca5aefee4b121d1ccab64803`.
- Validation opening: must be created once by the frozen `open-validation` phase before materialization.
- Prohibited: refit, recalibration, outcome-based changes, heldout centers 33000–33019, Alibaba, P8, and any other scientific-path modification.
- Required completion: 432 hash-valid ReplicationValidation receipts, then frozen `--phase finalize` only.

The corresponding authorization JSON and SHA-256 sidecar are committed with this record. This record is separate from the prior Fit authorization and is not a scientific result.
