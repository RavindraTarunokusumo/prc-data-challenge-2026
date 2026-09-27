## Advisor result: exchange X-D01-S01-0003 (batched review, H001–H008)

**All eight proposals are ACCEPTed** (confidence 0.80–0.95), but one row in S1's validation month may decide the Day 1 champion (finding 1).

Each proposal has its own review in `/home/user/prc-data-challenge-2026/research/day-01/advisor/` (`H001_review_v1.md` to `H008_review_v1.md`). Every review's front matter parses the way `scripts/gate.py` expects: `decision: ACCEPT`, and `proposal_sha256` matches the proposal on disk. I wrote only those eight files. Following the earlier exchanges, `response.md` and `checksums.sha256` are left for you to mirror.

### What I checked
- **Hashes:** all eight proposal hashes match the envelope. The six frozen files and the SPLITS v2 proposal, review and ack match `config/frozen.json`. The advisor definition matches `config/agents.yaml`. The working tree was clean at `01b2f2f`.
- **Tests:** 90 of 90 pass (run without caches) and ruff is clean.
- **No tuning:** hyperparameters and expected results are unchanged since the first drafts at `866b902`. That is the same commit as the resource calibration, which computes no metric.
- **Leakage:** every model fits only on training rows (`role == 'train'`), and I found no leakage path.
- **How I checked:** everything was read-only. I read no target column, excluded December throughout, and fitted or scored no model.

### Findings that matter
1. **One row may decide the Day 1 champion.**
   - S1's validation month (July 2025) has exactly one row with an anchor (`d_aobt3`) of 20,000 s or more: at LIRF, 87,181 s.
   - All its NM and schedule times sit about 24 h before takeoff. No S1 training month has any value that large, and July 2026 has one row with the same pattern.
   - H005 (the raw anchor) will predict about 87,000 s for it. H004, H006 and H007 will predict bounded values.
   - Whichever side is wrong carries an error of about 86,000 s on that row. That adds 40–45 s to S1's RMSE and 4–11 % to LIRF's pooled RMSE. It is enough to turn an S1 WIN into a TIE and to fail criterion 3.
   - Which side is wrong depends on whether the recorded block time is on the original day. I did not read the target.
   - My estimate: P ≈ 0.45 that the chain ends with H005 as the Day 1 champion, against P ≈ 0.40 for H006.
2. **January 2026 has an anchor tail that no fold reproduces.**
   - 0.375 % of its rows have an anchor of 3,600 s or more, against 0.067–0.132 % in every 2025 month. Most are at EHAM on 3–9 January.
   - How each model treats long anchors will therefore matter more on the January test than on any fold. That covers H004's winsorisation, H005 passing the anchor through, and the leaf values of the tree models.
3. **Fold H is the largest training fold, not S1.**
   - It has 1,919,370 training rows, 24.8 % more than S1.
   - The runtime totals still hold: about 9–10 minutes for H006 and 21–23 minutes for H007.
   - H004 is CLASS-S with a 4 GB target. The feature build alone measured 3.45 GB on fold H, so P ≈ 0.25 that H004 exceeds the target. If it does, criterion 7 fails and H004 cannot be promoted, but its reference numbers remain valid.
4. **H008's expected result contradicts itself.** Using the batch's own pre-registered ranges, "10–20 % above H006" means 337–479 s and "0–5 % below H003" means 497–557 s, so both cannot hold. Record this in the acknowledgement without substituting a new value. The falsification criterion is unaffected.
5. **Smaller confounds, recorded and not blocking:**
   - H002 switches from mean to median while adding the airport key, which costs about 4.7 s of a roughly 31.6 s airport effect.
   - H003's takeoff hour mixes diurnal demand with a mechanical effect: a long taxi pushes the takeoff into a later hour. Daylight saving also shifts W1's hour cells by an hour, but not W1c's.
   - H007 and H006 differ in capacity settings as well as library (minimum leaf size 10 against 100). A difference between them is attributable to configuration, not implementation. H007's check against H008 mixes libraries.

### Batch conditions (adopt them in each acknowledgement)
- **B1.** Brief §10 criteria 5, 7 and 8 also apply to promotions in the chain.
- **B2.** A candidate whose own falsification criterion is met is not promoted, even if it beats the current champion.
- **B3.** An S1 WIN together with a non-negative S1c point dRMSE is an unresolved Advisor objection.
- **B4 (new standing rule 6, row concentration).** Every comparison used for a promotion or a criterion-4 check also reports, per fold, the share of the SSE change carried by the single largest row and by the 10 largest rows. Where one row carries 50 % or more, report its airport, anchor, target and both predictions. This is for attribution only and never changes a fold outcome.

### Acknowledgements
Each `research/day-01/acks/H00X_ack_v1.md` must reference the proposal hash and the review hash. It should also record the corrections listed in that review.

```yaml
schema: advisor-task-result-v1
exchange_id: X-D01-S01-0003
status: COMPLETE
decisions:
  - proposal_id: H001
    proposal_sha256: 38225fb0d6b274cf6904445b2fe0b38de5c2267bee7d140c65e1c07d09dd2d84
    decision: ACCEPT
    review_path: research/day-01/advisor/H001_review_v1.md
    review_sha256: 11ee34242ff190108963443877937e7111e7b819806407ec2ce746c074778945
  - proposal_id: H002
    proposal_sha256: 83e85637037e74215694d0656639f9047fe823903a7f2f17758de544d74be77d
    decision: ACCEPT
    review_path: research/day-01/advisor/H002_review_v1.md
    review_sha256: 600c1de09de900794cc8ddf70514ff1721ab1a356b1f076cb3147b704d9a56e1
  - proposal_id: H003
    proposal_sha256: cbb3848e013eeb924ed5815417c1bd32a9517da323d90d7655ebe1316dc16b80
    decision: ACCEPT
    review_path: research/day-01/advisor/H003_review_v1.md
    review_sha256: 493c824e9a4e5e3e45fa9c48e335d7dede87c1fa7dd711ae55d46d87415265f2
  - proposal_id: H004
    proposal_sha256: 9eb6270e3a3166890a412c98442d07a8e4607c76e3d0206d12a643de496b2621
    decision: ACCEPT
    review_path: research/day-01/advisor/H004_review_v1.md
    review_sha256: 918535aab12f1fbc227ff3ebe7e4969736b4ffd27d1a2c1424016428b519fe01
  - proposal_id: H005
    proposal_sha256: ab97e4312158b0a5c26d6223423539969308daf39ac1807d3c93c6fcf054ff44
    decision: ACCEPT
    review_path: research/day-01/advisor/H005_review_v1.md
    review_sha256: 2b4658c558bd61ee5cca4a87167fa53832e2a16544299c678ead7db8d87b22ea
  - proposal_id: H006
    proposal_sha256: 435a63b783e3a09fef51c92b5608af48941680ca8966cab4303e6639a1a964a8
    decision: ACCEPT
    review_path: research/day-01/advisor/H006_review_v1.md
    review_sha256: 0ea1a1375c58a3dbecd363305f045a46860789ce50828596824aef7ac588a2d1
  - proposal_id: H007
    proposal_sha256: 541ea19a3b65c253a019b629f23a7a4b6fd727d51841bbdb062d0dcd1e011706
    decision: ACCEPT
    review_path: research/day-01/advisor/H007_review_v1.md
    review_sha256: 044e888b56166adddfb6c261afda87a4ccbc8fc24e95aaee5a8fdd5ddeeaa162
  - proposal_id: H008
    proposal_sha256: 8266cc62f8905511bb3a6232ee038fdf30e1f1a2f188ea2efcc9da27f997a525
    decision: ACCEPT
    review_path: research/day-01/advisor/H008_review_v1.md
    review_sha256: affdf8362d80346666a5609aaf87815e8761ef78ac9766e5085ae78b86fed47f
completed_utc: 2026-09-27T12:33:47Z
```
