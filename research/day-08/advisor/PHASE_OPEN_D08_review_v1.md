---
schema: advisor-review-v1
hypothesis_id: PHASE_OPEN_D08
proposal_version: 1
proposal_sha256: 6c91822f5a6d5456575f3f65f83b8a4b06a2078e909852aa934dba4db4ee1a3b
exchange_id: X-D08-S01-0001
advisor: advisor-subagent
advisor_model: claude-opus-5-5
advisor_policy: advisor-policy-v3.0
decision: ACCEPT
confidence: 0.80
created_utc: 2026-10-05T09:51:30Z
---

# Advisor Review

## Summary Assessment

**Decision: ACCEPT (0.80).** The acceptance carries binding conditions G1–G12, ruling H8, rule 15 as amended (G5), and corrections D8-C2 to D8-C6.

- Reopening for Days 8–12 is admissible as an owner-decided protocol deviation (INC-0017).
- Research resumes only after G1's preconditions are committed.
- This review authorizes no allocation, run, holdout access or upload.

**Answers to the three questions.**
- **(c) Hedges are inadmissible under any ranking rule.**
  - At most one new file is uploaded: the refreeze's file, and only if a candidate is promoted.
  - No Day 8–12 decision depends on the ranking rule, so no one confirms it before that upload (G2).
- **(d) H stays closed for all of Days 8–12 (ruling H8).** No access is granted now, and no later Day 8–12 review may grant one. H7 stands.
- **(e) Rule 15 is adopted, amended (G5).**
  - It counts every development-fold look, not only candidates.
  - It adds a discovery-footprint disclosure, with a consequence pre-registered now.

**What the proposal gets right.**
- It refuses to make the owner's "< 250 s" a criterion, a stopping rule or a mapping.
- It treats five uploads a day as a test-set query budget, and it bans intermediate uploads.
- It keeps H closed by default.
- It names fold reuse as the main risk of a five-phase push.
- It keeps compute off this container, whose ledger is stale (verified below).

**What this review adds: eight findings, all settled by conditions.**

1. **The owner's commitment is placed in the researcher's acknowledgement, and it ends at the refreeze.**
   - The acknowledgement is the researcher's file. It cannot carry the owner's word.
   - Ending at the refreeze leaves two channels open:
     - The owner could read E050's figure between the refreeze and the final upload, and then decide whether to upload. That makes the upload decision leaderboard-guided.
     - The owner could upload again after seeing the final file's figure. "Nothing is overwritten" does not prevent a re-upload of E050's file under a new version number.
   - G1 (a) closes both channels, in the owner's own words.
2. **The planned single upload is itself a two-file exposure.**
   - E050's file is already in the bucket, and nothing is overwritten.
   - Under a "best submission" rule, any new upload makes the ranked figure the better of two files.
   - The proposal treats the hedge question as a question about a third file only (G2).
3. **(c) would have the owner confirm the ranking rule on the page that carries the leaderboard.** That contradicts (c)'s own blindness requirement. The rule changes no Day 8–12 decision, so it is not confirmed before the final upload (G2).
4. **P7 (d) of X-D07-S01-0003 is unmet.**
   - The upload record lacks the upload time, the object name and the hash recomputed at upload.
   - Two different files share the name `submitting.parquet`: E044's (`predictions/final/`) and E050's (`predictions/final/E050/`).
   - So which file is in the bucket is unverified. (g)'s fallback, "E050's upload stands", rests on it (G1 (c)).
5. **"No score yet" does not establish that the owner has not viewed the leaderboard.**
   - The answer is consistent with the owner having looked and found no figure for E050.
   - The basis of the 250 s figure is unrecorded (G1 (b)).
6. **H's closure is enforced by records only.** `gate.py` records the phase from the proposal's directory. `evaluate.holdout_compare` would therefore permit one access in each of `day-08` to `day-12` (H8).
7. **Rule 15 as proposed counts candidates only, and it says nothing about how a mechanism was found.**
   - A five-phase push toward a target fails through mechanisms designed on the validation months' tail rows.
   - Those few rows decide each fold's RMSE, and the paired bootstrap cannot detect design on them (G5).
8. **§3's plain-words reading of the champion's error is wrong in three places, and each bears on the agenda** (D8-C2 to D8-C4):
   - LIRF's high bulk RMSE is largely E046's own subgroup cost.
   - The recording convention is specific to LIRF (Day 1).
   - W1's tail, in the January-analogue fold, is mostly LTFM.

**Verified here (read-only).**
- **Hashes.**
  - The proposal matches the envelope (`6c91822f…4ee1a3b`).
  - It was committed with the envelope, INC-0017, INC-0018 and the upload record in `66e8296` (09:35:18Z). It is unchanged since.
  - `.claude/agents/advisor.md` is `30fff5dd…0d19`, as in `config/agents.yaml`.
  - The six frozen files match `config/frozen.json`.
- **Tree.**
  - P7 (b) holds: `git diff 4c21eff 88cdb22` is empty, so the merged tree equals the FROZEN tree.
  - Nothing under `src`, `scripts`, `config`, `pyproject.toml`, `uv.lock`, `.claude` or `tests` changed after `88cdb22`.
- **Task ledger.**
  - It holds four `holdout_access` lines: `day-01`, `day-03`, `day-05` and `day-07`, the last at 2026-10-04T17:57:38Z.
  - The `frozen` event (22:05:46Z) is the last event. Nothing was allocated, run or reopened after FROZEN.
- **Ledgers and IDs.**
  - `experiments/ledger.jsonl` ends at E050.
  - This container's `runtime/ledger.sqlite` is git-ignored. Opened read-only, it holds 24 rows, E001–E024. An allocation here would reissue E025, so (f)'s ban is necessary. E051 is the correct next ID on the laptop.
- **Prediction files.** `predictions/final/` is empty here, so E050's file and its hash cannot be checked in this container.
- **§3's table, recomputed from `experiments/E046/metrics.json`.**
  - Every cell matches: all-rows RMSE, the ≥ 3,600 s shares, the LIRF share, wake `UNK` and the worst bulk airport.
  - LTFM is 34 % of W1's SSE, as stated.
  - Wake `UNK` is `WK_TBL_CAT_flt` filled with "UNK" when null (`prc.metrics`), so it is a fair NM-missing proxy.
- **Development-fold scores.** 44 of E001–E050 have them.
  - E025 is a RESOURCE_FAILURE.
  - E042–E044, E049 and E050 are SUBMIT fits without fold scores.
- **H records.** They hold aggregates only: two RMSEs, ΔRMSE and quantiles.
- **What I did not do.**
  - No target column, block-time column or December data was read.
  - No fit, score, holdout script or formatter was run.
  - No web page, leaderboard or bucket was accessed.
- **Secrets.** No credential pattern appears in the files committed in `66e8296`.

## Scientific Validity

### (a) Reopening

- **Admissible as a deviation.**
  - Brief §1 lets the owner start, stop or recover the run, and brief §3 defines seven phases.
  - Extending the run is a scope decision that only the owner can make, and INC-0017 correctly records it as a deviation.
  - It does not defeat the research question, provided two separations hold:
    - the seven-phase result stays intact and identifiable (E046 champion, E050's file, the Day 7 records unchanged; G8);
    - the leaderboard stays out of every Day 8–12 decision (G1–G3).
- **The risk lies in the motive, not in the extension.**
  - The owner states a threshold target on a metric no one in the run may read.
  - When the expected score sits above a threshold, a threshold target rewards variance: bets with large downside look attractive.
  - §3 and §4 already point the agenda at the tail, "where U6's forward risk lies".
  - G3 and G5 keep promotion on development evidence. Forward exposure stays a disclosure that the Advisor weighs, not a gamble that the target justifies.
- **The deadline relaxes nothing.** If nothing is promoted, E050's upload stands. That safe default removes any pressure to promote.

### (b) Leaderboard isolation in a reopened run

The researcher is isolated by rule. The owner is the only person who can see the board, and the owner also directs the run: windows, go and stop, uploads.

| Channel | Proposal | Gap | Closed by |
|---|---|---|---|
| The owner reads E050's figure during Days 8–12 | owner commitment, placed in the researcher's ack, until the refreeze | not in the owner's words; covers neither qualitative relays nor organiser e-mail | G1 (a) (i), (ii) |
| The owner reads E050's figure between the refreeze and the final upload, then decides whether to upload | not covered | the upload decision becomes leaderboard-guided | G1 (a) (i), (iii) |
| The owner re-uploads E050's file, or reopens again, after seeing a figure | "exactly one new file" | a re-upload under a new version number, or a further reopening, is not excluded | G1 (a) (iv) |
| Two files ranked under a "best" rule | asked only for a third (hedge) file | the single final upload already creates this | G2 (disclosure) |
| The owner confirms the ranking rule on the page that holds the board | the condition for a hedge | exposure before the final upload | G2 |
| The owner's target comes from board content | not asked | the target's provenance is unknown | G1 (b) |
| The owner chooses between candidates (INC-0015 type) | not addressed | target-guided selection | G3 |
| The researcher reads a challenge page | the index page was read on 2026-10-05 | its content is not recorded | G3 |

**The hedge question.**
- Uploading E044's file beside E050's, or any non-promoted file, adds nothing to the method. It buys a second draw from the test set, and the organiser's rule then keeps the better draw.
- That is selection on the test set. Brief §1 ("no leaderboard-guided optimisation") and LEADERBOARD_POLICY ("submit once") exclude it. Selection by the organiser's rule instead of by a person reading a figure changes nothing.
- It would also inflate the external evaluation that the final report sets against the research question.
- The ranking rule does not matter. Under "latest", a hedge is pointless. Under "first", it is void. Under "best", it is exactly this contamination.
- **Ruling: inadmissible** (G2).

**The single final upload** is the price of reopening.
- Under a "best" or unknown rule, it is unavoidably a two-file exposure.
- It is admissible because the upload decision comes from development evidence only, and because the default is no upload.
- The external evaluation must record it as a possible best of two (G2, G8).

### (c) The holdout: why H stays closed (ruling H8)

**Information state.**
- H has been read four times, each time by a pre-registered phase-close comparison.
- Its marginal distribution was read before the freeze (DATASET_AUDIT §6.6).
- The recorded results are aggregates only. Statistically, H is still usable.

The case for closing it rests on four other grounds.

1. **H7 is less than a day old, and no evidence has changed since it was made.** Only the owner's wish for a better score has changed. Reversing a ruling because of the reason for a push is the drift that the governance exists to prevent.
2. **H has little power where the agenda points.**
   - The likely Day 8–12 mechanisms act on a few hundred tail rows per month.
   - On Day 7, the exposure of 88 subgroup rows, Σ(E046 − E033)², was 53 % of E033's whole-month H SSE, and the top day carried 0.29 of it.
   - A fifth read would be decided by a handful of December rows and days.
   - December's subgroup delay tail is ordinary (X-D07-S01-0003 (e)). A tail mechanism would be tested for one month of persistence, never for 2026 (H7: "What H does not test").
3. **The figure would sit next to the target.**
   - E046's December RMSE, 244.94 s, is already below 250.
   - The owner would read any further H figure against "< 250 s", whatever its label. Once such a number exists, (b) cannot prevent that reading.
4. **A later grant would be post hoc.** If the door stays open until the last phase close, the decision to read H is made with the Day 8–12 results in view.

**The price, stated plainly.**
- A Day 8–12 file, if uploaded, will have had no out-of-sample check outside the development months.
- The defences:
  - criteria 1–8;
  - rule 15 with its pre-registered consequence (G5);
  - H8's statement that an objection of objection F's type cannot be resolved;
  - the default of no new upload.
- The asymmetry is right: the status quo is a file whose champion won on December.

### (d) Development-fold reuse

**The count.**
- 44 of E001–E050 have development-fold scores.
- Many more analyses have read fold targets: the tail-mechanism studies, Day 1 (c), the rule 6 row audits and U8.

**Why the count is not the main danger.**
- Under the null, a single candidate rarely passes criteria 1–2. It needs an S1 WIN at q0.90, two more WINs and no LOSS, plus a mean gain of at least 1.0 s with q0.95 < 0.
- With 15–20 looks, multiplicity matters, but it is bounded.
- The larger danger is design on the evaluation rows.
  - 0.14–0.53 % of rows carry 20–65 % of each fold's SSE (§3).
  - A mechanism shaped by looking at those rows will WIN on the same rows. This covers the choice of anchor, threshold, airport or day.
  - The cluster bootstrap measures the sampling noise of a fixed rule. It does not see how the rule was selected.

**The project's own precedent.**
- On Day 7, the development folds carried "no confirmatory weight" for H035, because they re-measured a contrast recorded on Day 3. H settled it (objection F, U7).
- With H closed, the same situation must be caught before the run, in the proposal's review. G5 (c) does this: the footprint is declared, and its confirmatory weight is ruled before allocation.

**What stays legitimate.**
- Aggregate residual analysis on development folds (by airport, band or segment), as in §3 and in Day 1 (c).
- Fold-local fitting of any parameter (DATA_POLICY §5 and §9).
- Design on months that lie in the training part of every fold the candidate is evaluated on (DATA_POLICY §5). January and April–June 2025 qualify for all five development folds. March is embargoed for W1, and August for S1.

### (e) The §3 evidence

The table is exact (Summary). The plain-words reading is not:

| §3 statement | Record (recomputed from recorded metrics) | Correction |
|---|---|---|
| bulk "about 180–310 s by airport, except LIRF" | non-LIRF bulk RMSE is 149 s (W1 LEBL) to 309 s (W1 LTFM) | D8-C2 |
| "LIRF (bulk 297–710 s by fold)" | 279 s (W1) to 710 s (S1). §3's own table already implies that W1's LIRF bulk is below LTFM's 309 s | D8-C2 |
| (implied) LIRF's bulk error is hard taxiing | E033's LIRF bulk is 273–374 s. E046's increase over it, which is the subgroup's bulk cost (rule 12; the criterion 8 statistic), is R1 45 %, R2 19 %, R3 16 %, S1 72 % and W1 5 % of E046's LIRF bulk SSE | D8-C2 |
| "Many of those are recording conventions" | The convention is specific to LIRF. Outside LIRF, 0–16.7 % of tail rows are block-at-schedule, at or below the base rates of 11.1–19.4 % (PHASE_CLOSE_D01 review (c)). LIRF holds 12–68 % of each fold's ≥ 3,600 s rows: W1 88 of 763 (LTFM 615); R3 77 of 223 | D8-C3 |
| "Fifty experiments have been scored on the same seven folds" | 44 | D8-C4 |
| the heading "What this means for the owner's aspiration" | it relates development figures to the leaderboard target by juxtaposition | D8-C5 (G3) |

### (f) The agenda against the record (non-binding; notes for later reviews, G9)

1. **Item 1 is ranked first "by share of squared error", but a segment's SSE share is not the SSE a mechanism can remove.**
   - Its premise, conventions beyond LIRF, is the question Day 1 (c) answered for block-at-schedule: outside LIRF, the in-tail rate is at or below base rates.
   - Other anchors have not been examined.
   - Its forward hazard is D3-C3: 435 non-LIRF NM-missing January rows with `d_sched` > 3 h and 92 above 5 h, 2.0–2.6 times the 2025 maximum. A mixture that predicts `takeoff − anchor` on those rows meets the largest per-row stakes in the ranking months.
2. **Item 2's development cost is measurable.**
   - Its subgroup bulk rows are predicted at hours, which is 5–72 % of E046's LIRF bulk SSE.
   - It is judged like any other candidate. "Lowering the downside" in 2026 is not a promotion ground.
   - A candidate that gives up development RMSE to reduce forward exposure re-adjudicates U7 and P4 (rule 10).
3. **Item 3.** W1's ≥ 3,600 s rows are 81 % LTFM (615 of 763). External data needs:
   - an owner decision recorded as an incident;
   - an allowlisted host;
   - DATA_POLICY §7.
4. **Item 4.**
   - The recorded −0.73 s comes from the CatBoost half's own curve. In the 0.5/0.5 blend, its all-rows effect is expected to fall below criterion 1's 1.0 s minimum.
   - An iteration count read off validation-fold curves is selection on the folds (G5 (c)).
   - It is unlikely to be worth a phase.

## Novelty Relative to Existing Research

- This is a governance request, and nothing runs.
- No earlier exchange governs a reopening after FROZEN, so it is not redundant.
- The nearest precedents:
  - P7 (the FROZEN definition);
  - ruling H7;
  - rule L v2 (environment binding);
  - INC-0015 (an owner choice among researcher-written options).
- The agenda's novelty against the record is in (f) and G9.

## Experimental Isolation

Not applicable as an experiment. For the governance:
- **Reference.** Each Day 8–12 candidate is compared with E046 under rule R.
- **The draw spread.** E046's draw analogues differ from E046 only off the LIRF NM-missing subgroup: they are E034 or E041 with E045's subgroup rows. Rule 15 (b)'s spread can therefore be computed from stored predictions on the laptop, with no new run.

## Validation Quality

- **Nothing frozen changes:** the folds, the metric, the bootstrap and the thresholds. The six frozen hashes are intact.
- **Promotion** rests on the development folds under criteria 1–8 and standing rules 1–15. Each Day 8–12 proposal pre-registers per-fold predictions, and misses are kept.
- **Holdout.** Each Day 8–12 phase close records "H: closed (H8)". The frozen phase-close design allows non-use, as Days 2, 4 and 6 recorded. Its LOSS-revert mechanism therefore does not operate in Days 8–12, and G7's default (no new upload) stands in for it.
- **Fold reuse** is disclosed (G5 (a), (b)). Its design channel is ruled before allocation (G5 (c)).

## Leakage Review

### Target Leakage

PASS

- Nothing is fitted or changed.
- This review read only recorded metrics and comparison files. No target column, block time or December data was read.
- SUBMIT fits may still unmask December targets for training only, as logged events (H8).

### Temporal Leakage

CONCERN

This is not blocking.
- **Design-level fold leakage is the Day 8–12 risk.** Item 1 proposes to characterise "on the folds", and item 4's iteration count could be read off validation curves.
- G5 (c) handles both, per proposal and before allocation.
- The T-label channel (`d_sched`, `MVT − AOBT_3`) stays admissible under rule 8.

### Competition Availability

CONCERN

This is not blocking, given G1.
- **Leaderboard isolation now rests on the owner's recorded commitments,** enforced by records only.
- **The ranking rule is unknown.** It is not needed (G2).
- **E050's upload is unverified** (G1 (c)).
- **External data** (item 3) needs DATA_POLICY §7, and its permission check must not expose anyone to ranking content.

## Compute Review

### RAM

PASS

No compute is authorized. Laptop runs are authorized only by later reviews.

### Runtime

PASS

None.

### Disk

PASS

One review file.

## Weakest Assumption

**That the reused development folds still carry confirmatory weight for mechanisms found during a five-phase push toward a target, with no out-of-sample check.**
- 0.14–0.53 % of rows carry 20–65 % of each fold's SSE.
- E046's dominant errors sit on rows already inspected one by one (rule 6, U8).
- If G5 (c)'s footprint is understated, a Day 8–12 WIN measures how well the design fits those rows, not whether the mechanism holds.

**The governance assumption:** that G1's commitments hold for six days, enforced by records only, while the board posts E050's figure during that time.

## Missing Control or Ablation

None is blocking, because nothing runs. Named:
- **The separation of design data from evaluation folds** (G5 (c)): months in the training part of every fold evaluated. January and April–June 2025 qualify for all five.
- **Rule 15 (b)'s draw spread,** computable from stored predictions.
- **The convention split** (named in the H035 review; still not done). It is relevant to item 2.

## Decision

ACCEPT

## Execution Authorization

Authorized scope:

1. **The rulings on (a)–(h):**
   - (a) reopening admissible, as a deviation;
   - (b) adopted, with G3;
   - (c) per G1 and G2;
   - (d) ruling H8;
   - (e) rule 15 as amended (G5);
   - (f) adopted, with G6;
   - (g) adopted, with G7;
   - (h) adopted (G11).
2. **This session (D08-S01, cloud) does governance and text work only:**
   - the acknowledgement;
   - the appended corrections;
   - the owner's appended statements;
   - STATE;
   - the `reopened` event, once G1 holds.
3. **After G1 and the `reopened` event:** Days 8–12 research follows the normal handshake on the laptop. Each item needs its own reviewed proposal. This review authorizes no experiment.

**G1. Preconditions.** No `reopened` event is written, and nothing below is executed, until these are committed.
- **(a) The owner's commitments,** quoted verbatim with their UTC, appended to INC-0017 or to a new incident:
  - (i) The owner reads no leaderboard content until the challenge closes, through any channel: the ranking page, organiser e-mail or messages. This covers any figure, rank or comparison, for any file or team. At minimum, the commitment runs until the refreeze's upload decision has been executed and recorded.
  - (ii) Before the challenge closes, the owner relays nothing about the board to the researcher, to workers or into records. This includes any figure, rank, direction or distance from 250 s.
  - (iii) There is no upload before the refreeze. Afterwards, the owner executes exactly the refreeze's decision: the recorded final file once, or nothing.
  - (iv) After that, there is no upload of any file and no further reopening, whatever any figure shows.
- **(b) The owner's statement of what the owner knew at reopening,** appended to INC-0017:
  - whether any leaderboard content has been viewed since FROZEN;
  - whether any figure for E050 has been seen;
  - the basis of the 250 s figure: the project's records, board content, or "not stated".

  If a figure for E050 has been seen, no `reopened` event is written until a new Advisor review rules.
- **(c) The owner's appended line in `research/day-07/submission/UPLOAD_RECORD.md`:**
  - the object name;
  - the upload time (UTC);
  - the local path uploaded and that file's SHA-256;
  - whether the hash was recomputed immediately before the upload.

  If the hash is not `f0dc2c7c…17d06e8`, or the uploaded file was `predictions/final/submitting.parquet` (E044's), or the object name does not follow the convention:
  - no `reopened` event is written;
  - a recovery review rules on any corrective action;
  - nothing is uploaded in the meantime.

  If the hash was not recomputed before the upload, a P7 (d) deviation is recorded.
- **(d) INC-0017 records, as the owner's decision, the deviation from LEADERBOARD_POLICY's "submit once":** a second upload becomes possible.

**G2. Uploads and the ranking rule (ruling on (c)).**
- **No intermediate upload** (adopted).
- **Hedges are inadmissible under any ranking rule.** This means no upload of:
  - E044's file;
  - any non-promoted Day 8–12 file;
  - E050's file again.

  A corrective upload needs a recovery review (G1 (c)).
- **The final upload:**
  - at most one, and only the refreeze's file;
  - its SHA-256 recomputed immediately before the upload;
  - the object name follows the owner's convention;
  - an appended record, as P7 (d).
- **The ranking rule is not confirmed by anyone** before the final upload is executed or "no upload" is recorded. It changes no Day 8–12 decision.
  - The owner may record it with the external evaluation after the challenge closes.
  - If the challenge requires designating the counted submission, it is pre-registered here: the final file if one is uploaded, otherwise E050's file.
- **No proposal, phase close or final-file rule may cite any of these as a motivation or an input:**
  - the ranking rule;
  - E050's presence on the board;
  - diversification against E050.
- **The external evaluation (after the challenge closes)** records:
  - each file's figure, if shown;
  - the ranking rule;
  - under a "best" or unknown rule, that the ranked figure may be the better of two files.

  It is never fed back.

**G3. The target, the owner's role and challenge pages ((b) adopted, with additions).**
- **(b) is adopted as written.** S9 and U6 carry over.
- **No record, and no message to the owner, may relate a development, H, bulk or segment figure to 250 s or to the leaderboard,** whether explicitly or by juxtaposition.
- **Proposals cite INC-0017 as the reason the phase exists.** They do not quote the number.
- **The researcher puts no choice between hypotheses, candidates or files to the owner** (the INC-0015 type).
  - Owner decisions are those of brief §1, plus run windows and policy (the allowlist, external data).
  - Any other owner choice is an incident, disclosed in the final report.
- **The researcher and workers open no challenge page in Days 8–12.**
  - If a page must be read, it must carry no ranking content, and the read is logged with what the page showed.
  - The acknowledgement states what the 2026-10-05 index-page read showed (the deadline; no ranking or score content). If it showed any ranking content, an incident is recorded instead.

**G4. Ruling H8 (holdout).**
- **H stays closed for all of Days 8–12.** No access is granted now, and no later Day 8–12 review may grant one.
- **H7 stands:** the Day 7 access remains the project's last H read.
- **Each Day 8–12 phase close records "H: closed (H8)",** not "0 of 1".
- **Enforcement is by records only.**
  - `evaluate.holdout_compare` would permit one access in each of `day-08` to `day-12`.
  - `holdout_check.py` is not run in Days 8–12.
  - Each phase-close review verifies that the task ledger has no `holdout_access` line after 2026-10-04T17:57:38Z.
- **SUBMIT fits** may unmask December targets for training only, logged as unmasking events, as on Day 7. No analysis reads December targets.
- **Pre-registered consequence:** an objection that only H could resolve (objection F's type) cannot be resolved in Days 8–12. A candidate that carries one ends INCONCLUSIVE, and its file is not uploaded.

**G5. Rule 15 (Days 8–12; disclosure, with one consequence pre-registered now).** Every Day 8–12 candidate's analysis reports three things.
- **(a) The look count.**
  - List, in order and with IDs, every run from E051 on that has development-fold scores (any purpose), and every Day 8–12 analysis that read validation-month targets.
  - State the candidate's position in that sequence.
  - The Days 1–7 baseline is 44 scored experiments.
- **(b) The margin against the draw spread.** Per development fold and twin, report:
  - its all-rows ΔRMSE against E046;
  - its ΔRMSE on the mechanism population;
  - beside both, the spread of E046's draw analogues on the same rows (E033, E034 and E041 off the subgroup; rules 13 and 14).
- **(c) The discovery footprint, stated in the proposal.**
  - Which months' targets the analyses behind the mechanism read.
  - At what granularity: fold or segment aggregates, or row, flight or airport-day level.
  - This includes the earlier records the design relies on.

**The consequence.** The proposal's review rules on confirmatory weight before allocation.
- **A fold has no confirmatory weight for the mechanism** if either holds:
  - the design read that fold's validation-month targets at row, flight or airport-day level;
  - the candidate re-measures a contrast already recorded on the same folds.
- **If this leaves S1, or the third WIN of criterion 2, without confirmatory weight:**
  - the candidate carries an objection of objection F's type, which H8 makes unresolvable;
  - it ends INCONCLUSIVE and is never uploaded.

Rules 1–14 and batch conditions B1–B4 carry over.

**G6. Champion, references and compute ((f) adopted).**
- **Champion and references:** E046 is the phase-opening champion. References follow rule R, under rule L v2 item 6.
- **Cloud sessions do governance and text work only.** No `gate.py allocate`, run, fit, holdout script or formatter run in the cloud.
- **Sessions do not overlap.** D08-S01 appends its session-end line and pushes before a laptop session writes to the task ledger or allocates.
- **The laptop session, before its first allocation:**
  - starts from the pushed `day-8` head;
  - records rule L v2 item 6 as in condition 3 (a) of the LAPTOP_REFS review (X-D05-S04-0002);
  - confirms that its `runtime/ledger.sqlite` holds E001–E050, matching `experiments/ledger.jsonl`.

  Any environment difference means no comparison against the laptop instances without a new ruling.
- **Where reviews run.** Reviews that rely on stored predictions, including every phase close, run where those files are. Otherwise the review states the checks it could not make.

**G7. Refreeze ((g) adopted, with constraints on the final-file rule).**
- **The last phase close pre-registers the rule** before any SUBMIT run it selects among. The rule's only inputs are recorded criteria outcomes and integrity checks: route checks, I1–I5, and flag analyses whose bounds were fixed before the runs (as S6 and P6).
- **Exactly one branch uploads:** the SUBMIT file of the latest Day 8–12 champion, complete and checked before 2026-10-11T12:00:00Z.
- **Every other branch is "no new upload; E050 stands".** This covers no promotion, a failed check, an open flag, and anything incomplete at the cutoff.
- **What no branch may do:**
  - upload E044's file;
  - upload E050's file again;
  - choose between Day 8–12 champions other than by "the latest".
- **A promoted candidate's SUBMIT fits and formatter run** go through their own reviewed proposals, as H031–H037 did.
- **FROZEN** follows P7 (a)–(f), plus G2's upload record.

**G8. Final report and provenance.**
- **Days 1–7.** That content stays unchanged.
- **Days 8–12.** A section is appended. It opens by stating:
  - that the owner reopened the project after FROZEN, with a stated leaderboard aspiration (INC-0017);
  - that the brief's seven-phase run ended at E046 and E050's file.
- **Holdout:** four reads in total; Days 8–12 closed (H8).
- **Uploads:**
  - E050's file, after the Day 7 FROZEN;
  - the Days 8–12 decision;
  - after the challenge closes, the external evaluation as in G2.
- **Provenance:** brief §15 is kept verbatim. Beside it go the Days 8–12 facts:
  - the reopening;
  - the cloud governance session;
  - laptop compute;
  - delegation under INC-0018.

**G9. Agenda notes, binding on later proposals.**
- **Item 1:**
  - cites PHASE_CLOSE_D01 (c) and states what is new;
  - reports D3-C3's January exposure under rule 12;
  - adds a forward statement of U6's type.
- **Item 2:**
  - is judged against E046 on the development folds;
  - "downside" in 2026 is not a promotion ground;
  - trading development RMSE for lower forward exposure re-adjudicates U7 and P4 (rule 10).
- **Item 3 needs:**
  - an owner decision recorded as an incident;
  - an allowlisted host;
  - DATA_POLICY §7, with competition permission verified without exposure to ranking content.
- **Item 4:** states how the iteration count is chosen. A count read off validation curves falls under G5 (c).

**G10. Breach handling.**
- Any breach of G1–G3 is recorded as an incident before any further allocation.
- A recovery review then rules on whether later promotions and the upload decision stand.
- Nothing is uploaded until it rules.

**G11. Delegation ((h) adopted).**
- INC-0018 applies as written.
- Workers are bound by G2–G4 and G6.
- Each DAY_SUMMARY carries the delegated-work list.

**G12. Records.**
- **The `reopened` event,** `{"event": "reopened", "basis": "INC-0017; X-D08-S01-0001"}`, is appended only once G1 holds: in the commit that records G1, or later.
- **STATE** records:
  - Phase: OPEN (Days 8–12);
  - champion E046;
  - H: closed (H8);
  - rule 15;
  - a summary of G1–G12;
  - next ID E051 (laptop).
- **Each Day 8–12 DAY_SUMMARY** records:
  - G1's status (no breach, or the incident);
  - the rule 15 tables;
  - "H: closed (H8)";
  - the delegated work.

**Not authorized:**
- any allocation, run, fit, holdout script or formatter run in this session;
- any H access in Days 8–12;
- any upload before the refreeze, any hedge, and any upload after the refreeze's decision;
- any change to frozen files, reviews or completed records (corrections are appended).

Required acknowledgement path: `research/day-08/acks/PHASE_OPEN_D08_ack_v1.md`

**Contents of the acknowledgement:**
- the proposal hash (`6c91822f…4ee1a3b`) and this review's hash;
- G1–G12, ruling H8 and rule 15 (G5) adopted as binding, with G5 recorded in full;
- corrections D8-C2 to D8-C6, appended;
- G3's statement on the 2026-10-05 index-page read.

The acknowledgement may be committed before G1 is complete. The `reopened` event may not.

**Corrections** (appended; the proposal is not edited):

- **D8-C2. §3, the bulk.**
  - Non-LIRF bulk RMSE is 149–309 s, not "about 180–310 s".
  - LIRF bulk RMSE is 279–710 s (W1 279 s), not 297–710 s.
  - E046's LIRF bulk is largely its own subgroup's bulk cost: rows predicted at hours that are below 3,600 s (rule 12; the criterion 8 statistic). The increase over E033 is R1 45 %, R2 19 %, R3 16 %, S1 72 % and W1 5 % of E046's LIRF bulk SSE. E033's LIRF bulk is 273–374 s.
- **D8-C3. §3, the tail.**
  - "Many of those are recording conventions" holds for LIRF only. The convention is specific to LIRF: outside LIRF, 0–16.7 % of tail rows are block-at-schedule, at or below the base rates of 11.1–19.4 % (PHASE_CLOSE_D01 review (c)).
  - LIRF holds 12–68 % of each fold's ≥ 3,600 s rows. In W1, the January analogue, it holds 88 of 763, and LTFM holds 615.
- **D8-C4. §2 (e).** "Fifty experiments have been scored on the same seven folds" becomes 44.
  - E025 is a RESOURCE_FAILURE.
  - E042–E044, E049 and E050 are SUBMIT fits without fold scores.
  - The folds' reuse also includes target-reading analyses.
- **D8-C5. §3, the heading.** "What this means for the owner's aspiration (plain words, not a prediction)" is withdrawn (G3). The table and the description of E046's error stand, as corrected by D8-C2 and D8-C3.
- **D8-C6. Clerical.** SESSION_START, INC-0017, INC-0018 and UPLOAD_RECORD all carry 09:31:17Z, the session start's measured time. That is not each file's writing time (as D7-C2 and D7-C6). Later records carry their own measured time.

## Revision

None required for this version. G1–G12, H8, G5 and D8-C2 to D8-C6 are conditions and records under ACCEPT.

## Advisor Prediction

Probability of improvement (governance outcomes):

| Event | P |
|---|---|
| G1 recorded in full before the end of 2026-10-06 (UTC) | 0.80 |
| The completed upload record shows `f0dc2c7c…` and a conforming object name | 0.85 |
| A G1–G3 breach incident before the challenge closes (a figure seen or relayed, a stray upload, or a page read that shows ranking content) | 0.15 |
| At least one Day 8–12 candidate promoted under criteria 1–8 | 0.35 |
| A new file uploaded after the refreeze | 0.30 |
| At least one Day 8–12 proposal ruled, before allocation, to carry G5 (c)'s consequence | 0.40 |
| The last phase close committed by 2026-10-11T12:00:00Z | 0.85 |

Expected magnitude:
- **If a candidate is promoted:** its development-mean ΔRMSE against E046 is between −2 and −20 s, central about −5 s. It is likely concentrated on tail or NM-missing rows (rule 6).
- **Item 4 alone:** an effect smaller than criterion 1's 1.0 s minimum.
- **No leaderboard figure and no expectation of one is given** (G3).

Primary expected failure mode:
- **Primary: fold-fitting under the push.**
  - A tail mechanism shaped on the validation months' tail rows wins on the reused folds.
  - It is uploaded with no out-of-sample check (H8).
  - Its 2026 behaviour depends on recording practice or on input ranges that no 2025 month tests: U6's type, D3-C3.
  - The defences are G5 (c) and the default of no new upload.
- **Secondary: an owner-side exposure.**
  - E050's figure posts during Days 8–12, and the owner sees it on the page or by e-mail.
  - The upload decision is then no longer blind (G10).
- **Tertiary: the deadline squeeze.**
  - A candidate promoted late cannot complete its SUBMIT fits, formatter run and records by the cutoff, as with Day 7's deferrals (D7-C4). Records are rushed, as in D7-C14.
  - G7 makes that case "no new upload".
