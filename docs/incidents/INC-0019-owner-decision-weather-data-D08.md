---
schema: incident-v1
incident_id: INC-0019
type: owner_decision
created_utc: 2026-10-05T14:15:21Z
status: open
---

# Day 8: owner approves external weather data (agenda item 3, G9)

**Raised by:** the researcher, recording an owner decision in D08-S02 (cloud session).

## Instruction (owner, D08-S02, verbatim)

> Weather data approved, make sure first the domain is in the allow list in the config file.

## What this covers (G9 item 3)

1. **The owner decision, recorded as an incident.** This file.
2. **Allowlisted hosts:** `config/network.yaml` gains a `weather` section with two hosts:
   - **`mesonet.agron.iastate.edu`** (Iowa Environmental Mesonet, Iowa State University).
     - Archived METAR and SPECI observations for the ten challenge airports (ICAO codes, e.g. LTFM).
     - Endpoint `/cgi-bin/request/asos.py`.
     - **Primary:** observed weather at the airport, including present-weather codes such as snow and freezing precipitation.
   - **`archive-api.open-meteo.com`** (Open-Meteo historical weather API).
     - Hourly reanalysis at airport coordinates.
     - Licence: CC BY 4.0.
     - **Fallback** if the METAR archive is incomplete.
3. **DATA_POLICY rule 7 (external data).**
   - **Pre-registration.** Any use needs its own H proposal and an Advisor review. The proposal states the exact fields and the availability rule.
   - **Availability at prediction time.** Only an observation issued before the flight's actual off-block time (or before the P anchor the feature uses) may enter a feature. METARs are issued at least hourly, and the issue time of the most recent observation is known in real time. The same holds for the ranking months, January and July 2026.
   - **Competition permission.** The challenge's eligibility page was read on 2026-10-05. It says external datasets must be "openly accessible/usable and documented", and additional datasets must be "openly available under an open source license".
     - Open-Meteo is CC BY 4.0.
     - Both IEM and Open-Meteo archives are publicly downloadable without an account.
     - The licence fit of the IEM METAR archive is recorded as a check for the proposal, not as settled.
   - **No exposure to ranking content.** Only `eligibility.html`, `data.html` and `rationale.html` were read. The ranking page and team pages were not opened.

## Network reachability

- **Cloud.** On 2026-10-05, this cloud environment's network policy refused both hosts (proxy CONNECT 403). `config/network.yaml` records what is permitted; the environment setting is the owner's to change.
- **Laptop.** Days 8–12 compute runs on the owner's laptop (G6). The weather fetch is expected to run there, under the same allowlist.

## Data handling

- Raw downloads go to `data/raw/weather/` (bronze; git-ignored), with a manifest giving source URL, retrieval time, row count and SHA-256 (DATA_POLICY bronze rules).
- No credential is needed for either host.

## Resolution

Open. Closes when the weather proposal is decided, or at the refreeze.

## Amendment (2026-10-07T18:50:07Z, D08-S03, laptop; appended)

- **The laptop session cannot reach either weather host either.** `scripts/fetch_weather.py` (commit 930b788) has not run.
  - `mesonet.agron.iastate.edu` and `archive-api.open-meteo.com` resolve, and TCP connects. The connection is then reset during the TLS handshake, after the server hello. `api.wandb.ai` behaves the same. `pypi.org` and `arxiv.org` answer 200 from the same shell.
  - No proxy variable is set, and no project or user Claude Code settings file configures the sandbox's network.
  - The researcher asked to run one probe outside the Claude Code sandbox. The harness refused it. The researcher does not pursue the fetch by any other route.
- **Owner decision needed:** (a) the owner runs the fetch from their own terminal; (b) the owner permits these hosts for the session; or (c) agenda item 3 is dropped for Days 8–12.
- No weather data exists in the repository. Nothing has been allocated for weather.

## Correction (2026-10-07T19:21:12Z, D08-S03; appended)

- **The cause is not the Claude Code sandbox.** The session's shell runs without one: there is no bubblewrap process and no proxy, and PID 1 is the host's systemd. Commit 930b788's message ("the session sandbox resets connections") and the amendment above were wrong to point to the sandbox. This was the researcher's error.
- The reset happens in the network path between the laptop and the hosts: in WSL, Windows, a security product, or the local network. A Claude Code permission change does not affect it.
- The owner reports that the fetch script also fails when the owner runs it.
