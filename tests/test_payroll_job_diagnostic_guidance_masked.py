"""Entrega das orientações da 2.6.10; nao mede obediencia da harness."""

from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
CAPACITIES = SKILLS / "operar-loki/references/CAPACIDADES_DP.md"
WORKFLOWS = SKILLS / "operar-loki/references/WORKFLOWS.md"
SECTION = "Diagnóstico do job da folha bloqueado no cálculo"

SHARED_RULES = (
    "`diagnostic.errors`",
    "`calculate`",
    "`dados_folha.funcionarios`",
    "contando do zero",
    "`.fatos_datados.K.alocacao`",
    "`.salario_base`",
    "`.periodo_remuneravel`",
    "`.parcelas_salariais`",
    "`.matricula`",
    "`verba_nao_mapeada`",
    "`codigo`",
    "mapa da empresa",
    "`operational_pending_employee_out_of_scope`",
    "`cadastro_pending_employee_out_of_scope`",
    "`tabela_legal_fora_da_competencia`",
    "efeito operacional",
    "`expected_snapshot`",
)
GROUPED_CODES = (
    "`base_inss_negativa`",
    "`salario_base_ausente`",
    "`quantity_fact_required`",
    "`fato_datado_sem_alocacao`",
    "`salary_installments_period_mismatch`",
    "`rubrica_dependencia_circular`",
    "`insalubridade_...`",
    "`vale_transporte_...`",
)


def flat(text: str) -> str:
    return " ".join(text.split())


def test_general_explains_blocked_payroll_job_diagnostic() -> None:
    general = flat(InstructionsProvider().get("geral")["instructions"])
    for required in (
        *SHARED_RULES,
        *GROUPED_CODES,
        "`get_case_workflow_job`",
        '{"field": ..., "index": N, "reason": ...}',
        "O índice do lançamento pode passar do número de lançamentos enviados",
        '`{"field": "dados_folha.valorizacao"}` sem `index`',
        "`fgts_mensal_exige_mapa_contextual`",
        "O Loki nunca devolve a matrícula",
        "não autoriza recomeçar o caso",
        "conjunto que o Loki serve no diagnóstico",
    ):
        assert required in general, required
    assert InstructionsProvider().metadata()["mcp_contract_version"] == "2.6.4"


def test_plugin_mirrors_2610_guidance() -> None:
    workflows = flat(WORKFLOWS.read_text(encoding="utf-8"))
    assert f"## {SECTION}" in workflows
    for required in GROUPED_CODES:
        assert required in workflows, required
    capacities = flat(CAPACITIES.read_text(encoding="utf-8"))
    for guide in (workflows, capacities):
        for required in SHARED_RULES:
            assert required in guide, required
    skill = flat((SKILLS / "operar-loki/SKILL.md").read_text(encoding="utf-8"))
    assert SECTION in skill
    report = flat((SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"))
    for required in (
        "`diagnostic.errors`",
        "não é defeito",
        "`payroll_valuation_invalid`",
        "`index` incoerente",
        "não recomece o caso para contornar",
    ):
        assert required in report, required
