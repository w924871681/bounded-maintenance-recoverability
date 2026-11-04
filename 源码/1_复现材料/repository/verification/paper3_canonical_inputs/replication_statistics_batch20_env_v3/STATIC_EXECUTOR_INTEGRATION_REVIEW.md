# V3 Statistics / Phase-Aware Executor Integration Review

Status: **STATIC_COMPATIBLE** for the inspected source. This is a read-only independent review, not a real scientific execution or completed runtime certificate. The parent's final executor source pin and actual focused synthetic proof must match the reviewed code before launch. No model, generator, real Bootstrap, statistics application or experiment-outcome read occurred in this review.

Statistics root: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_statistics_batch20_env_v3`.

Inspected executor source: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_env_v3\provenance.py`; SHA256 `a19dcb9d14edfca3598ba5ec1de9b03b3a3239fe378d00396a2a5acfc09cfe4a` at the read point. This review does not permit a later differing source to inherit its verdict without assessment.

## Findings

| Judgment | Full source/function/line evidence | Actual behavior and implication |
|---|---|---|
| VERIFIED — metadata-only statistics compatible | Above `provenance.py`, `_verify_model_runtime_environment`, lines 564–575; `statistics.py`, `validate_statistics_gate`, line 456 and `run_statistics`, lines 617/648 | Requires the complete 34-variable keyset and recorded digest. Without the private same-process post-import record, current values must exactly equal the raw recorded map. Statistics never declares an import transition, imports sklearn or sets these values, so it remains on the strict raw path. No raw-or-post global fallback exists. |
| VERIFIED — scientific transition is explicit | Above `provenance.py`, `begin_scientific_import_transition`, lines 647–665 and `_scientific_import_phase_guards`, lines 589–596 | Exact raw map, active write/generator/import-origin guards, no earlier sklearn import, valid manifest digest, exact package source, same PID, identity token and complete environment digest precede the original import. It does not set an environment variable. |
| VERIFIED — approved writer is source-bound | Above `provenance.py`, `_observe_scientific_import`, lines 613–644; `_scientific_import_writer`, lines 599–610; `_sklearn_import_source`, lines 578–586 | Only one execution of the compiled exact pinned sklearn initializer is admitted. Only originally absent `KMP_DUPLICATE_LIB_OK=True` at source line 56 and `KMP_INIT_AT_FORK=FALSE` at line 60 can change. Exact source/code/stack line, expected prior complete map, package bytes and nonduplicate event are required. Other observed runtime mutations fail. |
| VERIFIED — post state has no tolerance for rollback | Above `provenance.py`, `complete_scientific_import_transition`, lines 680–707; `_verified_scientific_import_post`, lines 710–725 | Completion requires the exact token/PID/manifest/environment, package module origin/version, one actual initializer execution, all applicable observed defaults and the complete expected current map. Serialized bytes are sealed inside an immutable same-process record. Subsequent verification checks PID, seal, full map, source bytes and exact module identity. Raw rollback or any other runtime-variable change fails. |
| VERIFIED — worker ordering preserves boundary | `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_env_v3\executor_worker.py`, `_load_context`, lines 81–108 | Isolation/write protection, full raw environment verification, generator and origin guards occur before the explicit transition token; unchanged `runtime_preflight` is enclosed by begin/complete. The resulting proof is saved in the worker runtime receipt. Metadata-only statistics does not use this worker branch. |
| VERIFIED — wrong PID/package/mutable proof are rejected by code | Above `provenance.py`, lines 684–687 and 710–725 | Wrong process or token, changed manifest/environment, nonimmutable cache, altered seal, changed package version/origin/file bytes and changed module object all encounter explicit assertions. This is trusted-process provenance with Python guards, not an adversarial OS sandbox guarantee. |
| VERIFIED — all statistics arithmetic remains unchanged | `SOURCE_ADAPTATION_BINDING.json` and `SOURCE_ADAPTATION_DIFF.patch` in the statistics root; `statistics.py`, lines 79–306 and 164–195 | Whole-text equality after the two declared path/private-ID substitutions covers every mathematical function. Center endpoint hierarchy, shared 4000×20 resampling with seed 2904, observed mean subtraction, diagnostics, costs and table fields are unchanged from V2. |
| VERIFIED — inference limits are explicit | Above `provenance.py`, `complete_scientific_import_transition`, lines 702–703 | Proof explicitly says `historical_environment_reproduced=False` and `numerical_neutrality_claimed=False`. Observing the unchanged package's import defaults establishes provenance compatibility, not historical/numerical equivalence. The paper/handoff must retain that limitation. |

## Focused synthetic coverage inspected

Read-only source: `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_env_v3\tests\test_scientific_import_transition.py`.

- `test_metadata_only_phase_is_strict_raw_and_never_imports_package`, lines 56–61 checks strict raw statistics behavior and rejects an unexplained default.
- `test_exact_two_observed_defaults_create_sealed_post_without_verifier_mutation`, lines 63–73 checks two observed defaults, independent returned proof and no numerical-equivalence claim.
- `test_no_token_no_initializer_and_module_key_alone_cannot_certify`, lines 75–81 and `test_missing_guards_or_nonraw_launch_fail_before_boundary`, lines 83–88 check token, actual execution, preimport and guard requirements.
- `test_post_phase_rejects_raw_rollback_and_every_other_variable_change`, lines 90–96 iterates the complete runtime variable list.
- `test_mutation_without_bound_writer_wrong_value_or_duplicate_is_rejected`, lines 98–108 and `test_source_exec_spoof_and_duplicate_initializer_are_rejected`, lines 110–115 check wrong source/value/event and repeated initialization.
- `test_token_pid_manifest_and_environment_cannot_change`, lines 117–125 and `test_post_seal_pid_manifest_source_or_module_identity_tampering_rejected`, lines 127–137 cover process, immutable seal, manifest/environment and module identity.
- `test_post_phase_cannot_be_reentered_reloaded_or_mutated`, lines 139–144 and `test_existing_launch_values_are_preserved_by_setdefault_not_replaced`, lines 146–152 cover no re-entry and unchanged existing values.
- `test_exact_writer_helper_checks_code_line_path_and_single_frame`, lines 154–164 and `test_loaded_module_key_requires_exact_origin_version_and_file_bytes`, lines 166–176 inspect exact frame and package identity.

These test sources were inspected; the independent reviewer did not execute them or certify the executor's actual full test run. The executor owner/parent must bind its final actual passing proof and source inventory. Statistics' actual separate 58/58 PASS is already saved in `SYNTHETIC_TEST_RESULTS_ATTEMPT001.json`, SHA256 `149cf3461cf5a70bf2e26f0cfaa06f3e8944271ff91b470d62a603031cc8ee10`.

## Conclusion

No static API or mathematics blocker was found for V3 metadata-only statistics on the inspected source. Full runtime fairness/completion and numerical behavior are NOT_VERIFIED by this review. Keep every original/V1/V2 asset and failure evidence intact. The actual root workflow must pass all final source/environment/F1/state/pairing/causal gates before using the unchanged statistics implementation.
