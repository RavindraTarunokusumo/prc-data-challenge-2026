# Acknowledgement — PHASE_CLOSE_D07 v1 (exchange X-D07-S01-0003)

- proposal: `research/day-07/proposals/PHASE_CLOSE_D07_v1.md`, sha256 `5c5011cc144e4a0f4fd469cfceafdd49f0bebce6b881d33ed00cd44bb722dd63`
- review: `research/day-07/advisor/PHASE_CLOSE_D07_review_v1.md`, sha256 `f65bae13f9294ec8b3c3b9ea3fe43404a58d75f25569afe7a115818fb96fe14e`
- decision received: **ACCEPT** (0.85). Both hashes verified by the researcher at 2026-10-04T17:57:28Z.

The researcher adopts the review's Execution Authorization, **P1–P9**, as binding, and ruling **H7**.

## The access (P1, P2)

Exactly once, after this acknowledgement is committed and pushed, from a clean tree with the lock free, no `day-07` `holdout_access` line, E046 and E033 COMPLETE, and the rule L v2 item 6 environment unchanged:

```bash
uv run python scripts/holdout_check.py E046 E033 --reason "Day 7 phase close (X-D07-S01-0003): phase-closing candidate E046 (H035 v1) vs phase-opening champion E033; objection F (U7 of X-D07-S01-0002)"
```

P2: `rmse_reference` must equal 369.1811742636602 s within 1e-9 s, or stop (recovery review). Failure handling as item 2 of the review.

## P3 (outcome mapping, U7 unchanged)

WIN: H035 promoted (E046 PROMOTE, E048 PROMOTE; CURRENT.json new record with history; `champion_change` event; the standing disclosures listed in P3). TIE or LOSS: E046 and E048 INCONCLUSIVE with the fixed wording; E033 stays champion; E044's file is final; E049 and E050 recorded "never run (not needed: H035 not promoted)"; no substitute comparison; INC-0015 closes.

## P4 (recorded in full; the only new pre-registration)

- **Under WIN, the final file is `predictions/final/E050/submitting.parquet` if and only if all hold:** E049 and E050 COMPLETE within class; `route_check.py E050 E044 E049` passes; `make_submission.py E050 E044 E049 --ref E046 E033 E045 --tag E050` passes I1–I5; no flag analysis is open and none found a defect (S6).
- **In every other case E044's file is final**, including no owner window (or the owner declining one), INVALID, a failed check, or a RESOURCE_FAILURE/TIMEOUT whose single U10 rerun fails or is not run. E046 then stays champion, and CURRENT.json, STATE and the final report say plainly that **the submitted file implements E033's procedure, not the champion's.**
- **Nothing else may select between the two files:** not U8 (b)'s per-month exposure, not E050's flag reading (non-blocking unless a defect is found), not any H figure.
- A fix by a new proposal version needs a new Advisor review before FROZEN; this review authorizes none.

## P5–P9

- **P5:** under WIN only, a new incident before the E049/E050 window, stating the owner-set window and either (a) a new pinned launcher derived from `run_window_2.sh` (diff limited to date, window, log name and queue) or (b) a committed checkpoint script; tree state, unmasking, freeze, environment and window arithmetic (about 100 s of W&B overhead per run) as stated.
- **P6:** E050's SUBMIT flag: a ranking month flags if its subgroup share above 3,600 s is below 0.226 or above 0.981 (non-blocking). U8 (b) per month is disclosure only. Before any upload the owner receives U6 in plain words and every flag analysis.
- **P7:** FROZEN as proposed, plus (a) appended manifest fields (producing command, formatter-run code commit, `make_submission.py` SHA-256, creation time), never by editing `SUBMISSION_RECORD*.json`; (b) a content-neutral PR into `main`; (c) after FROZEN only appended files; (d) the owner's single upload, the hash recomputed immediately before it, an appended upload record; the researcher neither uploads nor reads the leaderboard; (e) under WIN, FROZEN only after P4 decides the file; (f) FROZEN is enforced by records only.
- **P8 (ruling H7):** the Day 7 access decides U7 only; H figures are otherwise recorded only; no substitute comparison; **the project's last H read** (no audit of the result); under WIN neither E046's development margin nor its H ΔRMSE is quoted as the submission's expected gain or error; the H figure is labelled "December 2025, E046 against E033, one access"; H does not test the SUBMIT procedure, July's seven-month distance, or January's tail.
- **P9:** INC-0014 closes now. INC-0015 closes under TIE/LOSS with these records, under WIN when E049/E050 are COMPLETE or P4's fallback is invoked. INC-0004, INC-0009, INC-0010 stay open and are listed in the final report. DAY_SUMMARY and FINAL_REPORT are marked FINAL only with D7-C1 to D7-C13 applied.

## Corrections appended (D7-C1 to D7-C5: DAY_SUMMARY §7; D7-C6 to D7-C13: the review)

- **D7-C6.** STATE's "Updated 2026-10-04T17:45Z" was pre-written; its commit `4fc1678` is 17:33:38Z. Later STATE updates carry measured times.
- **D7-C7.** Forward support: the 2025 maximum subgroup q90 is July 2025's 14,939 s, not 13,865 s. July 2026 (14,945 s) is at the 2025 maximum (above by 6 s at the nearest rank; below by linear or lower interpolation). Only January 2026 lies above every 2025 month (17,816 s nearest rank; 19,592 s linear). The share of subgroup rows more than 1 h late is 81–96 %, not 81–94 %. "Both ranking months … above every 2025 month" reads "January 2026 above every 2025 month; July 2026 at the 2025 maximum". This corrects the E046 analysis U8 (a), the journal's E046 entry and DAY_SUMMARY §4.
- **D7-C8.** Final report §3 under rule 11: Day 3's −6.75 s is the mechanism figure on `NM_present_excl_LIRF`; congestion as served is −1.90 s on all rows (q95 −0.98; R1, R2 TIE; criterion 3 fails at EHAM +7.2 %), and 95 % of E019's margin over E005 was routed FS1 structure (D3-C1). Day 4's −0.3 s is the restricted figure (−0.29 s, q95 +0.12, S1 TIE, W1 LOSS, mechanism falsified); all rows −0.40 s (q95 −0.03).
- **D7-C9.** Final report §3, Day 6: D6-C12's wording replaces "seven controls found nothing contradicting E033".
- **D7-C10.** Final report §1 and §8, provenance: Sonnet delegation (INC-0005, INC-0013), launch-argument discrepancies (INC-0003, INC-0004), the owner's choice in INC-0015; phase-close reviews follow their phase's runs; brief §15 kept verbatim with these facts beside it.
- **D7-C11.** Final report §2, criterion 2: at least 3 WIN among the 5 development folds; S1 WIN; no development-fold LOSS; an S1 or W1 WIN counts only if its causal twin is not LOSS.
- **D7-C12.** `SUBMISSION_RECORD.json` lacks the code commit, creation time and reproduction command (DATA_POLICY §3); P7 (a) appends them for the final file.
- **D7-C13.** Final report outcome branches (§4, §5, §7) as the review states.
