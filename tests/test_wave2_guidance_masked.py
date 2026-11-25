"""Entrega das orientações da 2.8.0 (Onda 2); nao mede obediencia da harness.

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
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"

REFRESH_FLOWS = (
    "`restoration_declaration`",
    '`motivo: "troca_de_codigo_dominio"`',
    "`preview_onboarding_termination_revocation`",
    "`revoke_onboarding_termination`",
    "`revoga_com_rescisao_aberta`",
)
PAYROLL = (
    "## Janela de publicação e a fila de folha",
    "**Na janela que publica esta versão**",
    "**A partir das janelas seguintes**, não é mais preciso esvaziar a fila",
    "`case_job_build_repinned`",
    "`job_build_changed`",
    "`job_fingerprint_snapshot_changed`",
    "Não reenfileire um job que ainda esteja `queued` ou `running`",
    "Folhas de **empresas diferentes** rodam ao mesmo tempo no worker, no máximo uma por empresa",
    "gravar em casos de **outras** empresas também é seguro",
    "Consultas Dataprev mensais podem demorar mais",
    "## Contexto do mês por pessoa e hashes dos lançamentos",
    "`payroll_context.available=false`",
    "`context_current=true`",
    "`payroll_context_changed_since_calculation`",
    "`lancamentos_conciliados`",
    "`lancamento_hash`",
    "não calcule o hash você mesma",
    "`payroll_effective_launches_not_read`",
    "`payroll_effective_launch_codes_repeated`",
    "`payroll_context_qualification_stale`",
    "`populacao_desatualizada_por_revogacao`",
    "`vinculo_nao_identificado_na_competencia`",
)
THIRTEENTH = (
    "**`final_average` é a média mensal integral do Domínio.**",
    "Nunca envie uma média já proporcional aos avos",
    "`média × avos ÷ 12`",
    "## 13º com média importada que já estava em revisão",
    "registrar a decisão `ajustar`",
    "2. `calculate_case`;",
    "fazer nova conferência do pacote",
    "## Reiniciar um 13º",
    'mode:"replace_process_inputs"',
    "não exige a capacidade `corrigir_dados`",
    "`preparation_identity_changed`",
    "`restart_requires_adjustable_state`",
    "`historical_thirteenth_coverage_incomplete`",
    "`missing_intervals`",
)
COVERAGE = (
    "(estado `historical-state-v2`)",
    "O estado nunca certifica dia posterior ao corte",
    "Não é mais preciso terminar exatamente no corte",
    "`selection_matches_current_state: false`",
    "**Não reselecione se a seleção v1 for consumível.**",
    "`historical_state_stale`",
)
TERMINATION_MAP = (
    "## Acrescentar ou trocar uma parcela no mapa de rescisão da empresa",
    "`termination_map_patch_transport`",
    '"schema_version": "loki.company-termination-map-patch/1"',
    "`forma_incompativel`",
    "`termination_patch_selector_missing`",
    "`termination_patch_embedded_map_required`",
    "`termination_patch_parcel_exists`: use `replace`",
    "`termination_patch_parcel_missing`: use `add`",
    "`cliente_config_versao_desatualizada`",
    "Não presuma incidência",
)
REGISTRY = (
    "## Restaurar uma matrícula sobrescrita",
    "Não restaure por iniciativa própria",
    "`expected_current_matricula: <valor atual literal>`",
    "`restoration_declaration: {human_message, message_reference, reason}`",
    "`restauracao_matricula_valor_legado_use_reparo`",
    "`repair_employee_identifier_namespace`",
    "`restauracao_matricula_exige_conciliacao_de_consumidores`",
    "`vinculo_matricula_introduzida_pelo_caso`",
    "## Troca de código Domínio do mesmo contrato",
    "`message_reference` com prefixo `CX-` é obrigatória",
    "`troca_de_codigo_dominio_exige_message_reference_cx`",
    "`troca_de_codigo_dominio_fonte_do_codigo_anterior`",
    "`closed_consumers_without_closed_history`",
    "## Revogar desligamento gravado pelo onboarding",
    "Declaração no chat não basta como fonte",
    "`projected_state_after.desligado_em: null`",
    "`onboarding_termination_revocation_open_termination_case`",
    "`same_cpf_active_employee_ids`",
    "`onboarding_termination_fact_revoked`",
    "`populacao_desatualizada_por_revogacao`",
    "aparecem só depois do Refresh do conector e de uma conversa nova",
)
# Textos da 2.7.1 que ficaram contraditorios com a Onda 2.
STALE = {
    "ferias": ("Por enquanto, uma cobertura que termina **depois**",),
    "decimo_terceiro": ("de terminar no corte ou antes, emendada até ele",),
    "geral": ("registre o\n  problema com `registrar_problema` e avise a operadora",),
}


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    return " ".join(value.split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def test_versions_follow_the_new_contract_minor() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.35"
    assert metadata["instructions_version"] == "2.10.0"
    assert metadata["mcp_contract_version"] == "2.10.0"
    assert metadata["recommended_plugin_version"] == "2.10.0"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in (
        "2.0.0",
        "2.7.1",
        "2.8.0",
        "2.9.0",
        "2.9.1",
        "2.9.2",
        "2.9.3",
        "2.9.4",
        "2.9.5",
        "2.9.6",
        "2.9.7",
        "2.9.8",
        "2.9.9",
        "2.10.0",
    ):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.10.0", "2.10.1")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.10.0", path.name
        assert data["compatibility"]["mcp_contract_version"] == "2.10.0", path.name
    for path in DOMAINS.glob("*.md"):
        assert len(path.read_bytes()) <= 65536, path.name


def test_general_keeps_the_28_refresh_reminder() -> None:
    # O aviso da 2.9.3 substitui o da 2.9.2, mas lembra os fluxos da 2.8.0 que exigem Refresh.
    guide = text("geral")
    notice = guide[: guide.index("## Reaproveitar respostas e causas persistidas")]
    assert_all(
        notice,
        (
            "**Continua da 2.8.0**",
            "`restoration_declaration`",
            "`preview_onboarding_termination_revocation`",
            "`revoke_onboarding_termination`",
            'receive_case_data(case_id="@connector")',
        ),
    )


def test_payroll_thirteenth_coverage_and_termination_domains() -> None:
    assert_all(text("folha_mensal"), PAYROLL)
    assert_all(text("decimo_terceiro"), THIRTEENTH)
    assert_all(text("ferias"), COVERAGE)
    assert_all(text("afastamento"), ("`historical-state-v2`",))
    assert_all(text("rescisao"), (*TERMINATION_MAP, "`revoga_com_rescisao_aberta: true`"))


def test_registry_flows_live_in_employee_change_and_are_pointed_to() -> None:
    assert_all(text("alteracao_cadastral"), REGISTRY)
    for domain in ("geral", "admissao", "alteracao_cadastral"):
        assert_all(
            text(domain),
            ("restauração ou a troca auditada do código Domínio", "`registrar_problema`"),
        )


def test_contradicted_271_text_is_gone() -> None:
    for domain, stale in STALE.items():
        body = flat(text(domain))
        for item in stale:
            assert flat(item) not in body, (domain, item)


def test_plugin_mirrors_wave2_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    for section in (
        "## Onda 2: folha, 13º, rescisão, reajuste e cadastro",
        "## Cadastro: matrícula, código Domínio e desligamento do onboarding",
    ):
        assert section in workflows, section
    assert_all(
        workflows,
        (
            "**Não exige nada da operadora:**",
            "**Exige Refresh do conector e conversa nova (`alteracao_cadastral`):**",
            "`case_job_build_repinned`",
            "`excluidas_automaticamente`",
            "`troca_de_codigo_dominio_exige_message_reference_cx`",
            "depois dele (estado `historical-state-v2`)",
            *REFRESH_FLOWS,
        ),
    )
    assert "terminar no corte ou antes, emendada desde a admissão" not in flat(workflows)
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert_all(
        capacities,
        (
            "## Onda 2: dossiê da folha, rescisão e cadastro",
            "Nada disso exige Refresh",
            "nunca vai proporcional aos avos",
            "`reajuste_proporcional_nao_praticado`",
            *REFRESH_FLOWS,
        ),
    )
    skill = (OPERATOR / "SKILL.md").read_text(encoding="utf-8")
    assert_all(
        skill,
        (
            "“Onda 2: folha, 13º, rescisão, reajuste e cadastro”",
            "peça o Refresh só quando a operadora for usar um deles",
        ),
    )
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "`payroll_effective_launch_codes_repeated` é problema a relatar",
            "`restauracao_matricula_legado_nao_reparavel`",
            "`onboarding_termination_revocation_effect_unresolved`",
            "Ferramenta de revogação ausente do catálogo antes do Refresh também não é defeito",
            "sem a matrícula, o CPF ou o nome",
        ),
    )
