# Acknowledgement — PHASE_CLOSE_D05 v1 (exchange X-D05-S05-0001)

- proposal: `research/day-05/proposals/PHASE_CLOSE_D05_v1.md`, sha256 `ca9fff72ecc60effd757e1df132ae606cf6dfdbca3a29043bf1829073041ee00`
- review: `research/day-05/advisor/PHASE_CLOSE_D05_review_v1.md`, sha256 `4d1b8770914b97ea133a7c0f4eb672e33df6ebde435af0731b090b389d953cc5`
- decision received: **ACCEPT** (confidence 0.88). Both hashes verified by the researcher at 2026-10-02T13:14Z.

The researcher adopts the Execution Authorization as written:
1. The Day 5 decisions stand. E033 is the phase-closing champion, subject to the holdout access.
2. **Exactly one protected-holdout access,** after this acknowledgement is committed (clean tree, lock free, no `day-05` `holdout_access` line, environment unchanged):

   ```
   uv run python scripts/holdout_check.py E033 E026 --reason "Day 5 phase close (X-D05-S05-0001): phase-closing champion E033 (H023 v3) vs phase-opening champion E019, laptop instance E026 (rule L v2 item 5)"
   ```

   - **WIN or TIE:** E033 is champion; H023 v3 is PROMOTE, and E034 is PROMOTE as its reproduction.
   - **LOSS:** revert. E019 stays champion, and H023 v3 (E033, E034) is INCONCLUSIVE ("phase-close holdout LOSS, frozen revert"). No substitute comparison.
   - **Failure handling** as stated in the review.
3. **The champion change, WIN or TIE only,** as item 3 states: `CURRENT.json`, the `champion_change` event, and the disclosures (D3-C1 lineage; D3-C3 restated by D5-C16; D5-C8, D5-C9, D5-C10; the 1,000-iteration budget). D3-C2 is retired as a defect; D4-C9 is superseded for E033 by D5-C10.
4. The "Not authorized" list.

## Ruling H5 (recorded)

- The H figures are recorded only.
- **H is a joint test** of E029's D3-C2 treatment and the CatBoost half, on one draw (E031's H fit). Its outcome is not attributed to either.
- The routed `NM_missing_LIRF` rows are excluded by construction: they are bit-identical in both files.
- E026's H RMSE is recorded beside E019's 375.9272 s as an instance check. This is disclosure only.

## Standing rule 13 (recorded; from the next proposal on)

**Stochastic components.** A candidate or champion with a non-deterministic component (for example, CatBoost on GPU) reports, beside criterion 6, per development fold and twin:
- the reproduction's all-rows ΔRMSE;
- its ΔRMSE on the mechanism population;
- the RMS prediction change between the two draws.

It states that its evaluated and H figures are one draw. This is disclosure only.

## Corrections appended (D5-C8 to D5-C16; no completed record is edited)

- **D5-C8. Composition of the margin.** Beside E033 − E026 = −5.62 s:
  - −2.04 s is E029's D3-C2 treatment (E023's Day 4 margin);
  - −3.58 s is the CatBoost half;
  - on S1, +0.20 s and −4.38 s respectively;
  - the `NM_missing_other` share of the change is 0.27–0.68.
- **D5-C9. Stochastic champion.**
  - The figures are one draw.
  - The blend's re-draw is at most 0.48 s per development fold, with an RMS prediction change of 15–23 s (37 s on W1c).
  - Clause 1's W1 reading moves from WIN (E033) to TIE (E034).
  - The SUBMIT predictions will be a further draw.
- **D5-C10. Single rows.**
  - S1 is −3.76 s without row 192622644.
  - W1 is −2.56 s without row 183910286 (q90 not computed; W1 not needed for criterion 2).
  - The W1 row's prediction depends on post-validation months: W1c reverses it.
- **D5-C11. CatBoost alone is single-row carried on S1** (rule 6). E031 − E029 on S1 has a top-1 share of 0.616: −4.14 s with the row, −1.66 s without it (E032: 0.596). The R1–R3 top-10 shares are 0.64, 0.81 and 0.56. The E031 analysis omitted the rule 6 figure.
  - Finding 2 reads: "−1.69 s on all rows (q95 −0.74), W1 TIE; its S1 WIN is 62 % one row; the diffuse effect is the blend's."
- **D5-C12. Attribution and scope** (DAY_SUMMARY; rule 11):
  - (a) §1 "Its categorical statistics are the reason" is scoped to **within CatBoost at fixed capacity**: E031 against E030 on `NM_present_excl_LIRF`. It does not attribute E031's all-rows advantage over E029.
  - (b) Finding 3, "better than either half": against E031 these are point estimates only (S1 −0.23 s), neither pre-registered nor bootstrapped.
  - (c) Finding 4: the out-of-range reduction holds **for the codes arm only** (E030, < 1 h band 25). E031 has 86, E029 82 and the blend 82.
  - (d) Finding 5, "about 5× faster than on CPU", compares the Day 4 cloud CPU (4 vCPU, 0.88–1.13 s per iteration) with the laptop GPU (0.16–0.25 s). No laptop-CPU run at full combinations exists.
- **D5-C13. Missed forecasts** (added to DAY_SUMMARY §7):
  - **Advisor, H023 v3:**
    - `NM_present_excl_LIRF` −1.8 to +0.3 s → −3.96;
    - all rows −1.5 to +0.5 → −3.58;
    - against E026, −1.5 to −3.5 → −5.62;
    - S1 against E026, −0.3 to +1.8 → −4.17;
    - row 192622644, 4,500–8,000 s → 9,008;
    - H023r due, P 0.05 → due.
  - **Advisor, H021 v3:** development mean 446–458 → 440.76; runtime 28–35 min → 25.4; row 192622644 below 7,041 s, P 0.60 → 10,976.
  - **Advisor, H022 v3:** development mean 448–468 → 446.50; runtime 8–14 min → 3.7.
  - **Advisor record:** the H021–H023 reviews carried H020's "CatBoost worse and bounded" premise, and it was wrong in sign on both counts. The blend arithmetic was right on the realised inputs.
- **D5-C14. Ledger decisions.** E033 and E034 are filled per the holdout outcome. E026–E032 stay null, with their roles in `notes`.
- **D5-C15. Clerical.**
  - (a) E033's rule 12 call held E033 only, while its Validation Plan named `<H023> E029 E026`. The quoted E019 bands (83, 22, 81) come from `range_check_E023.json`; they equal E026's at non-LIRF airports (D5-C3).
  - (b) `src/prc/tracking.py` hard-codes the W&B champion lineage as {E001, E002, E005, E019}. It omits E003 and lacks E033 (mirror only; fixed after the access).
  - (c) "`prc.tracking` reads only `metrics.json`" is imprecise. It also reads `gate.json`, `config.yaml`, `resource-usage.json` and `curves.json`. None carries an H figure, so W&B cannot receive H.
  - (d) INC-0007 gets a pointer to INC-0010. The D05-S04 start line of `orchestration/session-registry.jsonl` ("swap 0") joins D5-C1's list.
- **D5-C16. D3-C3 restated for E033.** The January 2026 count fact and "H does not test it" stand. E033's development out-of-range share in the > 3 h band is 0.57 %, against E019's 15.3 %.
