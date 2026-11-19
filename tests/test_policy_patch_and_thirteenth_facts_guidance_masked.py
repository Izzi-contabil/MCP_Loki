"""Entrega das orientações da 2.9.2 (backend #365, #366 e #367).

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
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
SECTION_292 = "## 2.9.2: política do mapa de rescisão e fatos do 13º"

NOTICE = (
    "## O que mudou nesta versão (2.9.2)",
    "Atualizações devem ser imperceptíveis",
    "**Exige ação da operadora:** só atualizar o plugin instalado",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
    "**Não exige nada**",
    "`loki.company-termination-map-policy-patch/1`",
    "A política declarada substitui a atual inteira",
    "`termination_policy_preview`",
    "`blocking_facts`",
    "Qualificar um fato muda o `state_hash` do empregado",
    "alinhe com a DP antes",
)
POLICY_PATCH = (
    "## Trocar só a política de arredondamento do mapa",
    "`termination_map_policy_patch_transport`",
    '"schema_version": "loki.company-termination-map-policy-patch/1"',
    "Uma chamada leva várias empresas e grava uma única versão do cadastro",
    "avise a operadora que o servidor ainda não tem o patch",
    "**A política declarada substitui a atual inteira:** repita nela os `escopos`, "
    "a `fonte` e as opções que devem continuar ligadas",
    "Opção omitida fica desligada",
    "Todas as seleções indicadas de uma empresa recebem a mesma política",
    "`fonte` é obrigatória",
    "Não mande `medias_por_bloco`: ela continua desligada sem conferência com a DP",
    "O patch não pede `parcelas_do_mes`",
    "**Mostre à operadora, antes do apply:**",
    "`opcoes_ligadas`",
    "`escopos_removidos`",
    "`fonte_trocada`",
    "`politicas_distintas_unificadas`",
    "Só com a prévia `VALIDO` e o aceite dela",
    "`termination_policy_patch_remove_incompatible`",
    "`termination_patch_company_not_unique`",
    "`companies[*].policy.arredondamento_proporcionais` (`value_error`)",
    "qualquer recusa recusa o pedido inteiro, sem gravar",
)
THIRTEENTH_FACTS = (
    "## Fatos documentais não qualificados",
    "`code=historical_thirteenth_unqualified_documentary_facts`",
    "`blocking_facts_total`",
    'Servidor anterior devolve só `{"erro": "<código>"}`',
    "`path=qualify_legacy_fact`",
    "`allowed_types`",
    "`replaces_fact_id=<id da cobertura>`",
    "`qualifies_legacy_fact_ids` com todos os fatos daquela fonte",
    "Não crie cobertura nova nem intervalo que a ficha não certifique",
    "o `history_hash` e o `state_hash` dele",
    "exigem novo `apply_historical_state`",
    "**Não qualifique quem tem outros casos abertos sem alinhar com a DP.**",
    "só vale em cortes a partir do `effective_on` da cobertura, que é o fim dela",
    "`path=no_typed_exit`",
    "`path=dp_rule_pending`",
    "**não deve ser usado para qualificar fato do 13º**",
    "`path=episode_reconciliation`",
    "`reason=effective_date_missing`",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    return " ".join(value.split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def test_versions_follow_the_additive_contract_patch() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.27"
    assert metadata["instructions_version"] == "2.9.2"
    assert metadata["mcp_contract_version"] == "2.9.2"
    assert metadata["recommended_plugin_version"] == "2.9.2"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.8.0", "2.9.0", "2.9.1", "2.9.2"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.9.2", "2.9.3")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    backend = release["changes"]["backend"][-1]
    assert backend.startswith("Contrato2.9.2 aditivo")
    assert "as 96 ferramentas são as mesmas" in backend
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.2")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.2")


def test_general_notice_asks_only_for_the_plugin_update() -> None:
    guide = text("geral")
    end = guide.index("## Reaproveitar respostas e causas persistidas")
    assert guide.index("## O que mudou nesta versão (2.9.2)") < end
    notice = guide[:end]
    assert_all(notice, NOTICE)
    current = notice[: notice.index("**Continua da 2.8.0**")]
    for domain in ("`rescisao`", "`decimo_terceiro`"):
        assert domain in current, domain
    assert "Exige Refresh" not in current
    assert "## O que mudou nesta versão (2.9.1)" not in guide
    assert len(guide.encode("utf-8")) <= 65536


def test_domains_carry_the_new_guidance() -> None:
    termination = text("rescisao")
    assert_all(termination, POLICY_PATCH)
    policy = termination[termination.index("## Trocar só a política de arredondamento do mapa") :]
    policy = policy[: policy.index("\n## ", 1)]
    example = policy[policy.index("```json") : policy.index("```", policy.index("```json") + 1)]
    assert '"medias_por_bloco"' not in example
    assert '"parcelas_do_mes"' not in example
    assert_all(termination, ('para ela, veja "Trocar só a política de arredondamento do mapa"',))
    thirteenth = text("decimo_terceiro")
    assert_all(thirteenth, THIRTEENTH_FACTS)
    # A média importada continua valendo em medias_importadas; só não qualifica fato.
    assert_all(
        thirteenth,
        (
            "**`final_average` é a média mensal integral do Domínio.**",
            "Esse uso da média em `medias_importadas` não muda",
        ),
    )


def test_plugin_mirrors_292_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_292 in workflows
    assert_all(
        workflows,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "`loki.company-termination-map-policy-patch/1`",
            "A política declarada substitui a atual inteira",
            "Seleções da mesma empresa recebem a mesma política",
            "O patch não pede `parcelas_do_mes`",
            "Mostre o `termination_policy_preview` à operadora antes do apply",
            "`blocking_facts` (tipo, data, identificador, `reason` e `path`)",
            "`replaces_fact_id` e `qualifies_legacy_fact_ids`",
            "Isso muda o `state_hash` do empregado",
            "só vale em cortes a partir do fim da cobertura",
            "Não use `final_average` para qualificar fato do 13º",
        ),
    )
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert_all(
        capacities,
        (SECTION_292, "Nada disso exige Refresh; a operadora só atualiza o plugin"),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.2: política do mapa de rescisão e fatos do 13º”",
            "a operadora só atualiza o plugin",
        ),
    )
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "Na 2.9.2, no 13º",
            "`path=no_typed_exit`",
            "sem nome, CPF ou texto da ficha",
            "`termination_policy_patch_remove_incompatible`",
            "Relate sempre pelo assistente, com `registrar_problema`",
            "o Loki Suporte só responde nas threads dos pedidos que ele publicou "
            "ou quando alguém o menciona (`@Loki Suporte`)",
        ),
    )
