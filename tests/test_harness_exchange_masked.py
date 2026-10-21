"""Requests stay offline and only contain CSV bytes or structured parameters."""

import base64
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins/loki-bootstrap/skills/operar-loki/scripts"
sys.path.insert(0, str(SCRIPTS))

from loki_readers.exchange import (  # noqa: E402
    csv_request,
    render_records,
    save_receipt,
    source_csv,
    validate_parameters,
)
from loki_readers.private import ReadError  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def test_parameter_schema_preserves_absence_and_blocks_external_ref():
    schema = {
        "type": "object",
        "properties": {"zero": {"type": "integer"}, "missing": {"type": ["null", "string"]}},
        "required": ["zero", "missing"],
        "additionalProperties": False,
    }
    assert validate_parameters({"zero": 0, "missing": None}, schema) == {"zero": 0, "missing": None}
    with pytest.raises(ReadError, match="parameter_schema"):
        validate_parameters({"zero": "inventar"}, schema)
    with pytest.raises(ReadError, match="external_schema_ref"):
        validate_parameters({}, {"$ref": "https://example.invalid/schema.json"})


def test_source_csv_has_exact_field_provenance_and_pending_fields():
    evidence = {
        "data": {
            "zero": 0,
            "false": False,
            "null": None,
            "empty": [],
            "text": '="sintético";\nlinha',
        },
        "field_sources": {
            key: {"source_sha256": "a" * 64, "locator": "page:1", "basis": "documented"}
            for key in ["zero", "false", "null", "empty", "text"]
        },
        "missing_fields": ["pending"],
        "ambiguous_fields": ["conflict"],
    }
    content = source_csv(evidence)
    rows = list(csv.DictReader(io.StringIO(content.decode()), delimiter=";"))
    by_path = {row["field_path"]: row for row in rows}
    assert json.loads(by_path["zero"]["value_json"]) == 0
    assert json.loads(by_path["false"]["value_json"]) is False
    assert json.loads(by_path["null"]["value_json"]) is None
    assert json.loads(by_path["empty"]["value_json"]) == []
    assert json.loads(by_path["text"]["value_json"]) == evidence["data"]["text"]
    assert by_path["zero"]["source_sha256"] == "a" * 64
    assert by_path["pending"]["state"] == "missing"
    assert by_path["conflict"]["state"] == "ambiguous"
    assert source_csv(evidence) == content


def test_source_csv_rejects_extra_or_missing_provenance():
    with pytest.raises(ReadError, match="field_sources"):
        source_csv({"data": {"zero": 0}, "field_sources": {}})
    with pytest.raises(ReadError, match="field_sources"):
        source_csv({"data": {}, "field_sources": {"fake": {}}})


def test_typed_csv_matches_backend_golden_and_preserves_types():
    contract = json.loads((FIXTURES / "batch_csv_contract_masked.json").read_text())
    records = json.loads((FIXTURES / "batch_csv_records_masked.json").read_text())
    content = render_records(records, contract)
    assert content == (FIXTURES / "batch_csv_expected_masked.csv").read_bytes()
    with pytest.raises(ReadError, match="contract"):
        render_records(records, {**contract, "schema_version": "future/2"})
    records[0]["declaration"]["float"] = 0.1
    with pytest.raises(ReadError, match="csv_value_type"):
        render_records(records, contract)


def test_typed_csv_rejects_duplicate_keys_and_empty_batch():
    contract = json.loads((FIXTURES / "batch_csv_contract_masked.json").read_text())
    records = json.loads((FIXTURES / "batch_csv_records_masked.json").read_text())
    with pytest.raises(ReadError, match="duplicate_record"):
        render_records(records + records, contract)
    with pytest.raises(ReadError, match="empty_records"):
        render_records([], contract)


@pytest.mark.parametrize(
    "destination,tool",
    [
        ("case", "anexar_documento_conteudo"),
        ("onboarding-source", "attach_onboarding_source"),
        ("onboarding-csv", "submit_company_onboarding_csv"),
    ],
)
def test_csv_request_contains_only_real_csv_bytes_and_no_credentials(tmp_path, destination, tool):
    source = tmp_path / "leitura.csv"
    source.write_bytes(
        (FIXTURES / "batch_csv_expected_masked.csv").read_bytes()
        if destination == "onboarding-csv"
        else b"field;value\nzero;0\n"
    )
    result = csv_request(source, destination, "SYNTHETIC-1", reference="reading-1", revision=1)
    assert result["tool"] == tool
    assert base64.b64decode(result["arguments"]["content_base64"]) == source.read_bytes()
    assert result["content_hash"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert result["state"] == "prepared_not_sent"
    assert "token" not in json.dumps(result)
    if destination == "case":
        assert result["arguments"]["doc_role"] == "outro"


def test_pdf_cannot_be_disguised_as_csv(tmp_path):
    source = tmp_path / "leitura.csv"
    source.write_bytes(b"%PDF-1.7 synthetic")
    with pytest.raises(ReadError, match="csv"):
        csv_request(source, "case", "SYNTHETIC-1")
    source = tmp_path / "leitura.pdf"
    source.write_bytes(b"a;b\n0;false\n")
    with pytest.raises(ReadError, match="csv"):
        csv_request(source, "case", "SYNTHETIC-1")


def test_receipt_preserves_exact_observed_response_without_claiming_approval(tmp_path):
    request = tmp_path / "request.json"
    response = tmp_path / "response.json"
    request.write_text('{"tool":"anexar_documento_conteudo","state":"prepared_not_sent"}')
    response.write_text('{"status":"BLOCKED","code":"test_masked"}')
    result = save_receipt(request, response, tmp_path / "receipt")
    assert result["state"] == "response_recorded_not_interpreted"
    assert (tmp_path / "receipt/response.json").read_bytes() == response.read_bytes()
    assert result["request_sha256"] == hashlib.sha256(request.read_bytes()).hexdigest()
    assert result["human_approval"] is False


def test_first_csv_data_row_is_validated(tmp_path):
    source = tmp_path / "dados.csv"
    source.write_bytes(b"a;b\nonly-one-cell\n")
    with pytest.raises(ReadError, match="csv_columns"):
        csv_request(source, "case", "SYNTHETIC-1")


def test_nonfinite_numbers_and_invalid_formats_are_rejected():
    from loki_readers.private import strict_json

    for value in ('{"value":1e999}', '{"value":NaN}', '{"value":-Infinity}'):
        with pytest.raises(ReadError, match="json_number"):
            strict_json(value)
    with pytest.raises(ReadError, match="parameter_schema"):
        validate_parameters({"value": float("inf")}, {"type": "object"})
    for format_name, value in [
        ("date", "2026-99-99"),
        ("uuid", "not-a-uuid"),
        ("date-time", "2026-99-99T01:01:01Z"),
    ]:
        with pytest.raises(ReadError, match="parameter_schema"):
            validate_parameters(value, {"type": "string", "format": format_name})


@pytest.mark.parametrize("basis", ["derived", "reported"])
def test_qualified_source_requires_nonblank_derivation(basis):
    evidence = {
        "data": {"zero": 0},
        "field_sources": {"zero": {"source_sha256": "a" * 64, "locator": "page:1", "basis": basis}},
    }
    with pytest.raises(ReadError, match="field_sources"):
        source_csv(evidence)
    evidence["field_sources"]["zero"]["derivation"] = "declaração sintética documentada"
    assert b"loki.harness-reading/1" in source_csv(evidence)
    evidence["field_sources"]["zero"]["locator"] = "   "
    with pytest.raises(ReadError, match="field_sources"):
        source_csv(evidence)
