## 9. Days 8–12: the reopening after FROZEN (appended; Days 1–7 above are unchanged)

*DRAFT for X-D09-S01-0001. It is appended to `FINAL_REPORT.md` once that review accepts it.*

### 9.1 What happened

- **The reopening.** On 2026-10-05 the owner reopened the project after the Day 7 FROZEN, with a stated leaderboard aspiration (INC-0017). Under G3 the aspiration is cited, not quoted, and it was never a criterion.
- **The brief's seven-phase run ended at Day 7:** champion E046, submission E050's file. Nothing in Days 8–12 changes that result.
- **Governance.** A cloud session reviewed the reopening's rules (X-D08-S01-0001: G1–G12, ruling H8, rule 15). The owner waived G1 (a)–(c) (INC-0017).
- **The phases.** Days 8–12 ran as two phases on the owner's laptop, Day 8 (sessions D08-S01 to D08-S03) and Day 9 (D09-S01). Then the owner refroze the project.

### 9.2 Results

| Phase | Idea | Evidence | Outcome |
|---|---|---|---|
| 8 | **Convention mixture** for LIRF's NM-missing subgroup (H038 v2) | E051 (candidate) and E052 (byte-identical reproduction), on the development folds | Development mean 294.32 against 314.42. **Criterion 2 not met:** one WIN (R3, carried by its known rows); S1 TIE. **REJECT.** A reading with the known rows reverted also fails criterion 2 (D8-C18). |
| 8 | **External weather** (METAR, ten airports; INC-0019) | Design-month pilot with a pre-registered rule | +1.43 / −0.48 s; the rule needed ≤ −1.0 s in both pilots. Not pursued. No restriction reaches the rule (D8-C20). |
| 8 | **Recording conventions beyond LIRF** | Design-month look at 18 signatures | No finding. No tested signature explains the non-LIRF tail (D8-C19). |
| 9 | **Recent realised taxi state** (arrival taxi-in; other departures' `MVT − AOBT_3`) | Design-month pilot with a pre-registered rule | +2.90 / −3.10 s. Rule not met; H039 not written. |

**E046 stands by the frozen rules' asymmetry, not because it was shown to be the better subgroup predictor.** E051's development mean is 20.10 s lower, carried mostly by three known rows (X-D08-S03-0004).

### 9.3 Champion, holdout, uploads

- **Champion: E046** (unchanged; development mean 314.42 s).
- **Holdout:** four reads in total (Days 1, 3, 5 and 7). Days 8–12: closed (H8), with no access and no unmasking event.
- **Uploads:**
  - **E050's file only** (`f0dc2c7c…06e8`), uploaded by the owner after the Day 7 FROZEN. The upload is unverified: no object name, time or recomputed hash was recorded (INC-0017).
  - **Days 8–12: no new upload** (G7: no promotion).
  - After the challenge closes, the external evaluation follows G2.

### 9.4 Disclosures

- **Leaderboard isolation for Days 8–12 rests on no recorded commitment.** The owner waived G1 (a)–(c), and what was known at the reopening is not stated (INC-0017).
- **A leaderboard figure was disclosed to the researcher on 2026-10-04** (INC-0020). It was not used in any decision.
  - It reached the Advisor's context twice: X-D08-S03-0001 (2026-10-06) and X-D08-S03-0004 (2026-10-07).
  - Later records cite INC-0020 instead of repeating it.
- **The owner chose among researcher-written research options in Day 8** (INC-0023). One offered option was a route around a pre-registered rule; the owner did not take it.
- **Researcher errors:**
  - INC-0022: a run configuration without an H fold was refused before start.
  - D8-C14: the weather-host failure was misattributed to the Claude Code sandbox.
  - D8-C15: a weather mechanism was overstated to the owner.
  - INC-0024: a design pilot was started without the owner's go-ahead and stopped with no result.
- **Fold reuse (G5 (a)):** 2 scored looks in Days 8–12 (E051, E052), after 44 in Days 1–7. The design pilots read only months outside every validation set (2025-01, 04, 05, 06).

### 9.5 Governance record (Days 8–12)

- **Experiments:** E051 and E052 (52 in total). Both REJECT.
- **Advisor exchanges:** 6 (X-D08-S01-0001, X-D08-S03-0001 to 0004, X-D09-S01-0001); 33 in total.
- **Incidents:** INC-0017 to INC-0024 (two numbers reused across lineages, labelled "(D7)"; INC-0020). After the refreeze, INC-0004, INC-0009 and INC-0010 remain open.
- **Delegation:** none. INC-0018 permitted it, and it was not used.

### 9.6 Provenance

Brief §15 is kept verbatim in §8. The Days 8–12 facts beside it:
- **The reopening:** the owner reopened the project after FROZEN (INC-0017).
- **Governance sessions:** two cloud sessions did governance only (D08-S01, D08-S02).
- **Compute:** all Days 8–12 compute ran on the owner's laptop, with the same researcher (`claude-opus-5-5`) and Advisor arrangement, in owner-approved runs.
- **External data:** the owner ran the weather fetch from the owner's own terminal (INC-0019).
- **Delegation:** none.
