# P3 Data and Figure QA

- Dataset profiled: `results/p3/stage_records.csv` (5,184 rows, 53 columns).
- Balance: each of 8 scenarios has 648 records; each of 3 centers and 3 seeds has 1,728 records; no missing values were found in the primary outcome fields.
- Distribution warning: loss and re-instantiation-gain variables are strongly skewed. P3 therefore reports raw rows, center summaries, and center-cluster bootstrap summaries rather than relying on a Gaussian effect interpretation.
- Figure encoding: Okabe–Ito colors plus distinct line styles and point markers; no rainbow palette, dual y-axis, or truncated outcome axis.
- Programmatic QA: both publication PNGs passed the strict 600-DPI checker.
- Visual QA: preview and grayscale variants were inspected; labels, legends, stage-9 reference, zero line, panel alignment, and grayscale distinguishability passed.
- Interpretation boundary: shaded bands are exploratory normal-approximation intervals across 3 centers × 3 seeds at each stage. They are not final uncertainty intervals.
