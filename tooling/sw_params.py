#!/usr/bin/env python3
"""Read and change SolidWorks geometry parameters by logical name.

The mapping (logical name -> part file -> dimension name -> unit kind) lives in
simulation/cases/bga-2024r2-unsolved/data/geometry-parameters.csv.

Commands
  list                      enumerate dimensions of every part in the table
  show                      print the mapping table
  set NAME VALUE [--commit] change one parameter, verify, optionally save

Safety defaults
  * set works on a COPY of the part; the original is untouched unless --in-place
  * nothing is saved unless --commit is given
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TABLE = REPO / "simulation/cases/bga-2024r2-unsolved/data/geometry-parameters.csv"
MODELS = Path("D:/SWMCP/models/BGA")
WORK = Path("C:/Users/007/Documents/deepseek-harness/default-workspace/swtest")

MM_PER_M = 1000.0
DEG_PER_RAD = 57.29577951308232


def sw_app():
    import win32com.client as win32
    return win32.Dispatch("SldWorks.Application")


def load_table() -> list[dict]:
    with TABLE.open(encoding="utf-8-sig", newline="") as fh:
        return [row for row in csv.DictReader(fh) if row.get("logical_name")]


def enumerate_part(sw, part: str) -> dict:
    """Probe D1..D9 for every feature name; no UI interaction needed."""
    path = WORK / part
    if not path.exists():
        WORK.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MODELS / part, path)
    doc = sw.OpenDoc(str(path), 1)
    rec = {"part": part, "dimensions": []}
    if not doc:
        rec["error"] = "open failed"
        return rec
    try:
        features = [f.Name for f in (doc.FeatureManager.GetFeatures(True) or [])]
        for fname in features:
            for i in range(1, 10):
                name = "D%d@%s" % (i, fname)
                try:
                    dim = doc.Parameter(name)
                except Exception:
                    dim = None
                if dim:
                    try:
                        raw = float(dim.SystemValue)
                    except Exception:
                        raw = None
                    angular = _looks_angular(fname)
                    value = None
                    if raw is not None:
                        value = round(raw * DEG_PER_RAD, 6) if angular else round(raw * MM_PER_M, 6)
                    rec["dimensions"].append({"name": name, "value": value,
                                              "kind": "angle" if angular else "length"})
    finally:
        try:
            sw.CloseDoc(doc.GetTitle)
        except Exception:
            pass
    return rec


def _looks_angular(feature: str) -> bool:
    return any(k in feature for k in ("旋转", "Revolve", "角度"))


def set_parameter(args) -> dict:
    rows = load_table()
    row = next((r for r in rows if r["logical_name"] == args.name), None)
    if not row:
        return {"error": "unknown logical name: " + args.name,
                "known": [r["logical_name"] for r in rows]}
    part, dimension = row["part_file"], row["dimension_name"]
    kind = row["kind"]
    value = float(args.value)
    target = value / MM_PER_M if kind == "length" else value / DEG_PER_RAD

    WORK.mkdir(parents=True, exist_ok=True)
    src = MODELS / part
    if args.in_place:
        shutil.copy2(src, WORK / (part + ".backup"))
        work = src
    else:
        work = WORK / (part.replace(".SLDPRT", "") + "_edit.SLDPRT")
        shutil.copy2(src, work)

    sw = sw_app()
    time.sleep(1)
    doc = sw.OpenDoc(str(work), 1)
    if not doc:
        return {"error": "open failed", "path": str(work)}
    out = {"parameter": args.name, "part": part, "dimension": dimension, "kind": kind,
           "target_value": value, "path": str(work), "saved": False,
           "stack_axis": row.get("stack_axis") or "",
           "interferes_with": row.get("interferes_with") or "",
           "compensation": row.get("compensation") or "",
           "next_check": "重建后必须跑干涉检查；随动未实现时干涉体积约等于面积×增量"}
    try:
        dim = doc.Parameter(dimension)
        if not dim:
            out["error"] = "dimension not found in this part"
            return out
        out["before"] = round(float(dim.SystemValue) * (MM_PER_M if kind == "length" else DEG_PER_RAD), 6)
        dim.SystemValue = target
        try:
            doc.EditRebuild3()
        except Exception:
            try:
                doc.ForceRebuild3(False)
            except Exception:
                pass
        after_raw = float(dim.SystemValue)
        out["after"] = round(after_raw * (MM_PER_M if kind == "length" else DEG_PER_RAD), 6)
        try:
            out["needs_rebuild"] = bool(doc.Extension.NeedsRebuild2)
        except Exception:
            pass
        out["verified"] = abs(after_raw - target) < 1e-9
        if args.commit and out["verified"]:
            doc.Save3(1, None, None) if hasattr(doc, "Save3") else doc.Save()
            out["saved"] = True
    finally:
        try:
            sw.CloseDoc(doc.GetTitle)
        except Exception:
            pass
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["list", "show", "set"])
    ap.add_argument("name", nargs="?")
    ap.add_argument("value", nargs="?")
    ap.add_argument("--commit", action="store_true", help="save the document after verification")
    ap.add_argument("--in-place", action="store_true", help="edit the original file (a .backup copy is kept)")
    args = ap.parse_args()

    if args.command == "show":
        print(json.dumps(load_table(), ensure_ascii=False, indent=1))
        return 0
    if args.command == "list":
        sw = sw_app()
        time.sleep(1)
        parts = sorted({r["part_file"] for r in load_table()})
        print(json.dumps([enumerate_part(sw, p) for p in parts], ensure_ascii=False, indent=1))
        return 0
    if not args.name or args.value is None:
        print("set requires NAME and VALUE", file=sys.stderr)
        return 2
    print(json.dumps(set_parameter(args), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
