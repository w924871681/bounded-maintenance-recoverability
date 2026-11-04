# P7.6A-1 pre-metadata stream rule

This execution-only metadata rule is fixed **before inspecting candidate metadata**. It does not change the frozen scientific generator, A0/A1, or any previous result.

- Candidate stream: ascending center IDs **32248–32631 inclusive** (384 slots), safely above the 32200–32247 P7.4B range and below the permanently reserved 33000–33019 final heldout range.
- Preserve the existing `core.data.generate_base_centers` stream semantics: data seed 7311, start ID 32248, *batch length 384*, `seed_offset=start_id*17`, the existing prefix-balanced center-type schedule, and each slot's generator RNG seed. Batch length is bound because the frozen generator builds the type schedule before drawing per-center seeds; changing it can change metadata for the same ID.
- Inspect or persist **only** `center_id`, `center_type`, and `deployment_tier` (`budget_tier` in the generator). The metadata-only replay consumes the generator's random-number sequence without constructing latent workload, monitoring trajectories, labels, oracle values, service results, or representation outcomes. Verify the replay against the already-frozen P7.4B 48-center metadata before using it.
- First perform repository-wide center-identity provenance screening; any previously used ID is ineligible. For each of nine strata, take the first eight eligible IDs in ascending stream order. If 384 slots do not provide eight in every stratum, STOP for human review rather than changing the stream after seeing metadata.
- Within each stratum, sort the eight selected IDs and alternate odd positions to ReplicationFit, even positions to ReplicationValidation. Fit positions 1–4 determine OOF folds 0–3. No outcome is a selection input.
- A future generator implementation must reproduce the **exact same 384-slot schedule and per-slot RNG states** for selected centers; changing the number of slots or running the current contiguous-only generator on the noncontiguous selected 72 IDs is invalid. Implementation must be audited before P7.6B outcomes and cannot change any scientific factor.

The length 384 is an administrative, pre-outcome stream cap to provide substantially more than the required eight slots in the rarest metadata stratum (C/loose has nominal probability 0.3×0.15). It is not a power calculation and has no connection to the prior observed A1 effect.
