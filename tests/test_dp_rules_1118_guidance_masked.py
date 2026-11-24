"""Entrega das orientações da 2.9.1 (regras da DP de 18/11/2026, backend #363).

Prova só que os textos chegam aos domínios e ao plugin; não mede obediência.
O aviso do geral passou a ser o da 2.9.3
(test_payroll_v31_and_simulation_current_state_guidance_masked.py).
"""

import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
OPERATOR = SKILLS / "operar-loki"
WORKFLOWS = OPERATOR / "references/WORKFLOWS.md"
CAPACITIES = OPERATOR / "references/CAPACIDADES_DP.md"
GUIDE = OPERATOR / "references/REAJUSTE_SALARIAL.md"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"

ADMITTED_ON_BASE_DATE = (
    "## Admitido no mês da data-base",
    "`rule.admitted_on_base_date`",
    "`salario_anterior_esperado_cents` igual ao salário de admissão e sem `salario_novo_cents`",
    "`motivo_sem_reajuste = admitido_na_data_base_com_salario_novo`",
    "isso não é divergência",
    "Se o piso novo for maior, vale o piso",
    "`salario_novo_cents` maior sem motivo diverge da regra",
    "Sem o sinal (servidor anterior), só o próprio dia da data-base tem essa regra",
)
TRANSPORT = (
    "Descontos que dependem do salário, como o VT (6%), não entram na diferença",
    "Não declare VT em `origens_declaradas.<mês>.verbas`",
    "Ele não impede a afirmação `sem_outras_verbas_dependentes_do_salario: true`",
    "`declared_origins.transport_discount`",
)
ALREADY_REGISTERED = (
    "já registrado com vigência na data-base é o próprio reajuste da CCT",
    "a diferença ainda não foi paga. Envie a linha normalmente",
)
# Orientação antiga que a DP respondeu em 18/11/2026: não pode voltar.
STALE_ADJUSTMENT = (
    "**Pergunta para a DP (pendente; não decida sozinha).**",
    "Enquanto não houver resposta, deixe a linha pendente",
    "porque não há véspera no vínculo",
    "A pessoa admitida na própria data-base com o salário novo já no cadastro",
)
VACATION = (
    "o gozo termina antes do fim do próprio aquisitivo (`end < period_end`)",
    "`start <= period_end <= end`, inclusive no primeiro ou no último dia",
    "**Gozo programado antes de concluir o aquisitivo**",
    "Declare o `vacation_use` com o `period_end` do aquisitivo que ele quita",
    "**Lote recusado antes por `historical_vacation_use_period_incompatible`.**",
    "a próxima validação pode devolver `ready`",
    "aplique com o `validation_hash` novo",
    "com o `validation_hash` antigo é recusado com `snapshot_desatualizado`",
    "`ferias_gozo_antes_do_fim_do_aquisitivo`",
)
STALE_VACATION = (
    "o gozo começa até o fim do próprio aquisitivo",
    "Se a fonte mostra antecipação real, **não grave**",
)
LEAVE = (
    "## Atestados consecutivos e licença-maternidade",
    "dois atestados de 5 dias são dois afastamentos",
    "`retorno` (dia seguinte ao fim)",
    "Não junte atestados num afastamento só",
    "não são sobreposição",
    "Licença-maternidade não é falta e não reduz o aquisitivo de férias",
    "`categoria: licenca_maternidade`",
)
AVERAGES = (
    "**Regra da DP (18/11/2026): o Domínio soma as médias.**",
    "sem separar por empresa, em férias e no 13º",
    "Não ligue `medias_por_bloco` sem conferência com a DP",
    "A opção continua disponível só se a DP pedir uma exceção",
)
# A 2.9.5 condiciona a guarda: vale enquanto o contrato não citar a adoção.
REGISTRATION = (
    "não grave matrícula nova por worker `identifier_only`",
    "sem falar antes com a engenharia",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    return " ".join(value.split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def assert_none(guide: str, stale: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in stale:
        assert flat(item) not in body, item


def test_contract_291_entries_are_kept_in_the_release() -> None:
    provider = InstructionsProvider()
    for version in ("2.0.0", "2.8.0", "2.9.0", "2.9.1"):
        assert provider.check_version(version, version)["compatible"] is True
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    for category, prefix in (
        ("backend", "Contrato2.9.1 aditivo"),
        ("instructions", "Instruções2.9.1"),
        ("plugin", "Plugin2.9.1"),
    ):
        entry = [item for item in release["changes"][category] if item.startswith(prefix)]
        assert len(entry) == 1, prefix
    backend = [i for i in release["changes"]["backend"] if i.startswith("Contrato2.9.1")]
    assert "as 96 ferramentas são as mesmas" in backend[0]


def test_general_notice_is_no_longer_the_291_one() -> None:
    guide = text("geral")
    assert "## O que mudou nesta versão (2.9.1)" not in guide
    assert "## O que mudou nesta versão (2.9.0)" not in guide
    assert_all(guide, REGISTRATION)
    assert len(guide.encode("utf-8")) <= 65536


def test_domains_carry_the_dp_rules() -> None:
    adjustment = text("reajuste_salarial")
    assert_all(adjustment, (*ADMITTED_ON_BASE_DATE, *TRANSPORT, *ALREADY_REGISTERED))
    assert_none(adjustment, STALE_ADJUSTMENT)
    vacation = text("ferias")
    assert_all(vacation, VACATION)
    assert_none(vacation, STALE_VACATION)
    assert_all(text("afastamento"), LEAVE)
    termination = text("rescisao")
    assert_all(termination, AVERAGES)
    assert_none(termination, ("não usa blocos nem micros (pendente com a DP)",))
    thirteenth = text("decimo_terceiro")
    assert_all(thirteenth, ("o Domínio soma as médias de todas as empresas do grupo",))
    assert_none(thirteenth, ("Se o cálculo por bloco vale também para o 13º",))
    assert_all(text("alteracao_cadastral"), REGISTRATION)


def test_plugin_guide_keeps_the_domain_text() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    domain = text("reajuste_salarial")
    section = guide[guide.index("## Admitidos depois da data-base") :]
    assert section.rstrip() in domain
    assert_all(guide, (*ADMITTED_ON_BASE_DATE, *TRANSPORT, *ALREADY_REGISTERED))
    assert_none(guide, STALE_ADJUSTMENT)


def test_plugin_mirrors_291_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert "## 2.9.1: regras da DP de 18/11/2026" in workflows
    assert_all(
        workflows,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "`admitido_na_data_base_com_salario_novo`, `rule.admitted_on_base_date`",
            "`declared_origins.transport_discount`",
            "o hash antigo dá `snapshot_desatualizado`",
            "Licença-maternidade (`categoria: licenca_maternidade`) não é falta",
            "Não ligue `medias_por_bloco` sem conferência com a DP",
            "não grave matrícula nova por `identifier_only` sem falar com a engenharia",
        ),
    )
    assert_none(workflows, ("antecipação real de férias fica pendente com a DP",))
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert_all(
        capacities,
        (
            "## 2.9.1: regras da DP de 18/11/2026",
            "Nada disso exige Refresh; a operadora só atualiza o plugin",
        ),
    )
    assert_none(capacities, ("antecipação real de férias fica pendente com a DP",))
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        ("“2.9.1: regras da DP de 18/11/2026”", "a operadora só atualiza o plugin"),
    )
    assert_all(
        (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"),
        (
            "Na 2.9.1 não são defeito",
            "`admitido_na_data_base_com_salario_novo`",
            "`snapshot_desatualizado` ao aplicar com o `validation_hash` antigo",
        ),
    )
