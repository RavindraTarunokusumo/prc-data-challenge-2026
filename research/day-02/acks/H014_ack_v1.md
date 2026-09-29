# Acknowledgement — H014 v1 (exchange X-D02-S01-0004)

- proposal: `research/day-02/proposals/H014_v1.md`, sha256 `bfaadc501f4752e83171c10afff3290b1eb5b6dfa40d817ea21ffbe23ee4eca8`
- review: `research/day-02/advisor/H014_review_v1.md`, sha256 `479534116888f92aa63fb9d3187625e3569c24869b45816a7656f5111a2c2b09`
- decision received: **ACCEPT** (confidence 0.80), conditional. Both hashes verified by the researcher.

**Adopted preconditions** before `gate.py allocate H014 v1`: 1(a)–(e) as written in the review.
- (a) An H013 version ≥ 2 is ACCEPTED and acknowledged.
- (b) That version's training configuration is H014 v1's, except for the feature set, and sets no other training parameter.
- (c) It uses H014 as its M1 reference.
- (d) H013's primary run is COMPLETE, and H013 passes its clause 1.
- (e) The code and environment are unchanged, and nothing runs concurrently.

**Lapse rule adopted:** if (b) or (c) fails, this ACCEPT lapses and `H014_v2` is required.

**Recorded:** H014 matches H013 on the bin sample only while both use seed 42 on the same training rows.

**Status.** H013 v2 adds `bin_construct_sample_cnt` (option (a) of `H013_review_v1.md`). Precondition (b) will therefore not hold, and **this ACCEPT lapses by its own rule.** `H014_v2.md`, matched to H013 v2, is submitted in exchange X-D02-S01-0005. H014 v1 will never be allocated.
