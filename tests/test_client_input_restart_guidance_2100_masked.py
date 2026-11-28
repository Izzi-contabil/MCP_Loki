"""Entrega das orientações da 2.10.0 (rotina reinicia caso em revisão por insumo do cliente).

Contrato 2.10.0 muda o schema de `preparar_autorizacao` (valor novo no enum): exige Refresh
do conector e conversa nova. Prova que os textos chegam aos domínios e ao plugin e que as
versões e os hashes acompanham; não mede obediência.
"""

import hashlib
import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "plugins/loki-bootstrap/skills/operar-loki"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
LIMIT = 65536
CAPABILITY = "atualizar_por_insumo_do_cliente"
STOPS = (
    "restart_requires_effect_reconciliation",
    "client_input_restart_requires_review_state",
    "client_input_restart_scope_refused",
    "client_input_request_ref_invalid",
    "client_input_restart_grant_origin_unrecorded",
    "capacidade_nao_concedida",
    "caso_inexistente_ou_nao_autorizado",
)


def read(domain: str) -> str:
    return (DOMAINS / f"{domain}.md").read_text(encoding="utf-8")


def flat(value: str) -> str:
    return " ".join(value.split())


def test_general_notice_requires_refresh_and_states_the_capability_limits() -> None:
    guide = read("geral")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.13.0)")
    notice = guide[: guide.index("## Reaproveitar respostas e causas persistidas")]
    assert "Refresh do conector e conversa nova" in flat(notice)
    assert "**Continua da 2.9.9**" in notice
    body = flat(guide)
    for marker in (
        "`preparar_autorizacao`/`aplicar_autorizacao`",
        "`preparar_acesso_tecnico` recusa",
        "`capacidade_concedida_so_por_autorizacao`",
        "`capacidade_exclusiva_de_automacao`",
        "Ela não decide: aprovação, efeitos, entrega, cancelamento, retificação de data "
        "e afastamento continuam com pessoa",
        "o concedente registrado é quem gravou o modelo",
    ):
        assert marker in body, marker


def test_admission_and_termination_carry_the_restart_script() -> None:
    for domain in ("admissao", "rescisao"):
        body = flat(read(domain))
        for marker in (
            "## Insumo novo do cliente com o caso em revisão (rotina, 2.10.0)",
            "`aguardando_revisao`",
            "copie o `correction_snapshot`",
            "`preparation.mode=replace_process_inputs`",
            "`preparation.request_ref = sha256-<impressão do insumo>`",
            "`human_message`",
            "`receive_case_data`",
            "Não repita em laço",
            "idempotente",
            *STOPS,
        ):
            assert marker in body, (domain, marker)
    assert "`rectify_case_admission_date`" in flat(read("admissao"))


def test_payroll_restart_is_simple_with_the_capability() -> None:
    body = flat(read("folha_mensal"))
    assert f"`{CAPABILITY}`" in body
    assert "sem `preparation`, com `human_message`" in body
    assert "sem a capacidade, ela para e avisa a Ana" in body


def test_plugin_mirrors_the_release() -> None:
    workflows = (OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8")
    capacities = (OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8")
    skill = (OPERATOR / "SKILL.md").read_text(encoding="utf-8")
    assert "## 2.10.0: insumo novo do cliente e troca de motor pela rotina" in workflows
    assert "## 2.10.0: a rotina reinicia caso em revisão por insumo do cliente" in capacities
    assert "Na 2.10.0" in skill
    for text in (workflows, capacities, skill):
        assert CAPABILITY in text
        assert "Refresh do conector" in text
    for code in STOPS:
        assert code in flat(workflows) and code in flat(capacities), code


def test_release_versions_and_hashes() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.39"
    assert metadata["instructions_version"] == "2.13.0"
    assert metadata["mcp_contract_version"] == "2.13.0"
    assert metadata["recommended_plugin_version"] == "2.13.0"
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    # O histórico das edições anteriores vive em docs/MCP_UPDATES.md, não em release.json.
    history = (ROOT / "docs" / "MCP_UPDATES.md").read_text(encoding="utf-8")
    assert "## Candidata 0.4.35 / contrato, instruções e plugin 2.10.0" in history
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name


def test_thirteenth_transcription_rule_and_payroll_line_divisor() -> None:
    thirteenth = flat(read("decimo_terceiro"))
    for marker in (
        "`transcricao_cadastral_sem_efeito_no_13`",
        "`identificacao_cadastral`",
        "`alteracao_cargo_cbo`",
        "`historical_thirteenth_legal_rule_remuneration_unproven`",
        "`historical_thirteenth_legal_rule_effect_incompatible`",
        "`historical_thirteenth_legal_rule_scope_incompatible`",
        "até 1000",
        "{kind: declaration, reference, locator: data}",
        "`source_declarations`",
        "`thirteenth_rules.fact_assessment.legal_rules`",
    ):
        assert marker in thirteenth, marker
    payroll = flat(read("folha_mensal"))
    for marker in (
        '`formula.divisor_sob_calendario: "30" | "dias_do_mes"`',
        "CX-D0D4F1EF",
        "`folha_divisor_mes_retroativo`",
        "`afastamento_empregador`",
        "**fora da política o campo não tem efeito**",
        "`fator` **1 ou 2**",
        "`formula_day_factor_invalid`",
    ):
        assert marker in payroll, marker
    assert "quantidade = 2 × dias" not in payroll
    notice = flat(read("geral"))
    assert "`transcricao_cadastral_sem_efeito_no_13`" in notice
    assert "`formula.divisor_sob_calendario`" in notice


def test_unqualified_fact_source_and_authorization_busy_guidance() -> None:
    thirteenth = flat(read("decimo_terceiro"))
    for marker in (
        "`unqualified_facts`",
        "`locator_sha256`",
        "`reference_sha256`",
        "**cite o valor por extenso**",
        "**uma avaliação por fonte**",
        "`historical_legacy_qualification_source_incompatible`",
    ):
        assert marker in thirteenth, marker
    approvals = flat(read("aprovacoes"))
    for marker in (
        "code: authorization_change_busy",
        "retry_after_seconds}",
        "**não prepare nova autorização**",
        "`grants_count` e `grants_hash`",
        "`read_account_summary`",
        "`added_grants`",
        '{"error": "temporarily_unavailable"}',
        "sem `error_description`",
        "fica para o próximo login",
        "`Retry-After`",
    ):
        assert marker in approvals, marker
