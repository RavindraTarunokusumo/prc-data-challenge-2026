---
schema: incident-v1
incident_id: INC-0010
type: protocol_deviation
created_utc: 2026-10-01T19:33:00Z
status: open
---

# Day 5: swap kept at 4 GB, interpreter kept at CPython 3.13 (owner decisions)

**Raised by:** the researcher, after X-D05-S04-0001 (corrections D5-C1, D5-C2 in `research/day-05/acks/LAPTOP_REFS_ack_v1.md`).

## Facts

- **Swap.** `C:\Users\rvind\.wslconfig` reads `[wsl2]`, `memory=11GB`, `swap=4GB`. The researcher had written `swap=0` at 16:12Z; the file was modified at **16:30:17Z**, during the INC-0008 OOM sequence. Boot `cf2c705b` (16:33:25Z) attached 4 GiB of swap. It has not been used (`pswpin`/`pswpout` 0). E026–E029 ran with swap available. The records that said "swap 0" for this boot were not measured on the swap line (D5-C1).
- **Interpreter.** `.venv` is uv-managed **CPython 3.13.15** (`pyvenv.cfg`). No 3.11 interpreter was present, and `requires-python = ">=3.11"` let uv choose 3.13. The lock then resolves numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1, against the cloud's 3.11.15 with 2.4.6, 1.17.1 and 3.2.0. The brief (§11) and CLAUDE.md say Python 3.11. No record stated this before X-D05-S04-0001 (D5-C2).

## Owner decisions (D05-S04, 2026-10-01, in reply to the researcher)

- **Keep 4 GB swap** for Days 5–7, as a safety net against a VM-wide OOM like INC-0008's. The owner did not state who changed the file.
- **Stay on CPython 3.13** for Days 5–7.

## Consequences (stated, accepted)

- **Brief §4 "no swap" does not hold on the laptop.** The runner's RAM guard and `within_class` are RSS-based, and swapped-out pages are not counted. Mitigation: each Day 5 analysis reports swap use during its run (`pswpout` before and after, from `/proc/vmstat`). Any swap-out is disclosed beside the RSS figure, and a run that swaps is not called within class on RSS alone.
- **The laptop environment is not the cloud's.** Laptop reproductions differ from cloud originals (at LIRF's routed rows for the routed models; everywhere for the ridge). The cause is open (`LAPTOP_REFS_review_v1.md` (b), (c)). Instances of cloud references hold only within this environment: CPython 3.13.15, the lock at the time of the run, these library builds and this host. **Any change to the interpreter, the lock or the libraries during the Day 5–7 chain ends the instances,** and needs a new ruling.
- No frozen artifact changes.

## Resolution

Stays open through Day 7; reviewed at each phase close.
