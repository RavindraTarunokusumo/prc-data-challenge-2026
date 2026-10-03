"""Day 7: format a SUBMIT blend's stored predictions as the challenge submission, and
report the target-free sanity readings pre-registered for it. Never reads a target.

    uv run python scripts/make_submission.py BLEND HALF_A HALF_B --ref BLEND_REF REF_A REF_B

BLEND is the gate-allocated blend experiment that predicted the final folds SUBMIT_JAN and
SUBMIT_JUL; HALF_A / HALF_B are its components. REF_* are the champion and its components
(development folds and H; predictions only, no truth), used as the reference distribution.

Writes predictions/final/submitting.parquet (git-ignored): the template's rows in the
template's order and dtypes, `MVT_ID_mvt` Float64 copied from the template and
`TAXITIME_SEC_mvt` Int32 = the blend's prediction rounded to the nearest integer (half to
even). Nothing else is applied (no clipping, no recalibration). Writes the tracked record
research/day-07/submission/SUBMISSION_RECORD.json (hashes, counts, readings).

Integrity checks (any failure exits 1 and writes no submission file):
  I1  the template matches its raw-manifest SHA-256;
  I2  every prediction file matches its experiment's manifest (prc.blending);
  I3  the blend's IDs equal the template's IDs, 1:1, all finite;
  I4  the blend equals w_a * HALF_A + w_b * HALF_B within 1e-9 s (weights from its config);
  I5  |rounded - raw| <= 0.5 s on every row.
The submission bucket is never touched (docs/governance/LEADERBOARD_POLICY.md).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl
import yaml

from prc.blending import stored_predictions
from prc.paths import EXPERIMENTS, RAW, RAW_MANIFEST, ROOT, SILVER, sha256_file

FINAL_FOLDS = ("SUBMIT_JAN", "SUBMIT_JUL")
REF_FOLDS = ("R1", "R2", "R3", "S1", "W1", "S1c", "W1c", "H")
TEMPLATE = RAW / "submitting.parquet"
OUT = ROOT / "predictions" / "final" / "submitting.parquet"
RECORD = ROOT / "research" / "day-07" / "submission" / "SUBMISSION_RECORD.json"
QS = (0.001, 0.01, 0.05, 0.5, 0.95, 0.99, 0.999)


def fail(msg: str) -> None:
    sys.exit(f"SUBMISSION REFUSED: {msg}")


def subgroups() -> pl.DataFrame:
    """Rule 7 subgroups from target-free silver columns (as scripts/route_check.py)."""
    s = pl.read_parquet(SILVER, columns=["MVT_ID_mvt", "ADEP_mvt", "AOBT_3_flt"])
    return s.select(pl.col("MVT_ID_mvt").cast(pl.Int64), "ADEP_mvt",
                    pl.col("AOBT_3_flt").is_null().alias("nm_missing"))


def manifest_sha(eid: str, fold: str) -> str:
    """The prediction file's SHA-256 as recorded (and verified by stored_predictions)."""
    arts = json.loads((EXPERIMENTS / eid / "manifest.json").read_text())["artifacts"]
    return next(x["sha256"] for x in arts if x["fold"] == fold)


def pred(eid: str, fold: str) -> pl.DataFrame:
    return stored_predictions(eid, fold).select(pl.col("MVT_ID_mvt").cast(pl.Int64), "pred")


def describe(p: np.ndarray) -> dict:
    return {"rows": int(p.size), "mean": float(p.mean()), "std": float(p.std()),
            "min": float(p.min()), "max": float(p.max()),
            **{f"q{q:g}": float(v) for q, v in zip(QS, np.quantile(p, QS), strict=True)}}


def out_of_range(frame: pl.DataFrame) -> dict:
    """Counts below 0 s and above 3,600 s on all rows (no truth, so not bulk rows), by
    rule 7 subgroup."""
    lirf, miss = (frame["ADEP_mvt"] == "LIRF").to_numpy(), frame["nm_missing"].to_numpy()
    p = frame["pred"].to_numpy()
    out = {}
    for name, m in (("NM_present_other", ~miss & ~lirf), ("NM_present_LIRF", ~miss & lirf),
                    ("NM_missing_other", miss & ~lirf), ("NM_missing_LIRF", miss & lirf),
                    ("all", np.ones(p.size, bool))):
        out[name] = {"rows": int(m.sum()), "below0": int((p[m] < 0).sum()),
                     "above3600": int((p[m] > 3600).sum())}
    return out


def fold_reading(blend: str, a: str, b: str, fold: str, sub: pl.DataFrame) -> dict:
    f = pred(blend, fold).join(sub, on="MVT_ID_mvt", how="left", validate="1:1")
    pa, pb = pred(a, fold)["pred"].to_numpy(), pred(b, fold)["pred"].to_numpy()
    by_airport = (f.group_by("ADEP_mvt").agg(pl.len().alias("rows"),
                                             pl.col("pred").mean().alias("mean_pred"))
                  .sort("ADEP_mvt"))
    return {"distribution": describe(f["pred"].to_numpy()),
            "out_of_range": out_of_range(f),
            "rms_half_difference": float(np.sqrt(np.mean((pa - pb) ** 2))),
            "routed_rows": int(((f["ADEP_mvt"] == "LIRF") & f["nm_missing"]).sum()),
            "mean_pred_by_airport": {r["ADEP_mvt"]: {"rows": r["rows"],
                                                     "mean_pred": r["mean_pred"]}
                                     for r in by_airport.iter_rows(named=True)}}


def main(a: argparse.Namespace) -> None:
    # I1
    entry = next(f for f in json.loads(RAW_MANIFEST.read_text())["files"]
                 if f["path"].endswith("submitting.parquet"))
    if sha256_file(TEMPLATE) != entry["sha256"]:
        fail("template does not match data/manifests/raw_manifest.json")
    template = pl.read_parquet(TEMPLATE)
    tid = template["MVT_ID_mvt"]
    if tid.null_count() or tid.is_duplicated().any() or (tid != tid.round(0)).any():
        fail("template IDs are not unique integers")
    weights = yaml.safe_load((EXPERIMENTS / a.blend / "config.yaml").read_text())["params"]
    if weights["components"] != [a.half_a, a.half_b]:
        fail(f"{a.blend}'s components are {weights['components']}, not {[a.half_a, a.half_b]}")
    wa, wb = weights["weights"]

    # I2 (inside stored_predictions), I3, I4
    parts, sources = [], {}
    for fold in FINAL_FOLDS:
        p = pred(a.blend, fold)
        h = pred(a.half_a, fold).rename({"pred": "pa"}).join(
            pred(a.half_b, fold).rename({"pred": "pb"}), on="MVT_ID_mvt", how="full",
            coalesce=True, validate="1:1")
        j = p.join(h, on="MVT_ID_mvt", how="full", coalesce=True, validate="1:1")
        if j.null_count().sum_horizontal().item() or j.height != p.height:
            fail(f"{fold}: blend and halves cover different rows")
        dev = np.abs(j["pred"].to_numpy() - wa * j["pa"].to_numpy() - wb * j["pb"].to_numpy())
        if float(dev.max()) > 1e-9:
            fail(f"{fold}: blend differs from the weighted halves by {dev.max():.3g} s")
        parts.append(p)
        sources[fold] = {e: manifest_sha(e, fold) for e in (a.blend, a.half_a, a.half_b)}
    allp = pl.concat(parts)
    if allp["MVT_ID_mvt"].is_duplicated().any():
        fail("an ID is predicted in both final folds")
    if not np.isfinite(allp["pred"].to_numpy()).all():
        fail("non-finite prediction")
    joined = template.select(pl.col("MVT_ID_mvt"), pl.col("MVT_ID_mvt").cast(pl.Int64)
                             .alias("id")).join(allp.rename({"MVT_ID_mvt": "id"}), on="id",
                                                how="left", validate="1:1")
    if joined.height != template.height or joined["pred"].null_count():
        fail(f"{joined['pred'].null_count()} template IDs have no prediction")
    if allp.height != template.height:
        fail(f"{allp.height - template.height} predicted IDs are not in the template")

    # I5 and the file
    raw = joined["pred"].to_numpy()
    rounded = np.rint(raw)  # half to even
    if np.abs(rounded - raw).max() > 0.5:
        fail("rounding moved a prediction by more than 0.5 s")
    if rounded.min() < np.iinfo(np.int32).min or rounded.max() > np.iinfo(np.int32).max:
        fail("prediction outside Int32")
    sub_df = pl.DataFrame({"MVT_ID_mvt": joined["MVT_ID_mvt"],
                           "TAXITIME_SEC_mvt": pl.Series(rounded.astype(np.int64))
                           .cast(pl.Int32)})
    if sub_df.schema != template.schema or not sub_df["MVT_ID_mvt"].equals(tid):
        fail("output schema or row order differs from the template")

    sub = subgroups()
    readings = {f: fold_reading(a.blend, a.half_a, a.half_b, f, sub) for f in FINAL_FOLDS}
    ref = {f: fold_reading(a.ref[0], a.ref[1], a.ref[2], f, sub) for f in REF_FOLDS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sub_df.write_parquet(OUT)
    record = {
        "schema": "submission-record-v1",
        "blend": a.blend, "halves": [a.half_a, a.half_b], "weights": [wa, wb],
        "reference": {"blend": a.ref[0], "halves": a.ref[1:]},
        "template": {"path": str(TEMPLATE.relative_to(ROOT)), "sha256": entry["sha256"],
                     "rows": template.height, "schema": {k: str(v) for k, v in
                                                         template.schema.items()}},
        "submission": {"path": str(OUT.relative_to(ROOT)), "sha256": sha256_file(OUT),
                       "size": OUT.stat().st_size, "rows": sub_df.height,
                       "post_processing": "round to nearest integer (half to even), Int32; "
                                          "nothing else"},
        "source_prediction_sha256": sources,
        "rounding": {"max_abs_s": float(np.abs(rounded - raw).max()),
                     "rms_s": float(np.sqrt(np.mean((rounded - raw) ** 2)))},
        "integrity": {"I1": True, "I2": True, "I3": True, "I4": True, "I5": True},
        "final_folds": readings,
        "reference_folds": ref,
    }
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(record, indent=1) + "\n")
    print(json.dumps({"rows": sub_df.height, "sha256": record["submission"]["sha256"],
                      "rounding_rms_s": record["rounding"]["rms_s"],
                      **{f: {"mean": r["distribution"]["mean"],
                             "below0": r["out_of_range"]["all"]["below0"],
                             "above3600": r["out_of_range"]["all"]["above3600"],
                             "rms_half_difference": r["rms_half_difference"]}
                         for f, r in readings.items()}}, indent=1))
    print(f"-> {OUT.relative_to(ROOT)}, {RECORD.relative_to(ROOT)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("blend")
    ap.add_argument("half_a")
    ap.add_argument("half_b")
    ap.add_argument("--ref", nargs=3, required=True, metavar=("BLEND", "HALF_A", "HALF_B"))
    main(ap.parse_args())
