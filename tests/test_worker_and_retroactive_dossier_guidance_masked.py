"""Entrega das orientações da 2.9.7 (backend #387 publicado e #392 aberta).

Prova só que os textos chegam aos domínios e ao plugin; não mede obediência.
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
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
SECTION_297 = "## 2.9.7: worker sem concessão por empresa e pendências do reajuste no dossiê"
LIMIT = 65536

NOTICE = (
    "## O que mudou nesta versão (2.9.7)",
    "O Loki pode chegar em partes: cada item vale quando a resposta servida mostrar o "
    "sinal indicado; sem o sinal, siga a orientação anterior do mesmo domínio.",
    "Atualizar o plugin instalado",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
    "O worker de folha não precisa mais de concessão por empresa",
    "`retroactive_actions`",
    "`envelope_schema`",
    "**Continua da 2.9.6**",
)
STALE_NOTICE = (
    "## O que mudou nesta versão (2.9.6)",
    "A 2.9.5 e a 2.9.6 chegam juntas",
    "Da 2.9.5:",
)
WORKER = (
    "**Worker de folha.** O worker não precisa de concessão por empresa",
    "o escopo de quem enfileirou é conferido no enqueue e em cada fase",
    "Empresa nova não entra na conta do worker e ninguém a inclui",
    "não use `prepare_authorization_addition` nem `preparar_autorizacao` para o worker",
    "`worker_service_not_authorized`",
    '`worker_not_authorized` com `reason: "worker_company_grant_missing"`: '
    "servidor anterior a esta regra",
    "registre o problema e avise a engenharia pelo Caixa",
    "A conta da rotina continua precisando de concessão por empresa explícita",
    "Uma conta pode ter até 5000 concessões",
    "aceita até 500 por pedido",
)
STALE_WORKER = (
    "no worker de folha, `folha_mensal` com",
    "inclui a empresa pelo comando aditivo `prepare_authorization_addition` com o "
    "`required_grant` da recusa",
    "nunca para incluir empresa no worker",
    "**Empresa nova sem o worker.**",
    "`worker_account_revision`",
    "Com a concessão automática, empresa nova já entra no worker sozinha",
)
DECLARED = (
    "**`quantidade` segue a fórmula do mapa da competência de origem**",
    "nunca envie `quantidade`, mesmo que o holerite mostre 30 dias",
    "`salario_base_nao_aceita_quantidade`",
    "Quando o `retroactive_detail` mostrar a regra "
    "`remuneracao_periodo_quantidades_divergentes`, pode haver mais de uma no mesmo mês",
    "todas com a mesma `quantidade`, a do período pago no holerite",
    "Quantidades ou unidades diferentes no mesmo mês dão `diferenca_origem_invalida`",
    "Sem esse sinal (servidor anterior, regra `remuneracao_periodo_repetida`), declare "
    "uma única por mês",
    "`formula_exige_quantidade`",
    "`verba_proporcional_automatica`",
)
CORRECTION = (
    "## Corrigir o pago declarado de lote já aplicado",
    "`withdraw: true` e `supersedes_effect_id`; exige `corrigir_dados`",
    "o mesmo instrumento (mesmo tipo, data-base, regra e competência de lançamento) "
    "e outra `reference`",
    "`dados_reajuste_salarial.instrumento.reference`",
    "`linhas.<matricula>.origens_declaradas.<AAAA-MM>`",
    "`salary_adjustment_reopen_invalid`",
    "`salary_adjustment_exclusion_invalid`",
    "nenhuma das duas corrige linha `APPLIED`",
)
POLICY = (
    "faça um `add` de vigência nova com `vigente_desde` no dia 1 da competência de lançamento",
    "`loki.company-payroll-map-patch/1`",
    "nunca um `replace` numa vigência que cubra mês de origem fechado",
    "`get_client_config.payroll_map_patch_transport`",
)
DOSSIER = (
    "## Pendências da diferença no dossiê da folha",
    "Vale quando a issue `contexto_operacional_pendente`",
    "`retroactive_actions` traz uma ação por código",
    "`diferenca_funcionario_fora_da_folha` não tem ação própria",
    "`escolher_pela_regra_em_retroactive_detail`",
    "só é feita com a folha em preparação",
    "`retroactive_detail_case_not_in_preparation`",
    "`retroactive_detail_busy`",
    "`retroactive_detail_unavailable`",
    "`codigo_origem_available: false`",
    "`folha_loki_fechada`",
    "`retirar_efeito_no_caso_filho_e_relancar_reajuste_com_origem_corrigida`",
    "`registrar_problema`",
    "`matches_calculation: false`",
    "`retroactive_proof_not_recognized`",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
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


def test_versions_follow_the_additive_contract_patch() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.32"
    assert metadata["instructions_version"] == "2.9.7"
    assert metadata["mcp_contract_version"] == "2.9.7"
    assert metadata["recommended_plugin_version"] == "2.9.7"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.9.5", "2.9.6", "2.9.7"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.9.7", "2.9.8")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    backend = release["changes"]["backend"][-1]
    assert backend.startswith("Contrato2.9.7 aditivo")
    assert "as 96 ferramentas são as mesmas" in backend
    for marker in ("#387", "5b8de2b3", "#392", "60160952", "#393", "a51d5b80"):
        assert marker in backend
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.7")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.7")
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.9.7", path.name
        assert data["updated_at"] == "2026-11-23", path.name
        assert data["compatibility"]["mcp_contract_version"] == "2.9.7", path.name


def test_every_domain_stays_within_the_size_limit() -> None:
    provider = InstructionsProvider()
    for domain in provider.domains():
        size = len(provider.get(domain)["instructions"].encode("utf-8"))
        assert size <= LIMIT, (domain, size)


def test_general_notice_is_conditional_and_needs_no_refresh() -> None:
    guide = text("geral")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.9.7)")
    notice = guide[: guide.index("## Reaproveitar respostas e causas persistidas")]
    assert_all(notice, NOTICE)
    assert_none(notice, STALE_NOTICE)
    assert notice.index("**Exige ação da operadora:**") < notice.index("**Não exige nada**")
    assert notice.index("**Não exige nada**") < notice.index("**Continua da 2.9.6**")
    assert notice.index("**Continua da 2.9.6**") < notice.index("**Continua da 2.8.0**")


def test_worker_needs_no_company_grant_and_routines_keep_theirs() -> None:
    general = text("geral")
    section = general[general.index("## Empresa nova e onboarding pela rotina") :]
    section = section[: section.index("**Onboarding pela rotina (conta técnica)**")]
    assert_all(section, (*WORKER, "`access_auto_granted`", "`@empresas-novas`"))
    payroll = text("folha_mensal")
    assert_all(
        payroll,
        (
            "0. **Worker de folha sem concessão por empresa.**",
            "`worker_service_not_authorized`",
            "repita o mesmo enqueue com o mesmo `request_ref`",
        ),
    )
    for guide in (general, payroll):
        assert_none(guide, STALE_WORKER)


def test_salary_adjustment_carries_declared_rules_correction_and_dossier() -> None:
    guide = text("reajuste_salarial")
    assert_all(guide, (*DECLARED, *CORRECTION, *POLICY, *DOSSIER))
    assert_none(
        guide,
        (
            "abra um caso coletivo com nova referência do instrumento; o mesmo "
            "instrumento não é reaplicado",
            "Leve as pendências à DP; nunca as zere",
        ),
    )
    payroll = text("folha_mensal")
    assert_all(
        payroll,
        (
            "Quando a issue trouxer `retroactive_actions`, `missing_fields` também lista",
            "não tornam `context_fields_complete` falso",
            '"Pendências da diferença no dossiê da folha"',
        ),
    )


def test_plugin_salary_guide_is_the_domain_text() -> None:
    domain = text("reajuste_salarial")
    body = domain[domain.index("## Quando usar") : domain.index("\nToda operação usa o conector")]
    guide = GUIDE.read_text(encoding="utf-8")
    assert guide.endswith(body.rstrip("\n") + "\n")


def test_plugin_mirrors_297_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_297 in workflows
    assert workflows.index(SECTION_297) < workflows.index("## 2.9.6: correções no reinício")
    section = workflows[workflows.index(SECTION_297) :]
    section = section[: section.index("\n## ", 1)]
    assert_all(
        section,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "Cada item vale quando a resposta servida mostrar o sinal indicado",
            "não use `prepare_authorization_addition` nem `preparar_autorizacao` para ele",
            "`worker_service_not_authorized`",
            "a conta da rotina (`carga_historica`) continua precisando de concessão por empresa",
            "5000 concessões",
            "`retroactive_detail`",
            "`retroactive_detail_case_not_in_preparation`",
            "`envelope_schema`",
            "nunca em `salario_base`",
            "outra `reference`",
        ),
    )
    assert_all(
        workflows,
        (
            "> Substituída em parte pela 2.9.7: o worker de folha não recebe empresa nem",
            "> Substituída em parte pela 2.9.5 e pela 2.9.7: o worker de folha não precisa",
            "Substituído pela 2.9.7: o worker não precisa de concessão por empresa",
            "Com `retroactive_actions` na issue, `missing_fields` lista também as",
            "Reabertura e exclusão não corrigem linha `APPLIED`",
        ),
    )
    assert_none(workflows, ("siga o `prepare_authorization_addition` do item",))
    assert_all(
        CAPACITIES.read_text(encoding="utf-8"),
        (
            SECTION_297,
            "Substituída em parte pela 2.9.7: worker de folha.",
            "Substituída em parte pela 2.9.7: o worker não precisa de concessão por empresa.",
        ),
    )
    assert_none(
        CAPACITIES.read_text(encoding="utf-8"),
        ("`prepare_authorization_addition` fica para a recusa",),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.7: worker sem concessão por empresa e pendências do reajuste no dossiê”",
            "Substituída em parte pela 2.9.7: o worker não precisa de concessão por empresa.",
        ),
    )
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "são problema a registrar e avisar à engenharia pelo Caixa",
            "não peça à pessoa owner que inclua a empresa no worker",
            "`retroactive_proof_not_recognized`",
        ),
    )
    assert_none(
        report,
        (
            "a pessoa owner inclui a empresa no worker",
            "`worker_company_grant_missing` não é defeito",
        ),
    )
