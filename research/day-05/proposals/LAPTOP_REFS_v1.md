---
schema: governance-request-v1
request_id: LAPTOP_REFS
proposal_version: 1
day: 5
session: D05-S04
exchange_id: X-D05-S04-0001
researcher: claude
researcher_model_id: claude-opus-5-5
status: proposed
created_utc: 2026-10-01T18:44:38Z
---

# Request LAPTOP_REFS v1: laptop instances of E019, E005 and E023 for row-level comparisons

Batch X-D05-S04-0001 (with H021, H022 and H023). This is a governance request, not a hypothesis: no experiment depends on it beyond the reproductions already run under their original ACCEPTs. A ruling is requested because the frozen comparison tools cannot run against the Day 1–4 references on the laptop.

## Problem

- `prc.evaluate` loads stored prediction files and refuses unless each file matches its experiment's `manifest.json` SHA-256 (`_predictions`). Every row-level comparison depends on that: `compare.py`, `mechanism_check.py`, `route_check.py`, `range_check.py` and `holdout_check.py`.
- **The prediction files of E019 (champion), E005 (`route_check` and criterion 8 reference) and E023 (matched reference under the hand-off base ruling) are git-ignored and were left on the cloud container.** The brief notes that the container is reclaimed when idle (§4). The laptop has only their manifests (hand-off §6: "covered by" a manifest means integrity, not availability).
- **Re-running the same configurations on the laptop does not restore the files byte for byte.** Same `uv.lock`, same silver (byte-identical rebuild, `research/day-05/sessions/D05-S02/DATA_VERIFICATION.md`), different CPU (AMD Ryzen 7 260 against Intel Xeon). So the originals' manifests can never be satisfied on the laptop.

## Evidence: laptop reproductions under the original ACCEPTs

| Original | Laptop run | Hypothesis | Max \|ΔRMSE\| over development folds | Byte-identical to original | Notes |
|---|---|---|---|---|---|
| E019 | **E027** (and E026) | H015 v2, reproduction, seed 43 | **0.0072 s** (S1) | no (all 8 files) | **E026 and E027 are byte-identical to each other**: the laptop is deterministic. E027 records learning curves |
| E005 | **E028** | H004 v1, reproduction, seed 43 | **0.0113 s** (W1) | no (all 8 files) | ridge: BLAS low-order bits |
| E023 | **E029** | H018 v2, reproduction, seed 43 | **0.0072 s** (S1) | no (all 8 files) | peak RSS 6.60 GB against E023's 5.29 GB (cause not established; E027 with curves 5.19 GB; within class) |

All three pass `reproduce_check.py` (1.0 s tolerance). The laptop–cloud difference is two to three orders of magnitude below criterion 1's 1.0 s.

## Requested ruling (rule L)

1. **Instances.** For Days 5–7 on the laptop, **E027 is the laptop instance of E019, E028 of E005, and E029 of E023**. Every row-level comparison that the frozen rules or a ruling define against E019, E005 or E023 runs against the instance. That covers `compare.py`, `mechanism_check.py`, `route_check.py`, `range_check.py`, the criterion 8 statistic, and the reference side of `holdout_check.py`.
2. **Identity unchanged.**
   - E019 stays the champion of record. Records say "against E019 (laptop instance E027)".
   - The instances carry their originals' restrictions:
     - E027 and E028 are never NEW;
     - **E029 is never NEW, and is not a candidate** (rules 9 and 10, as for E023);
     - E029 is the matched reference for `route_train_exclude` candidates on FS2, as E023 is under the hand-off base ruling (X-D04-S02-0001 (e)).
3. **E029 as a blend component** (H023). E029's configuration enters a *new* candidate configuration (H023), so rule 10 is not engaged. H023 is judged against E019's instance, and its criterion 4 carries H018 v2's clauses 1–2 under the hand-off base ruling.
4. **Boundary sensitivity (disclosure).** A comparison against an instance reports, per fold, whether the deciding bootstrap quantile lies within 0.02 s of its threshold. 0.02 s is about twice the largest instance–original difference. If it does, the fold outcome is flagged "instance-sensitive". It is still decided as computed: no outcome is changed, and the flag is a disclosure.
5. **Holdout.** The Day 5 access, if the phase close names one, uses E027's H file as the reference side. E027's H predictions are the laptop's E019 H predictions. No H truth has been read on the laptop.

## Alternatives considered

- **Retrieve the cloud files.** They are not on the laptop. The container's lifetime is not under the project's control, and a later retrieval cannot be relied on. If the owner retrieves them, they are verified against the original manifests and noted; the instances still stand for consistency within Day 5.
- **Edit the original manifests to the laptop hashes.** That would rewrite completed records. Refused.
- **Compare against metrics.json only.** That loses the bootstrap, rules 1, 6 and 7 and the criterion 8 statistic. Not acceptable for promotion.

## Decision Requested From Advisor

ACCEPT (adopt rule L as written), or REVISE with the changes needed.
