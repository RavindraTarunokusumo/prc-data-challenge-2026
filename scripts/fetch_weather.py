"""Day 8 (INC-0019): download archived METAR/SPECI observations from the Iowa Environmental
Mesonet (IEM) ASOS archive, an allowlisted host (config/network.yaml, `weather`).

    uv run python scripts/fetch_weather.py                # LTFM, 2025-01-01 .. 2026-08-01
    uv run python scripts/fetch_weather.py --station LTFM --start 2025-01 --end 2026-07

One request per calendar month (UTC), all IEM fields (`data=all`), routine and special reports
(report_type 3 and 4). Raw CSV goes to data/raw/weather/ (bronze; git-ignored). The manifest
data/manifests/weather_<station>_manifest.json (tracked) records, per month, the source URL,
retrieval time, byte and row counts and SHA-256 (DATA_POLICY bronze rules). No credential is
needed. Nothing here reads a challenge file or a target; use of the data needs its own
reviewed proposal (DATA_POLICY rule 7).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
UA = "prc-data-challenge-2026 research (weather for taxi-out modelling; INC-0019)"


def months(start: str, end: str) -> list[tuple[dt.date, dt.date]]:
    y, m = map(int, start.split("-"))
    ye, me = map(int, end.split("-"))
    out = []
    while (y, m) <= (ye, me):
        a = dt.date(y, m, 1)
        y2, m2 = (y + 1, 1) if m == 12 else (y, m + 1)
        out.append((a, dt.date(y2, m2, 1)))
        y, m = y2, m2
    return out


def url_for(station: str, a: dt.date, b: dt.date) -> str:
    q = [("station", station), ("data", "all"), ("year1", a.year), ("month1", a.month),
         ("day1", a.day), ("year2", b.year), ("month2", b.month), ("day2", b.day),
         ("tz", "Etc/UTC"), ("format", "onlycomma"), ("latlon", "no"), ("elev", "no"),
         ("missing", "M"), ("trace", "T"), ("direct", "no"), ("report_type", 3),
         ("report_type", 4)]
    return HOST + "?" + urllib.parse.urlencode(q)


def fetch(url: str, tries: int = 4) -> bytes:
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except OSError as e:
            if k == tries - 1:
                raise
            print(f"  retry {k + 1}: {e}", file=sys.stderr)
            time.sleep(5 * (k + 1))
    raise RuntimeError("unreachable")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--station", default="LTFM")
    ap.add_argument("--start", default="2025-01")
    ap.add_argument("--end", default="2026-07")
    a = ap.parse_args()
    out_dir = ROOT / "data/raw/weather" / a.station
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for m0, m1 in months(a.start, a.end):
        url = url_for(a.station, m0, m1)
        body = fetch(url)
        if not body.startswith(b"station,"):
            sys.exit(f"{a.station} {m0:%Y-%m}: unexpected response: {body[:200]!r}")
        path = out_dir / f"{a.station}_{m0:%Y-%m}.csv"
        path.write_bytes(body)
        rows = body.count(b"\n") - 1
        entries.append({"month": f"{m0:%Y-%m}", "path": str(path.relative_to(ROOT)),
                        "url": url, "retrieved_utc": dt.datetime.now(dt.UTC)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"), "bytes": len(body), "rows": rows,
                        "sha256": hashlib.sha256(body).hexdigest()})
        print(f"{a.station} {m0:%Y-%m}: {rows} rows", flush=True)
        time.sleep(1)  # be polite to the archive
    man = ROOT / "data/manifests" / f"weather_{a.station}_manifest.json"
    man.write_text(json.dumps({"schema": "bronze-manifest-v1", "source": "IEM ASOS archive",
                               "host": "mesonet.agron.iastate.edu", "basis": "INC-0019",
                               "station": a.station, "months": entries}, indent=1) + "\n")
    print(f"manifest: {man.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
