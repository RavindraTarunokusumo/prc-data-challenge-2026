# D05-S04 session start

*Written 2026-10-01T17:06Z (environment measured 16:58:33Z with `date -u`).*

- **Why a new session:** the VM powered off at 16:33:09Z after a global OOM that killed E025 (INC-0008), which ended D05-S03. Boot ID `cf2c705b…`.
- **State recovered:** `day-5` at `590ebd8` plus D05-S03's uncommitted work, all reviewed by the researcher before commit:
  - `FS2_RAW` (FS2 without the `__RARE__` collapse) and its test;
  - `scripts/calibrate_gpu.py`;
  - E025's `worker.log`, and a ledger row stuck at RUNNING.

  Champion E019 (development mean 444.49). Day 5 holdout 1 of 1 available. Last exchange X-D04-S02-0001, nothing pending.
- **Environment:** WSL2 10,951 MiB, swap 0; silver present.
- **E025:** RESOURCE_FAILURE (records reconstructed from the kernel log). R1 completed, RMSE 446.40 (equal to E019), with a prediction hash different from E019's.
- **Guard added:** an experiment lock in `run_experiment.py`. The real-silver tests and the GPU calibration stand down while an experiment runs (INC-0008, closed).
- **Resolved model ID:** researcher `claude-opus-5-5` (`--effort high`); Advisor `advisor` subagent, definition `30fff5dd3c54`; delegation INC-0006.
- **Next:** commit; allocate a new H015 v2 reproduction (E026) and run it **with nothing else running**; then the GPU calibration; then the Day 5 proposals.

## Owner methodological suggestion (2026-10-01T18:48:34Z, logged per brief §1)

> I saw the curves for E027. You could use early stopping.

**Not adopted as a suggestion.** It is methodological input, outside the owner's safety, infrastructure and policy role (brief §1). It would become an instruction only through an incident record, as INC-0006 and INC-0009 were. The researcher's own assessment, which stands independently:
- **Early stopping on the validation folds is validation-guided tuning.** The stopping point would be picked with the targets that then score the model ("no early stopping on validation data", `gbm.py`).
- **Fold-local early stopping** on an inner temporal split of the training months is admissible. But E027's curves bound its gain: the development folds sit within 0.03–0.78 s of an *oracle* minimum, below criterion 1's 1.0 s, before the cost of holding a training month out. Only W1c (one training month; diagnostic) loses 4.9 s, and no submission fold trains on one month.
- **For CatBoost (H021) the risk is the opposite** (under-convergence), and it is recorded from H021's own curve.

## Correction (appended 2026-10-01T19:35Z; D5-C1, D5-C2)

"Environment: WSL2 10,951 MiB, swap 0" above is wrong on swap. The check printed only the memory line. This boot has had 4 GiB of swap since 16:33:25Z (unused). The interpreter is CPython 3.13.15, which was not recorded. See INC-0010.
