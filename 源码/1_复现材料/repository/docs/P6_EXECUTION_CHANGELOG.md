# P6 Execution Changes and Recovery Log

## Authorization and scientific boundary

On 2026-09-16 the human explicitly authorized autonomous procedural recovery and output completion within the existing P6 limits, provided modifications are reported in Markdown. P7, calibration, heldout, Proposed and generator modification remain prohibited. A scientific CV failure must be reported as FAIL, not repaired by changing the representation, candidate grid, selection rule or stopping criteria.

The P6 protocol/configuration/code preregistration commit is `104efe7c19af17f99a36a8cbfce059e46f754880`, made before fitting-center outcome materialization. Candidate configuration SHA-256 remains `5f36327ef196410aa7e43ecd3e1b7cffc46cb22619f875dea264bdae06ae9f43`; center-fold configuration SHA-256 remains `a9e6990b58493a79dd40689b64d90cdbdbe9c4035f9cee7cdcc7f5ef33901306`.

## Recovery history

1. The initial foreground execution ended after 164 complete trajectory checkpoints; the command session and Python process were no longer available. The cause of process termination is not established. Completed fitting-center files were preserved and verified, not regenerated.
2. A hidden detached execution resumed and produced checkpoints 165–168. The resumed ETA incorrectly counted previously completed checkpoints as newly computed work.
3. After human authorization, the matching P6 Python process (PID 34868) was stopped after checkpoint 168. No completed checkpoint was deleted or overwritten.
4. Procedural fixes were committed as `8cfd3c8`. Preflight confirmed all 11 frozen checkpoint hashes; pre-output tests returned 12 passed and 3 expected skips for not-yet-produced CV/data outputs. At 2026-09-16 16:52:03 +08:00 a hidden detached process (PID 31228) resumed `scripts/run_p6.py --phase all`, using separate `continued_stdout.log` and `continued_stderr.log` without overwriting previous logs.
5. A thread-attached fifteen-minute heartbeat monitor (`p6-completion-and-scientific-boundary-monitor`) was activated to supervise progress and authorized procedural recovery, finish output/visual QA and Git binding, and stop before P7. It must not change scientific settings or repair scientific FAIL by tuning.

## Procedural changes before CV outcome inspection

- Convert DataFrame records to object dtype before replacing undefined descriptive statistics with `None`. This prevents an absent MLP alpha or undefined descriptive metric from remaining IEEE NaN and breaking strict JSON serialization. Undefined statistics are null, not imputed or treated as passing.
- Compute resumed ETA using newly completed trajectories only. Report an unknown ETA until a new checkpoint is completed.
- Verify every P4-frozen native and r3 checkpoint hash at preflight, in addition to the previously checked incumbent and source-training manifest.
- Guard final refit: subsequent report regeneration reuses the already-frozen scaler/estimator only after hash verification, rather than fitting again.
- Add canonical SHA-256 values for feature specification, selected window pair and fitting-center IDs. Bind P4, frozen generator config, P6 source/tests and this log into the final manifest.
- Draw descriptive center-bootstrap calibration intervals by their actual endpoints, avoiding Matplotlib's requirement that intervals be centered around the observed estimate. Empty-bin bootstrap draws are omitted explicitly; zero valid draws stop execution. This does not change model selection or any decision threshold.
- Add redundant line styles to scenario error-density curves and move the legend outside the data region. Run the scipilot layout audit on each figure. Defer vector exports until PNG visual inspection is separately documented.

## Invariants

The frozen generator, source assets, fitting centers 31200–31229, three seeds, C0/C1/C3/C4 scenario roles, H_R=4, eta=0.25, B50 policies, two-component response event, exact six features, eight window pairs, Ridge/MLP configurations, center-group folds, fold-local scaling and predeclared selection/stop rules are unchanged. C4 remains secondary Nonlinear Dependency-Shift Stress, not architecture mismatch. No calibration or heldout data have been accessed.

The numerical P6 development stopping checks were agent operationalizations committed before fitting outcomes. They are not claimed to have originated verbatim in the human protocol, and they are not lifecycle gate calibration.

## Completion record

At the 2026-09-16 19:43 +08:00 heartbeat, all 360 trajectory checkpoints and all eight window-pair CV computations were complete. The process had stopped at selected-estimator JSON serialization: the constant fold-training-mean baseline has undefined within-center Spearman, a separate nested-JSON NaN case not covered by the initial DataFrame-record fix. This is an undefined descriptive statistic, not an invalid prediction or a scientific check made to pass.

A P6-local recursive JSON sanitizer now writes undefined NaN statistics as null; the shared common module and other phases are unchanged. A `recover-output` phase reconstructs the same one-SE/family/tie-break selection from persisted candidate summaries and selected OOF predictions, verifies candidate completeness, selected windows, fold assignment, selected scaler identity and recomputed macro-MAE agreement, and writes the missing output. No trajectory or CV model was refitted during recovery. Constant-baseline Spearman remains explicitly undefined. The unchanged scientific checks returned CV_PASS, and all 15 required tests passed with zero skipped before the authorized one-time final fitting-center refit.

Additional output/QA-only changes: an already-frozen selected estimator cannot be overwritten by output recovery. Three output regression tests cover nested NaN/null serialization, infinity rejection and recovery immutability; all 18 tests (15 required plus 3 regressions) passed. The final estimator/scaler guard checks existing hashes instead of refitting during report regeneration. Statistical Material Passports now say ANALYZED, distinguishing executed audit tests from an independent stochastic reproduction rerun that was not performed.

The final MLP `mlp_ks2_kl6` was fitted once on all 30 fitting centers only. Scaler SHA-256: `1d4cb0b91206bb7defe8389aa8f27ff4776c2acc016662e952bc5f5dc3612f3b`; estimator SHA-256: `2bbad97427506b0260d3ed9370bc88ed4c91a8879c34787a184e37b5185f6b9b`.

Figure QA replaced manually positioned panel labels with the skill's uniform point-offset helper and generated grayscale previews. A first vector-export attempt correctly stopped because preview and vector modes had different numbers of layout-render passes. Both modes now use the same preview/grayscale render sequence before hash comparison. All four approved PNG hashes subsequently matched, and all four PDF/SVG figures exported without touching any fitted estimator. The saved descriptive calibration-bin table is reused without repeated CSV rewrites during plotting; bootstrap bins and estimator results are unchanged. Visual QA and the explicit scenario-specific-axis caveat are documented in `reports/P6_FIGURE_VISUAL_QA.md`.

Git-byte provenance: the existing repository defaults normalize text to LF, whereas some Windows-generated P6 JSON/CSV/Markdown artifacts contain CRLF. Scoped P6-only `.gitattributes` rules now disable text conversion for configs, results, fitted artifacts, audits, reports and this log so the exact SHA-bound bytes survive Git checkout. Previously frozen P3/P3.2 attributes and bytes are untouched.

A final descriptive check removed every pair of fitting centers from the saved OOF predictions (435 combinations, no model refitting): remaining pooled Spearman ranges 0.3808–0.4455. It supplements the requested one/two-center dominance diagnosis only; no selection rule or scientific gate was changed based on this additional output-stage analysis.

Completion: all required P6 outputs exist; the estimator-development CV result is PASS, all 15 required tests and three output regressions pass, four diagnostics passed inline visual/grayscale QA and exported PDF/SVG, and the report retains weak C0/C1 association and development-selection cautions. The final manifest is regenerated after this log update and binds files before the artifact commit. Final Git provenance is obtained from the commit containing that manifest rather than a self-referential commit field. P7/calibration/heldout remain prohibited. No new trajectories, CV fittings, handcrafted features, scientific thresholds or generator changes were introduced by these recovery/QA steps.
