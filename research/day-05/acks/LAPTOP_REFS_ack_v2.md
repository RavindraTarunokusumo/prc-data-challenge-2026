# Acknowledgement — LAPTOP_REFS v2 (exchange X-D05-S04-0002)

- proposal: `research/day-05/proposals/LAPTOP_REFS_v2.md`, sha256 `4a4a03d75eeb6a5318003a9bb5d80ebbf5b34dda0df30b87af6bed61d95312da`
- review: `research/day-05/advisor/LAPTOP_REFS_review_v2.md`, sha256 `fc96008d7577548baf77fa66b9dc4e7a4db129971e13e55b6168929448be52e1`
- decision received: **ACCEPT** (confidence 0.88). Both hashes verified by the researcher at 2026-10-01T20:21Z.

**Adopted: rule L v2, items 1–4 of the Execution Authorization**:
1. Rule L v2 as written (items 1–7).
   - E026 is E019's instance; E027 is cited for curves only.
   - E029 is E023's instance; E028 is E005's instance in the reduced role.
   - The boundary-disclosure table, E026's H file as the holdout reference side, the environment of item 6, and E029's routed rows as the route-integrity reference for FS2 and FS2_RAW frames.
2. Ratifications: E029 (instance, H023 component, route-integrity reference), E028 (reduced role), E027 (curves only).
3. Conditions:
   - (a) The environment record for every chain run:
     - before allocation: the interpreter, the `uv.lock` SHA-256 at the run commit, and the launching shell's thread variables;
     - the venv's library versions, read once per session and after any `uv` command;
     - after the run: the manifest's `python` and `polars_threads`.

     The worker now also writes the lock hash, the library versions and the thread variables into every manifest (`environment`). Any difference from item 6 bars comparison against the instances without a new ruling.
   - (b) The item 4 flags, for every comparison against an instance.
   - (c) E029 is a reference for FS2 and FS2_RAW frames only.
4. Not authorized:
   - E028 as a route-integrity reference;
   - allocations beyond a review's stated scope;
   - E026–E029 as NEW;
   - edits to the manifests or records of E025–E029;
   - any change that ends item 6's environment during the chain, `POLARS_MAX_THREADS` included.

Noted for the record: "established" in the Cause section means the proximate cause. The worker-level FS2 = FS2_RAW equivalence rests on the four-fold check and the builders' code structure.

**Session environment record (condition (a)), D05-S04, read 2026-10-01T20:21Z:**

- interpreter: CPython 3.13.15; `uv.lock` `efa4fd78eaa6…`; thread variables set: none
- libraries: numpy 2.5.3, scipy 1.18.1, sklearn 1.9.1, polars 1.44.2, lightgbm 4.7.0, catboost 1.2.10, xgboost 3.4.1, pandas 3.0.6
