"""Entrega das orientações da 2.6.8 e 2.6.11; nao mede obediencia da harness."""

from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
CAPACITIES = SKILLS / "operar-loki/references/CAPACIDADES_DP.md"
WORKFLOWS = SKILLS / "operar-loki/references/WORKFLOWS.md"

VACATION_CODES = (
    "ferias_aquisitivo_29_fevereiro_exige_qualificacao",
    "ferias_aquisitivo_incompleto",
    "ferias_gozo_duracao_invalida",
    "ferias_gozo_antes_do_fim_do_aquisitivo",
    "ferias_gozo_fora_do_concessivo",
    "ferias_aviso_fora_do_prazo",
    "ferias_pagamento_fora_do_prazo",
    "ferias_abono_pedido_incoerente",
    "ferias_pedido_abono_fora_do_prazo",
    "ferias_inicio_antes_de_feriado",
    "ferias_inicio_antes_de_repouso",
    "ferias_inicio_antes_de_repouso_source_sem_uso",
    "ferias_inicio_antes_de_repouso_source_sem_fundamento",
    "ferias_medias_alternativas_exclusivas",
    "ferias_media_repetida",
    "ferias_media_competencias_invalidas",
)
LEAVE_CODES = (
    "afastamento_inicio_antes_da_admissao",
    "afastamento_inicio_diverge_do_primeiro_periodo",
    "afastamento_periodos_descontinuos",
    "afastamento_fonte_de_retorno_sem_data",
    "afastamento_retorno_fora_da_vespera",
    "afastamento_periodo_invertido",
)
LEGACY_REST_CODE = "ferias_inicio_antes_de_repouso_ou_feriado"
REST_SECTION = "Férias antes do repouso semanal e recibos obsoletos"
REST_RULES = (
    "`dados_ferias.inicio_antes_de_repouso_source`",
    '`kind: "declaration"`',
    "`foundation`",
    "`ressalvas.declaracoes_dp`",
    '"Declaração do DP"',
    "aceite explícito das ressalvas",
    "`submit_operator_correction`",
    "`OBSOLETO`",
    "`medias_rescisao_obsoletas`",
    "Casos aprovados ou entregues não mudam",
)
OPERATOR_RULES = (
    "olhe a lista `errors`",
    "Corrija só o campo apontado, conferindo com o documento original",
    "novo `request_ref` e o snapshot atual do caso",
    "com ou sem `field_sources`, vai ser recusado de novo",
    "não force o valor",
    "registre a dúvida com a DP antes de reenviar",
    "valem somente quando a resposta servida os apresentar",
)


def flat(text: str) -> str:
    return " ".join(text.split())


@pytest.mark.parametrize(
    ("domain", "example", "codes"),
    [
        ("ferias", "dados_ferias.data_aviso", VACATION_CODES),
        ("afastamento", "leave.retorno", LEAVE_CODES),
    ],
)
def test_domain_explains_field_and_rule_code(
    domain: str, example: str, codes: tuple[str, ...]
) -> None:
    text = flat(InstructionsProvider().get(domain)["instructions"])
    assert "## Recusa com campo e código de regra" in text
    assert f"`{example}`" in text
    for required in (*OPERATOR_RULES, *codes):
        assert required in text, required


def test_leave_return_is_day_after_last_period() -> None:
    text = flat(InstructionsProvider().get("afastamento")["instructions"])
    assert "dia seguinte ao fim do último período" in text


def test_general_points_to_vacation_and_leave_domains() -> None:
    general = flat(InstructionsProvider().get("geral")["instructions"])
    for required in (
        "`dados_ferias.data_aviso`",
        "`leave.retorno`",
        "`ferias_...`",
        "`afastamento_...`",
        "domínios `ferias` e `afastamento`",
    ):
        assert required in general, required
    assert InstructionsProvider().metadata()["mcp_contract_version"] == "2.6.4"


def test_plugin_mirrors_268_guidance() -> None:
    workflows = flat(WORKFLOWS.read_text(encoding="utf-8"))
    assert "## Recusas de férias e afastamento com campo e código de regra" in workflows
    capacities = flat(CAPACITIES.read_text(encoding="utf-8"))
    for guide in (workflows, capacities):
        for required in (*VACATION_CODES, *LEAVE_CODES, "`field_sources`", "DP"):
            assert required in guide, required
        assert "dia seguinte ao fim do último período" in guide
    skill = flat((SKILLS / "operar-loki/SKILL.md").read_text(encoding="utf-8"))
    assert "Recusas de férias e afastamento com campo e código de regra" in skill
    report = flat((SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"))
    assert "não é defeito do Loki" in report
    assert "registre a dúvida com a DP, não como problema" in report


def test_vacation_domain_explains_rest_declaration_and_obsolete_receipts() -> None:
    text = flat(InstructionsProvider().get("ferias")["instructions"])
    for required in (
        *REST_RULES,
        "## Início antes do repouso semanal: declaração do DP",
        "## Recibos de componentes obsoletos depois do deploy",
        f"`{LEGACY_REST_CODE}` não é mais emitido",
        "A véspera de feriado continua vedada",
        "não há exceção: mude a data com o cliente",
        "a Izzi não acompanha a escala praticada",
        "Inferência, contexto, regra ou histórico são recusados",
        "A exceção não muda valores",
        "`confirmed: false`",
        "as duas folhas juntas em `changes`",
        "`dados_ferias.repouso_semanal`",
        "`recibo_componentes_obsoleto`",
        "nova qualificação dos componentes, nova consolidação",
        "novo cálculo, depois geração, conferência e revisão",
        "O Loki não recalcula nada sozinho",
    ):
        assert required in text, required
    termination = flat(InstructionsProvider().get("rescisao")["instructions"])
    for required in ("`medias_rescisao_obsoletas`", "`OBSOLETO`", "nova consolidação"):
        assert required in termination, required
    assert InstructionsProvider().metadata()["mcp_contract_version"] == "2.6.4"


def test_plugin_mirrors_2611_guidance() -> None:
    workflows = flat(WORKFLOWS.read_text(encoding="utf-8"))
    assert f"## {REST_SECTION}" in workflows
    capacities = flat(CAPACITIES.read_text(encoding="utf-8"))
    for guide in (workflows, capacities):
        for required in (*REST_RULES, f"`{LEGACY_REST_CODE}` não é mais emitido"):
            assert required in guide, required
    skill = flat((SKILLS / "operar-loki/SKILL.md").read_text(encoding="utf-8"))
    assert REST_SECTION in skill
    assert "`dados_ferias.inicio_antes_de_repouso_source`" in skill
    report = flat((SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"))
    for required in (
        "`ferias_inicio_antes_de_feriado`",
        "`ferias_inicio_antes_de_repouso`",
        "não é defeito",
        "`OBSOLETO`",
        "`medias_rescisao_obsoletas`",
        "siga o caminho de recuperação",
        "sem recomeçar o caso",
    ):
        assert required in report, required
