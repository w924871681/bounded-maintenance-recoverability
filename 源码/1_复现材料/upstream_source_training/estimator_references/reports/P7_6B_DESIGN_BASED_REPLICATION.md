# P7.6B design-based replication

Formal verdict: **P7_6B_REPLICATION_PASS**

Fit checks: `{"A1_balanced_accuracy_gt_0_5": true, "A1_macro_center_Spearman_gt_0": true, "A1_non_C3_macro_center_Spearman_gt_0": true, "A1_positive_center_fraction_gt_0_5": true}`

Validation checks: `{"A1_balanced_accuracy_gt_0_5": true, "A1_macro_center_Spearman_gt_0": true, "A1_non_C3_macro_center_Spearman_gt_0": true, "A1_positive_center_fraction_gt_0_5": true, "Delta_balanced_accuracy_gt_0": true, "Delta_macro_Spearman_gt_0": true, "paired_uncertainty_rule": true}`

Paired effects: `{"Delta_balanced_admission_accuracy": 0.03010517445491334, "Delta_macro_Spearman": 0.1865534106661919}`

Paired intervals: `{"Delta_balanced_admission_accuracy": [0.0035699749423104585, 0.057871353408224406], "Delta_macro_Spearman": [0.12137435008809669, 0.25050224611846694]}`

LOO passes: 36/36. Transport deterioration stop: False.

No final heldout, Alibaba, or P8 access. Stops for human scientific review.
