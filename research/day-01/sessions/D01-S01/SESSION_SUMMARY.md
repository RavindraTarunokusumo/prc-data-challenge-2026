# SESSION_SUMMARY — D01-S01

- **Start / end (UTC):** 2026-09-27T10:54:05Z / 2026-09-27T13:43:31Z
- **Researcher model:** `claude-opus-5-5` (session metadata), effort `high`. **Advisor:** `advisor` subagent; the resolved ID `claude-opus-5-5` is recorded in each review.
- **Branch:** `day-1` (renamed from `claude/quirky-dirac-c0gnnp` on owner instruction; convention recorded in CLAUDE.md). Base: `main` @ `b83acd5`.

## Exchanges

| Exchange | Purpose | Decision |
|---|---|---|
| X-D01-S01-0001 | SPLITS v1 split freeze | REVISE (R1–R6) |
| X-D01-S01-0002 | SPLITS v2 split freeze | ACCEPT, then frozen (`config/frozen.json`) |
| X-D01-S01-0003 | H001–H008 baselines (batched) | 8 × ACCEPT, conditions B1–B4 |
| X-D01-S01-0004 | Day 1 phase close | ACCEPT, corrections C1–C7, rules 7–8 |

## Experiments

- **Allocated through the gate:** E001–E011. Primaries: E001–E006, E010, E011. Reproductions: E007–E009.
- **Status:** all COMPLETE, all within class.
- **Champion:** E005 (H004 ridge, development mean 482.73). Day 1 holdout: WIN (411.29 against 514.74).

## Operational notes

- **Old remote branch.** `claude/quirky-dirac-c0gnnp` could not be deleted: the container's git proxy refuses ref deletion. It points at an ancestor of `day-1`, and the owner can delete it on GitHub.
- **Concurrency.** E006 ran concurrently with the reproductions and comparisons (C5). There is no numerical effect.
- **Last exchange carried over:** none open. Next session: D02-S01 on branch `day-2` from `main` after the Day 1 PR merges.
