"""Distribution checks for guidance; these do not exercise a model or provider."""

import json
import re
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "plugins/loki-bootstrap/skills/operar-loki"
GUIDE = OPERATOR / "references/DATAPREV_MENSAL.md"
FIXTURE = ROOT / "tests/fixtures/dataprev_monthly_contract_masked.json"


def test_dataprev_is_reachable_and_distributed_in_the_wheel_domain() -> None:
    for entry in (OPERATOR / "SKILL.md", OPERATOR / "references/CAPACIDADES_DP.md"):
        links = re.findall(r"\]\(([^)]+\.md)\)", entry.read_text(encoding="utf-8"))
        assert GUIDE.resolve() in {(entry.parent / link).resolve() for link in links}
    guide = GUIDE.read_text(encoding="utf-8")
    assert guide in InstructionsProvider().get("geral")["instructions"]


def test_discovery_and_command_fields_follow_the_served_contract() -> None:
    assert GUIDE.is_file()
    guide = GUIDE.read_text(encoding="utf-8")
    for required in (
        'get_process_contract("folha_mensal")',
        "compatibility_transport",
        "dataprev_monthly.request_schema",
        "receive_case_data(case_id, request)",
        "contrato ausente",
        "não comprova publicação",
        "consultar",
        "operar_casos",
        "próprio ator",
    ):
        assert required in guide, required
    examples = [json.loads(block) for block in re.findall(r"```json\n(.*?)\n```", guide, re.S)]
    assert {item["operation"] for item in examples} == {"enqueue", "get", "apply"}
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    discovery = fixture["discovery"]
    monthly = discovery["dataprev_monthly"]
    transport = discovery["compatibility_transport"]
    assert monthly["schema_version"] == "loki.dataprev-monthly/1"
    assert monthly["tool"] == transport["tool"] == "receive_case_data"
    assert transport["routes"][monthly["schema_version"]] == "dataprev_monthly"
    assert transport["request_schema_fields"][monthly["schema_version"]] == (
        "dataprev_monthly.request_schema"
    )
    assert monthly["applies_automatically"] is False
    assert monthly["transactional_provider_snapshot"] is False
    schema = fixture["request_schema"]
    assert monthly["request_schema"] == schema
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for example in examples:
        validator.validate(example)
    fields = {
        "enqueue": {"schema_version", "operation", "request_ref", "employee_id", "input_snapshot"},
        "get": {"schema_version", "operation", "request_ref"},
        "apply": {"schema_version", "operation", "request_ref", "input_snapshot"},
    }
    for example in examples:
        assert set(example) == fields[example["operation"]]


@pytest.mark.parametrize("field", ["endpoint", "token", "role", "max_pages", "company_id"])
def test_captured_schema_rejects_operator_supplied_infrastructure(field: str) -> None:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))["request_schema"]
    validator = Draft202012Validator(schema)
    valid = {
        "schema_version": "loki.dataprev-monthly/1",
        "operation": "get",
        "request_ref": "masked",
    }
    assert validator.is_valid(valid)
    errors = list(validator.iter_errors({**valid, field: "masked"}))
    assert errors
    assert any(error.validator == "oneOf" for error in errors)


def test_recovery_completeness_application_and_authority_are_distinct() -> None:
    assert GUIDE.is_file()
    guide = GUIDE.read_text(encoding="utf-8")
    for required in (
        "queued",
        "running",
        "complete",
        "incomplete",
        "failed",
        "antes de repetir qualquer comando com efeito incerto",
        "referência original",
        "nova execução externa",
        "somente o campo mensal ausente",
        "dataprev_existing_monthly_source",
        "CAS",
        "recibo de aplicação",
        "paginação completa",
        "não confirma zero",
        "snapshot transacional",
        "mTLS",
        "procuração",
        "provisionamento externo",
        "homologação real",
        "episódio",
        "CPF isolado",
        "CNPJ raiz",
        "CSV tipado",
        "pagamento",
        "repasse",
        "aceite do DP",
    ):
        assert required in guide, required
    assert not re.search(r"/home/|/var/|cert_file|key_file|DATAPREV_MONTHLY_PROFILES", guide)


def test_captured_backend_schema_is_versioned_and_has_the_known_commands() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--", str(FIXTURE.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert tracked.stdout.strip() == str(FIXTURE.relative_to(ROOT))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert fixture["source_commit"] == "7dc7fd093651fdf52daad8fbd280dbb5b216cb14"
    assert set(fixture["request_schema"]["$defs"]) == {"Enqueue", "Get", "Apply"}
    assert len(fixture["request_schema"]["oneOf"]) == 3
