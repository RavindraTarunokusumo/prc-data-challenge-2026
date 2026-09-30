# Acknowledgement — H018 v2 (exchange X-D04-S01-0002)

- proposal: `research/day-04/proposals/H018_v2.md`, sha256 `1fa63bb4964ddb11221aae095dafe669d6f7568a2971868eef8f53ebaa9c6f61`
- review: `research/day-04/advisor/H018_review_v2.md`, sha256 `07a8c67e8bf6e456c1b24522a8b2a9d280c6f5b928fc4437cbb52d8de5762770`
- decision received: **ACCEPT** (confidence 0.86). Both hashes verified by the researcher at 2026-09-30T17:48:35Z.

**Adopted:** the review's Execution Authorization items **1** (preconditions, including the tools freeze from `d1cc43b` until the chain's last comparison), **7** (promotion, and the definition of "promoted first in this chain"), **8** (recording (a)–(e)) and **9** (not authorized), verbatim.

**Authorized next step:**
- `gate.py allocate H018 v2`.
- The config is E019's with `hypothesis_id: H018`, `proposal_version: 2` and `params.route_train_exclude: true`; everything else is identical.
- Then `run_experiment.py`, and the comparisons of item 3 in order.
- The reproduction runs only under item 4. An infrastructure re-run is allowed only under item 5, and item 6 applies if the run is INVALID.

**Record corrections:**
- **D4-C2.** The Implementation Plan of `H018_v2.md` reads "`gate.py allocate H018 v1`" and "`proposal_version: 1`". Both mean **`v2`** and **`2`**.
- **D4-C3.** `research/day-04/eda/range_check_refs.json` was committed in `e4c57f8` (with the X-D04-S01-0001 records), before the `--bands` code that produced it was committed in `99db208`. It re-derives byte for byte from that code (verified by the Advisor). The citation "commit `99db208`" refers to the code.

**Recording condition adopted (item 8(e)).** If clause 1 is met, D3-C2's attribution to LIRF NM-missing rows is recorded as falsified. The record will not conclude that a treatment must act on the T windows, because the NM-missing tail rows at the other nine airports remain in training.
