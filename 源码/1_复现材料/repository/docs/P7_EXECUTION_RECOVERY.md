# P7 execution-only recovery: explicit Torch RNG binding

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Verification Status: ANALYZED (execution realization, not P7 final performance)

Before any closed-loop calibration trajectory or method decision outcome was written, code inspection found that the reused SGD primitive seeds numpy minibatch sampling but does not itself seed Torch Dropout. The bank includes dropout-enabled MLP/two-layer GRU models. The predeclared paired-seed and exact memoization semantics therefore need an explicit caller-side Torch RNG binding; this is not a new optimizer, model, candidate, feature, gate or cost rule.

The initial parent process PID21112 was paused after common causal-prefix/C0-reference computations only. No `results/p7/raw` trajectory directory or completed reference file existed at the pause. Those initial reference computations were not persisted or used for tuning. All original pre-outcome P7 source/config/doc hashes, the pre-outcome manifest, every P4/P6 artifact and both earlier-paper repositories remain unchanged.

`scripts/run_p7_seed_bound.py` is an additional Git-bound execution entry point. It calls the **unchanged** adaptation primitive inside an isolated Torch RNG context seeded by that primitive's already-prespecified seed. Dropout remains enabled, with its architecture-defined probability. No different update counts, minibatches, learning rate, loss, gradient clipping or checkpoint weights are introduced. RNG state is restored after each adaptation so unrelated ordering/model loading cannot alter paired masks. This applies to copied probes, source RI candidates, frozen RAVM local blocks, warmup and offline P10/P20 candidates; the estimator is still loaded with no gradients and never fitted. Spawned worker initializers install the same binding. Repeated train-mode dropout adaptation and source-candidate cache equivalence are checked using toy fixtures, not real-center outcomes.

Supplemental `audits/P7_EXECUTION_RNG_BINDING.json` binds the new entry point, this record and its extra tests to a Git commit before closed-loop outcomes. Its parent pre-outcome manifest hash preserves the original preregistration lineage; it does not overwrite/redefine that manifest. The binding is a realization of its planned paired-seed semantics, not an outcome-based scientific amendment. P7 primary .10 cap, secondary .05, seven deltas, all baseline/cost grids, center pools, response representation and claim scope are unchanged.

Use the seed-bound entry point for P7 execution/resumption and finalization. Only complete original trajectory CSVs with matching hash receipts can be reused. Scientific/leakage/fairness/hash failures still require STOP; this execution clarification does not authorize protocol redesign or heldout access.
