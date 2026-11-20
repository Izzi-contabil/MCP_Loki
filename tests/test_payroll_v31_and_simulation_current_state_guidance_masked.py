"""Entrega das orientações da 2.9.3 (backend #368 e #370) que seguem na 2.9.4.

O salário-família, o VT do admitido, o aviso e as versões passaram à 2.9.4
(`test_payroll_v32_and_worker_guidance_masked.py`). Ficam aqui a insalubridade
no mês de admissão, a simulação com o estado atual e a seção histórica do plugin.
Prova só que os textos chegam aos domínios e ao plugin; não mede obediência.
"""

from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
OPERATOR = SKILLS / "operar-loki"
WORKFLOWS = OPERATOR / "references/WORKFLOWS.md"
CAPACITIES = OPERATOR / "references/CAPACIDADES_DP.md"
SECTION_293 = "## 2.9.3: folha v31 (salário-família e insalubridade) e simulação com o estado atual"

HAZARD = (
    "## Insalubridade no mês de admissão (desde a folha-v31)",
    "O mapa precisa ter só a rubrica do grau declarado (`rubrica_loki`)",
    "Não acrescente a incompatível ao mapa",
    "declare `vigente_desde` igual à data de admissão",
    "pelos dias de `periodo_remuneravel` (ou pela quantidade lançada)",
    "Uma regra iniciada depois da admissão continua pendente",
)
SIMULATION_CURRENT = (
    "## Simulação com o estado histórico atual",
    '`payload.simulation.historical_state: "current"`',
    "`simulation_ref` **nova**",
    "`simulation_intent_conflict`",
    "consulte `get_case_historical_state` do caso real",
    "Não renova a seleção do caso real nem grava nada nele",
    "num caso real é recusado com `parameters_invalid`",
    "fontes `CPH-*` de folha fechada nova ainda não entram",
    "`source_document_missing`",
    "`historical_state_basis`",
    "`selected_state_hash`",
    "`differs_from_selection`",
    "`history_consumed`",
    "Repasse-as à operadora sempre que mostrar números da simulação",
    "HISTÓRICO NÃO CONSUMIDO NO CÁLCULO DESTA SIMULAÇÃO",
    "QUALIFICAÇÕES DO HISTÓRICO PERTENCEM À SELEÇÃO ANTERIOR",
    "`simulation.pending_qualifications`",
    "`historical_qualification_context_incompatible`",
    '"renovar seleção e qualificação no caso real"',
    "`historical_state_not_selected`",
    "`historical_state_source_incompatible` (novo)",
    "`historical_settlement_bound_to_selection` (novo",
    "`simulation_source_changed`",
)
STALE_TERMINATION = (
    "Sem reiniciar o caso real, não há caminho",
    "depende do reinício acima",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    # O aviso em citação (`> `) quebra a frase em linhas; a comparação ignora o marcador.
    lines = (line.removeprefix(">").strip() for line in value.splitlines())
    return " ".join(" ".join(lines).split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def assert_none(guide: str, stale: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in stale:
        assert flat(item) not in body, item


def test_payroll_domain_keeps_the_v31_hazard_guidance() -> None:
    payroll = text("folha_mensal")
    assert_all(payroll, HAZARD)
    assert_all(
        text("alteracao_cadastral"),
        ("Exceção da folha `folha-v31`", "cobre o mês de entrada, paga pelos dias"),
    )


def test_termination_domain_carries_current_state_simulation() -> None:
    termination = text("rescisao")
    assert_all(termination, SIMULATION_CURRENT)
    assert_none(termination, STALE_TERMINATION)
    assert_all(
        text("geral"),
        ('("Simulação de rescisão" e "Simulação com o estado histórico atual")',),
    )


def test_plugin_mirrors_293_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_293 in workflows
    assert_all(
        workflows,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "**Recálculo obrigatório (`folha_mensal`).**",
            "todas as folhas mensais não entregues",
            "As entregues não mudam",
            "`salario_familia_mes_admissao_pendente_regra`",
            "`salario_familia_remuneracao_zero_sem_declaracao`",
            "`salario_familia_base_inss_zero_com_proventos`",
            '`submit_operator_correction` com `target: "calculation"`',
            "`funcionarios.<matricula>.bases.salario_familia_cents`",
            "Falta de filhos se resolve completando o cadastro",
            "1/3 de férias e faltas na base do limite",
            "o mapa só exige a `rubrica_loki` do grau declarado",
            "VT do admitido no mês continua retido",
            '`payload.simulation.historical_state: "current"` e `simulation_ref` nova',
            "renovar seleção e qualificação no caso real",
            "`historical_state_source_incompatible`",
            "`historical_settlement_bound_to_selection`",
            "Fontes `CPH-*` de folha fechada nova ainda recusam",
        ),
    )
    assert_none(workflows, ("seleção desatualizada não tem caminho sem reiniciar o caso real",))
    # A seção histórica avisa que salário-família e VT passaram à 2.9.4.
    section = workflows[workflows.index(SECTION_293) :]
    assert "Substituída em parte pela 2.9.4" in section[: section.index("\n## ", 1)]
    assert_all(
        CAPACITIES.read_text(encoding="utf-8"),
        (
            "## 2.9.3: folha v31 e simulação com o estado atual",
            "**todas as folhas mensais não entregues precisam ser recalculadas, "
            "conferidas e aceitas de novo**",
            "Nada disso exige Refresh; a operadora atualiza o plugin e recalcula as folhas",
        ),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.3: folha v31 (salário-família e insalubridade) e simulação com o estado atual”",
            "**todas as folhas mensais não entregues precisam ser recalculadas, "
            "conferidas e aceitas de novo**",
            "a operadora atualiza o plugin e recalcula as folhas",
        ),
    )
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "Na 2.9.3 não são defeito",
            "`calculation_stale` depois da troca para `folha-v31`",
            "`salario_familia_mes_admissao_pendente_regra` (regra da DP, pergunte à Rafa)",
            "`vale_transporte_vigencia_parcial_exige_regra`",
            "fonte `CPH-*` de folha fechada nova (limite conhecido)",
            "`historical_state_source_incompatible` com fonte que a operadora confirma "
            "íntegra é problema a relatar",
            "sem nome ou CPF",
        ),
    )
