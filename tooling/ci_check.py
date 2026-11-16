#!/usr/bin/env python3
"""Repository checks that need no third-party packages.

Run locally with:  python tooling/ci_check.py
Checks documentation only; does not execute a solver or model.

Checks
  1. the indexed corpus matches tooling/corpus-baseline.json
  2. no UTF-8 BOM and no CRLF in tracked text files
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import kb_retrieve  # noqa: E402

# Only files this project authors by hand. Machine exports (CSV under data/ and
# datasets/) can carry a BOM from spreadsheet exports and are read with utf-8-sig.
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml"}
TEXT_NAMES = {".gitattributes", ".gitignore"}
SKIP_DIRS = {".git", "files", "node_modules", "__pycache__"}


def main() -> int:
    failures: list[str] = []

    # 1. corpus baseline
    report = kb_retrieve.info(kb_retrieve.REPO)
    print(f"documents={report['documents']} chunks={report['chunks']}")
    print(f"corpus_sha256={report['corpus_sha256']}")
    if not report.get("baseline_match"):
        base = report.get("baseline") or {}
        failures.append(
            "corpus differs from tooling/corpus-baseline.json "
            f"(baseline: {base.get('documents')} docs, {str(base.get('corpus_sha256'))[:16]}...)"
            " — update the baseline in the same PR that changes knowledge content"
        )

    # 2. BOM / CRLF hygiene
    bad: list[str] = []
    for path in kb_retrieve.REPO.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(kb_retrieve.REPO)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            bad.append(f"BOM: {rel}")
        if b"\r\n" in data:
            bad.append(f"CRLF: {rel}")
    if bad:
        failures.append(f"{len(bad)} file(s) with BOM or CRLF:\n  " + "\n  ".join(bad[:20]))

    # 3. source registry integrity
    catalog = kb_retrieve.REPO / "shared/references/catalog.csv"
    if catalog.exists():
        import csv as _csv
        import re as _re
        with catalog.open(encoding="utf-8-sig", newline="") as fh:
            ids = [row["source_id"] for row in _csv.DictReader(fh) if row.get("source_id")]
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            failures.append("duplicate source_id in catalog.csv: " + ", ".join(dupes))
        known = set(ids)
        unknown: dict[str, str] = {}
        for md in kb_retrieve.REPO.rglob("*.md"):
            if ".git" in md.parts:
                continue
            try:
                text = md.read_text(encoding="utf-8-sig")
            except OSError:
                continue
            m = _re.search(r"(?m)^source_ids:\s*\[(.*?)\]", text)
            if not m:
                continue
            for raw in m.group(1).split(","):
                sid = raw.strip().strip("\"'")
                if sid.startswith("SRC-") and sid not in known:
                    unknown.setdefault(sid, md.relative_to(kb_retrieve.REPO).as_posix())
        if unknown:
            sample = "; ".join(f"{k} ({v})" for k, v in list(unknown.items())[:5])
            failures.append(f"{len(unknown)} unknown source id(s) referenced: {sample}")

        docs = kb_retrieve.load_docs(kb_retrieve.REPO)
        for doc in docs:
            for sid in doc["source_ids"]:
                if sid not in known:
                    failures.append(f"Unknown effective source {sid}: {doc['path']}")
            if doc["status"] in kb_retrieve.STRICT and not (doc["reviewed_by"] and doc["reviewed_at"]):
                failures.append(f"Missing review evidence: {doc['path']}")

    # 4. routes and local links must survive directory cleanup.
    import re
    from urllib.parse import unquote
    for item in kb_retrieve.profile(kb_retrieve.REPO).get("core_operation_documents", []):
        path = kb_retrieve.REPO / item["path"]
        if not path.is_file():
            failures.append(f"Missing routed document: {item['path']}")
            continue
        meta, _ = kb_retrieve.front_matter(path.read_text(encoding="utf-8-sig"))
        if item["id"] != meta.get("id"):
            failures.append(f"Route ID mismatch: {item['path']}")
    for path in kb_retrieve.REPO.rglob("*.md"):
        rel = path.relative_to(kb_retrieve.REPO).as_posix()
        if ".git/" in rel or "shared/templates/" in rel:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
            target = target.strip().split(' "', 1)[0].strip("<>")
            if not target or re.match(r"^[A-Za-z][\w+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).exists():
                failures.append(f"Broken local link: {rel} -> {target}")

    # 5. generated navigation and query-state guardrails.
    import rebuild_metadata
    for path, content in rebuild_metadata.generated_files().items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            failures.append(f"Stale generated metadata: {path.relative_to(kb_retrieve.REPO)}")
    evaluation = kb_retrieve.run_eval(kb_retrieve.REPO, HERE / "kb_eval.csv")
    if evaluation["gate_violations"] or evaluation["hit_at_5"] != 1.0:
        failures.append(f"Retrieval regression: {evaluation}")
    if kb_retrieve.lookup(kb_retrieve.REPO, "__missing__", "cte").get("usable_for_arguments"):
        failures.append("Missing entity was authorized as an engineering argument")

    if failures:
        for message in failures:
            print("FAIL: " + message, file=sys.stderr)
        return 1

    print("OK: metadata, sources, routes, links, encoding and retrieval guardrails")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
