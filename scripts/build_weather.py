"""Build the weather report table from the bronze IEM files (INC-0019; DATA_POLICY rule 7).

Reads data/manifests/weather_<station>_manifest.json for the ten challenge airports,
verifies every month file's SHA-256, and writes one typed table of reports
(prc.weather.reports) to data/processed/weather_reports.parquet, with its manifest
data/manifests/weather_reports_manifest.json. Reads no challenge file and no target.

    uv run python scripts/build_weather.py
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from prc.features import AIRPORT_TZ
from prc.paths import MANIFESTS, PROCESSED, ROOT, git_commit, git_dirty, sha256_file
from prc.weather import reports

OUT = PROCESSED / "weather_reports.parquet"
OUT_MANIFEST = MANIFESTS / "weather_reports_manifest.json"


def main() -> None:
    frames, sources = [], []
    for station in sorted(AIRPORT_TZ):
        man = json.loads((MANIFESTS / f"weather_{station}_manifest.json").read_text())
        for e in man["months"]:
            path = ROOT / e["path"]
            if sha256_file(path) != e["sha256"]:
                sys.exit(f"{path}: SHA-256 differs from {station}'s manifest")
            frames.append(pl.read_csv(path, infer_schema_length=0))
        sources.append({"station": station, "manifest": f"data/manifests/weather_{station}_manifest.json",
                        "manifest_sha256": sha256_file(MANIFESTS / f"weather_{station}_manifest.json"),
                        "months": len(man["months"])})
    table = reports(pl.concat(frames, how="diagonal"))
    table.write_parquet(OUT)
    OUT_MANIFEST.write_text(json.dumps({
        "schema": "silver-manifest-v1", "path": str(OUT.relative_to(ROOT)),
        "sha256": sha256_file(OUT), "bytes": OUT.stat().st_size, "rows": table.height,
        "per_station_rows": dict(table.group_by("station").len().sort("station").iter_rows()),
        "valid_min": str(table["valid"].min()), "valid_max": str(table["valid"].max()),
        "sources": sources, "code_commit": git_commit(), "code_dirty": git_dirty(),
        "created_utc": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "command": "uv run python scripts/build_weather.py"}, indent=1) + "\n")
    print(f"{OUT.relative_to(ROOT)}: {table.height} reports, {len(sources)} stations")


if __name__ == "__main__":
    main()
