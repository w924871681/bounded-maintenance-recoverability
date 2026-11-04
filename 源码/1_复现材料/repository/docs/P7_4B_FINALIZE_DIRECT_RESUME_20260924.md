# P7.4B Finalize Direct-Resume Execution Amendment — 2026-09-24

## User direction and current condition

After the low-memory finalize stop recorded in
`P7_4B_FINALIZE_RESOURCE_RECOVERY_20260924.md`, the user explicitly directed:
"直接恢复即可" (resume directly). This supersedes that record's additional
conservative 4.5 GiB pre-launch waiting margin. It does not alter the
established 1.5 GiB available-memory runtime stop boundary or any scientific
protocol, frozen input, outcome rule, or heldout restriction.

At the time of this amendment, no P7.4B process was active. All 288 Fit and
288 Validation receipts remained materialized, and the eight intermediate
output hashes matched the prior user-pause record. Available memory samples
were approximately 1.465, 1.789, and 1.066 GiB. Starting a process while
available memory is already below the 1.5 GiB runtime stop boundary would
immediately recreate the resource failure, so no new finalize process was
launched at those readings.

## Direct-resume condition

For the single finalize process, conservatively budget 0.8 GiB and retain at
least 1.5 GiB available after launch. Once two fresh readings at least ten
seconds apart both show at least **2.3 GiB** available memory, resume promptly
without the previous fifteen-minute stability wait. Before launch verify no
matching P7.4B process, frozen preflight, all 288 complete Validation receipts
and A0/A1 stagewise path equality, and the eight saved intermediate-file
hashes. Run only the exact frozen command with new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py finalize`

Check memory and stderr immediately after launch. If available memory remains
below 1.5 GiB on two consecutive checks, stop only the verified P7.4B process,
preserve files, and document the event separately. Never close WeChat/Weixin,
QQMusic, or another application. Never modify scientific files or access
heldout centers 33000–33019, Alibaba, or P8. No P7.4B scientific verdict has
yet been produced.
