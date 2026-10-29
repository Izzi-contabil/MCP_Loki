"""Offline batch preparation never sends, executes or treats staging as application."""

import csv
import importlib
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins/loki-bootstrap/skills/operar-loki/scripts"
sys.path.insert(0, str(SCRIPTS))


def contract():
    return {
        "schema_version": "loki.operational-batch-contract/1",
        "command_schema_version": "loki.operational-command/1",
        "csv_columns": ["schema_version", "record_ref", "operation", "arguments", "depends_on"],
        "delimiter": ";",
        "allowed_operations": ["receive_case_data", "run_prepared_case_workflow"],
        "limits": {"max_bytes": 8388608, "max_rows": 100},
        "request_schema": {
            "type": "object",
            "properties": {
                "schema_version": {"const": "loki.operational-batch/1"},
                "request_ref": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$"},
                "csv_content": {"type": "string", "maxLength": 8388608},
            },
            "required": ["schema_version", "request_ref", "csv_content"],
            "additionalProperties": False,
        },
    }


def records():
    return [
        {
            "record_ref": "data-1",
            "operation": "receive_case_data",
            "arguments": {
                "case_id": "CASE-MASKED",
                "request": {
                    "schema_version": "loki.case-data/1",
                    "request_ref": "informal-1",
                    "expected_snapshot": "a" * 64,
                    "data": {"zero": 0, "flag": False, "missing": None, "text": "Não;\n00:00"},
                },
            },
            "depends_on": [],
        },
        {
            "record_ref": "calculate-1",
            "operation": "run_prepared_case_workflow",
            "arguments": {"case_id": {"$ref": "data-1.case_id"}},
            "depends_on": ["data-1"],
        },
    ]


def render(value, schema=None):
    function = getattr(
        importlib.import_module("loki_readers.exchange"), "render_operational_csv", None
    )
    assert callable(function), "missing offline operational CSV renderer"
    return function(value, contract() if schema is None else schema)


def prepare(path, reference="batch-1", schema=None):
    function = getattr(
        importlib.import_module("loki_readers.exchange"), "operational_batch_request", None
    )
    assert callable(function), "missing offline operational request preparation"
    return function(path, contract() if schema is None else schema, reference=reference)


def test_operational_csv_keeps_informal_parameters_types_and_reference_objects(tmp_path):
    content = render(records())
    rows = list(csv.DictReader(io.StringIO(content.decode()), delimiter=";"))
    assert list(rows[0]) == contract()["csv_columns"]
    assert rows[0]["schema_version"] == "loki.operational-command/1"
    assert json.loads(rows[0]["arguments"]) == records()[0]["arguments"]
    assert json.loads(rows[1]["arguments"])["case_id"] == {"$ref": "data-1.case_id"}
    path = tmp_path / "parameters_masked.csv"
    path.write_bytes(content)
    request = prepare(path)
    assert request["state"] == "prepared_not_sent"
    assert request["tool"] == "execute_operational_batch"
    assert request["arguments"]["request"] == {
        "schema_version": "loki.operational-batch/1",
        "request_ref": "batch-1",
        "csv_content": content.decode(),
    }
    assert "content_base64" not in request["arguments"]["request"]
    assert "field_sources" not in request["arguments"]["request"]["csv_content"]


@pytest.mark.parametrize(
    "fault", ["unknown_operation", "future_dependency", "duplicate", "bad_ref", "too_many"]
)
def test_operational_renderer_rejects_invalid_shape_allowlist_and_dependency_order(fault):
    from loki_readers.private import ReadError

    values = records()
    schema = contract()
    if fault == "unknown_operation":
        values[0]["operation"] = "retired_writer"
    elif fault == "future_dependency":
        values[0]["depends_on"] = ["calculate-1"]
    elif fault == "duplicate":
        values[1]["record_ref"] = "data-1"
    elif fault == "bad_ref":
        values[1]["arguments"] = {"case_id": {"$ref": "future.id"}}
    else:
        schema["limits"]["max_rows"] = 1
    with pytest.raises(ReadError, match="operational_batch"):
        render(values, schema)


@pytest.mark.parametrize(
    "arguments", ['{"secret":"PRIVATE_MASKED","secret":1}', "[]", '{"value":NaN}']
)
def test_batch_parser_rejects_non_object_and_non_strict_json_without_echoing_input(
    tmp_path, arguments
):
    from loki_readers.private import ReadError

    path = tmp_path / "parameters_masked.csv"
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, delimiter=";", lineterminator="\n")
    writer.writerow(contract()["csv_columns"])
    writer.writerow(["loki.operational-command/1", "data-1", "receive_case_data", arguments, "[]"])
    path.write_text(buffer.getvalue())
    with pytest.raises(ReadError, match="operational_batch") as error:
        prepare(path)
    assert "PRIVATE_MASKED" not in str(error.value)


@pytest.mark.parametrize("fault", ["record_ref", "empty_ref_path", "field_limit", "depth_limit"])
def test_offline_csv_respects_the_served_parser_limits(fault):
    from loki_readers.private import ReadError

    values = records()
    schema = contract()
    if fault == "record_ref":
        values = [values[0]]
        values[0]["record_ref"] = "invalid.ref"
    elif fault == "empty_ref_path":
        values[1]["arguments"]["case_id"] = {"$ref": "data-1..case_id"}
    elif fault == "field_limit":
        schema["limits"]["max_field_chars"] = 128
    else:
        value = {"leaf": "masked"}
        for _ in range(33):
            value = {"nested": value}
        values[0]["arguments"] = value
    with pytest.raises(ReadError, match="operational_batch"):
        render(values, schema)


def test_shipped_batch_cli_only_prepares_utf8_csv_and_request(tmp_path):
    source = tmp_path / "records_masked.json"
    source.write_text(json.dumps(records()))
    schema = tmp_path / "contract_masked.json"
    schema.write_text(json.dumps(contract()))
    script = SCRIPTS / "loki_local.py"
    output = tmp_path / "csv privado"
    rendered = subprocess.run(
        [
            sys.executable,
            str(script),
            "render-operational-csv",
            str(source),
            str(output),
            "--contract",
            str(schema),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert rendered.returncode == 0, rendered.stderr
    prepared = subprocess.run(
        [
            sys.executable,
            str(script),
            "operational-batch-request",
            str(output / "parameters.csv"),
            str(tmp_path / "pedido privado"),
            "--contract",
            str(schema),
            "--reference",
            "batch-1",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert prepared.returncode == 0, prepared.stderr
    assert json.loads(prepared.stdout)["status"] == "prepared_not_sent"
    request = json.loads((tmp_path / "pedido privado/request.json").read_text())
    assert request["tool"] == "execute_operational_batch"
