"""Entrega das orientações da 2.6.9; nao mede obediencia da harness."""

from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
CAPACITIES = SKILLS / "operar-loki/references/CAPACIDADES_DP.md"
WORKFLOWS = SKILLS / "operar-loki/references/WORKFLOWS.md"

POPULATION_REASONS = (
    "admissao_posterior_ao_mes",
    "entrada_empresa_posterior_ao_mes",
    "desligamento_anterior_ao_mes",
    "matricula_sem_vinculo_operacional",
    "matricula_ambigua_na_competencia",
    "funcionario_id_diverge_da_matricula",
    "vinculo_fora_da_competencia",
)
PREPARATION_RULES = (
    "## Preparação corrente: recusa por campo",
    "valem somente quando a resposta servida os apresentar",
    "`missing`",
    "`extra_forbidden`",
    "novo `request_ref` e o snapshot atual",
    "nunca numa chave própria",
)


def flat(text: str) -> str:
    return " ".join(text.split())


@pytest.mark.parametrize(
    ("domain", "code", "example", "section", "source"),
    [
        (
            "ferias",
            "vacation_preparation_requires_complete_input",
            '{"field": "dados_ferias.data_aviso", "reason": "ferias_aviso_fora_do_prazo"}',
            "reenvie a seção `dados_ferias` completa",
            "`programacao_source`",
        ),
        (
            "afastamento",
            "leave_preparation_requires_complete_input",
            '{"field": "leave.retorno", "reason": "afastamento_retorno_fora_da_vespera"}',
            "reenvie a seção `leave` completa",
            "`retorno_source`",
        ),
    ],
)
def test_domain_explains_current_preparation_refusal_by_field(
    domain: str, code: str, example: str, section: str, source: str
) -> None:
    text = flat(InstructionsProvider().get(domain)["instructions"])
    for required in (*PREPARATION_RULES, f"`{code}`", example, section, source):
        assert required in text, required


def test_general_explains_population_index_and_restart_reuse() -> None:
    general = flat(InstructionsProvider().get("geral")["instructions"])
    for required in (
        "`payroll_population_identity_changed`",
        '`next_action: "preview_payroll_population_correction"`',
        '{"field": "population[*]", "index": N, "reason": ...}',
        "contando do zero",
        *POPULATION_REASONS,
        "peça a prévia de novo",
        '`{"field": "population"}` sem `index`',
        "`vacation_preparation_requires_complete_input`",
        "`leave_preparation_requires_complete_input`",
        "`harness_sources`",
        "Reutilize os mesmos EXTSRC e anexos",
        "não registre nem anexe de novo o mesmo original",
    ):
        assert required in general, required
    assert InstructionsProvider().metadata()["mcp_contract_version"] == "2.7.1"


def test_documents_domain_points_to_reuse_after_restart() -> None:
    text = flat(InstructionsProvider().get("documentos")["instructions"])
    for required in ("`restart_case`", "`harness_sources`", "Reutilize os mesmos EXTSRC"):
        assert required in text, required


def test_plugin_mirrors_269_guidance() -> None:
    workflows = flat(WORKFLOWS.read_text(encoding="utf-8"))
    assert "## Preparação corrente, população da folha e fontes após reinício" in workflows
    capacities = flat(CAPACITIES.read_text(encoding="utf-8"))
    for guide in (workflows, capacities):
        for required in (
            "`vacation_preparation_requires_complete_input`",
            "`leave_preparation_requires_complete_input`",
            "`extra_forbidden`",
            "`payroll_population_identity_changed`",
            "contando do zero",
            *POPULATION_REASONS,
            "`harness_sources`",
        ):
            assert required in guide, required
    skill = flat((SKILLS / "operar-loki/SKILL.md").read_text(encoding="utf-8"))
    assert "Preparação corrente, população da folha e fontes após reinício" in skill
    report = flat((SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"))
    assert "`payroll_population_identity_changed`" in report
    assert "não registre o original de novo para contornar" in report
