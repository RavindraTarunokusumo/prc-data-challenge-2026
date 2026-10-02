# E034 analysis: H023 v3 reproduction (blend of E029 and E032; seed 43)

**PASS: criterion 6 for H023.** Due under H023 v3: criteria 1–3 passed against E026, no clause was met, clause 1 was not INCONCLUSIVE, and H021r (E032) had passed its route check.

- **Config:** components [E029, E032], weights [0.5, 0.5], seed 43, CLASS-S. COMPLETE: 7.3 s, 3.40 GB.
- **Development mean 438.95 s:** R1 440.36, R2 264.63, R3 393.13, S1 628.19, W1 468.43; S1c 632.14, W1c 480.50.
- **`route_check.py E034 - E029`:** passes on all 8 folds.
- **`reproduce_check.py E034 E033 --champion E026`:**
  - development folds within tolerance: R1 +0.478, R2 −0.248, R3 +0.093, S1 +0.272, W1 −0.204 s;
  - **criteria 1–3 hold** against E026: WIN on all 7 folds;
  - `passes: true`.
- **Clause 1 reported on H023r** (`mechanism_check.py E034 E029 NM_present_excl_LIRF`): −3.70 s (q95 −3.19); counted R1–S1 WIN, W1 TIE. It agrees with E033.
- The half-size transfer of H021's re-draw held: E032 − E031 on R1 (+1.056 s) became +0.478 s in the blend.
