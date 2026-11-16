"""Rebuild navigation and corpus identity without external dependencies or solver calls."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import kb_retrieve

ROOT = Path(__file__).resolve().parents[1]


def generated_files() -> dict[Path, str]:
    report = kb_retrieve.info(ROOT)
    baseline = {
        "note": "Effective knowledge text and metadata, including sidecar provenance. Rebuild in the same PR.",
        "commit": "set-at-merge", "generated_at": "2026-11-16",
        **{key: report[key] for key in ("documents", "chunks", "corpus_sha256", "by_status")},
        "excludes": list(kb_retrieve.EXCLUDED_FILES) + list(kb_retrieve.EXCLUDED_DIRS),
    }
    entries = []
    for doc in kb_retrieve.load_docs(ROOT):
        if not doc["path"].startswith("packaging/"):
            continue
        entry = {key: value for key, value in doc.items() if key != "body"}
        parts = Path(doc["path"]).parts
        entry.update(topic=parts[1], category=parts[2],
                     content_sha256=hashlib.sha256((ROOT / doc["path"]).read_bytes()).hexdigest())
        entries.append(entry)
    index = {"schema_version": "1.1", "generated": True, "path_base": "repository_root",
             "purpose": "Metadata navigation; retrieve source Markdown and preserve review scope.",
             "solver_authorization": False, "entries": entries}
    return {ROOT / "tooling/corpus-baseline.json": json.dumps(baseline, ensure_ascii=False, indent=2) + "\n",
            ROOT / "packaging/data/knowledge-index.json": json.dumps(index, ensure_ascii=False, indent=2) + "\n"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for path, content in generated_files().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Stale metadata: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        print(("Checked " if args.check else "Generated ") + str(path.relative_to(ROOT)))


if __name__ == "__main__":
    main()
