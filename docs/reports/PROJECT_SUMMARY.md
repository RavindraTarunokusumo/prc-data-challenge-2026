# PRC Data Challenge 2026: project summary

*FINAL. Written at the owner's request ("write a 7-Day summary of what happened"), at the refreeze in session D09-S01, and reviewed in X-D09-S01-0001 (ACCEPT 0.80), with D9-C9 to D9-C14 applied. It restates reviewed records in plain words: `docs/reports/FINAL_REPORT.md` §§1–9, the day summaries and the phase-close reviews. It adds no new figure or decision.*

## In one paragraph

Over seven planned research days (27 September to 4 October 2026), an AI researcher built and tested models that predict how long departing aircraft take to taxi out at ten European airports. A separate AI advisor reviewed every proposal before it ran, and every day's close. The best model's average error on the development folds fell from **581 s** (a constant guess) to **314 s**.

The largest single step (439 s to 314 s) came from one discovery: at Rome Fiumicino, many very long "taxi times" are a recording quirk, not real taxiing, and a model can learn it. **That step is a bet that Rome's recording quirk persists in 2026, with a downside of similar size if it does not** (§ "What the submission is betting on").

The owner then reopened the project for a short extension (Days 8–9). Four more ideas were tested, and none passed its pre-set bar. The project was refrozen with no new upload: the Day 7 file stands.

## How the work was organised

- **The researcher** (Claude, `claude-opus-5-5`) proposed each idea in writing, implemented it, ran it and analysed it, with these recorded exceptions:
  - **Delegation.** On the owner's instruction, Day 4 implementation work and experiment launches were delegated to `claude-sonnet-5-5` workers under the researcher's review (INC-0005). One Day 6 analysis script was delegated in the same way (INC-0013). There was no delegation in Days 8–9.
  - **Model and effort settings.** On Day 2 (INC-0003) and Day 3 (INC-0004), the researcher's own model and effort settings differed from the registered configuration. Day 3's effective tier cannot be determined, and INC-0004 is still open.
- **The advisor** (a separate Claude reviewer at maximum effort) reviewed every proposal before its runs, and every phase close. It could approve, revise, reject or hold, but could not run experiments.
  - The extension's design pilots and looks ran under rules committed before each run, without a review of each pilot.
- **Fixed rules, set on Day 1 and never changed:**
  - five validation folds;
  - a December 2025 holdout, used at most once per day;
  - an eight-point promotion test.

  A new model became champion only if it beat the old one on at least 3 of 5 folds, including the July-like fold, with no fold clearly worse.
- **The owner** started and stopped the run, set run windows, and made the decisions recorded in the incident files, acknowledgements and day summaries.
  - On Day 7 that included choosing, among options the researcher wrote and recommended, to test the model that became the final champion (INC-0015).
  - In Day 8 the owner chose among researcher-written research options, including dropping weather (INC-0023).
  - The owner did no feature selection, tuning or interpretation.

## What each day found

| Day | Focus | What happened |
|---|---|---|
| 1 | Setup, data audit, baselines | Froze the folds and the metric. Simple baselines went from 581 s down to **483 s** (a ridge model on time deltas). **Found that RMSE is dominated by a few very long records,** and that at Rome many of them are block times recorded at the scheduled time. |
| 2 | Flight and stand details | Stand, aircraft type and operator help ordinary flights by 9–30 s, but the effect couldn't be separated from the Rome records on all flights. No new champion. |
| 3 | Airport congestion | A tree model became champion at **444 s**, and won on the December holdout. **95 % of its margin over the Day 1 champion was routed static structure** (stand, aircraft type, operator, destination; D3-C1), not congestion. Congestion as served added −1.90 s on all rows. Day 3 also showed that handling Rome's unmatched flights with a simple model cost about 122 s. |
| 4 | Historical averages | Past taxi-time averages added almost nothing for a tree model. Fixed a defect that produced out-of-range predictions. No new champion. |
| 5 | A second model type (on the laptop GPU) | Averaging the tree model with a CatBoost model gave **439 s**, better on all 7 folds, and won on the December holdout. |
| 6 | Trying to break the champion | Attribution and repeat-run tests. Nothing overturned the champion, but the tests had little power. |
| 7 | Submission and freeze | Built the submission pipeline. Then, on the owner's choice (INC-0015), tested a model that learns Rome's recording quirk instead of routing around it. Development error fell to **314 s**, it passed every criterion, and it **won on December by 124 s**. It became champion, and its procedure produced the final file. |
| 8 | Extension | **A dedicated mixture model for Rome's unmatched flights:** 294 s, but only one fold clearly better, so rejected. **Weather data for all ten airports:** failed its trial. **Recording quirks at the other airports:** none of the 18 patterns tested explained their long taxi times, and the look does not show what those flights are. |
| 9 | Extension | **How long recent flights at the same airport took:** failed its trial rule. The trial did not test the idea in the form a real candidate would have taken, so it is untested in that form, not disproven. The owner refroze the project. |

## The result

| Model | Average development error | December 2025 holdout |
|---|---|---|
| Constant guess (Day 1 starting point) | 580.79 s | 514.74 s |
| Day 1 champion | 482.73 s | 411.29 s |
| Day 3 champion | 444.49 s | 375.93 s |
| Day 5 champion | 438.87 s | 369.18 s |
| **Final champion (Day 7)** | **314.42 s** | **244.94 s** |
| Best extension run (rejected) | 294.32 s | not measured (holdout closed) |

**These figures belong to the evaluated models, not to the submitted file.** Neither the final champion's development margin nor its December improvement is the file's expected gain. No fold and no holdout measures the submitted file itself.

**The submitted file** is the final champion's procedure, refit on all of 2025 (SHA-256 `f0dc2c7c…06e8`).
- The owner reports uploading it after the Day 7 freeze. The record names the object and the expected hash, but the upload is the owner's report and is unverified.
- No new file was uploaded in Days 8–9.

## What the submission is betting on

- The final step, from 439 s to 314 s, comes from predicting Rome's recording quirk instead of routing around it. That depends on Rome still recording block times at schedule in 2026.
- The December holdout supported it, but only for December.
- If the quirk had stopped in 2026, the final model would lose 0.25 to 1.3 times what it gains in 2025: a downside of similar size. This is stated in the final report (§5).

## Things that went wrong, or are worth knowing

- **Errors and deviations are recorded in the incident files and in the correction lists.** Examples:
  - the researcher's model and effort settings on Days 2–3;
  - a run script defect on Day 7, which affected no output (D7-C14);
  - a refused run on Day 8;
  - a wrongly diagnosed network block and an overstated weather idea on Day 8;
  - a trial started without the owner's go-ahead on Day 9, which was stopped. Its empty log was deleted, so "no figure was seen" rests on the researcher's word.
- **After the Day 7 freeze, a leaderboard figure was disclosed to the researcher.** It was never used. It also reached the advisor's context twice during the extension. Leaderboard isolation did not hold at the reopening.
- **The owner waived the extension's leaderboard-isolation commitments,** and what was known at the reopening is not stated. Both are disclosed beside every extension result.
- **Three incidents remain open:** a Day 3 launch configuration, the experiment-tracking mirror, and the laptop environment choices.

## By the numbers

- **52 experiments** (E001–E052), each allocated by the gate after an advisor ACCEPT.
- **33 advisor exchanges.**
- **4 holdout reads,** all wins.
- **1 upload reported by the owner** (unverified).
- **24 incident numbers,** 26 incident files.
