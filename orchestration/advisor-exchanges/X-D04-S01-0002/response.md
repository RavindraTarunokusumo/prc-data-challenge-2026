I accepted both proposals: **H018 v2 is ACCEPT (0.86)** and **H019 v2 is ACCEPT (0.80)**. Both hashes match the envelope, and every required revision from the v1 reviews is met. Each ACCEPT comes with a precise authorized scope, and a few readings and record corrections that the v2 acks must adopt before any allocation. None of them changes the design.

I wrote only the two review files. Every check was read-only, target-free, synthetic, or a comparison of existing prediction files. I read no December target, fitted or scored no model on a real fold, and kept scratch output in the session scratchpad.

**What I verified**
- **Integrity:** the frozen files and the Advisor definition (`30fff5dd…`) match their pins, and so does `uv.lock` (`39df945c…`). The X-D04-S01-0001 mirror checks 8/8.
- **Predictions:** all 80 prediction files of E005, E006, E012, E015 and E017–E022 match their manifests.
- **Code and tree:** `pytest` passes 143/143 and `ruff` is clean. Nothing under `src/` has changed since the v1 review. There was no container reset and no Day 4 allocation, and no experiment is running.
- **Evidence:** the committed script re-derives `range_check_refs.json` byte for byte. All band, noise and rule 8 figures reproduce, as do the S1 shares (10.4 %, 1.9 %), the joint-key table and the noise-scale contrasts.

**H018 v2**
- **Clause 1 is now decisive.** The threshold of 50 on the >3 h band sits 9 above the highest fit without T windows (13–41) and 31 below E019 (81). The band noise is ±12–15, so either outcome would be clear.
- **The mechanism is supported by existing files.** E019's `NM_missing_other` loss against E017 sits 92 %, 97 % and 88 % in the >3 h band on R1, R2 and R3. On W1, one LTFM row carries 64 %.
- **The treatment probably cannot win S1.** I replaced E019's predictions on the treated rows with those of the fits without T windows (E017, E021). That moves all rows by R1 about −3.2 s, R2 −4.2 s and R3 −1.4 s, but S1 only +0.1 to +0.4 s. S1 is the WIN that promotion requires, so a promotion would likely come from other rows. W1c may also move against H018 (+3.9 to +6.7 s in the same bound).
- **The H018 ack must record:**
  - its Implementation Plan still says `gate.py allocate H018 v1` and `proposal_version: 1`; both must read v2. The gate would refuse v1, but `run_experiment.py` does not check the config's version, so a wrong label would go unnoticed.
  - `range_check_refs.json` was committed in `e4c57f8`, before the `--bands` code it needs (`99db208`, the commit the proposal cites). It re-derives exactly, so this is a citation fix.
- **Recording condition:** if clause 1 is met, the record must not conclude that "a treatment must act on the T windows". NM-missing tail rows at the other nine airports remain in training.

**H019 v2**
- **Clause 1(a) lost its twin rule.** v1 said "criterion 2 (twin rule included)". v2 rewrote the WIN count to leave W1 out and silently dropped that phrase. The ack adopts the frozen reading: WINs are taken from `fold_outcome_counted`. The tool's `criterion_2` field still counts W1, so it cannot be used for the clause.
- **"Promoted first in this chain" is now defined** in `H018_review_v2.md` item 7. H018's status must be recorded in the journal before H019 is allocated, so H019's comparison target and criterion 4 are fixed in advance.
- **The rule 8 claim overreaches.** "The prior block adds no convention exposure" is true of what enters the priors, but not of the fitted model. When FS1's static keys were added, the LIRF NM-present cell moved by +36.9 s on S1 (E017 − E018), which is about +3.8 s on S1 overall. The ack corrects the sentence, and H018's S1 recording rule is extended to H019.
- **The ack must also correct** "allocate H019 v1" to v2.
- **Disclosure:** report the 4-fold mean (R1–R3, S1) beside the 5-fold mean.

**Preconditions before either allocation**
- `STATE.md` (last written 16:50:42Z) and the journal must record X-D04-S01-0001, including H020's REJECT, and this exchange.
- No changes under `src/`, `scripts/`, `pyproject.toml` or `uv.lock` from `d1cc43b` until the chain's last comparison.

**My predictions**
- **H018:** clause 1 not met 0.85, clause 2 not met 0.88, S1 WIN 0.20, promotion 0.12. Most likely outcome: the mechanism holds but H018 is not promoted.
- **H019:** mean ≤ −3.0 s 0.30, mechanism supported 0.27, W1c identical to H018 0.99, promotion 0.10.

Files are in /home/user/prc-data-challenge-2026/research/day-04/advisor:
- H018_review_v2.md
- H019_review_v2.md

```yaml
schema: advisor-task-result-v1
exchange_id: X-D04-S01-0002
status: COMPLETE
decisions:
  - proposal_id: H018
    proposal_sha256: 1fa63bb4964ddb11221aae095dafe669d6f7568a2971868eef8f53ebaa9c6f61
    decision: ACCEPT
    review_path: research/day-04/advisor/H018_review_v2.md
    review_sha256: 07a8c67e8bf6e456c1b24522a8b2a9d280c6f5b928fc4437cbb52d8de5762770
  - proposal_id: H019
    proposal_sha256: df74347ccaeeb6f1b48b5089744010ce8951b943365792f49e74c3664e1d2c6d
    decision: ACCEPT
    review_path: research/day-04/advisor/H019_review_v2.md
    review_sha256: 9f85d2e93b1f951fc3bce5453f276938c931ea8c3c0ab45576a6bcfdf97dc914
completed_utc: 2026-09-30T17:47:09Z
```
