"""Draft static contract checker; never imports or starts ANSYS.

Source: SRC-EXEC-JSONSCHEMA-202012 and SRC-EXEC-CONTRACT-USER-001.
Only --record writes the schema's audit metadata, after a successful clean-tree check.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

METADATA = {
    "id": "KB-TOOLS-STATIC-VALIDATOR-001",
    "status": "draft",
    "reviewed_by": "",
    "reviewed_at": "",
    "source_ids": ["SRC-EXEC-JSONSCHEMA-202012", "SRC-EXEC-CONTRACT-USER-001"],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def content_digest(schema: dict) -> str:
    normalized = copy.deepcopy(schema)
    audit = normalized["x-contract"]["static_validation"]
    audit.pop("last_run", None)
    audit.pop("last_result", None)
    payload = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def check(root: Path, schema: dict) -> dict:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        installed = version("jsonschema")
    except (ImportError, PackageNotFoundError) as exc:
        raise ValueError("Missing python-jsonschema 4.26.0; install via reachable PyPI/mirror or offline wheels.") from exc

    contract = schema["x-contract"]
    tools = contract["tools"]
    require(installed == contract["static_validation"]["validator_version"], "Validator version mismatch; do not silently substitute a subset validator.")
    Draft202012Validator.check_schema(schema)
    registry = Registry().with_resource(schema["$id"], Resource.from_contents(schema))
    validator = Draft202012Validator(schema, registry=registry)
    def sub(pointer: str):
        return validator.evolve(schema={"$ref": schema["$id"] + pointer})
    slot_validator = sub("#/$defs/tool_contract_slots")
    rejected = []
    def reject(name: str, instance: dict, checker=validator) -> None:
        require(not checker.is_valid(instance), "Unexpected acceptance: " + name)
        rejected.append(name)

    require(contract["status"] == "draft", "Contract must stay draft.")
    require(contract["reviewed_by"] == contract["reviewed_at"] == "", "Reviewer fields must remain empty.")
    require(contract["software_version"] is None, "Unconfirmed software package version was filled.")
    require(contract["execution_enabled"] is False, "Execution must remain disabled.")
    branches = {b["properties"]["tool"]["const"]: b for b in schema["oneOf"]}
    declared = []
    for entry in contract["toolsets"].values():
        for field in ("engineering_data_tools", "project_tools", "tools"):
            declared.extend(entry.get(field, []))
    require(len(declared) == len(set(declared)) and set(declared) == set(tools) == set(branches), "Toolset/branch keys differ.")
    parameter_checks = []
    for name, tool in tools.items():
        require(tool["status"] == "draft" and tool["reviewed_by"] == tool["reviewed_at"] == "", "Tool review state changed: " + name)
        require(tool["execution_enabled"] is False and tool["api_binding"]["adapter_method"] is None, "Premature adapter binding: " + name)
        request = tool["example"]
        require(all(v is None for v in request["arguments"].values()), "Non-null engineering example: " + name)
        validator.validate(request)
        slot_validator.validate({key: tool[key] for key in ("preconditions", "readback", "failure_handling")})
        args_validator = sub(tool["argument_schema_ref"])
        args_validator.validate(request["arguments"])
        require(set(tool["parameters"]) == set(tool["parameter_semantics"]), "Missing parameter semantics: " + name)
        target_rule = branches[name]["properties"].get("target")
        expected = {"entity": {"$ref": "#/$defs/entity_ref"}, "project": {"type": "null"}, "analysis": {"anyOf": [{"$ref": "#/$defs/entity_ref"}, {"type": "null"}]}}[tool["scope_kind"]]
        require(target_rule == expected and "target" in branches[name]["required"], "Missing per-branch target rule: " + name)
        x = copy.deepcopy(request); x["scope_kind"] = "<INVALID>"; reject(name + ":scope", x)
        x = copy.deepcopy(request); x["arguments"].pop(tool["parameters"][0]); reject(name + ":missing-parameter", x)
        slots = {key: tool[key] for key in ("preconditions", "readback", "failure_handling")}
        for key in slots:
            x = copy.deepcopy(slots); x[key] = ["<INVALID>"]; reject(name + ":" + key, x, slot_validator)
        for parameter in tool["parameters"]:
            x = copy.deepcopy(request["arguments"]); x[parameter] = {"<UNDECLARED>": None}
            reject(name + ":typed:" + parameter, x, args_validator)
            parameter_checks.append(name + ":" + parameter)
        if tool["effect"] != "read_only":
            for bad_id in (None, "", "   "):
                x = copy.deepcopy(request); x["request_id"] = bad_id; reject(name + ":request-id", x)
        if tool["scope_kind"] == "analysis":
            x = copy.deepcopy(request); x["target"] = tools["mechanical.read_property"]["example"]["target"]
            validator.validate(x)

    mandatory = {"reject-execution-mode", "reject-non-null-argument", "reject-entity-null-target", "reject-project-non-null-target", "reject-analysis-invalid-target"}
    cases = contract["static_validation"]["negative_cases"]
    require(mandatory <= {case["id"] for case in cases}, "Missing required negative cases.")
    for case in cases:
        x = copy.deepcopy(tools[case["base_tool"]]["example"])
        x.update(case["replace"])
        reject(case["id"], x)
        print("REJECT", case["id"])

    # Validate typed fragments with symbolic fields only; no real engineering values.
    definitions = schema["$defs"]
    for key, definition in definitions.items():
        if key.startswith("arguments_"):
            require(definition["additionalProperties"] is False, "Open parameter object: " + key)
            for parameter in definition["properties"]:
                require(parameter in definition["required"], "Parameter key not declared required: " + key)
    quantity = {"value": None, "unit": "K", "temperature_kind": "absolute_temperature", "source_ref": None}
    sub("#/$defs/absolute_temperature_quantity").validate(quantity)
    wrong = dict(quantity, temperature_kind="temperature_difference")
    reject("absolute-vs-difference", wrong, sub("#/$defs/absolute_temperature_quantity"))
    typed = copy.deepcopy(tools["mechanical.apply_temperature"]["example"]["arguments"])
    typed["temperature"] = quantity
    typed["time_table"] = {"interpolation": None, "points": None, "source_ref": None}
    reject("static-vs-time-temperature", typed, sub(tools["mechanical.apply_temperature"]["argument_schema_ref"]))
    typed = copy.deepcopy(tools["mechanical.apply_constraint"]["example"]["arguments"])
    typed["kind"] = "fixed_support"
    typed["components"] = {"x": None, "y": None, "z": None}
    reject("fixed-support-components", typed, sub(tools["mechanical.apply_constraint"]["argument_schema_ref"]))
    component = {"mode": "free", "value": {"value": None, "unit": "m", "temperature_kind": "not_temperature", "source_ref": None}}
    reject("free-component-prescribed-value", component, sub("#/$defs/displacement_component"))
    typed = copy.deepcopy(tools["mechanical.export_results"]["example"]["arguments"])
    typed["formats"] = ["CSV"]
    reject("missing-required-png", typed, sub(tools["mechanical.export_results"]["argument_schema_ref"]))
    typed["formats"] = ["CSV", "PNG"]
    sub(tools["mechanical.export_results"]["argument_schema_ref"]).validate(typed)
    reference = tools["mechanical.read_property"]["example"]["target"]
    sub("#/$defs/entity_ref").validate(reference)

    with (root / "shared/references/catalog.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    sources = {row["source_id"] for row in rows}
    require(len(sources) == len(rows), "Duplicate source ID.")
    require(set(contract["source_ids"]) <= sources, "Unregistered contract source.")
    for evidence in contract["api_evidence"].values():
        require(evidence["source_id"] in sources, "Unregistered API source.")
    unresolved = (root / "shared/tools/unresolved.md").read_text(encoding="utf-8")
    for tool in tools.values():
        require(all("| " + key + " |" in unresolved for key in tool["unresolved_refs"]), "Unlisted unresolved ID.")
    require(contract["contract_version"] in schema["$id"], "Contract version/id mismatch.")
    recorded = contract["static_validation"].get("last_run")
    if recorded is not None:
        require(recorded["schema_content_sha256"] == content_digest(schema), "Stale last_run: schema content differs from the recorded digest.")
        require(recorded["validation_script_sha256"] == hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "Stale last_run: validation script changed.")
    print("PASS", len(tools), "tools; typed parameters; slots; target guards; offline $ref")
    return {"python": sys.version.split()[0], "jsonschema": installed, "schema_content_sha256": content_digest(schema), "tool_count": len(tools), "parameter_checks": len(parameter_checks), "rejection_checks": len(rejected)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true", help="Record a successful check of a clean committed tree.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    path = root / "shared/tools/tools.schema.json"
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        if args.record:
            require(not git(root, "status", "--porcelain"), "--record requires a clean committed tree; commit contract changes first.")
        report = check(root, schema)
        if args.record:
            run = {"commit": git(root, "rev-parse", "HEAD"), "at": datetime.now(timezone.utc).isoformat(),
                   "python": report["python"], "jsonschema": report["jsonschema"],
                   "schema_content_sha256": report["schema_content_sha256"],
                   "validation_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
            audit = schema["x-contract"]["static_validation"]
            audit["last_run"] = run
            audit["last_result"] = "passed_static_only"
            # Replace only the audit fields; preserve the reviewed JSON formatting.
            text = path.read_text(encoding="utf-8")
            marker = '"last_run":'
            start = text.index(marker) + len(marker)
            start += len(text[start:]) - len(text[start:].lstrip())
            _, length = json.JSONDecoder().raw_decode(text[start:])
            text = text[:start] + json.dumps(run, ensure_ascii=False) + text[start + length:]
            text = re.sub(r'"last_result": (?:null|"passed_static_only")', '"last_result": "passed_static_only"', text)
            path.write_text(text, encoding="utf-8")
            print("RECORDED", run["commit"], run["at"])
        print(json.dumps(report, ensure_ascii=False))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
