# Independent Stage E Statistics — V3 Static Review

Repository: `D:\dt-talk\DT_LIFECYCLE_ESCALATION`.

Implementation: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_statistics_batch20_env_v3`.

Exclusive result root: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7_integrity_replication_batch20_env_v3`.

**READY_FOR_GATED_STAGE_E — statistics implementation only.** Actual synthetic validation is VERIFIED. Real statistics/Bootstrap, real outcome inspection and completed experiment integrity remain NOT_EXECUTED/NOT_VERIFIED by this subtask. The parent alone may execute Stage E after all 1200/1200 trajectories, 240/240 groups, 60/60 initial states and frozen-source/input/environment checks pass.

## Exact controlled adaptation

The retained V2 sources were copied into this new directory after exactly two declared text substitutions: `_env_v2` → `_env_v3`, and `P7_7_JOINT_CENTER_STATISTICS_BATCH20_ENV_V2` → `P7_7_JOINT_CENTER_STATISTICS_BATCH20_ENV_V3`. Whole-text equality after these substitutions was verified for all four Python files. Every changed line is saved in `SOURCE_ADAPTATION_DIFF.patch`, and original/adapted SHA256 values and the exact-substitution checks are bound in `SOURCE_ADAPTATION_BINDING.json`.

The implementation changes are limited to `statistics.py:26–27` result/executor roots, `:37–38` statistics identity/output prefix, `:313` private loader name; `runtime_guard.py:134` exact publication prefix; `run_statistics.py:23` private package name; and `test_statistics.py:23/214/221` corresponding test package/path references. The V3 proof remains the first exclusive `SYNTHETIC_TEST_RESULTS_ATTEMPT001.json` in this new directory. V2's proof was not reused.

The F1 input at `statistics.py:28`, scientific definitions, centers/seeds/scenarios/methods, 24 stages, original model/config/source pins, endpoint calculations, joint resampling, diagnostics, cost summaries and saved-result schemas are unchanged. No original, V1 or V2 file was modified by this adaptation. V1/V2 failed-runtime source/log/manifest evidence must remain a separately bound parent handoff supplement; failed initial-state attempts do not qualify as V3 state/trajectory/phase success.

## Scientific definitions and code evidence

All locations in this table are inside the complete implementation directory printed above.

| Requirement | Function/lines | Behavior and interpretation |
|---|---|---|
| Endpoint hierarchy | `statistics.py`, `aggregate_rows`, line 79 | Exactly 24 stages per trajectory, three seeds and four scenarios inside each center, then the 20-center mean. Neither stages nor trajectories become independent Bootstrap units. |
| Joint center Bootstrap | `statistics.py`, `joint_center_tables`, lines 164–173 | One `default_rng(2904)` draw matrix; real shape 4000×20. All five methods, four contrasts and four scenarios share the center draws. Linear 95% percentile CIs are pointwise, without multiplicity adjustment. |
| Observed contrasts | `statistics.py`, lines 194–195 | Observed Proposed center-mean endpoint minus each baseline's observed endpoint. Replicate means cannot replace observed effects. |
| Diagnostics | `statistics.py`, `aggregate_rows`, line 151 | Four frozen offline `R_B50`/action/best-local-policy masks, denominator all 5760 Proposed stages. Masks can overlap and are nonexhaustive; missed escalation is not solely a closed-gate error. |
| Action penalty | `statistics.py`, line 109 | Zero retain, `0.1*service_unit` maintain, ten times that for RI. Penalty is kept separate from the primary service-loss endpoint and measured compute. |
| Runtime and search data | `statistics.py`, `execution_cost_tables`, line 219 | Saved cached-call timers, standalone estimates, candidate counts, charged-update counters and cache indicators are separate. Action penalties/charged updates do not establish full measured computational cost; summed timers do not establish parallel walltime. |
| Original versus corrected | `statistics.py`, `original_comparison_tables`, line 267 | All five methods, four scenarios and four observed contrasts are saved regardless of sign/significance. Differences do not identify a causal mechanism. The correction follows observed old results and cannot be called an unseen heldout experiment. |

Frozen authority: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py`, `_trajectory_metrics`/`_center_metrics` at lines 501/528 and diagnostic masks at lines 597–609; `D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json`, `statistical_plan`; and the researcher's explicit joint-center correction authorization. The historical advancing per-method draw sequence is not claimed bit-identical to the authorized one-joint-matrix implementation.

## Gates and exclusive attempt recovery

`statistics.py`, `validate_statistics_gate:449–456` requires the exact V3 repository/root and actual supplied manifest digest, then performs complete frozen-source/model/config/F1/environment verification before model-outcome reads. Later checks require the predeclared minimal five-method gate, actual accepted-record 1200/240 proof, complete 60 initial references, exact input identity and current matching synthetic proof/source hashes.

`_phase_evidence:384` and `validate_phase_attempts` bind exclusive `execution/<phase>/A_<PHASE>_NNNN/` histories. Required populations are initial 60, minimal five and remaining full 1195 tasks. Retry tasks may repeat only the predeclared population. Failed logs/worker/task records remain bound. Missing/unexpected tasks, ambiguous terminal files, final failures or absent successful phase-end integrity checks fail closed. V1/V2 evidence never enters V3's success population.

The current matching test receipt is read at `statistics.py:501`; each current Python hash, interpreter/executable hash, site root and NumPy version must agree with the manifest and proof. A prior receipt from an earlier directory or a different interpreter cannot pass.

## Environment phase and platform interface

Statistics imports no sklearn, Torch, River, pandas, project model or generator. It loads only SHA-bound V3 stdlib integrity readers and later NumPy. `verify_frozen(...verify_environment=True, full=True, check_inputs=True)` at `statistics.py:456` precedes worker guard installation at `:582`; subsequent complete rechecks at `:617/:648` use the same metadata-only statistics process.

The V3 executor must verify the raw environment for this process without entering the scientific-model import transition, setting environment values, requiring a worker post-import value or importing sklearn. No statistics call to `begin_scientific_import_transition` or `complete_scientific_import_transition` exists. The executor peer's separate design uses an explicit token and source-bound import-side-effect proof for scientific workers, observing `KMP_DUPLICATE_LIB_OK` and `KMP_INIT_AT_FORK` as well as the full environment map. That design does not justify a global raw-or-post fallback. Direct V3 executor integration evidence is recorded separately when its actual source is available; this statistics proof alone does not certify that executor.

Windows platform metadata must still be queried before the irreversible subprocess guard, through the V3 executor's same-process immutable bootstrap. Statistics introduces no platform subprocess exception and does not query platform metadata itself. Actual source/native/environment and input hashes must continue to be verified. The metadata binding correction must not change scientific model calculations or inputs.

## Import, read and write audit

All statistics top-level imports are standard-library-only. `runtime_guard.py`, `allowed_module_origin:33–49` accepts only exact SHA-bound NumPy name/origin below the selected independent site, including a site inside the repository; only `provenance.py` and `executor_driver.py` are allowed from the executor. Original methods, adapters, model libraries, other site packages, name-spoofed sources and unbound source bytes are denied. There is no new import exemption for sklearn.

The read guard binds exact protected originals, F1/Stage-B files, runtime/environment evidence, executor files, V3 raw/phase/worker/initial receipts and current statistics/test bytes. It never allows an entire original directory. Existing unbound bytecode is denied, apart from permitted nonexistent cache probes. Native NumPy is trusted: Python audit hooks plus before/after complete SHA verification do not constitute an OS sandbox.

`statistics.py:580` rejects any existing `statistics_batch20_env_v3` output directory. Publication is exclusive and restricted to the new root, with no original replacement. Frozen/environment/F1 bytes are rechecked at `:617/:648`, saved output hashes at `:650`, and success published only at `:651–656`. The output manifest excludes its own hash, avoiding circular SHA dependencies. Partial failures remain evidence and are not completed statistics.

## Actual synthetic tests and SHA256

**58/58 PASS**, zero errors/failures. UTC `2026-10-09T07:59:23.801624+00:00` to `2026-10-09T07:59:38.814655+00:00`; unittest 15.013 seconds; NumPy 2.4.6. Receipt `SYNTHETIC_TEST_RESULTS_ATTEMPT001.json` SHA256 `149cf3461cf5a70bf2e26f0cfaa06f3e8944271ff91b470d62a603031cc8ee10`. Its scope fields explicitly state no project model/generator execution and no real outcome reads.

Interpreter: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\model_env_recovery_v1_20261009\P7_7_REPLICATION_MODEL_ENV_V1\Scripts\python.exe`; executable SHA256 `8e83e4f932e02ffcf93d6ce00ef19791d9e78f1ca37fa2da31c45e99061d4dcc`.

Tests verify matrix completeness, finite values/action consistency, hierarchy, shared draws, observed effects versus replicate means, overlapping diagnostics, center leave-one-out, unchanged global NumPy RNG, cost separation, recovered unions/failure retention, complete adverse/favorable comparisons, exact nested-site NumPy imports and denied unrelated imports/reads. Actual experiment proofs remain synthetic fixture values; the tests do not certify an actual completed replication.

| Source | SHA256 |
|---|---|
| `statistics.py` | `5ccda537c83bf88f7531eeee7c9b4b82a55b23f4ba81b3c031b978ac8375e33c` |
| `runtime_guard.py` | `42a7fff9b32493904537e89737d5b4ed7adc2f32ab155915d3c5dfdbcc40bcb8` |
| `run_statistics.py` | `0346c5cdecfc595bab20f4f98b53547d215103931fd6d4aff7eb7783296e96bc` |
| `test_statistics.py` | `06ee1a6e1e15808bab2f8aa82b1b2aa0cea2bd94e318ceb1252a2d41edabdc86` |

## Gated production interface

Only the parent may invoke this command after every actual scientific gate passes. TEMP/TMP/TORCH_HOME/CUDA_CACHE_PATH must lie inside the V3 root, and the pycache prefix must be absent:

```text
<independent interpreter> -I -S -B -X pycache_prefix=<V3-result-root>/never_created_statistics_pycache
  D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_statistics_batch20_env_v3\run_statistics.py
  --expected-manifest-digest <actual saved V3 provenance manifest_digest>
```

All outputs are exclusive to `<V3-result-root>/statistics_batch20_env_v3/`. All CSV, manifest and final receipt fields remain identical to V2. Real statistics and Bootstrap are NOT_EXECUTED here. Any Python modification invalidates the current proof and requires complete new tests with a fresh receipt.
