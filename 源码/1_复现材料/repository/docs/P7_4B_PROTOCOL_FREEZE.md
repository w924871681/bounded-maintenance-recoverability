# P7.4B-0 Prospective Representation Study Protocol Freeze

**Frozen:** 2026-09-21 16:28:33 Asia/Shanghai

**Scientific status:** P7.4A passed at theory/protocol-feasibility level only. A1 has no empirical effectiveness claim.

**Execution status:** not authorized. No P7.4B trajectory, outcome, fit, Validation opening, heldout access, Alibaba access, or P8 execution is part of this freeze.

## 1. Question and claim boundary

P7.4B is a prospective, paired test of whether the accepted fixed deployment-reference representation A1 transports continuous recoverability and its natural zero boundary across fresh heterogeneous centers better than the absolute control A0.

A future P7.4B PASS may support only:

> The fixed deployment-reference representation improves prospective cross-center recoverability transport relative to the paired absolute representation under the evaluated synthetic protocol.

It cannot establish final C2 validation, restore the rejected C3 hard gate, establish lifecycle superiority, establish final-heldout performance or Alibaba generality, or authorize P8 without another human review.

## 2. Fresh-center reservation and provenance audit

The contiguous range **32200–32247** is frozen. A structured audit found no prior use of any of these 48 IDs as a `center_id`:

- 1,499 repository CSV files containing a `center_id` column were searched at that column; zero target IDs were found.
- Repository filenames contained zero target IDs.
- Structured configuration/audit fields contained only the prospective reservation in `configs/P7_4B_PROSPECTIVE_STUDY_DRAFT.json`.
- Pure-text Git-history matches were reviewed as timestamps, row indices, numerical values, or hash substrings rather than center identities.
- The range is disjoint from generator development, P3/P3.1/P3.2, P6, P7, P7.1, P7.2, P7.3, debug/development center identities, external evaluation, and final heldout 33000–33019.

Metadata inspection was restricted to `center_id`, `center_type`, and the generator's `budget_tier` field mapped to `deployment_tier`. No trajectory arrays, labels, oracle margins, predictions, service outcomes, or representation outcomes were inspected or persisted.

## 3. Deterministic pool and fold assignment

Within each `(center_type, deployment_tier)` stratum, IDs were sorted ascending. Strata were processed in type order A, B, C and tier order loose, medium, tight. The first ID of each stratum went to the currently smaller pool (RepresentationFit on a tie), then allocation alternated within the stratum. This produced exactly 24 disjoint centers per pool.

**RepresentationFit (24):** 32200, 32202, 32206, 32209, 32210, 32212, 32213, 32215, 32218, 32219, 32220, 32223, 32226, 32229, 32230, 32233, 32234, 32236, 32237, 32239, 32240, 32243, 32244, 32246.

**RepresentationValidation (24):** 32201, 32203, 32204, 32205, 32207, 32208, 32211, 32214, 32216, 32217, 32221, 32222, 32224, 32225, 32227, 32228, 32231, 32232, 32235, 32238, 32241, 32242, 32245, 32247.

The four frozen Fit center-group validation folds are:

| Fold | Validation centers | Training centers |
|---|---|---:|
| 0 | 32202, 32206, 32239, 32243, 32244, 32246 | other 18 Fit centers |
| 1 | 32200, 32210, 32215, 32218, 32230, 32237 | other 18 Fit centers |
| 2 | 32212, 32213, 32220, 32223, 32226, 32234 | other 18 Fit centers |
| 3 | 32209, 32219, 32229, 32233, 32236, 32240 | other 18 Fit centers |

All seeds, scenarios, identities, and stages stay with their center. Random stage splitting and outcome-dependent replacement are forbidden. The complete metadata table is in `configs/P7_4B_CENTER_ASSIGNMENT.json`.

## 4. Paired design

A0 and A1 use exactly the same centers, raw traces, center metadata, data seed 7311, model seeds 7311/7312/7313, scenarios C0/C1/C3/C4, 24 stages, L=96, D_upd=400, D_assess=240, D_srv=400, H_R=4, eta=0.25, B50, local policies P0/P10/P20/P50, frozen `tau_service`, K_S=2, K_L=6, generator, identity bank, and deployment limits. Only the representation differs.

### A0 — absolute control

- Scientific target: `R_B50`.
- Response event: `[gain, post_assessment_mse]`.
- Natural decision boundary: zero after converting predictions back to scientific units.
- Fixed optimization unit conversion: multiply target by 1000; divide predictions by 1000 before every metric or boundary decision.

### A1 — fixed deployment-reference median-error scale

For every identity birth:

`S_m = max(median(e_1,...,e_104), 1e-12)`, where `e_i=(y_i-yhat_i)^2`.

- Scientific target: `R_B50/S_m`.
- Response event: `[gain, post_assessment_mse/S_m]`.
- Initial identity reference: exactly raw indices `[800,1000)` after frozen warm-up and before stage 1.
- RI identity reference: exactly the latest 200 raw observations of current D_assess after the candidate receives the frozen adaptation and before the selected identity is committed.
- Window length 96 gives exactly 104 required point errors.
- `S_m` is stored once and fixed for the active identity tenure.
- At RI, discard old `S_m` and response history and construct the new selected identity's scale by the identical rule.
- Natural decision boundary: zero in dimensionless scientific units.
- Fixed optimization multiplier: 1.

No fitted target scaler, target centering, validation-derived transform, alternative statistic, alternative reference source, or post-outcome multiplier is allowed. Inspection of the existing full-batch Adam/MSE implementation found no prospective numerical inconsistency from A1's multiplier of 1. Any later implementation inconsistency causes STOP rather than outcome-dependent rescaling.

## 5. Feature preprocessing and training

Both representations use the same six-feature construction and `StandardScaler` procedure. Each fold fits an independent scaler for each representation using only the 18 training centers, with per-feature arithmetic mean and population standard deviation (`ddof=0`); zero fitted standard deviation maps to 1.0. The held-out Fit centers are transformed only after scaler fitting. After OOF evaluation, each final scaler is fitted on all 24 Fit centers and frozen before Validation opens. A0 and A1 scaler parameters may differ because units differ, but their class and fitting procedure are identical.

Both use `6→16→8→1`, ReLU hidden activations, identity output, float32, Adam (`lr=0.001`, `weight_decay=0.0001`), MSE, full-fold batch, no shuffling, 400 epochs, no early stopping, no checkpoint/model selection, and terminal epoch 400. Paired fold initialization seeds are 9632, 9633, 9634, and 9635; the final all-Fit seed is 19631. A0 and A1 are separately restarted from the identical corresponding seed.

Fit reporting uses strictly OOF predictions. Validation uses the two final all-Fit pipelines frozen before its single opening.

## 6. Scale and RI-selection audits

Every floor activation and every scale must be reported by pool, center, type, tier, and initial-versus-RI birth source. Any non-finite scale or reference with other than exactly 104 valid point errors is an immediate STOP. If the floor is activated for strictly more than 1% of all constructed identity scales in either pool, STOP and reject A1 as numerically unstable. The floor may not be changed after outcomes.

The selected RI candidate is evaluated on D_assess and its `S_m` is constructed from the same causal D_assess. This is not future-service leakage, but it can create selection optimism. P7.4B must report initial-deployment and post-RI scale distributions, selected-candidate provenance, and initial-versus-RI transport metrics. It may not claim the two scale sources are statistically identical or redesign this mechanism during P7.4B.

## 7. Metrics and prospective decision rule

Center is the statistical unit. Within-center Spearman is calculated across that center's included seeds, scenarios, and stages; macro-center Spearman is the arithmetic mean across all 24 centers. Undefined center correlations count as non-positive and fail the corresponding absolute condition. Positive-center fraction uses all 24 centers as the denominator. Non-C3 repeats the calculation after excluding C3 records.

For admission, negative recoverability is the positive class. Center TPR and TNR are calculated where their respective class exists. Macro TPR and macro TNR are arithmetic means over centers defining each class, and zero-boundary balanced admission accuracy is `0.5*(macro TPR+macro TNR)`. Contributing center counts must be reported; an undefined macro component causes STOP.

A1 must satisfy in **both Fit OOF and Validation**:

- macro-center Spearman > 0;
- positive-Spearman-center fraction > 0.5;
- zero-boundary balanced admission accuracy > 0.5;
- non-C3 macro-center Spearman > 0.

On Validation, paired point estimates `A1-A0` must be strictly positive for both macro-center Spearman and balanced admission accuracy.

The paired uncertainty calculation resamples the 24 Validation centers with replacement 4,000 times using seed 2904, retaining all records and using the identical resample for A0 and A1. It reports percentile 95% intervals using linear 0.025/0.975 quantiles. At least one interval must have lower bound > 0, while the other must not have upper bound < 0. Any undefined required replicate or fewer than exactly 4,000 paired replicates causes STOP. No p-value optimization is allowed.

Define deterioration as `Fit_OOF metric - Validation metric`. STOP if A1 deteriorates strictly more than A0 on **both** macro-center Spearman and balanced admission accuracy. In addition, repeat all absolute, paired point-estimate, and bootstrap proceed conditions after removing each Validation center in turn; if any one-center removal causes any otherwise-held condition to fail, STOP.

Every integrity, leakage, pairing, or outcome-dependent-revision failure also causes STOP. Every eventual P7.4B result stops for human scientific review.

## 8. Prospective execution order

After separate human authorization only:

1. Materialize paired RepresentationFit records only.
2. Fit A0 and A1 using the frozen folds and training rules.
3. Freeze both scalers, both estimators, formulas, Fit OOF results, and all code/config/input hashes.
4. Open RepresentationValidation once only after both pipelines are frozen.
5. Apply the predeclared criteria without refit, threshold tuning, scale-statistic tuning, feature change, model selection, or center replacement.
6. Stop for human scientific review. Do not access final heldout, Alibaba, or P8.

## 9. Component bindings

Hashes use UTF-8 canonical JSON with sorted keys and separators `(',', ':')`.

| Frozen component | SHA-256 |
|---|---|
| A0 formula | `ce323d6001592fc44cc2b233234a3bd08722222e65c3b26edc33cfb65c380e24` |
| A1 formula | `1ec3b3786cf84696e651429916fb3c2e9b4ef3e2625b8c15149d1448a8f9d771` |
| Center IDs | `bafb1c5d83188384ad5ab12db2de7914ccbd0699f98ea8c7e03baf44ff25c963` |
| Pool assignment | `414230ee95a920158725daf8f592e7e3a45c8dee7c804c9a1b78bd7ffd1a5a3e` |
| Scale source | `0539d02cbf0a40ceea596b49eab69080f2b87a27c052be6ce0ba9203f957a8b7` |
| Median statistic | `e73db72447976a0ce29bf9e608dc0530a2ab11df0292205ee6f89cf270b091a1` |
| Floor and floor audit | `ecb7c045c4e79104ce4e67646053923baadf908ab895925f672b0903734954fa` |
| Target multipliers | `f2af0d50129ecea274a67c77a11036b559cab230b66947b0a740aa11b374613b` |
| Feature preprocessing | `506e59c9c1de368281b1c64e6ad8ad996d19b0936604912b94b0e0599c698cc7` |
| Model architecture | `02f503ba834d360903d8ec1bd25db599f3c421f4443c9b2193982df662f83b11` |
| Training schedule | `cc1ce7e077b4f2a157f71107c88a7c19439db2dadb9eba11ad2e91776d2dc48d` |
| Random seeds | `e2d91c15ba790e3f4baa7d4769944f2bdc4ea9b6ecf91c0405c63846607ca693` |
| Stop rules | `244943d863750015be3fbc5ae2c6dee7d5aea56d60613ddf6e236f2891823648` |
| Bootstrap rule | `21b0df797e7970f820cbc000099b32244d4e30d3b3d4fca6f7f88bcc852cda29` |

The machine-readable selectors and file-level bindings are in `audits/P7_4B_PRE_OUTCOME_FREEZE.json` and its sidecar.

READY_FOR_P7_4B_EXECUTION
