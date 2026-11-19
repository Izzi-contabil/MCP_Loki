"""Entrega das orientações da 2.9.0 (backend #358, #359, #360); nao mede obediencia.

O aviso do geral passou a ser o da 2.9.2
(test_policy_patch_and_thirteenth_facts_guidance_masked.py).
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

ADJUSTMENT = (
    "## Folha que bloqueia a linha e pendência de cadastro",
    '`folha_bloqueante: {competencia: "AAAA-MM", estado}`',
    '`get_process_contract("reajuste_salarial").preview.blocking_payroll`',
    "competência X **ou qualquer competência posterior**",
    "O histórico importado não conta",
    "Lance na primeira competência depois da última folha do Loki",
    "com a DP confirmando o mês",
    "`salary_adjustment_instrument_case_mismatch`",
    "**fecha no apply**",
    "`decision.config_pending_reconciled`",
    "Ela não impede o `apply_case_effects`",
    "`processo_nao_habilitado_no_cliente`, o apply segue, mas o certo é habilitar",
    "Use sempre o `expected_snapshot` da prévia mais recente",
)
DOMINIO_METHOD = (
    "## Método do Domínio na rescisão (opt-in por empresa e vigência)",
    '"metodo_ferias": "valor_dia_6_casas"',
    '"terco": "por_parcela"',
    '"saldo": "valor_dia_6_casas"',
    '"medias_por_bloco": true',
    "`rescisao_saldo_valor_dia_exige_trinta_fixo`",
    "`saldo_valor_dia_exige_mes_comercial`",
    "Não troque a convenção para contornar",
    "`+metodo-dominio-v1`",
    "O Loki não confere a fonte",
)
AVERAGES = (
    "## Médias com seis casas e por bloco de empresa",
    "`horas_micros`, `valor_micros` e\n  `vantagens_micros`",
    "(R$ 30,125003 → `30125003`)",
    "`componentes_media_micros_incoerente`",
    "`imported_average_micros_incoerente`",
    "a carga por CSV\n  ainda não tem colunas de micros",
    "O formulário de fatos de `medias_variaveis`\n  passa a trazer o campo `bloco`",
    "sem a opção, os blocos somam como uma média só",
)
SIMULATION = (
    "## Simulação de rescisão",
    "compare o\n`state_hash` de `get_case_historical_state` com o da seleção",
    "Sem reiniciar o caso real, não há caminho",
    "`shadow_scenario_id`, `occurrence_ref` e `shadow_termination`",
    "Omitir uma\n  chave dá `identity_changed`",
    "`$.payload.dados_rescisao.salario_base_cents`",
    "`get_process_contract(...).version_refusal_subreasons`",
    "`historical_state_stale`",
    "`historical_state_window_pin_missing`",
    "`canonical_anchor_changed`",
)
ADMISSION = (
    "## Data de admissão errada no caso",
    "A data de admissão é identidade",
    "não se troca",
    "transcrevendo em `human_message` a mensagem do cliente",
    "abrir outro caso de admissão",
    "confira se o episódio antigo já recebeu matrícula",
    "O `cancel_case` não libera a\nmatrícula",
    "registre o\nproblema com `registrar_problema`",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    return " ".join(value.split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def test_contract_290_entry_is_kept_in_the_release() -> None:
    provider = InstructionsProvider()
    for version in ("2.0.0", "2.8.0", "2.9.0"):
        assert provider.check_version(version, version)["compatible"] is True
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    entry = [
        item for item in release["changes"]["backend"] if item.startswith("Contrato2.9.0 aditivo")
    ]
    assert len(entry) == 1
    assert "mesmo hash" in entry[0]


def test_general_notice_is_no_longer_the_290_one() -> None:
    guide = text("geral")
    assert "## O que mudou nesta versão (2.9.0)" not in guide
    assert "## O que mudou nesta versão (2.8.0)" not in guide
    assert_all(guide, ('Simulação de rescisão"',))


def test_domains_carry_the_answers_given_to_the_operator() -> None:
    assert_all(text("reajuste_salarial"), ADJUSTMENT)
    assert_all(text("rescisao"), (*DOMINIO_METHOD, *AVERAGES, *SIMULATION))
    assert_all(text("admissao"), ADMISSION)
    assert_all(text("decimo_terceiro"), ("O 13º continua com os centavos e não\nrateia por bloco",))


def test_plugin_guide_keeps_the_domain_text() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    domain = text("reajuste_salarial")
    section = guide[guide.index("## Folha que bloqueia a linha") :]
    section = section[: section.index("## Pendente até a DP decidir")]
    assert section in domain
    assert_all(guide, ADJUSTMENT)


def test_plugin_mirrors_290_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert "## 2.9.0: reajuste, rescisão, simulação e admissão" in workflows
    assert_all(
        workflows,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "atualizar o plugin instalado",
            "`folha_bloqueante`",
            "o histórico importado não conta",
            "`processo_nao_habilitado_no_cliente` não barra o apply",
            "`rescisao_saldo_valor_dia_exige_trinta_fixo`",
            "`+metodo-dominio-v1`",
            "seleção desatualizada não tem caminho sem reiniciar o caso real",
            "a data de admissão é identidade e não se troca",
        ),
    )
    assert_all(
        CAPACITIES.read_text(encoding="utf-8"),
        (
            "## 2.9.0: método do Domínio na rescisão, reajuste e simulação",
            "Nada disso exige Refresh; a operadora só atualiza o plugin",
        ),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        ("“2.9.0: reajuste, rescisão, simulação e admissão”", "a operadora só\natualiza o plugin"),
    )
    assert_all(
        (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"),
        (
            "o `cancel_case` não libera a matrícula",
            "`saldo_valor_dia_exige_mes_comercial` também é problema a relatar",
            "`folha_do_lancamento_em_revisao_ou_fechada` (leia `folha_bloqueante`)",
        ),
    )
