"""Generate a deterministic navigation index; requires PyYAML. Not solver authorization."""
from pathlib import Path
import argparse, hashlib, json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/knowledge-index.json"

def build():
    entries, seen = [], set()
    for path in sorted(ROOT.rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8-sig")
        if not text.startswith("---\n"):
            raise ValueError(f"Missing front matter: {path}")
        meta = yaml.safe_load(text.split("---", 2)[1])
        for key in ("id", "title", "domain", "status", "source_ids"):
            if not meta.get(key):
                raise ValueError(f"Missing {key}: {path}")
        if meta["id"] in seen:
            raise ValueError(f"Duplicate id: {meta['id']}")
        seen.add(meta["id"])
        if meta["domain"] != "packaging":
            raise ValueError(f"Unexpected domain: {path}")
        if meta["status"] not in ("draft", "reviewed", "validated", "deprecated"):
            raise ValueError(f"Unknown status: {path}")
        if meta["status"] in ("reviewed", "validated") and not all(meta.get(k) for k in ("reviewed_by", "reviewed_at")):
            raise ValueError(f"Missing review evidence: {path}")
        rel = path.relative_to(ROOT)
        entry = {k: meta.get(k) for k in ("id", "title", "document_type", "domain", "status", "tags", "physics", "source_ids", "source_locator", "updated_at", "reviewed_by", "reviewed_at")}
        entry.update(path="packaging/" + rel.as_posix(), topic=rel.parts[0], category=rel.parts[1], content_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest())
        entries.append(entry)
    return {"schema_version": "1.0", "generated": True, "path_base": "repository_root", "purpose": "metadata navigation; retrieve original Markdown for conditions and evidence", "solver_authorization": False, "entries": entries}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the committed index is stale")
    args = parser.parse_args()
    content = json.dumps(build(), ensure_ascii=False, indent=2, default=str) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Index stale: run build_knowledge_index.py")
        print("Index is current")
    else:
        OUTPUT.parent.mkdir(exist_ok=True)
        OUTPUT.write_text(content, encoding="utf-8")
        print(f"Generated {OUTPUT}")
