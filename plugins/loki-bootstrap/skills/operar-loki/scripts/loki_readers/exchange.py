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
BATCH_COLUMNS = ["schema_version", "record_ref", "operation", "arguments", "depends_on"]
BATCH_MAX_BYTES = 8 * 1024 * 1024


def validate_parameters(value: Any, schema: dict[str, Any], *, partial_case: bool = False) -> Any:
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
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
            value
        ):
            # The writer validates provided object fields, rather than requiring
            # an absent sibling. Array elements and union alternatives still
            # require their complete declared shape, as in the backend adapter.
            if (
                partial_case
                and error.validator == "required"
                and not any(isinstance(part, int) for part in error.absolute_path)
                and "items" not in error.absolute_schema_path
            ):
                continue
            if (
                partial_case
                and error.instance is None
                and error.absolute_path
                and not any(isinstance(part, int) for part in error.absolute_path)
            ):
                # Explicit null is a sourced unknown in the case writer. The
                # parent object still rejects undeclared properties.
                continue
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


def case_data_request(
    evidence: dict[str, Any],
    contract: dict[str, Any],
    target: str,
    *,
    reference: str,
    snapshot: str,
) -> dict[str, Any]:
    """Prepare the current writer request offline; no attachment or interpretation."""
    if (
        contract.get("schema_version") != "loki.process-contract/1"
        or not isinstance(contract.get("data_schema"), dict)
        or not isinstance(contract.get("input_schema"), dict)
        or not isinstance(evidence, dict)
        or set(evidence) not in ({"data"}, {"data", "field_sources"})
        or not isinstance(evidence["data"], dict)
        or not evidence["data"]
        or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,200}", target)
    ):
        raise ReadError("case_data_contract_invalid")
    if "field_sources" in evidence and (
        not isinstance(evidence["field_sources"], dict)
        or not set(evidence["field_sources"]) <= set(_leaves(evidence["data"]))
    ):
        raise ReadError("case_data_source_path_invalid")
    if any(isinstance(value, float) for value in _leaves(evidence["data"]).values()):
        raise ReadError("case_data_float_not_allowed")
    validate_parameters(evidence["data"], contract["data_schema"], partial_case=True)
    request = {
        "schema_version": "loki.case-data/1",
        "request_ref": reference,
        "expected_snapshot": snapshot,
        "data": evidence["data"],
    }
    if "field_sources" in evidence:
        request["field_sources"] = evidence["field_sources"]
    validate_parameters(request, contract["input_schema"])
    return {
        "schema_version": "loki.harness-request/2",
        "state": "prepared_not_sent",
        "tool": "receive_case_data",
        "arguments": {"case_id": target, "request": request},
    }


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
        raise ReadError("case_data_required_instead_of_csv_attachment")
    if destination == "onboarding-source":
        raise ReadError("typed_parameters_required_instead_of_source_attachment")
    if destination == "onboarding-csv":
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


def _batch_contract(contract: dict[str, Any]) -> tuple[int, int, int, set[str]]:
    limits = contract.get("limits", {})
    operations = contract.get("allowed_operations")
    field_limit = limits.get("max_field_chars", 131072) if isinstance(limits, dict) else None
    if (
        contract.get("schema_version") != "loki.operational-batch-contract/1"
        or contract.get("command_schema_version") != "loki.operational-command/1"
        or contract.get("csv_columns") != BATCH_COLUMNS
        or contract.get("delimiter") != ";"
        or not isinstance(contract.get("request_schema"), dict)
        or not isinstance(limits, dict)
        or type(limits.get("max_bytes")) is not int
        or not 1 <= limits["max_bytes"] <= BATCH_MAX_BYTES
        or type(limits.get("max_rows")) is not int
        or not 1 <= limits["max_rows"] <= 100
        or type(field_limit) is not int
        or not 1 <= field_limit <= BATCH_MAX_BYTES
        or not isinstance(operations, list)
        or not operations
        or any(not isinstance(value, str) or not value for value in operations)
    ):
        raise ReadError("operational_batch_contract_invalid")
    return limits["max_bytes"], limits["max_rows"], field_limit, set(operations)


def _batch_references(value: Any, dependencies: list[str], depth: int = 0) -> None:
    if depth > 32:
        raise ReadError("operational_batch_depth_limit")
    if isinstance(value, dict):
        if "$ref" in value:
            reference = value["$ref"]
            if (
                set(value) != {"$ref"}
                or not isinstance(reference, str)
                or len(reference.split(".")) < 2
                or any(not part for part in reference.split("."))
                or reference.split(".")[0] not in dependencies
            ):
                raise ReadError("operational_batch_reference_invalid")
        else:
            for child in value.values():
                _batch_references(child, dependencies, depth + 1)
    elif isinstance(value, list):
        for child in value:
            _batch_references(child, dependencies, depth + 1)


def _batch_records(records: Any, contract: dict[str, Any]) -> list[dict[str, Any]]:
    _, max_rows, field_limit, operations = _batch_contract(contract)
    if not isinstance(records, list) or not 1 <= len(records) <= max_rows:
        raise ReadError("operational_batch_rows_invalid")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or set(record) - set(BATCH_COLUMNS):
            raise ReadError("operational_batch_record_invalid")
        item = {"schema_version": "loki.operational-command/1", "depends_on": [], **record}
        reference, dependencies = item.get("record_ref"), item["depends_on"]
        if (
            item["schema_version"] != "loki.operational-command/1"
            or not isinstance(reference, str)
            or re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", reference) is None
            or reference in seen
            or not isinstance(item.get("operation"), str)
            or item.get("operation") not in operations
            or not isinstance(item.get("arguments"), dict)
            or not isinstance(dependencies, list)
            or any(not isinstance(value, str) or value not in seen for value in dependencies)
            or len(dependencies) != len(set(dependencies))
        ):
            raise ReadError("operational_batch_record_or_dependency_invalid")
        _batch_references(item["arguments"], dependencies)
        try:
            json.dumps(item, allow_nan=False)
            cells = [
                item["schema_version"],
                reference,
                item["operation"],
                json.dumps(item["arguments"], ensure_ascii=False, allow_nan=False),
                json.dumps(dependencies, ensure_ascii=False, allow_nan=False),
            ]
            if any(len(cell) > field_limit for cell in cells):
                raise ReadError("operational_batch_field_limit")
        except (ValueError, TypeError, RecursionError):
            raise ReadError("operational_batch_json_invalid") from None
        normalized.append(item)
        seen.add(reference)
    return normalized


def render_operational_csv(records: Any, contract: dict[str, Any]) -> bytes:
    """Serialize the served batch format without executing any operation."""
    maximum, _, _, _ = _batch_contract(contract)
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=";", lineterminator="\n")
    writer.writerow(BATCH_COLUMNS)
    for record in _batch_records(records, contract):
        writer.writerow(
            [
                record["schema_version"],
                record["record_ref"],
                record["operation"],
                json.dumps(record["arguments"], ensure_ascii=False, allow_nan=False),
                json.dumps(record["depends_on"], ensure_ascii=False, allow_nan=False),
            ]
        )
    content = output.getvalue().encode("utf-8")
    if len(content) > maximum:
        raise ReadError("operational_batch_size_limit")
    return content


def operational_batch_request(
    source: Path, contract: dict[str, Any], *, reference: str
) -> dict[str, Any]:
    """Validate CSV parameters and prepare the HTTPS call for the harness."""
    maximum, max_rows, maximum_field, _ = _batch_contract(contract)
    if source.suffix.lower() != ".csv":
        raise ReadError("operational_batch_csv_required")
    content = checked_bytes(source, maximum)
    field_limit = csv.field_size_limit()
    try:
        text = content.decode("utf-8-sig")
        if "\x00" in text:
            raise ReadError("operational_batch_csv_invalid")
        csv.field_size_limit(maximum_field)
        reader = csv.reader(io.StringIO(text, newline=""), delimiter=";", strict=True)
        if next(reader) != BATCH_COLUMNS:
            raise ReadError("operational_batch_columns_invalid")
        records: list[dict[str, Any]] = []
        for row in reader:
            if len(row) != len(BATCH_COLUMNS) or len(records) >= max_rows:
                raise ReadError("operational_batch_rows_invalid")
            records.append(
                dict(
                    zip(
                        BATCH_COLUMNS,
                        [*row[:3], strict_json(row[3]), strict_json(row[4])],
                        strict=True,
                    )
                )
            )
        _batch_records(records, contract)
    except (UnicodeError, csv.Error, StopIteration, ValueError, ReadError):
        raise ReadError("operational_batch_csv_invalid") from None
    finally:
        csv.field_size_limit(field_limit)
    request = {
        "schema_version": "loki.operational-batch/1",
        "request_ref": reference,
        "csv_content": text,
    }
    validate_parameters(request, contract["request_schema"])
    return {
        "schema_version": "loki.harness-request/2",
        "state": "prepared_not_sent",
        "tool": "execute_operational_batch",
        "arguments": {"request": request},
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
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
