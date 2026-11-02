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
    "source_ids": ["SRC-EXEC-JSONSCHEMA-202012", "SRC-EXEC-CONTRACT-USER-001", "SRC-ENTITY-REGISTRY-USER-001"],
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


def script_digest() -> str:
    # Universal-newline text hashing is stable across Git LF/CRLF checkouts.
    return hashlib.sha256(Path(__file__).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def text_digest(path: Path) -> str:
    """Hash UTF-8 evidence text with BOM removed and universal LF newlines."""
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").encode("utf-8")).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def validate_registry_rows(root: Path, schema: dict, entities: list, sources: set) -> dict:
    """Check declarative registry evidence; do not resolve any live ANSYS object."""
    policy = schema["x-contract"]["entity_policy"]
    with (root / "shared/materials/catalog.csv").open(encoding="utf-8-sig", newline="") as stream:
        material_pairs = {(row["material_id"], row["revision"]) for row in csv.DictReader(stream)}
    index, alias_keys, case_evidence = {}, set(), {}
    for entity in entities:
        stable = entity["stable_id"]
        require(bool(stable) and stable not in index, "Duplicate stable_id or empty stable_id.")
        index[stable] = entity
        require(entity["entity_kind"] in policy["registry_enums"]["entity_kind"], "Invalid entity_kind enum.")
        require(entity["status"] in policy["registry_enums"]["status"], "Invalid registry status enum.")
        require(entity["resolution_state"] in policy["registry_enums"]["resolution_state"], "Invalid resolution_state enum.")
        if entity["status"] == "draft":
            require(entity["reviewed_by"] == entity["reviewed_at"] == "", "Draft registry review fields must be empty.")
        elif entity["status"] in ("reviewed", "validated"):
            require(bool(entity["reviewed_by"]) and bool(entity["reviewed_at"]), "Reviewed registry row lacks review evidence.")
        material = (entity["material_id"], entity["material_revision"])
        if any(material) or entity["entity_kind"] == "material":
            require(all(material) and material in material_pairs, "Material ID/revision not in authoritative catalog.")
        case_id = entity["case_id"]
        require(re.fullmatch(r"[A-Za-z0-9_-]+", case_id) is not None, "Invalid case_id.")
        if case_id not in case_evidence:
            directory = root / "simulation/cases" / case_id / "data"
            with (directory / "bodies.csv").open(encoding="utf-8-sig", newline="") as stream:
                bodies = list(csv.DictReader(stream))
            objects = json.loads((directory / "object-names.json").read_text(encoding="utf-8-sig"))
            manifest = json.loads((directory / "source-manifest.json").read_text(encoding="utf-8-sig"))
            ids = {row["object_id"] for row in bodies} | {str(row["object_id"]) for row in objects}
            case_evidence[case_id] = (ids, "archive-sha256:" + manifest["archive_snapshot"]["sha256"])
        native_ids, archive_revision = case_evidence[case_id]
        if entity["source_object_id"]:
            require(entity["source_object_id"] in native_ids, "source_object_id absent from bodies/object-names.")
        require(entity["model_revision"] in ("", archive_revision), "Unproven model revision overlay.")
        require(entity["resolved_from"] in schema["$defs"]["entity_ref"]["properties"]["resolved_from"]["properties"]["kind"]["enum"], "Unknown registry resolution source.")
        require(set(entity["source_ids"].split(";")) <= sources, "Unregistered entity evidence source.")
        artifact = (root / entity["source_artifact"]).resolve()
        require(artifact.is_relative_to(root.resolve()) and artifact.suffix.lower() != ".pdf", "Unexpected registry evidence path.")
        require(entity["source_hash_kind"] == "utf8-lf", "Unknown registry evidence hash normalization.")
        require(text_digest(artifact) == entity["source_artifact_sha256"], "Registry evidence artifact hash mismatch.")
        if artifact == (root / "simulation/cases" / case_id / "data/bodies.csv").resolve():
            require(entity["entity_kind"] == "body", "Historical body evidence kind mismatch.")
        if artifact == (root / "shared/materials/catalog.csv").resolve():
            require(entity["entity_kind"] == "material", "Material catalog evidence kind mismatch.")
        if entity["resolution_state"] == "unresolved":
            require(not any(entity[field] for field in ("mechanical_tree_id", "geometry_body_ids", "geometry_face_ids")), "Unresolved registry row contains an unproved runtime mapping.")
        else:
            require(bool(entity["model_revision"]) and not entity["blocking_reason"], "Resolved registry row has unresolved identity prerequisites.")
            require(any(entity[field] for field in ("mechanical_tree_id", "geometry_body_ids", "geometry_face_ids")), "Resolved registry row lacks a runtime identity.")
        if artifact.suffix == ".csv":
            with artifact.open(encoding="utf-8-sig", newline="") as stream:
                evidence_rows = list(csv.DictReader(stream))
            if entity["entity_kind"] == "body":
                matches = [row for row in evidence_rows if row.get("object_id") == entity["source_object_id"]]
                require(len(matches) == 1 and matches[0]["name"] == entity["display_name_hint"] and matches[0]["material"] == entity["material_name_hint"], "Historical body evidence mismatch.")
            elif entity["entity_kind"] == "material":
                matches = [row for row in evidence_rows if (row.get("material_id"), row.get("revision")) == material]
                require(len(matches) == 1 and stable == entity["material_id"], "Material registry differs from its evidence catalog.")
        elif entity["source_object_id"]:
            evidence_rows = json.loads(artifact.read_text(encoding="utf-8-sig"))
            matches = [row for row in evidence_rows if str(row["object_id"]) == entity["source_object_id"]]
            require(len(matches) == 1 and matches[0]["name"] == entity["display_name_hint"], "Historical object index mismatch.")
        for alias in filter(None, (value.strip() for value in entity["aliases"].split(";"))):
            key = (case_id, entity["model_revision"], alias)
            require(key not in alias_keys, "Ambiguous scoped alias.")
            alias_keys.add(key)
    for stable, entity in index.items():
        parent = entity["parent_id"]
        if parent:
            require(parent in index and parent != stable, "Unknown or self parent_id.")
            require(index[parent]["case_id"] == entity["case_id"] and index[parent]["model_revision"] == entity["model_revision"] and bool(entity["model_revision"]), "Parent revision/case mismatch.")
        seen, current = set(), stable
        while current:
            require(current in index, "Unknown parent_id.")
            require(current not in seen, "Cyclic parent_id hierarchy.")
            seen.add(current)
            current = index[current]["parent_id"]
    return index


def lookup_alias(entities: list, alias: str, case_id: str, model_revision: str) -> dict:
    require(bool(case_id) and bool(model_revision), "Alias lookup requires explicit case_id and model_revision.")
    matches = [row for row in entities if row["case_id"] == case_id and row["model_revision"] == model_revision and alias in [x.strip() for x in row["aliases"].split(";")]]
    require(len(matches) == 1, "Alias is unregistered or ambiguous in this revision.")
    return matches[0]


def entity_refs(value, path="root", declared_reference=False):
    if isinstance(value, dict):
        if "stable_id" in value and ("resolved_from" in value or declared_reference or path == "root") and isinstance(value["stable_id"], (str, type(None))):
            yield path, value
        for key, child in value.items():
            if key not in ("$defs", "shape_schema", "negative_cases"):
                is_reference = key.endswith("entity_ref") or key in ("target", "scope_ref", "analysis_ref", "coordinate_frame_ref", "parameter_ref")
                yield from entity_refs(child, path + "." + key, is_reference)
    elif isinstance(value, list):
        for position, child in enumerate(value):
            yield from entity_refs(child, path + "[" + str(position) + "]")


def validate_entity_ref_bindings(value, index: dict, case_id=None, model_revision=None, kind_expectations=None) -> None:
    for path, reference in entity_refs(value):
        stable = reference["stable_id"]
        if stable is None:
            continue
        require(stable in index, "Unknown entity_ref stable_id at " + path)
        row = index[stable]
        require(bool(row["model_revision"]), "entity_ref targets a registry row with empty model_revision: " + stable)
        normalized_path = re.sub(r"\[\d+\]", "[]", path).removeprefix("root.")
        for field, kind in (kind_expectations or {}).items():
            if normalized_path == field or normalized_path.endswith("." + field):
                require(row["entity_kind"] == kind, "entity_ref kind mismatch at " + path + ": expected " + kind)
        require(reference.get("model_revision") == row["model_revision"], "entity_ref model revision mismatch: " + stable)
        if case_id:
            require(case_id == row["case_id"], "entity_ref case mismatch: " + stable)
        if model_revision:
            require(model_revision == row["model_revision"], "entity_ref base revision mismatch: " + stable)


def validate_package_document(document: dict, index: dict, material_pairs: set, validator, contract: dict, trusted_shape: dict) -> list:
    require(document["validation"]["shape_schema"] == trusted_shape, "Package validation schema policy drift.")
    validator.evolve(schema=trusted_shape).validate(document)
    require(document["reviewed_by"] == document["reviewed_at"] == "", "Package draft review fields must be empty.")
    require(document["entity_contract_ref"]["schema_id"] == validator.schema["$id"], "Package contract reference drift.")
    kinds = contract["entity_policy"]["reference_kind_expectations"]
    require(document["validation"]["expected_entity_kinds"] == kinds, "Package kind policy drift.")
    validate_entity_ref_bindings(document, index, document["case_id"], document["base_model_revision"], kinds)
    component_ids = [row["id"] for row in document["components"]]
    require(len(set(component_ids)) == len(component_ids), "Duplicate package component ID.")
    connections = [row["id"] for row in document["connections"]]
    require(len(set(connections)) == len(connections), "Duplicate package connection ID.")
    components = {row["id"]: row for row in document["components"]}
    pending = []
    for name in ("case_id", "base_model_revision"):
        if document[name] is None:
            pending.append(name)
    for component in document["components"]:
        material = component["material_ref"]
        if material["id"] is not None or material["revision"] is not None:
            require((material["id"], material["revision"]) in material_pairs, "Package material ID/revision missing or unknown.")
            require(material["id"] in index and index[material["id"]]["entity_kind"] == kinds["components[].material_ref.id"], "Package material entity kind mismatch.")
            require(index[material["id"]]["material_revision"] == material["revision"], "Package material registry revision mismatch.")
        else:
            pending.append(component["id"] + ".material_ref")
    for connection in document["connections"]:
        low, high = connection["lower_component"], connection["upper_component"]
        require(low in components and high in components and low != high, "Package connection has an unknown or identical endpoint.")
        for endpoint, name in (("lower_entity_ref", low), ("upper_entity_ref", high)):
            actual, expected = connection[endpoint]["stable_id"], components[name]["entity_ref"]["stable_id"]
            if actual is not None and expected is not None:
                require(actual == expected, "Connection endpoint differs from component entity_ref.")
        underfill = connection["underfill"]
        if underfill["material_id"] is not None or underfill["material_revision"] is not None:
            require((underfill["material_id"], underfill["material_revision"]) in material_pairs, "Underfill material revision missing or unknown.")
            require(underfill["material_id"] in index and index[underfill["material_id"]]["entity_kind"] == kinds["connections[].underfill.material_id"], "Underfill material entity kind mismatch.")
            require(index[underfill["material_id"]]["material_revision"] == underfill["material_revision"], "Underfill registry revision mismatch.")
    for path, reference in entity_refs(document):
        if reference["stable_id"] is None or index[reference["stable_id"]]["resolution_state"] != "resolved":
            pending.append(path)
    if document["validation_state"] != "draft":
        require(not pending, "Package cannot be promoted while references/materials remain unresolved.")
    if document["validation_state"] == "executable" or document["ready_for_execution"]:
        require(contract["execution_enabled"] and contract["software_version"] is not None, "Contract preview version forbids executable package state.")
        require(document["validation"]["geometry_overlap"]["implementation_state"] != "unresolved" and document["validation"]["geometry_overlap"]["result"] == "passed", "Geometry overlap check has not been implemented or evidenced.")
        require(document["validation"]["units"]["implementation_state"] != "unresolved", "Unit conversion remains unresolved.")
    return pending


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
    registry_path = root / contract["entity_policy"]["registry_path"]
    require(contract["entity_policy"]["registry_hash_kind"] == "utf8-lf", "Unknown registry hash normalization.")
    require(text_digest(registry_path) == contract["entity_policy"]["registry_sha256"], "Entity registry content differs from its pinned digest.")
    with registry_path.open(encoding="utf-8-sig", newline="") as stream:
        entities = list(csv.DictReader(stream))
    index = validate_registry_rows(root, schema, entities, sources)
    with (root / "shared/materials/catalog.csv").open(encoding="utf-8-sig", newline="") as stream:
        material_pairs = {(row["material_id"], row["revision"]) for row in csv.DictReader(stream)}
    package_info = contract["package_structure_template"]
    package_path = root / package_info["path"]
    require(package_info["hash_kind"] == "utf8-lf" and text_digest(package_path) == package_info["sha256"], "Package template differs from pinned content.")
    package = json.loads(package_path.read_text(encoding="utf-8-sig"))
    require(set(package["source_ids"]) <= sources, "Unregistered package contract source.")
    trusted_shape = copy.deepcopy(package["validation"]["shape_schema"])
    pending = validate_package_document(package, index, material_pairs, validator, contract, trusted_shape)
    for directory in ("shared", "simulation", "packaging"):
        for candidate in (root / directory).rglob("*.json"):
            document = json.loads(candidate.read_text(encoding="utf-8-sig"))
            if isinstance(document, dict):
                context = document.get("context", {})
                validate_entity_ref_bindings(document, index, document.get("case_id"), document.get("base_model_revision", context.get("model_revision")), contract["entity_policy"]["reference_kind_expectations"])
    def reject_semantic(name, callback, expected):
        try:
            callback()
        except ValueError as error:
            require(expected in str(error), "Wrong rejection reason for " + name + ": " + str(error))
            rejected.append(name)
        else:
            raise ValueError("Unexpected semantic acceptance: " + name)
    mutation_cases = [
        ("registry-material-id", "material", "material_id", "<UNKNOWN>", "Material ID/revision"),
        ("registry-material-revision", "material", "material_revision", "<UNKNOWN>", "Material ID/revision"),
        ("registry-object-id", "body", "source_object_id", "<UNKNOWN>", "source_object_id absent"),
        ("registry-artifact-hash", "body", "source_artifact_sha256", "<MISMATCH>", "artifact hash mismatch"),
        ("registry-status", "body", "status", "<INVALID>", "status enum"),
        ("registry-resolution-state", "body", "resolution_state", "<INVALID>", "resolution_state enum"),
        ("registry-entity-kind", "body", "entity_kind", "<INVALID>", "entity_kind enum"),
        ("registry-body-kind-spoof", "body", "entity_kind", "analysis", "body evidence kind mismatch"),
        ("reference-analysis-as-body", "reference", "entity_ref", "ENT-BGA-ANALYSIS-5938", "entity_ref kind mismatch"),
        ("reference-material-as-body", "reference", "entity_ref", "MAT-BGA-SI-001", "entity_ref kind mismatch"),
    ]
    for label, kind, field, value, reason in mutation_cases:
        if kind == "reference":
            changed = copy.deepcopy(package)
            target = changed["components"][0][field]
            target["stable_id"] = value
            target["model_revision"] = index[value]["model_revision"]
            reject_semantic(label, lambda data=changed: validate_package_document(data, index, material_pairs, validator, contract, trusted_shape), reason)
            continue
        changed = copy.deepcopy(entities)
        next(row for row in changed if row["entity_kind"] == kind)[field] = value
        reject_semantic(label, lambda data=changed: validate_registry_rows(root, schema, data, sources), reason)
    duplicate = copy.deepcopy(entities); duplicate.append(copy.deepcopy(duplicate[0]))
    reject_semantic("registry-stable-id-unique", lambda: validate_registry_rows(root, schema, duplicate, sources), "Duplicate stable_id")
    reference = copy.deepcopy(tools["mechanical.read_property"]["example"]["target"])
    reference["stable_id"] = "ENT-BGA-NS-OUTER-001"
    reject_semantic("reference-to-unbound-revision", lambda: validate_entity_ref_bindings(reference, index), "empty model_revision")
    body = index["ENT-BGA-BODY-25"]
    require(lookup_alias(entities, "die_1", body["case_id"], body["model_revision"])["stable_id"] == "ENT-BGA-BODY-25", "die_1 alias mapping drift.")
    require(lookup_alias(entities, "substrate_1", body["case_id"], body["model_revision"])["stable_id"] == "ENT-BGA-BODY-496", "substrate_1 alias mapping drift.")
    reject_semantic("alias-without-revision", lambda: lookup_alias(entities, "die_1", body["case_id"], None), "explicit case_id")
    reject_semantic("interposer-alias-not-invented", lambda: lookup_alias(entities, "interposer_1", body["case_id"], body["model_revision"]), "unregistered")
    changed = copy.deepcopy(package); changed["validation_state"] = "resolved"
    reject_semantic("package-false-resolved-state", lambda: validate_package_document(changed, index, material_pairs, validator, contract, trusted_shape), "cannot be promoted")
    changed = copy.deepcopy(package); changed["ready_for_execution"] = True
    reject_semantic("package-preview-cannot-execute", lambda: validate_package_document(changed, index, material_pairs, validator, contract, trusted_shape), "preview version forbids")
    changed = copy.deepcopy(package); changed["components"][0]["entity_ref"] = reference
    reject_semantic("package-unbound-scope-reference", lambda: validate_package_document(changed, index, material_pairs, validator, contract, trusted_shape), "empty model_revision")
    changed = copy.deepcopy(package); changed["validation"]["shape_schema"] = {}
    reject_semantic("package-cannot-relax-its-schema", lambda: validate_package_document(changed, index, material_pairs, validator, contract, trusted_shape), "policy drift")
    changed = copy.deepcopy(package); changed["connections"][0]["entity_ref"] = None
    reject("connection-self-entity-ref-forbidden", changed, validator.evolve(schema=trusted_shape))
    changed = copy.deepcopy(package)
    for target, stable in ((changed["components"][0]["entity_ref"], "ENT-BGA-BODY-25"), (changed["connections"][0]["upper_entity_ref"], "ENT-BGA-BODY-496")):
        target["stable_id"] = stable
        target["model_revision"] = index[stable]["model_revision"]
    reject_semantic("package-conflicting-connection-endpoint", lambda: validate_package_document(changed, index, material_pairs, validator, contract, trusted_shape), "endpoint differs")
    print("PASS", len(entities), "registry rows; six mechanical checks; scoped aliases; parent references")
    print("PASS package entity-ref shape; validation_state=draft; pending identity/material fields:", len(pending))
    unresolved = (root / "shared/tools/unresolved.md").read_text(encoding="utf-8")
    for tool in tools.values():
        require(all("| " + key + " |" in unresolved for key in tool["unresolved_refs"]), "Unlisted unresolved ID.")
    require(contract["contract_version"] in schema["$id"], "Contract version/id mismatch.")
    recorded = contract["static_validation"].get("last_run")
    if recorded is not None:
        require(recorded["schema_content_sha256"] == content_digest(schema), "Stale last_run: schema content differs from the recorded digest.")
        require(recorded["validation_script_sha256"] == script_digest(), "Stale last_run: validation script changed.")
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
                   "validation_script_sha256": script_digest()}
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
