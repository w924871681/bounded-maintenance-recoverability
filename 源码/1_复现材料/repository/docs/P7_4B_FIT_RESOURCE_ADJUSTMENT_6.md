# P7.4B Fit Execution Resource Adjustment 6

## Trigger and derived count

After authorized QQMusic and Weixin/WeChat processes were closed, the
one-worker P7.4B Fit continuation had two consecutive healthy samples with
5.97 GiB and 3.77 GiB available physical memory. The active worker used about
0.49 GiB private memory, stderr was empty, and valid receipts continued to
grow.

Across both samples, four total workers are the largest count that predicts at
least 2.0 GiB remaining memory using the conservative second sample. Four
workers also predict about eight occupied physical cores, below 90% of the 14
physical-core limit. With 153 Fit trajectories remaining, the expected saved
runtime exceeds restart cost.

## Procedure

Stop only the verified P7.4B Fit process tree rooted at PID 29656. Preserve
and hash-check every complete trajectory, scale, and integrity receipt,
confirm no orphan remains, and resume the identical seed-bound command with
four workers and new timestamped logs:

`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py fit-materialize --workers 4`

The runner skips only complete hash-valid receipts. This execution-only change
does not alter any scientific degree of freedom. Downscale if two consecutive
samples fall below 1.5 GiB or resource failure repeats. No Validation, final
heldout, Alibaba, or P8 access is authorized here.
