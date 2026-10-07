# Acknowledgement: H038 v2 (exchange X-D08-S03-0002)

*Written 2026-10-06T20:10:51Z (measured with `date -u`).*

- **Proposal:** `research/day-08/proposals/H038_v2.md`, SHA-256 `3104c018121e46b1a7ba7aafcd453b5781ebe0da41d538ac38ffe9b50cfc294c`.
- **Review:** `research/day-08/advisor/H038_review_v2.md`, SHA-256 `cab179656000b329e4b58d208c0c9cf187b351483863610f072c966382a238af`.
- **Decision received: ACCEPT (0.80).** The researcher verified both hashes, and the launcher's (`54ee5ab8b120530b7f6eaa83e3efc5ceb046ee1be6c650c656f68ce58208b92d`), at 2026-10-06T20:10Z.
- **Mirror:** `orchestration/advisor-exchanges/X-D08-S03-0002/` (`envelope.yaml`, `response.md` verbatim, `checksums.sha256`).

## Rulings adopted as binding

**(G) Criterion 4's decisive reading is the proposal's sign test.**
- On each development fold where the subgroup's SSE change against E046 is negative, `subgroup_sse_change_convention` must also be negative.
- The frozen tool's `criterion4_reading_a` boolean (`CONV_SHARE = 0.5`) is a different rule. It is reported as **"the majority-share reading"** and decides nothing.

**(E)(vi) The no-LOSS condition under the known-row reading.**
- Suppose criteria 1–3 pass as frozen, but some development fold is LOSS once its known rows are reverted (`reverted.fold_outcome_counted` in `E051_vs_E046_known_rows.json`).
- Then G5's consequence applies: INCONCLUSIVE, never uploaded.
- The tool's `g5_consequence` flag does not compute this case. The phase close reads it from the JSON.

Rulings (D) and (E) of X-D08-S03-0001 stand (ack v1).

## Corrections (appended; no proposal is edited)

- **D8-C11. The label of reading (a).**
  - `scripts/mixture_analysis.py` names the majority-share rule `criterion4_reading_a`, and `tests/test_known_rows.py` calls it "Criterion 4 (a) of H038 v2". H038 v2 did not adopt that rule: it restated the claim, and its reading (a) is the sign test (ruling (G)).
  - Ack v1's "Revisions for v2" item 2 ("a decisive convention-row reading") describes the option v2 did not take.
  - The tooling stays frozen and unchanged. The analysis reports the boolean under its correct name.
- **D8-C12. Four minor slips in H038 v2.**
  - After the known-row reversion, W1 has 14 bulk and 43 tail rows, not 13 and 43.
  - The components path is `predictions/validation/<EID>/components/`, not `predictions/val/`.
  - The configs carry `proposal_version: 2`. § Proposed Change still shows the 1 carried over from v1.
  - The launcher's header comment still says "v1". The launcher is pinned, so it is not changed.

## Authorized scope (from the review)

- **Allocation:** `gate.py allocate H038 v2` (primary), then `--purpose reproduction`. The pinned launcher hard-codes **E051** and **E052**, so the allocation must yield exactly those IDs.
- **Configs:** exactly § Proposed Change of H038 v2:
  - `model: convention_mixture`, `feature_set: FS2`;
  - params as the `mixture` section of `H038_params.yaml` (`b22c02c1…`);
  - folds R1, R2, R3, S1, W1, S1c, W1c; CLASS-M;
  - seed 42 for E051; seed 43 with `purpose: reproduction` for E052;
  - `proposal_version: 2`.
- **Execution:**
  - only through `research/day-08/sessions/D08-S03/run_window.sh` (`54ee5ab8…`);
  - **armed only on the owner's go-ahead** (INC-0021), with END = START + 30 minutes;
  - queue E051 then E052, guards 840 s, one run at a time;
  - `mixture_check.py EID E046` after each run. A FAIL makes the run INVALID.
- **Analysis**, after the queue and from a clean tree:
  - H038 v2 § Validation Plan, on development and diagnostic folds only;
  - the readings under (G) and (E)(vi);
  - the rule 15 (G5) tables;
  - the INC-0017 and INC-0020 disclosure lines.
- **Freeze from `ce89aeb`:** no change under `src/`, `scripts/` or `config/`, and none to `pyproject.toml`, `uv.lock` or the launcher, until the batch's last comparison.
- **Not authorized:**
  - any H fold, holdout script or December target read;
  - any refit, rerun with changed parameters, added fold or other experiment;
  - any SUBMIT fit, formatter or upload;
  - any run outside the owner's window;
  - any change to a model component after results are seen.
- **A deferred E052 leaves criterion 6 open:** nothing is promoted until it runs.

## Appended (2026-10-06T21:28:44Z): the owner's window

The owner changed the run window to at most 2 hours, still starting only on the owner's go-ahead (INC-0021 amendment). The scope line "END = START + 30 minutes" above now reads **END = START + 2 hours**. Nothing else in the scope changes.
