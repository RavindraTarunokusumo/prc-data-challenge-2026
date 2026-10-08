# PRC Data Challenge 2026: project summary

*Written at the owner's request ("write a 7-Day summary of what happened"), at the refreeze in session D09-S01. DRAFT for X-D09-S01-0001. It restates reviewed records in plain words: `docs/reports/FINAL_REPORT.md` §§1–9, the day summaries and the phase-close reviews. It adds no new figure or decision.*

## In one paragraph

Over seven planned research days (27 September to 4 October 2026), an AI researcher built and tested models that predict how long departing aircraft take to taxi out at ten European airports. A separate AI advisor reviewed every step, and the project owner made the key decisions. The best model's average error on the development folds fell from **581 s** (a constant guess) to **314 s**. The largest single step (439 s to 314 s) came from one discovery: at Rome Fiumicino, many very long "taxi times" are a recording quirk, not real taxiing, and a model can learn it. The final model was submitted once.

The owner then reopened the project for a short extension (Days 8–9). It tested four more ideas, and none passed its pre-set bar. The project was refrozen with the original submission standing.

## How the work was organised

- **The researcher** (Claude) proposed each idea in writing, implemented it, ran it and analysed it.
- **The advisor** (a separate Claude reviewer at maximum effort) approved, revised or rejected every proposal before anything ran, and reviewed every day's close. It could not run experiments.
- **Fixed rules, set on Day 1 and never changed:**
  - five validation folds;
  - a December 2025 holdout, used at most once per day;
  - an eight-point promotion test.

  A new model became champion only if it beat the old one on at least 3 of 5 folds, including the July-like fold, with no fold clearly worse.
- **The owner** started and stopped work, set run windows, and made the recorded decisions. Every owner intervention is logged as an incident.

## What each day found

| Day | Focus | What happened |
|---|---|---|
| 1 | Setup, data audit, baselines | Froze the folds and the metric. Simple baselines went from 581 s down to **483 s** (a ridge model on time deltas). **Found that RMSE is dominated by a few very long records,** and that at Rome many of them are block times recorded at the scheduled time. |
| 2 | Flight and stand details | Stand, aircraft type and operator help ordinary flights by 9–30 s, but the effect couldn't be separated from the Rome records on all flights. No new champion. |
| 3 | Airport congestion | Counted the traffic around each departure. A tree model with congestion features became champion at **444 s**, and won on the December holdout. It also showed that a deliberate choice, handling Rome's unmatched flights with a simple model, cost about 122 s. |
| 4 | Historical averages | Past taxi-time averages added almost nothing for a tree model. Fixed a defect that produced out-of-range predictions. No new champion. |
| 5 | A second model type (on the laptop GPU) | Averaging the tree model with a CatBoost model gave **439 s**, better on all 7 folds, and won on the December holdout. |
| 6 | Trying to break the champion | Attribution and repeat-run tests. Nothing overturned the champion, but the tests had little power. |
| 7 | Submission and freeze | Built the submission pipeline. Then tested a model that learns Rome's recording quirk instead of routing around it. Development error fell to **314 s**, it passed every criterion, and it **won on December by 124 s**. It became champion, and its file was submitted. |
| 8 | Extension | A dedicated mixture model for Rome's unmatched flights (294 s, but only one fold clearly better: rejected); weather data for all ten airports (failed its trial); recording quirks at other airports (none found). |
| 9 | Extension | How long recent flights at the same airport took (failed its trial). The owner refroze the project. |

## The result

| Model | Average development error | December 2025 holdout |
|---|---|---|
| Constant guess (Day 1 starting point) | 580.79 s | 514.74 s |
| Day 1 champion | 482.73 s | 411.29 s |
| Day 3 champion | 444.49 s | 375.93 s |
| Day 5 champion | 438.87 s | 369.18 s |
| **Final champion (Day 7)** | **314.42 s** | **244.94 s** |
| Best extension run (rejected) | 294.32 s | not measured (holdout closed) |

**The submitted file is the final champion's procedure,** refit on all of 2025. SHA-256 `f0dc2c7c…06e8`, uploaded by the owner once, after the Day 7 freeze.

## What the submission is betting on

- The final step, from 439 s to 314 s, comes from predicting Rome's recording quirk instead of routing around it. That depends on Rome still recording block times at schedule in 2026.
- The December holdout supported it, but only for December.
- If the quirk had stopped in 2026, the final model would lose 0.25 to 1.3 times what it gains in 2025: a downside of similar size. This is stated in the final report (§5).

## Things that went wrong, or are worth knowing

- **Process errors are all recorded, and none affected a submitted result.** Examples:
  - run settings that differed from the plan on Days 2–3;
  - a run script defect on Day 7;
  - a refused run on Day 8;
  - a wrongly diagnosed network block and an overstated weather idea on Day 8;
  - a trial started without the owner's go-ahead on Day 9, stopped with no result.
- **After the Day 7 freeze, a leaderboard figure was disclosed to the researcher.** It was never used, and the extension's records disclose it.
- **The owner waived the extension's leaderboard-isolation commitments.** That is disclosed beside every extension result.
- **No result can measure the submission itself.** The folds and the holdout measure the models, not the refit file.
- **Three incidents remain open:** a Day 3 launch configuration, the experiment-tracking mirror, and the laptop environment choices.

## By the numbers

- **52 experiments** (E001–E052), every one approved by the advisor before it ran.
- **33 advisor exchanges.**
- **4 holdout reads,** all wins.
- **1 upload.**
- **24 incident numbers,** 26 incident files.
