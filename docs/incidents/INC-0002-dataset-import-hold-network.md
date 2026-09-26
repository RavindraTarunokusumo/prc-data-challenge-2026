---
schema: incident-v1
incident_id: INC-0002
type: infrastructure_hold
created_utc: 2026-09-26T00:00:00Z
status: open
---

# Dataset import on HOLD: network policy

The cloud environment's egress policy returned HTTP 403 (CONNECT denied) for:

- `prc-data-challenge-2026.netlify.app` (dataset documentation)
- `s3.opensky-network.org` (presumed MinIO endpoint)
- `opensky-network.org`

**Resolution required (owner):** allow these hosts in the cloud environment's
network settings, and provide credentials as environment variables (brief v3 §5.2).
Then run `scripts/fetch_data.py --list` and `--pull`, and close this incident with
the manifest hashes.
