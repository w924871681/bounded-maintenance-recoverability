# P7.4B Validation Execution Resource Adjustment 1

## Trigger and derived count

P7.4B Validation began conservatively with one worker after the committed Fit
freeze and one-time Validation opening. After the serial causal-reference
construction completed, two consecutive healthy materialization checks showed
3.29 GiB and 2.97 GiB available physical memory. The worker used approximately
0.45--0.46 GiB private memory and about two CPU cores, stderr was empty, and
complete integrity receipts increased from three to six.

Adding two workers predicts approximately 2.05 GiB available-memory reserve
from the conservative second sample. Three total workers predict about six
occupied physical cores, below 90% of the 14-core limit. A fourth worker would
reduce the predicted reserve below 2.0 GiB. With 282 Validation trajectories
remaining, the expected runtime saving exceeds restart cost. Three workers are
therefore the largest count authorized by the current phase-specific samples.

## Procedure

Stop only the verified P7.4B Validation process tree rooted at PID 24600.
Preserve and hash-check every complete trajectory, scale, and integrity receipt,
confirm that no matching parent or worker remains, and resume the identical
seed-bound command with three workers and new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py validation-materialize --workers 3`

The runner skips only complete hash-valid receipts. This adjustment changes
wall-clock execution only. It does not modify the frozen behavior path, A0/A1
representations, centers, seeds, scenarios, Fit pipelines, scales, metrics,
thresholds, or STOP rules. Downscale after two consecutive available-memory
samples below 1.5 GiB or repeated worker/resource failure. No final heldout,
Alibaba, or P8 access is authorized.
