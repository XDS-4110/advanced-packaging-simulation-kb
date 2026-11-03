#!/usr/bin/env python3
"""Knowledge-base retrieval for advanced-packaging-simulation-kb.

Stdlib only. Subcommands:
  search  <query> [--tier strict|explain] [--k N]
  resolve <stage>
  lookup  <entity> [property]
  eval    [--csv path]
  serve                     # minimal MCP stdio server (JSON-RPC 2.0, newline framed)

Status gating is enforced here, not in prompts:
  strict  -> reviewed, validated only            (usable for arguments)
  explain -> strict + draft (labelled)           (never usable for arguments)
"""

from __future__ import annotations

import argparse
import csv
import json
import hashlib
import math
import os
import re
import sys
from pathlib import Path

def find_repo(start: Path) -> Path:
    """Walk up until a repository marker is found, so the file can move."""
    for candidate in [start, *start.parents]:
        if (candidate / "shared/rag/thermal-structural-profile.json").exists() \
                or (candidate / "shared/references/catalog.csv").exists():
            return candidate
    return start.parents[1]


REPO = Path(os.environ.get("KB_REPO") or find_repo(Path(__file__).resolve().parent)).resolve()

STRICT = {"reviewed", "validated"}
EXPLAIN = STRICT | {"draft"}
# Only knowledge entries are searched. Instruction files and code must never
# become citable "sources": the agent would otherwise cite its own rules.
EXCLUDED_DIRS = ("shared/templates/", "shared/tools/", "files/", "tooling/")
EXCLUDED_FILES = ("README.md", "AGENTS.md", "CONTRIBUTING.md")

CJK = re.compile(r"[\u4e00-\u9fa5]+")
ASCII = re.compile(r"[A-Za-z][A-Za-z0-9_\-\.]{1,}")


# ---------------------------------------------------------------- corpus

def front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            v = v.strip().strip('"').strip("'")
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            meta[k.strip()] = v
    return meta, text[m.end():]


def excluded(rel: str) -> bool:
    if any(rel.startswith(d) for d in EXCLUDED_DIRS):
        return True
    return Path(rel).name in EXCLUDED_FILES


def load_docs(root: Path) -> list[dict]:
    docs = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if excluded(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        meta, body = front_matter(text)
        docs.append({
            "path": rel,
            "id": str(meta.get("id", "")) or f"PATH:{rel}",
            "title": str(meta.get("title", "")) or Path(rel).stem,
            "status": str(meta.get("status", "")) or "none",
            "domain": str(meta.get("domain", "")),
            "document_type": str(meta.get("document_type", "")),
            "tags": meta.get("tags", []) if isinstance(meta.get("tags", []), list) else [],
            "source_ids": meta.get("source_ids", []) if isinstance(meta.get("source_ids", []), list) else [],
            "source_locator": str(meta.get("source_locator", "")),
            "body": body,
        })
    return docs


def tokens(text: str) -> list[str]:
    out = []
    for run in CJK.findall(text):
        if len(run) == 1:
            out.append(run)
        for i in range(len(run) - 1):
            out.append(run[i:i + 2])
    for w in ASCII.findall(text):
        out.append(w.lower().strip(".-"))
    return [t for t in out if t]


def chunk(doc: dict) -> list[dict]:
    parts = re.split(r"(?m)^##\s+", doc["body"])
    chunks = []
    head = parts[0]
    if head.strip():
        chunks.append({"heading": "", "text": head})
    for part in parts[1:]:
        lines = part.splitlines()
        heading = lines[0].strip() if lines else ""
        chunks.append({"heading": heading, "text": part})
    out = []
    for c in chunks:
        c["text"] = c["text"].strip()
        if len(c["text"]) < 40:
            continue
        out.append({**{k: doc[k] for k in ("path", "id", "title", "status", "domain",
                                           "document_type", "source_locator", "source_ids")},
                    "heading": c["heading"], "text": c["text"],
                    "tokens": tokens(doc["title"] + " " + c["heading"] + " " + c["text"])})
    return out


class Index:
    def __init__(self, root: Path):
        self.docs = load_docs(root)
        self.chunks = [c for d in self.docs for c in chunk(d)]
        self.df: dict[str, int] = {}
        for c in self.chunks:
            for t in set(c["tokens"]):
                self.df[t] = self.df.get(t, 0) + 1
        self.n = len(self.chunks)
        self.avgdl = sum(len(c["tokens"]) for c in self.chunks) / max(self.n, 1)
        self.tf = [{t: c["tokens"].count(t) for t in set(c["tokens"])} for c in self.chunks]

    def idf(self, term: str) -> float:
        df = self.df.get(term, 0)
        return math.log(1 + (self.n - df + 0.5) / (df + 0.5))

    def search(self, query: str, tier: str = "explain", k: int = 5) -> list[dict]:
        q = tokens(query)
        if not q:
            return []
        allowed = STRICT if tier == "strict" else EXPLAIN
        k1, b = 1.2, 0.75
        scored = []
        for i, c in enumerate(self.chunks):
            if c["status"] not in allowed:
                continue
            dl = len(c["tokens"]) or 1
            score = 0.0
            for term in set(q):
                f = self.tf[i].get(term, 0)
                if not f:
                    continue
                score += self.idf(term) * (f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / self.avgdl))
            if not score:
                continue
            low_title = c["title"].lower()
            score += sum(1.5 for term in set(q) if term in low_title)
            if c["id"] and c["id"].lower() == query.strip().lower():
                score += 10
            scored.append((score, i))
        scored.sort(reverse=True)
        out, seen = [], set()
        for score, i in scored:
            c = self.chunks[i]
            if c["id"] in seen:
                continue
            seen.add(c["id"])
            out.append({
                "id": c["id"], "path": c["path"], "heading": c["heading"],
                "status": c["status"], "score": round(score, 3),
                "usable_for_arguments": c["status"] in STRICT,
                "source_locator": c["source_locator"],
                "excerpt": c["text"][:280].replace("\n", " "),
            })
            if len(out) >= k:
                break
        return out


# ---------------------------------------------------------------- staging

def profile(root: Path) -> dict:
    p = root / "shared/rag/thermal-structural-profile.json"
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else {}


def resolve(root: Path, stage: str) -> list[dict]:
    prof = profile(root)
    hits = [d for d in prof.get("core_operation_documents", []) if d.get("stage") == stage]
    if not hits:
        stages = sorted({d.get("stage", "") for d in prof.get("core_operation_documents", [])})
        return [{"error": f"unknown stage: {stage}", "available_stages": stages}]
    out = []
    for h in hits:
        p = root / h["path"]
        meta = {}
        if p.exists():
            meta, _ = front_matter(p.read_text(encoding="utf-8-sig"))
        out.append({"id": h.get("id"), "path": h["path"], "stage": stage,
                    "status": meta.get("status", "missing"),
                    "title": meta.get("title", "")})
    deps = prof.get("conditional_dependencies", {})
    return [{"documents": out, "conditional_dependencies": deps,
             "allowlist": prof.get("default_status_allowlist", []),
             "exclude": prof.get("exclude_from_default_context", [])}]


# ---------------------------------------------------------------- lookup

def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


PROPERTY_ALIASES = {
    "anand": "viscoplasticity", "粘塑性": "viscoplasticity", "本构": "viscoplasticity",
    "cte": "coefficient of thermal expansion", "热膨胀": "coefficient of thermal expansion",
    "e": "elasticity", "young": "elasticity", "模量": "elasticity", "泊松": "elasticity",
    "导热": "thermal conductivity", "conductivity": "thermal conductivity",
    "密度": "density", "比热": "specific heat", "specific heat": "specific heat",
}


def lookup(root: Path, entity: str, prop: str | None = None) -> dict:
    registry = read_csv(root / "shared/entities/registry.csv")
    row = next((r for r in registry if r["stable_id"] == entity), None)
    result = {"entity": entity, "found_in_registry": bool(row)}
    if row:
        result.update({
            "entity_kind": row["entity_kind"],
            "model_revision": row["model_revision"] or None,
            "resolution_state": row["resolution_state"],
            "blocking_reason": row["blocking_reason"] or None,
            "aliases": [a for a in row.get("aliases", "").split(";") if a],
            "source_ids": [s for s in row["source_ids"].split(";") if s],
            "source_locator": row["source_locator"],
            "usable_for_arguments": bool(row["model_revision"]) and row["resolution_state"] == "resolved",
        })
    if prop and row and row["entity_kind"] == "material":
        catalog = {r["material_id"]: r for r in read_csv(root / "shared/materials/catalog.csv")}
        mat = catalog.get(entity, {})
        name = row.get("material_name_hint") or mat.get("material_name_as_imported", "")
        needle = PROPERTY_ALIASES.get(prop.lower(), prop.lower())
        rows = [r for r in read_csv(root / "shared/materials/datasets/bga-2024r2-draft/material-parameters.csv")
                if r.get("material") == name
                and needle in (r.get("property", "") + " " + r.get("parameter", "")).lower()]
        result["property"] = prop
        result["values"] = [{"property": r["property"], "value": r["raw_values"],
                             "unit": r["unit_as_exported"], "temperature_axis_degC": r["temperature_axis_degC"],
                             "source": "shared/materials/datasets/bga-2024r2-draft/material-parameters.csv"}
                            for r in rows][:12]
        result["value_count"] = len(rows)
    return result


# ---------------------------------------------------------------- eval

def run_eval(root: Path, csv_path: Path) -> dict:
    idx = Index(root)
    rows = read_csv(csv_path)
    detail, hits, mrr, violations = [], 0, 0.0, 0
    for r in rows:
        q = r["question"]
        tier = r.get("tier") or "explain"
        got = idx.search(q, tier=tier, k=5)
        ids = [g["id"] for g in got]
        expected = [x for x in (r.get("expected_ids") or "").split(";") if x]
        banned = [x for x in (r.get("must_not_include") or "").split(";") if x]
        hit = any(e in ids for e in expected)
        rank = next((i + 1 for i, g in enumerate(got) if g["id"] in expected), None)
        bad = [b for b in banned if b in ids]
        hits += hit
        mrr += (1.0 / rank) if rank else 0.0
        violations += len(bad)
        detail.append({"question": q, "tier": tier, "hit": hit, "rank": rank,
                       "got": ids, "expected": expected, "gate_violations": bad})
    return {"n": len(rows), "hit_at_5": round(hits / max(len(rows), 1), 3),
            "mrr": round(mrr / max(len(rows), 1), 3), "gate_violations": violations,
            "detail": detail}


def info(root: Path) -> dict:
    """Self-check for a fresh machine: same KB revision produces the same digest."""
    idx = Index(root)
    h = hashlib.sha256()
    for d in sorted(idx.docs, key=lambda x: x["path"]):
        h.update(d["path"].encode("utf-8"))
        # normalise newlines: git autocrlf must not change the corpus identity
        h.update(hashlib.sha256(d["body"].replace("\r\n", "\n").encode("utf-8")).digest())
    status: dict[str, int] = {}
    for d in idx.docs:
        status[d["status"]] = status.get(d["status"], 0) + 1
    digest = h.hexdigest()
    base_path = Path(__file__).with_name("corpus-baseline.json")
    expected = json.loads(base_path.read_text(encoding="utf-8")) if base_path.exists() else None
    report = {"repo": str(root), "python": sys.version.split()[0],
              "platform": sys.platform, "documents": len(idx.docs),
              "chunks": len(idx.chunks), "by_status": status,
              "corpus_sha256": digest,
              "registry_present": (root / "shared/entities/registry.csv").exists()}
    if expected:
        report["baseline"] = {"commit": expected.get("commit"),
                              "corpus_sha256": expected.get("corpus_sha256"),
                              "documents": expected.get("documents")}
        report["baseline_match"] = (digest == expected.get("corpus_sha256")
                                    and len(idx.docs) == expected.get("documents"))
    return report


# ---------------------------------------------------------------- MCP

TOOLS = [
    {"name": "kb_search", "description": "Semantic-ish BM25 search over the knowledge base with status gating. tier=strict returns only reviewed/validated (usable for arguments); tier=explain also returns draft, labelled.",
     "inputSchema": {"type": "object", "required": ["query"], "properties": {
         "query": {"type": "string"}, "tier": {"type": "string", "enum": ["strict", "explain"]},
         "k": {"type": "integer"}}}},
    {"name": "kb_resolve", "description": "Return the documents assigned to a workflow stage by thermal-structural-profile.json.",
     "inputSchema": {"type": "object", "required": ["stage"], "properties": {"stage": {"type": "string"}}}},
    {"name": "kb_lookup", "description": "Deterministic lookup: registry row for an entity, optionally material property rows. Never infer values.",
     "inputSchema": {"type": "object", "required": ["entity"], "properties": {
         "entity": {"type": "string"}, "property": {"type": "string"}}}},
]


def call_tool(root: Path, name: str, args: dict) -> dict:
    if name == "kb_search":
        idx = Index(root)
        return {"results": idx.search(args["query"], args.get("tier", "explain"), int(args.get("k", 5)))}
    if name == "kb_resolve":
        return {"stage": args["stage"], "result": resolve(root, args["stage"])}
    if name == "kb_lookup":
        return lookup(root, args["entity"], args.get("property"))
    raise ValueError("unknown tool: " + name)


def serve(root: Path) -> None:
    # MCP stdio is UTF-8; Windows consoles default to a legacy code page.
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method, mid = msg.get("method"), msg.get("id")
        if method == "initialize":
            result = {"protocolVersion": "2024-11-05",
                      "capabilities": {"tools": {}},
                      "serverInfo": {"name": "kb-retrieve", "version": "0.1.0"}}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = msg.get("params", {})
            try:
                payload = call_tool(root, params.get("name", ""), params.get("arguments") or {})
                result = {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}
            except Exception as exc:  # noqa: BLE001
                result = {"content": [{"type": "text", "text": "ERROR: " + str(exc)}], "isError": True}
        elif method == "ping":
            result = {}
        else:
            if mid is None:
                continue
            print(json.dumps({"jsonrpc": "2.0", "id": mid,
                              "error": {"code": -32601, "message": "method not found"}}), flush=True)
            continue
        print(json.dumps({"jsonrpc": "2.0", "id": mid, "result": result}, ensure_ascii=False), flush=True)


# ---------------------------------------------------------------- cli

def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(REPO))
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--tier", default="explain", choices=["strict", "explain"]); s.add_argument("--k", type=int, default=5)
    r = sub.add_parser("resolve"); r.add_argument("stage")
    l = sub.add_parser("lookup"); l.add_argument("entity"); l.add_argument("property", nargs="?")
    e = sub.add_parser("eval"); e.add_argument("--csv", default=str(Path(__file__).with_name("kb_eval.csv")))
    sub.add_parser("info")
    sub.add_parser("serve")
    args = ap.parse_args()
    root = Path(args.repo).resolve()

    if args.cmd == "search":
        out = Index(root).search(args.query, args.tier, args.k)
    elif args.cmd == "resolve":
        out = resolve(root, args.stage)
    elif args.cmd == "lookup":
        out = lookup(root, args.entity, args.property)
    elif args.cmd == "eval":
        out = run_eval(root, Path(args.csv))
    elif args.cmd == "info":
        out = info(root)
    else:
        serve(root)
        return 0
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
