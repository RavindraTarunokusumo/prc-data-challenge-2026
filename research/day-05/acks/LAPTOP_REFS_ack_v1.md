# Acknowledgement — LAPTOP_REFS v1 (exchange X-D05-S04-0001)

- proposal: `research/day-05/proposals/LAPTOP_REFS_v1.md`, sha256 `e6d76c9c1729cdde8fa3cec9012052bc42b0866ac0306eee25888552bfcfbb94`
- review: `research/day-05/advisor/LAPTOP_REFS_review_v1.md`, sha256 `7d505b6ed857d0e5044210d534427c6eb4c21ebcbee1e4a5bae60d28e70e38c2`
- decision received: **REVISE** (confidence 0.90). Both hashes verified by the researcher at 2026-10-01T19:30Z.

This acknowledgement confers **no authority**. Rule L is not adopted, and no allocation follows from it. The researcher accepts all seven required revisions and will submit `LAPTOP_REFS_v2.md` in a new exchange.

## Corrections appended (no completed record is edited)

- **D5-C1. Swap.** The VM has 4 GiB of swap since boot `cf2c705b` (16:33:25Z); `.wslconfig` was changed to `swap=4GB` at 16:30:17Z. It was unused. E026–E029 ran with swap available. These say "swap 0" for this boot and are wrong on that point:
  - `research/STATE.md` (Day 5 section);
  - D05-S04 `SESSION_START.md`;
  - the E026 analysis (Host);
  - the X-D05-S04-0001 envelope.

  The researcher's D05-S04 check printed only the memory line of `free -m`, not the swap line. INC-0007's closing condition (swap 0) no longer holds. Owner decision: keep swap (INC-0010).
- **D5-C2. Interpreter.** The laptop runs CPython 3.13.15, so the lock resolves numpy 2.5.3, scipy 1.18.1 and xgboost 3.4.1. The cloud ran 3.11.15, with 2.4.6, 1.17.1 and 3.2.0. This was unrecorded against the brief's Python 3.11. The lock hash changed with W&B (`efa4fd78…`, additions only). "Same `uv.lock`, different CPU" (LAPTOP_REFS v1, E026 analysis, E028 analysis) is wrong. Owner decision: stay on 3.13 (INC-0010).
- **D5-C3. Location of the instance differences.**
  - E026, E027 and E029 equal their originals exactly at the nine non-LIRF airports. The differences sit in LIRF's routed rows (the ridge).
  - These are not supported, and are withdrawn:
    - the E026 analysis's attribution to "CPU-architecture-dependent floating-point paths in the same LightGBM build";
    - the journal's "not bit-stable from Intel Xeon to AMD Ryzen";
    - the E029 analysis's "common CPU-architecture effect on the shared LightGBM path".
  - E028 against E005 is not "low-order bits": W1c +0.339 s on all rows, LTFM +1.94 s on W1c (`sparse_cg`, tol 1e-4).
- **D5-C4. Laptop routed-ridge path.** E027 = E029 on all routed rows. Both differ from E028 on every routed row of every fold, by up to 190.9 s (R3). On the cloud the two paths were bit-identical. Cause open.
- **D5-C5. Allocation scope.**
  - E027, E028 and E029 were allocated outside their reviews' authorized scope. **E029 is contrary to H018 v2 review item 9.**
  - `gate.py` refuses only a second primary, so it does not enforce reproduction scope; the researcher must.
  - The researcher allocated them believing the hand-off's reproduction procedure covered them. It covers the E019 reproduction only (E025, E026).
  - From now on, every allocation beyond a review's stated scope is requested in a proposal first.
- **D5-C6. E029 provenance.**
  - E029's `manifest.json` names `code_commit` `ed5151f`, committed at 18:41:35Z during the run (18:38–18:53Z). The run commit is `f89dc60`, and the predictions are `f89dc60`'s code. `ed5151f` left the LightGBM, ridge and feature paths unchanged, and the worker had loaded its modules at start.
  - Cause: `prc.worker` reads `git_commit()` when it writes the manifest, at the end of the run. It is fixed to record the commit at worker start.
  - Practice: **no commit under `src/` or `scripts/` while an experiment runs.**
