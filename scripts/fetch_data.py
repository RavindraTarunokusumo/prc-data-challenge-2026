"""Inventory and download PRC 2026 competition data from the OpenSky MinIO store.

Credentials come from environment variables or the git-ignored .env file and are
never printed. The team submission bucket is refused for any operation
(docs/governance/LEADERBOARD_POLICY.md).

Usage:
    uv run python scripts/fetch_data.py --list [--bucket NAME]
    uv run python scripts/fetch_data.py --pull [--bucket NAME] [--prefix P]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFESTS = ROOT / "data" / "manifests"
SECRET_VARS = ("PRC_S3_ACCESS_KEY", "PRC_S3_SECRET_KEY", "OPENSKY_PASSWORD")


def load_env() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"missing environment variable {name} (see .env.example)")
    return value


def redact(text: str) -> str:
    for var in SECRET_VARS:
        secret = os.environ.get(var)
        if secret:
            text = text.replace(secret, f"<REDACTED:{var}>")
    return text


def client():
    import boto3
    from botocore.config import Config

    endpoint = require("PRC_S3_ENDPOINT")
    if not endpoint.startswith("http"):
        endpoint = f"https://{endpoint}"
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=require("PRC_S3_ACCESS_KEY"),
        aws_secret_access_key=require("PRC_S3_SECRET_KEY"),
        config=Config(signature_version="s3v4", retries={"max_attempts": 5}),
        region_name="us-east-1",
    )


def guard(bucket: str) -> None:
    forbidden = os.environ.get("PRC_SUBMISSION_BUCKET", "prc-2026-genuine-cabbage")
    if bucket == forbidden:
        sys.exit(f"refused: {bucket} is the submission bucket (LEADERBOARD_POLICY)")


def list_objects(s3, bucket: str, prefix: str = "") -> list[dict]:
    guard(bucket)
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            out.append(
                {
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "etag": obj["ETag"].strip('"'),
                    "last_modified": obj["LastModified"].isoformat(),
                }
            )
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true")
    mode.add_argument("--pull", action="store_true")
    parser.add_argument("--bucket", default=None)
    parser.add_argument("--prefix", default="")
    args = parser.parse_args()

    load_env()
    s3 = client()
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    submission = os.environ.get("PRC_SUBMISSION_BUCKET", "prc-2026-genuine-cabbage")

    try:
        if args.bucket or os.environ.get("PRC_DATA_BUCKET"):
            buckets = [args.bucket or os.environ["PRC_DATA_BUCKET"]]
        else:
            names = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
            buckets = [b for b in names if b != submission]
    except Exception as exc:  # noqa: BLE001  (network / auth errors must not leak secrets)
        sys.exit(redact(f"S3 error: {exc}"))

    inventory = {b: list_objects(s3, b, args.prefix) for b in buckets}

    if args.list:
        (MANIFESTS / "remote_inventory.json").write_text(
            json.dumps({"created_utc": now(), "buckets": inventory}, indent=2)
        )
        for b, objs in inventory.items():
            total = sum(o["size"] for o in objs) / 1e9
            print(f"{b}: {len(objs)} objects, {total:.2f} GB")
            for o in objs[:50]:
                print(f"  {o['size']:>14,d}  {o['key']}")
        return

    entries = []
    for b, objs in inventory.items():
        for o in objs:
            dest = RAW / b / o["key"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not (dest.exists() and dest.stat().st_size == o["size"]):
                print(f"get {b}/{o['key']} ({o['size']:,d} B)")
                s3.download_file(b, o["key"], str(dest))
            if dest.stat().st_size != o["size"]:
                sys.exit(f"size mismatch for {b}/{o['key']}")
            entries.append(
                {
                    "path": str(dest.relative_to(ROOT)),
                    "source": f"s3://{b}/{o['key']}",
                    "size": o["size"],
                    "etag": o["etag"],
                    "sha256": sha256(dest),
                    "downloaded_utc": now(),
                }
            )
    (MANIFESTS / "raw_manifest.json").write_text(
        json.dumps({"schema": "raw-manifest-v1", "files": entries}, indent=2)
    )
    print(f"wrote {len(entries)} entries to data/manifests/raw_manifest.json")


if __name__ == "__main__":
    main()
