# P3.2 Protocol and Claim-Scope Amendment

## Material Passport

- Origin: human scientific review of P3.2a, P3.2b and P3.2c
- Date: 2026-09-16 (Asia/Shanghai)
- Status: prospective, binding claim-scope amendment; not a rerun or replacement of the frozen P3.2 analysis
- Integrity: the SHA-256 of this complete file is recorded externally in `audits/P3_2_PROTOCOL_AND_CLAIM_AMENDMENT.sha256` and in the P4 scope manifest. A file cannot contain its own complete SHA-256 without a self-reference.

## 1. Original intent and unchanged audit history

The original Section-5 execution specification assigned C3 to source-identity mismatch / prior-family replacement: a different source-trained initialization should be closer under the same bounded adaptation budget, including a same-architecture comparison. It assigned C4 to architecture-level mismatch: a changed temporal dependency structure should give a different architecture family in the reusable bank a persistent post-adaptation advantage. C0 was stationary; C1 gradual parameter-level drift; C2 abrupt parameter-level drift; C5 persistent regime replacement; C6 recurring regime; C7 transient corruption; C8 mismatch plus unreliable monitoring. The original main full-baseline matrix was C0/C1/C2/C3/C4/C6, with C7/C8 robustness conditions. This amendment does not alter their generator definitions or delete the original intended roles from history.

P3.2a generator redesign was judged **PASS** on the design centers. The resulting r3 generator and source bank were frozen before P3.2b fresh-center outcomes. P3.2b's formal confirmatory verdict is **FAIL**, and shall remain FAIL in its report, analysis files, future audit histories and any account of preregistered gates. P3.2c is a read-only mechanism/provenance audit; it does not replace P3.2b or refit any model. No calibration or final held-out center data have been accessed.

## 2. Evidence that motivates the prospective amendment

At the frozen primary `H_R=4`, `eta=0.25`, `B50={P0,P10,P20,P50}` setting on six fresh development centers, P3.2b found C0/C1 pooled negative recoverability `86/576=14.93%`, C3/C4 pooled `411/576=71.35%`, and center-cluster bootstrap separation `+0.564236` (95% CI `[+0.411415,+0.729167]`). C3 was `288/288` negative post-shift, with persistent negative intervals in `18/18` trajectories. C4 was `123/288=42.708%` negative post-shift, with persistent intervals in `12/18` trajectories. A better feasible alternative existed for `375/411=91.24%` of pooled mismatch negative-R records; `36/411` had no better alternative and remain in every denominator. The combined C3/C4 post-shift negative-R `>=0.50` gate is **PASS** (`411/576`).

The separately defined single-scenario C4 post-shift negative-R `>=0.50` auxiliary confirmatory gate is **FAIL** (`123/288`). Its provenance differs from the original combined gate: the combined gate was already in the committed P3 development protocol; the per-scenario 0.50 rule was agent-authored in `configs/p3_2_protocol.json` before P3.2a design outcomes and was present in the frozen P3.2b config before fresh-center outcome materialization. P3.2c verdict: `PRE_FROZEN_CONFIRMATORY_GATE`, qualified as code/config-level pre-freeze rather than the original human-specified combined gate. The failure may not be erased, relabeled PASS, or made to disappear by pooling, subgroup selection, normalization, a changed denominator or a changed threshold.

The P3.2c paired C4_C source-bank comparison used identical center/seed/stage, data-role hashes, adaptation budget and deployment limits. The TCN_C model won frozen H=4 horizon service loss in only `102/288=35.42%` of post-shift keys; GRU_C_control won `186/288`. Mean TCN-minus-GRU H=4 loss was `+0.000310`, with center-cluster 95% CI `[−0.000356,+0.001136]`; four of six center means favored GRU. Among C4 negative-R records, the best alternative was TCN_C in 89 and same-regime GRU_C_control in 34, not 123 architecture replacements. P3.2c architecture verdict is **`IDENTITY_MATCH_SUPPORTED_BUT_ARCHITECTURE_NOT_SUPPORTED`**. The six-center C4 negative-R counts were `0,6,21,48,0,48` out of 48 each. This supports descriptive center-specific heterogeneity; deployment tier association is not causal evidence.

## 3. Human scientific decision and claim boundary

The core finite-policy recoverability phenomenon is sufficiently supported for subsequent development, primarily by the controlled C3 identity-mismatch condition and the maintainable-vs-mismatch separation. C3 is the **primary controlled model-identity mismatch condition**. C4 is retained only as a **secondary “Nonlinear Dependency-Shift Stress” condition**, also described as a **heterogeneous dependency-shift stress condition**. Its generator remains the frozen direct nonlinear multi-lag target-dependency regime; the new name is an interpretation and claim-scope change, not a scenario or trajectory change. C4's 42.7% pooled negative-R rate and center heterogeneity must be reported, including the failed single-C4 auxiliary gate.

No manuscript, report, figure caption or abstract may claim that C4 demonstrates architecture-family replacement, an architecture-level mismatch, architecture failure, or a persistent advantage of the TCN architecture family. The regime-C identity match is relative to the recorded bank and does not isolate architecture from checkpoint/source-seed and stochastic adaptation differences. C4 may test robustness to a heterogeneous nonlinear dependency shift, but it cannot serve as primary architecture-mechanism evidence. No further C4-based generator tuning, re-freezing, service-threshold tuning, local-budget tuning, denominator change or outcome-driven scenario redesign is permitted. The P3.2b formal FAIL and both gate outcomes remain immutable scientific history.

This is a **prospective claim-scope amendment made before recoverability-estimator fitting (P6), decision-gate calibration, Proposed evaluation and final synthetic held-out evaluation**. It is not a retrospective change to the original P3.2b confirmatory decision. Future work must preserve the frozen generator/source bank and perform calibration and held-out evaluation only after this amendment and the P4 experiment-scope manifest are Git-bound.

## 4. Updated Section-5 scenario-role table

| Scenario | Original intended role | Binding revised role and permissible inference |
|---|---|---|
| C0 | Stationary | Maintainable/no-shift reference; unnecessary escalation. |
| C1 | Gradual parameter-level drift | Same-family maintainable drift reference; no automatic identity escalation. |
| C2 | Abrupt parameter-level drift | Same-family rapid-adaptation condition; not yet part of the P3.2 frozen four-scenario confirmation. |
| C3 | Source-identity mismatch / prior-family replacement | **Primary controlled model-identity mismatch** under bounded local maintenance; retain synthetic severity caveat. |
| C4 | Intended architecture-level mismatch | **Secondary Nonlinear Dependency-Shift Stress / heterogeneous dependency-shift stress**; describe center heterogeneity and failed single-scenario gate; no architecture-family replacement/failure inference. |
| C5 | Persistent regime replacement | Original optional/subtype role retained; no P3.2 evidence claim. |
| C6 | Recurring regime | Original recurring-regime role retained; no P3.2 evidence claim. |
| C7 | Transient corruption | Robustness-only transient-monitoring condition; no P3.2 evidence claim. |
| C8 | Persistent mismatch plus unreliable monitoring | Robustness-only overlap condition; no P3.2 evidence claim. |

The already-frozen P3.2 generator/confirmatory matrix is C0/C1/C3/C4. The original intended later full-baseline matrix C0/C1/C2/C3/C4/C6 may remain a planning matrix, but C4's label and evidentiary role in that matrix are changed as above. No new C2/C5/C6/C7/C8 trajectory or generator variant is authorized by this amendment.

## 5. Maintenance-response event and future estimation boundary

The frozen probe always uses 50 optimizer updates, making response effort variance zero. The effort component is **permanently removed** from the response event, future estimator inputs and manuscript feature definition; no artificial effort variability may be manufactured. The binding response event is

\[
\xi_t = [\mathrm{gain}_t,\ \mathrm{residual}_t]^T,\qquad
\mathrm{gain}_t=\frac{L^{\mathrm{pre}}_{\mathrm{assess},t}-L^{\mathrm{post}}_{\mathrm{assess},t}}{L^{\mathrm{pre}}_{\mathrm{assess},t}+10^{-12}},\qquad
\mathrm{residual}_t=L^{\mathrm{post}}_{\mathrm{assess},t}.
\]

Both losses come from the stage-t decision-time `D_assess` after the copied current local probe trains only on `D_upd`; neither future service outcomes nor offline oracle horizon losses are response features. P5 may audit existing development-only records for validity and association. It may not fit the final estimator, change the generator, add handcrafted features without a scientific blocker, or access calibration/held-out outcomes. Scaling parameters for a later estimator may be learned only from the prospectively frozen fitting pool in P6.

## 6. Integrity anchors and review gate

- Original execution specification: `docs/DT_LIFECYCLE_ESCALATION_EXPERIMENT_EXECUTION_SPEC.md`.
- Frozen P3.2 generator config SHA-256: `529655647c1359e2a164cddc3c5c8b534f5cdbad53e2ede29ada477910975646`.
- Frozen r3 source-training manifest SHA-256: `84ab3d962e9a566303060fa98febcadef26eb1e5d472f81d32d986c35de3b940`.
- P3.2a r3 analysis/scientific-audit SHA-256: `cf8503285dc797e85abe2f9d52fc6105e0b5b0768753195683d38f1ac36ba540` / `d95e20ff60b53a441f0f1d991c8e76b5cf5854bf4392e87fad4679798149b0e4`.
- P3.2b and P3.2c reports: `reports/P3_2B_FRESH_DEVELOPMENT_CONFIRMATION.md` / `reports/P3_2C_ARCHITECTURE_AND_GATE_FORENSIC.md`.
- Binding checksum: `audits/P3_2_PROTOCOL_AND_CLAIM_AMENDMENT.sha256`; the P4 freeze must include the same amendment hash and the Git commit that records this amendment.

After P5, stop for human scientific review. Do not begin P6 merely because P4/P5 artifacts exist.
