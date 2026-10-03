# Acknowledgement — H035 v1 (exchange X-D07-S01-0002)

- proposal: `research/day-07/proposals/H035_v1.md`, sha256 `ece127cbbec41fa96bc91950add8d6604be548e9607cf85522ef91f095cfff81`
- review: `research/day-07/advisor/H035_review_v1.md`, sha256 `4f1c428d6995fc316ab8efba0df789e39ee4bf80307f531f95851b3b7b22afd7`
- decision received: **ACCEPT**. Both hashes verified by the researcher at 2026-10-03T20:53:52Z.

The researcher adopts the Execution Authorization of `research/day-07/advisor/H035_review_v1.md` and its conditions **U1–U10** as binding (allocation order and ids E045–E050, or no arming (U1); the committed pre-arming record (U2); the pre-registered dirty tree after E049/E050 (U3); unmasking events for E049 and E050 only (U4); run status (U5); the forward-risk correction (U6); objection F (U7); the U8 disclosures; formatting and upload only after a promotion that resolves objection F (U9); deferral, failure and reruns (U10)). **This proposal maps to E046 (primary, the batch's only candidate) and E048 (reproduction: equal to E046 except `purpose: reproduction`, `seed: 43`, `override: E047`).** The proposal's sentence "the ack records the mapping and the configs use the allocated ids" does not apply (U1).

## U6 (recorded in full): forward-risk correction

- The Day 3 break-even rates (0.009–0.099) are mixture-weight break-evens at fixed 2025 per-row tail gains and bulk losses. They describe a change in the subgroup's composition.
- Under a change in how the same kind of row is recorded, a row predicted at T + a(D − T) loses in expectation once its convention probability falls below a/2 (for a calibrated fit, below half its 2025 value). If the convention were absent, the loss is of the same order as the 2025 gain. The bet's stakes are of comparable size on both sides.
- H035 §Batch's "loses … only for r below the fold-wise break-even" and "under a sixth of the lowest 2025 month" are read with this qualification; Day 3 (e)'s "would lose only if the convention nearly vanished" is corrected likewise. The researcher's recommendation to the owner (INC-0015: "it would only lose if the quirk nearly vanished") repeated the uncorrected wording and is corrected by this ack; the owner is told in plain words.
- "A bet on the convention persisting" stands. Criteria 1–3, 4 and 6 have no power on the bet. **No record will quote E046's development margin as the submission's expected gain.**

## U7 (recorded in full): objection F

- The statistic is the outcome of the Day 7 phase-close access, if the phase close names it as `holdout_check.py E046 E033`.
- **WIN** resolves objection F for December only (it does not test July's seven-month distance or January's heavier delay tail, and does not discharge U6).
- **TIE** does not resolve it: H035 INCONCLUSIVE ("phase-close holdout TIE; forward bet not confirmed"); E033 stays champion; E044's file stands.
- **LOSS:** the frozen revert applies; H035 INCONCLUSIVE ("phase-close holdout LOSS, frozen revert").
- **Without an access,** objection F stands and H035 is not promotable. Objection F changes neither H009 v3's rule nor its threshold (ruling B).
