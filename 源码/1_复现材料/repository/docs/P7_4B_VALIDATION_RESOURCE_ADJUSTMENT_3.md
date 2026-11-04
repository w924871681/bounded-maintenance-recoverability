# P7.4B Validation Execution Resource Adjustment 3

## Trigger

After the mandatory three-to-one-worker downscale, two post-stop memory samples
were 2.42 GiB and 2.37 GiB. The identical seed-bound Validation command was
therefore attempted with one worker. Once the parent and worker were resident,
available physical memory measured 1.44 GiB and then 1.40 GiB and 1.21 GiB on
two consecutive follow-up samples. This remained below the 1.5 GiB stop
threshold even at the minimum worker count. Stderr was empty.

The one-worker process tree rooted at PID 25592 was stopped immediately. No
matching P7.4B parent or orphan worker remained. Exactly 25 complete Validation
trajectory, scale, and integrity receipts were preserved and their SHA-256
values and integrity flags were revalidated with zero failures. Available
memory recovered only to about 2.02 GiB after the process stopped.

## Deferred recovery

Do not launch another Validation process under the current external-memory
condition. Resume the identical seed-bound command with one worker and new
timestamped logs only after two fresh stable pre-launch samples predict at
least 1.5 GiB available memory after accounting conservatively for the parent
plus one worker footprint (about 0.8 GiB):

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py validation-materialize --workers 1`

Before launch, verify that no matching process or orphan worker exists and
revalidate all preserved complete receipts. The runner skips only complete
hash-valid receipts. Any later worker-count change requires a new separate
Git-bound execution record. No frozen scientific input is modified, and no
final heldout, Alibaba, or P8 access is authorized.
