# P7.4B Behavior-Path Supplement

## Status and timing

This supplement is prospective. It is frozen before any P7.4B trajectory,
recoverability label, representation target, prediction, metric, or other
P7.4B outcome is materialized.

The human scientific authorization fixes the common P7.4B behavior and data
generation path to the already frozen P7.2 Proposed configuration:

- method: `Proposed`
- `delta_R = -0.000272181217042075`
- cost ratio: `10`
- configuration identifier: `Proposed_ratio10_grid33`
- gate source: `GateCal-v2`

This supplement resolves behavior-path semantics only. It does not change any
P7.4B representation formula, center, fold, feature, estimator, optimizer,
seed, metric, proceed condition, STOP rule, or claim boundary.

## Single shared behavior path

Exactly one closed-loop trajectory is generated for every frozen
center/seed/scenario tuple. The gate is evaluated by the immutable P6
recoverability estimator used by P7.2. The frozen P7 decision executor then
selects retain, bounded local maintenance, or RI under the P7.2 Proposed
configuration above.

A0 and A1 are computed only after the current-stage behavior decision is
fixed. Neither representation's target, response normalization, feature
vector, fitted scaler, fitted estimator, prediction, or metric is supplied to
the gate, action selector, candidate search, identity selection, or parent
update. The same selected action and deployed model produce the service
outcome used by both paired representation records.

The RI candidate bank, feasibility filter, per-task seed binding, 50-update
candidate adaptation rule, lifecycle costs, source cache semantics, parent
state evolution, and service path remain exactly those of the frozen P7/P7.2
implementation.

## Fixed A1 identity-scale timing

The initial active identity scale is constructed from the initial deployed
model and raw observations `[800,1000)`, yielding exactly 104 pointwise squared
errors for window length 96.

When RI is selected, the selected candidate has already received the frozen
adaptation procedure. Its new identity scale is constructed from exactly the
last 200 raw observations of the current `D_assess` before that identity is
used at the next stage. The old active scale applies to the current stage's A1
response and target. The new scale is stored once and held fixed throughout
the selected identity's tenure. A representation history reset accompanies
the identity change. Rejected candidates never create persistent scales.

Every reference must contain exactly 104 finite point errors. Any non-finite
scale, reference-count mismatch, or pool-level floor activation rate strictly
above 1% is an immediate STOP under the already frozen protocol.

## Mandatory paired path audit

Every stage records independently named A0 and A1 values for:

- parent-state hash;
- selected action;
- post-action identity;
- cumulative post-action path hash.

The cumulative path hash binds the preceding path hash, current parent-state
hash, selected action, post-action identity, and deployed-state hash. All four
A0/A1 fields must be identical at every stage. Any mismatch raises an
assertion and immediately stops execution; no later phase may continue.

## Boundaries

The original P7 PASS, P7.1 verdict, and P7.2 scientific verdict remain
immutable. P7.4B remains a paired representation-transport study only. It may
not access centers 33000--33019, Alibaba, or P8, and it may not support a
lifecycle-superiority claim. After the required P7.4B report and audit are
produced, execution stops for human scientific review.
