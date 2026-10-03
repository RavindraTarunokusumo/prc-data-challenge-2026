## Day 6: adversarial science (phase close X-D06-S01-0004 ACCEPT; holdout closed unused; E033 remains champion)

**Outcome.** No Day 6 result contradicts the champion's promotion. Neither Day 6 batch had real power against its performance claim, and the strongest open attacks (the 12-month SUBMIT procedure, January's long-delay exposure) were not run. E033 stays champion; no candidate existed.

| | Validation RMSE (development mean) |
|---|---|
| **Champion E033** (0.5 LightGBM + 0.5 CatBoost GPU) | **438.87** |
| Best Day 6 run (E041, E033 on a fixed-seed re-draw; control) | 438.97 |
| E029 (the LightGBM half alone) | 442.46 |
| Previous champion E019 (instance E026) | 444.49 |

**What was tested**
- **Attribution ladder (E035–E039):** each 0.5/0.5 blend with E029 replaced the CatBoost half with a cheaper stand-in: the codes CatBoost (440.68), the per-key CatBoost (440.04) and a perturbed LightGBM twin (441.44). None substitutes for E031; they keep 39–66 % of the gain on normal taxis (most favourable champion draw as denominator). The "statistics" reading is at its threshold and draw-dependent; "statistics" and "combinations" are not separated from CatBoost's `data_partition`.
- **Draw robustness (E040–E041):** a fixed-seed GPU refit of the CatBoost half, blended as E033: criteria 1–3 against E026 hold, 7/7 WIN, within 0.40 s of E033 per fold. On the January analogue's (W1) normal taxis the gain over E029 varies −1.59 / −0.31 / +0.40 s across three draws.

**Holdout:** Day 6 0 of 1, closed unused (ruling H6).

**Governance:** exchanges X-D06-S01-0001 (REVISE ×5), -0002 (ACCEPT ×5), -0003 (ACCEPT ×2), -0004 (phase close ACCEPT 0.84; corrections D6-C6 to D6-C15; standing rule 14). INC-0012 (owner run window) and INC-0013 (Sonnet delegation; one diagnostics script) closed. INC-0009 records that E036–E039 never reached W&B.

**No change** under `src/`, `scripts/`, `config/`, `pyproject.toml` or `uv.lock`.

**Day 7 carries:** the SUBMIT procedure, D3-C3, the causal-only variant, the iteration budget; one holdout access.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
