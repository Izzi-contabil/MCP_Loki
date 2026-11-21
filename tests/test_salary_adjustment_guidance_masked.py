"""Entrega das orientações da 2.7.0 (reajuste coletivo); nao mede obediencia da harness."""

import json
import re
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
OPERATOR = SKILLS / "operar-loki"
GUIDE = OPERATOR / "references/REAJUSTE_SALARIAL.md"
WORKFLOWS = OPERATOR / "references/WORKFLOWS.md"
CAPACITIES = OPERATOR / "references/CAPACIDADES_DP.md"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"

INTERFACES = (
    "`loki.salary-adjustment/1`",
    "`loki.salary-adjustment-preview/1`",
    "`loki.salary-adjustment-exclusion/1`",
    "`loki.salary-adjustment-reopen/1`",
)
STEPS = (
    "`create_case` com `case_type=reajuste_salarial`",
    'get_process_contract("reajuste_salarial")',
    "blocos de até 100 matrículas",
    "`validate_case`",
    "`proximo_inicio`",
    "`resumo_total`",
    "aceite explícito da operadora para o lote inteiro",
    "decisão humana explícita",
    "Retome pelo mesmo `request_ref`",
    "até `APPLIED` ou `PARTIAL`",
)
AUTHORITY = (
    "O Loki só valida a coerência interna",
    "O Loki nunca confere a fonte",
    '`conferencia_das_fontes: "harness"`',
    "não invente convenção",
    "`reajuste_salarial` e `alteracao_cadastral`",
    "`salary_adjustment_requires_employee_change_scope`",
)
EXITS = (
    "mostra o estado real",
    'Nunca diga "nada foi gravado" quando já houve efeito',
    "`effects_written=true`",
    'saida: ["reabertura", "exclusao"]',
    "`nao_aplicavel_apos_decisao`",
    "`decisao_da_dp`",
    "retirada no caso filho",
    "`withdraw:true`",
    "`salary_adjustment_child_requires_collective`",
    "`reserved_occurrence_ref`",
    "`salary_adjustment_line_key_changed`",
)
DECLARED = (
    "`origens_declaradas",
    "`sem_outras_verbas_dependentes_do_salario: true`",
    "`diferenca_origem_declarada_incompleta`",
    "`diferenca_origem_sem_base`",
    "`diferenca_reflexos_nao_calculados`",
    "Não invente o pago",
    "`codigo_origem`",
    "`valor_pago_cents`",
)
REASONS = (
    "`proporcional_admissao`",
    "`reajuste_proporcional_nao_praticado`",
    "`acima_do_piso_mantido`",
    "`outro_declarado`, com `motivo_texto` obrigatório",
    "`salario_novo_diverge_da_regra`",
    "`sem_reajuste`",
)
PAYROLL = (
    "`reajuste_coletivo_em_execucao`",
    "`diferenca_rescisao_complementar_pendente`",
    "`diferenca_funcionario_fora_da_folha`",
    "`retroactive_difference_informed`",
    "nunca as zere",
)
PENDING_DP = (
    "## Pendente até a DP decidir",
    "O cálculo da rescisão complementar dos desligados abrangidos (`sim`) ainda não existe",
    "Admitido no mesmo mês da data-base, mas depois do dia 1 e antes do dia da data-base",
)
# Regras da DP de 17/11/2026 (backend #346 e #349), na 2.8.0.
DP_RULES = (
    "O padrão da DP é `nao`",
    "ausente ou `pendente` valem `nao`",
    "`regra.salario_base_anterior_cents`",
    "`linhas.<matricula>.salario_base_anterior_cents`",
    "## Admitidos depois da data-base",
    "`motivo_sem_reajuste = admitido_apos_data_base_acima_do_salario_base`",
    "`salario_base_nao_declarado_para_admitido_apos_data_base`",
    "`salario_anterior_abaixo_do_salario_base`",
    "`exclusao_automatica = desligado_nao_abrangido_pelo_instrumento`",
    "`excluidas_automaticamente`",
    "`resumo_total.excluidas`",
    "o mês da vigência inteiro leva o salário novo",
    "(sem RRA)",
    "como `decimo_terceiro`",
    "meio centavo para cima, igual ao Domínio",
    "## Salário novo já registrado no cadastro",
    "`salario_novo_provavelmente_registrado: a_confirmar_na_aplicacao`",
    "`salario_novo_ja_registrado_no_cadastro:<fonte>`",
    "`fato_onboarding`, `alteracao_cadastral` ou `evento_vinculo`",
    "já paga no sistema de origem",
    "não desfaz o fato de onboarding",
)
# Textos do rascunho que contradizem o backend: BLOCKED pode deixar casos filhos sem
# efeito; a saida do recibo e uma lista; ha tres transportes, nao dois.
STALE = (
    "BLOCKED` significa que nada foi gravado",
    "`saida: exclusao`",
    "dois transportes",
    # Respondidos pela DP em 17/11/2026: nao podem voltar como pendencia ou codigo.
    "`diferenca_exige_particao_do_periodo`",
    "`diferenca_rra_exige_qualificacao`",
    "`abrangencia_de_desligados_pendente`",
    "- `proporcional_admissao`;",
    "arredondamento do percentual",
    "use `pendente` e pergunte à DP",
    # Respondidos pela DP em 18/11/2026 (2.9.1).
    "admitida na própria data-base",
    "Enquanto não houver resposta, deixe a linha pendente",
    "se o salário registrado na data-base é o próprio reajuste da CCT;",
)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def domain() -> str:
    return flat(InstructionsProvider().get("reajuste_salarial")["instructions"])


def test_collective_domain_is_served_with_the_new_contract() -> None:
    provider = InstructionsProvider()
    guide = provider.get("reajuste_salarial")
    assert guide["version"] == "2.9.5"
    assert guide["compatibility"]["mcp_contract_version"] == "2.9.5"
    assert guide["permissions"] == {
        "capabilities": ["consultar"],
        "processes": ["reajuste_salarial"],
    }
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.30"
    assert metadata["instructions_version"] == "2.9.5"
    assert metadata["mcp_contract_version"] == "2.9.5"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in (
        "2.0.0",
        "2.6.5",
        "2.7.0",
        "2.7.1",
        "2.8.0",
        "2.9.0",
        "2.9.1",
        "2.9.2",
        "2.9.3",
        "2.9.4",
        "2.9.5",
    ):
        assert provider.check_version(version, version)["compatible"] is True


def test_no_new_tool_so_no_connector_refresh_is_claimed() -> None:
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    # Nenhuma ferramenta nova entra na lista de compatibilidade da distribuicao.
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    assert InstructionsProvider().check_version()["refresh_tools_required"] is None
    text = domain()
    assert "Não há ferramenta nova" in text
    assert "não é preciso Refresh do conector" in text
    assert "atualizar o plugin instalado continua sendo outra etapa" in text
    for interface in INTERFACES:
        assert interface in text, interface


def test_domain_explains_flow_authority_exits_and_pending_decisions() -> None:
    text = domain()
    for required in (
        *STEPS,
        *AUTHORITY,
        *EXITS,
        *DECLARED,
        *REASONS,
        *PAYROLL,
        *PENDING_DP,
        *DP_RULES,
        "`dados_reajuste_salarial`",
        "`BLOCKED` (`salary_adjustment_lines_divergent`",
        "nenhum efeito foi gravado",
        "`casos_filhos_sem_efeito`",
        "`VALIDATING`",
        "`IN_PROGRESS`",
        "não peça nova decisão",
        "`tentativas_transitorias_esgotadas`",
        "`reajuste_retroativo_ja_lancado_na_competencia`",
        "nova referência do instrumento",
        "`enqueue_case_workflow`",
        "verba 19",
    ):
        assert required in text, required
    for stale in STALE:
        assert stale not in text, stale


def test_general_and_employee_change_point_to_the_collective_domain() -> None:
    provider = InstructionsProvider()
    general = flat(provider.get("geral")["instructions"])
    for required in (
        "## Reajuste coletivo retroativo e a folha X",
        "domínio `reajuste_salarial`",
        "`reajuste_coletivo_em_execucao`",
        "`diferenca_rescisao_complementar_pendente`",
        "nunca viram zero",
    ):
        assert required in general, required
    change = flat(provider.get("alteracao_cadastral")["instructions"])
    for required in (
        "## Reajuste retroativo vem do caso coletivo",
        "`retroactive_launch_not_available`",
        "`reserved_occurrence_ref`",
        "`salary_adjustment_child_requires_collective`",
        "`withdraw:true`",
        "`salary_adjustment_requires_employee_change_scope`",
    ):
        assert required in change, required


def test_plugin_guide_is_the_served_domain_text_and_is_reachable() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    body = guide[guide.index("## Quando usar e o que o contrato oferece") :]
    assert body in InstructionsProvider().get("reajuste_salarial")["instructions"]
    assert "não comprova publicação do backend" in flat(guide)
    for entry in (OPERATOR / "SKILL.md", WORKFLOWS, CAPACITIES):
        links = re.findall(r"\]\(([^)]+\.md)\)", entry.read_text(encoding="utf-8"))
        assert GUIDE.resolve() in {(entry.parent / link).resolve() for link in links}, entry


def test_plugin_mirrors_270_guidance() -> None:
    workflows = flat(WORKFLOWS.read_text(encoding="utf-8"))
    assert "## Reajuste coletivo com efeito retroativo" in workflows
    for required in (
        *INTERFACES[1:],
        "retomada pelo mesmo `request_ref` até `APPLIED` ou `PARTIAL`",
        'nunca diga "nada foi gravado" se já houve efeito',
        "`withdraw:true`",
        "`reajuste_coletivo_em_execucao`",
        "`diferenca_rescisao_complementar_pendente`",
    ):
        assert required in workflows, required
    capacities = flat(CAPACITIES.read_text(encoding="utf-8"))
    for required in (
        "## Reajuste coletivo com efeito retroativo",
        "Não há ferramenta nova",
        "`salary_adjustment_requires_employee_change_scope`",
        "nunca confere a fonte",
        "`sem_outras_verbas_dependentes_do_salario`",
        "até a DP decidir",
    ):
        assert required in capacities, required
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    for required in ("`reajuste_salarial` e `alteracao_cadastral`", "`PARTIAL`"):
        assert required in skill, required
    report = flat((SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"))
    for required in (
        "`salary_adjustment_lines_divergent`",
        "`salary_adjustment_line_key_changed` é problema a relatar",
        "não recomece o lote para contornar",
        "nunca diga que nada foi gravado se já houve efeito",
    ):
        assert required in report, required
