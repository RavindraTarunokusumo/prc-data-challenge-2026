---
schema: incident-v1
incident_id: INC-0017
type: owner_intervention
created_utc: 2026-10-04T22:26:33Z
status: closed
---

# After FROZEN: owner instructs the licence and a researcher upload

**Raised by:** the researcher (brief §1: every owner intervention is logged).

## Instruction (owner, verbatim)

> Please do them. Submit to the bucket yourself. You have the credentials.

"Them" refers to the researcher's two open items: adding the GNU GPLv3 licence (the eligibility page requires all source code on GitHub under GPLv3) and the upload of `genuine-cabbage_v1.parquet`.

## Handling

- **Licence: done.** `LICENSE` is added, a verbatim copy of the GNU GPL version 3 text from the system's `/usr/share/common-licenses/GPL-3` (674 lines; SHA-256 `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986`, the canonical `gpl-3.0.txt`). It is a new file only. No research record, code, frozen file or submission changes, and the FROZEN tree is otherwise unchanged (P7 (c)).
- **Upload: not done by the researcher.**
  - The owner's instruction overrides P7 (d)'s "the researcher does not upload", which is the owner's to waive.
  - The researcher's first step was to inspect how `scripts/fetch_data.py` builds its connection. The session's permission system denied it as credential exploration. Following that denial, the researcher did not try the upload by any other route.
  - **The upload stays with the owner,** as originally recorded. Alternatively, the owner may grant the permission in their Claude Code settings and ask again.

## Resolution

Open until the upload record is appended (P7 (d): upload time, SHA-256 `f0dc2c7c40063e238ef57f51d31192008e37c5327afcdc67d563868af17d06e8`, FROZEN commit `4c21eff`).

## Closure

The owner uploaded `genuine-cabbage_v1.parquet` by hand; recorded in `research/day-07/submission/UPLOAD_RECORD.md`.
