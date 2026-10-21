"""Offline serialization only. The authenticated harness sends and checks responses."""

import base64
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .private import (
    ReadError,
    checked_bytes,
    private_directory,
    strict_json,
    write_bytes,
    write_json,
)

COLUMNS = [
    "schema_version",
    "record_key",
    "revision",
    "kind",
    "state",
    "path",
    "value_type",
    "value",
]
ROOTS = ["declaration", "source_ids", "dependencies", "missing_fields"]
MAX_BYTES = 32 * 1024 * 1024


def validate_parameters(value: Any, schema: dict[str, Any]) -> Any:
    pending: list[Any] = [schema]
    while pending:
        node = pending.pop()
        if isinstance(node, dict):
            if any(
                key in node and (not isinstance(node[key], str) or not node[key].startswith("#"))
                for key in ("$ref", "$dynamicRef")
            ):
                raise ReadError("external_schema_ref")
            pending.extend(node.values())
        elif isinstance(node, list):
            pending.extend(node)
    try:
        json.dumps(value, allow_nan=False)
        Draft202012Validator.check_schema(schema)
        if (
            next(
                Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
                None,
            )
            is not None
        ):
            raise ReadError("parameter_schema_invalid")
    except ReadError:
        raise
    except Exception:
        raise ReadError("parameter_schema_invalid") from None
    return value


def _leaves(value: Any, prefix: str = "", depth: int = 0) -> dict[str, Any]:
    if depth > 64:
        raise ReadError("value_depth_limit")
    result = {}
    children = (
        value.items()
        if isinstance(value, dict) and value
        else enumerate(value)
        if isinstance(value, list) and value
        else None
    )
    if children is None:
        return {prefix: value}
    for key, child in children:
        path = (
            f"{prefix}.{key}"
            if isinstance(value, dict) and prefix
            else str(key)
            if isinstance(value, dict)
            else f"{prefix}[{key}]"
        )
        for child_path, item in _leaves(child, path, depth + 1).items():
            if child_path in result:
                raise ReadError("ambiguous_field_path")
            result[child_path] = item
    return result


def source_csv(evidence: dict[str, Any]) -> bytes:
    data, sources = evidence.get("data"), evidence.get("field_sources")
    if not isinstance(data, dict) or not isinstance(sources, dict):
        raise ReadError("field_sources_invalid")
    leaves = _leaves(data) if data else {}
    if set(leaves) != set(sources):
        raise ReadError("field_sources_coverage")
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=";", lineterminator="\n")
    writer.writerow(
        [
            "schema_version",
            "field_path",
            "state",
            "value_json",
            "source_sha256",
            "source_locator",
            "basis",
            "derivation",
        ]
    )
    for path, value in sorted(leaves.items()):
        source = sources[path]
        if (
            not isinstance(source, dict)
            or not re.fullmatch(r"[a-f0-9]{64}", source.get("source_sha256", ""))
            or not isinstance(source.get("locator"), str)
            or not source["locator"].strip()
            or source.get("basis", "documented") not in {"documented", "derived", "reported"}
            or (
                source.get("basis", "documented") != "documented"
                and not (source.get("derivation") or "").strip()
            )
        ):
            raise ReadError("field_sources_invalid")
        raw = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        writer.writerow(
            [
                "loki.harness-reading/1",
                path,
                "observed",
                raw,
                source["source_sha256"],
                source["locator"],
                source.get("basis", "documented"),
                source.get("derivation", ""),
            ]
        )
    known = set(leaves)
    for key, state in (("missing_fields", "missing"), ("ambiguous_fields", "ambiguous")):
        fields = evidence.get(key, [])
        if not isinstance(fields, list):
            raise ReadError("pending_fields_invalid")
        for path in fields:
            if not isinstance(path, str) or not path or path in known:
                raise ReadError("pending_fields_overlap")
            known.add(path)
            writer.writerow(["loki.harness-reading/1", path, state, "", "", "", "", ""])
    content = output.getvalue().encode("utf-8")
    if not known or len(content) > MAX_BYTES:
        raise ReadError("csv_empty_or_size_limit")
    return content


def render_records(records: list[dict[str, Any]], contract: dict[str, Any]) -> bytes:
    if (
        contract.get("schema_version") != "loki.batch-csv/1"
        or contract.get("columns") != COLUMNS
        or contract.get("roots") != ROOTS
    ):
        raise ReadError("csv_contract_incompatible")
    if not records:
        raise ReadError("empty_records")
    limits = contract["limits"]
    if len(records) > min(limits["max_records"], 10000):
        raise ReadError("record_limit")
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=";", lineterminator="\n")
    writer.writerow(COLUMNS)
    rows = 0
    keys: set[str] = set()

    def emit(path: tuple[str, ...], value: Any, metadata: list[str]) -> None:
        nonlocal rows
        rows += 1
        if rows > min(limits["max_rows"], 200000) or len(path) > min(limits["max_depth"], 64):
            raise ReadError("csv_structure_limit")
        if type(value) is dict:
            kind, raw = "object", ""
        elif type(value) is list:
            kind, raw = "array", ""
        elif value is None:
            kind, raw = "null", ""
        elif type(value) is bool:
            kind, raw = "boolean", "true" if value else "false"
        elif type(value) is int:
            kind, raw = "integer", str(value)
        elif type(value) is str:
            kind, raw = "string", value
        else:
            raise ReadError("csv_value_type")
        pointer = "/" + "/".join(p.replace("~", "~0").replace("/", "~1") for p in path)
        row = [*metadata, pointer, kind, raw]
        if any(len(cell) > min(limits["max_cell_chars"], 65536) or "\x00" in cell for cell in row):
            raise ReadError("csv_cell_limit")
        writer.writerow(row)
        if output.tell() > min(limits["max_bytes"], MAX_BYTES):
            raise ReadError("csv_size_limit")
        if kind == "object":
            for key in sorted(value):
                emit((*path, key), value[key], metadata)
        elif kind == "array":
            if len(value) > min(limits["max_array_index"], 9999) + 1:
                raise ReadError("csv_array_limit")
            for index, item in enumerate(value):
                emit((*path, str(index)), item, metadata)

    for record in records:
        validate_parameters(record, contract["record_schema"])
        key = record["key"]
        if key in keys:
            raise ReadError("duplicate_record")
        keys.add(key)
        normalized = {
            "revision": 1,
            "state": "ready",
            "source_ids": [],
            "dependencies": [],
            "missing_fields": [],
            **record,
        }
        if type(normalized["revision"]) is not int:
            raise ReadError("csv_revision_type")
        metadata = [
            "loki.batch-csv/1",
            key,
            str(normalized["revision"]),
            record["kind"],
            normalized["state"],
        ]
        for root in ROOTS:
            emit((root,), normalized[root], metadata)
    content = output.getvalue().encode("utf-8")
    if len(content) > min(limits["max_bytes"], MAX_BYTES):
        raise ReadError("csv_size_limit")
    return content


def csv_request(
    source: Path, destination: str, target: str, *, reference: str = "", revision: int = 1
) -> dict[str, Any]:
    if source.suffix.lower() != ".csv":
        raise ReadError("csv_required")
    content = checked_bytes(source, MAX_BYTES)
    try:
        text = content.decode("utf-8-sig")
        if "\x00" in text or text.startswith(("%PDF-", "PK\x03\x04")):
            raise ReadError("csv_required")
        rows = csv.reader(io.StringIO(text, newline=""), delimiter=";", strict=True)
        header = next(rows)
        first = next(rows, None)
        if len(header) < 2 or first is None:
            raise ReadError("csv_empty_or_invalid")
        if len(first) != len(header):
            raise ReadError("csv_columns_invalid")
        for row in rows:
            if len(row) != len(header):
                raise ReadError("csv_columns_invalid")
    except (UnicodeError, csv.Error, StopIteration):
        raise ReadError("csv_invalid") from None
    if not re.fullmatch(r"[A-Za-z0-9_.:-]{1,200}", target):
        raise ReadError("target_invalid")
    digest = hashlib.sha256(content).hexdigest()
    arguments: dict[str, Any] = {
        "filename": source.name,
        "content_base64": base64.b64encode(content).decode("ascii"),
    }
    if destination == "case":
        tool = "anexar_documento_conteudo"
        arguments.update(case_id=target, doc_role="outro")
    elif destination == "onboarding-source":
        tool = "attach_onboarding_source"
        arguments["onboarding_id"] = target
    elif destination == "onboarding-csv":
        if (
            header != COLUMNS
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}", reference)
            or type(revision) is not int
            or not 1 <= revision <= 2147483647
        ):
            raise ReadError("csv_contract_or_revision_invalid")
        tool = "submit_company_onboarding_csv"
        arguments.update(
            onboarding_id=target, reference=reference, revision=revision, content_hash=digest
        )
    else:
        raise ReadError("csv_destination_invalid")
    return {
        "schema_version": "loki.harness-request/1",
        "state": "prepared_not_sent",
        "tool": tool,
        "arguments": arguments,
        "content_hash": digest,
        "source_kind": "harness_declared_csv_not_original_document",
    }


def save_receipt(request: Path, response: Path, output: Path) -> dict[str, Any]:
    request_bytes = checked_bytes(request, MAX_BYTES * 2)
    response_bytes = checked_bytes(response, MAX_BYTES * 2)
    strict_json(request_bytes.decode("utf-8"))
    strict_json(response_bytes.decode("utf-8"))
    output = private_directory(output)
    write_bytes(output / "request.json", request_bytes)
    write_bytes(output / "response.json", response_bytes)
    result = {
        "schema_version": "loki.harness-receipt/1",
        "state": "response_recorded_not_interpreted",
        "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
        "response_sha256": hashlib.sha256(response_bytes).hexdigest(),
        "human_approval": False,
    }
    write_json(output / "receipt.json", result)
    return result
