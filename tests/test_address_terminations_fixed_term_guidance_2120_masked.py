"""Entrega das orientações da 2.12.0 (endereço novo, férias pela rotina, intermitente,
confirmação de desligamento, prazo determinado e saldo de férias)."""

import hashlib
import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/loki-bootstrap"
OPERATOR = PLUGIN / "skills/operar-loki"
PROBLEMS = PLUGIN / "skills/registrar-problema-loki/SKILL.md"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
LIMIT = 65536
NEW_ADDRESS = "https://loki.izzicontabil.com.br/mcp"
OLD_ADDRESS = "loki.tominho.com"


def flat(value: str) -> str:
    return " ".join(value.split())


def read(domain: str) -> str:
    return flat((DOMAINS / f"{domain}.md").read_text(encoding="utf-8"))


def assert_all(body: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        assert flat(marker) in body, marker


def test_general_notice_keeps_the_2120_refresh_for_the_new_tools_and_the_new_address() -> None:
    guide = (DOMAINS / "geral.md").read_text(encoding="utf-8")
    notice = flat(guide[: guide.index("## Reaproveitar respostas e causas persistidas")])
    assert_all(
        notice,
        (
            "**Continua da 2.12.0:**",
            "`confirm_termination`",
            "retirada de saldo de férias",
            "`confirmar_rescisao` por `preparar_autorizacao`",
            "**Refresh do conector e conversa nova**",
            "**Endereço novo:**",
            NEW_ADDRESS,
            "devolve 503",
            "precisa ser recadastrado",
            "o resto não exige",
        ),
    )
    assert notice.index("**Vale quando o Loki for publicado:**") < notice.index(
        "**Continua da 2.12.0:**"
    )
    assert notice.index("**Continua da 2.12.0:**") < notice.index("**Continua da 2.11.0**")
    assert notice.index("**Continua da 2.11.0**") < notice.index("**Continua da 2.10.1:**")
    # A rotina passa a reiniciar férias; só o afastamento continua com pessoa.
    body = flat(guide)
    assert "retificação de data e afastamento continuam com pessoa" in body
    assert "férias e afastamento continuam com pessoa" not in body
    assert "`confirmar_rescisao`, `configurar_cliente`" in body


def test_live_texts_use_the_new_address_and_keep_only_dated_history() -> None:
    # Registro histórico datado que mantém o endereço antigo de propósito: o parágrafo
    # "Esta candidata orienta 100% HTTPS" da edição 0.4.6 (README e docs/MCP_UPDATES.md) e,
    # em docs/MCP_UPDATES.md, a frase que anuncia a troca de endereço desta edição.
    allowed = {"README.md": 1, "docs/MCP_UPDATES.md": 2}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".venv" in path.parts:
            continue
        if path.suffix not in {".md", ".json", ".py", ".toml", ".yml"}:
            continue
        if path.name == Path(__file__).name:
            continue
        relative = path.relative_to(ROOT).as_posix()
        count = path.read_text(encoding="utf-8", errors="ignore").count(OLD_ADDRESS)
        assert count == allowed.get(relative, 0), (relative, count)
    for domain in InstructionsProvider().domains():
        assert NEW_ADDRESS in InstructionsProvider().get(domain)["instructions"], domain


def test_company_name_rules_are_carried_by_admission_payroll_and_termination() -> None:
    admission = read("admissao")
    assert_all(
        admission,
        (
            "`razao_social_natureza_juridica_divergente`",
            "`razao_social_tipo_societario`",
            "**conferência dupla CNPJ + código da empresa.**",
            "**Caso sem código**",
            "só o CNPJ",
            "**conferência de novo na geração.**",
            "`identity_changed`",
        ),
    )
    for domain in ("folha_mensal", "rescisao"):
        assert_all(
            read(domain),
            ("`razao_social_natureza_juridica_divergente`", "`razao_social_tipo_societario`"),
        )


def test_vacation_restart_by_the_routine_and_its_limits() -> None:
    guide = read("ferias")
    assert_all(
        guide,
        (
            "## Insumo novo do cliente com o caso em revisão (rotina, 2.12.0)",
            "**férias passou a ter**",
            "Afastamento continua fora",
            "`client_input_restart_scope_refused`",
            "`aquisitivo_inicio`, `aquisitivo_fim`, `inicio` e `fim`",
            "`preparation_identity_changed`",
            "dispensa `corrigir_dados`",
            "`vacation_preparation_requires_human_correction`",
            "`record_vacation_schedule`",
            "`restart_requires_effect_reconciliation`",
            "`client_input_restart_requires_review_state`",
            "`client_input_request_ref_invalid`",
            "`client_input_restart_grant_origin_unrecorded`",
        ),
    )


def test_payroll_carries_intermittent_and_the_missing_credit_mapping_line() -> None:
    guide = read("folha_mensal")
    assert_all(
        guide,
        (
            "## Vínculo intermitente: `categoria_esocial` (2.12.0)",
            "**ainda não calcula contrato intermitente**",
            "`vinculo_intermitente_nao_suportado`",
            "`retirar_vinculo_intermitente_da_folha_mensal`",
            "**Declare em TODA competência.**",
            "só dentro do caso da competência",
            "## Consignado sem linha no mapa de verbas (2.12.0)",
            "`credito_trabalhador_mapeamento_pendente`",
            "`configurar_mapeamento_empresarial_do_credito`",
            "`loki.company-payroll-map-patch/1`",
            "`dominio_codes`",
            "`sem_efeito` em INSS, FGTS e IRRF",
        ),
    )


def test_termination_confirmation_and_its_compensation() -> None:
    guide = read("rescisao")
    assert_all(
        guide,
        (
            "## Confirmar o desligamento efetivo: `confirm_termination` (2.12.0)",
            "**Ferramenta nova: exige Refresh do conector e conversa nova**",
            "`confirmar_rescisao`",
            "`termination_confirmation_snapshot`",
            "`aguardando_revisao`",
            "`estado_nao_confirmavel`",
            "`confirmacao_desligamento_recusada`",
            "`desligamento_divergente_no_historico`",
            "`referencia_sem_efeito_vigente`",
            "`ajustar`",
            "`cancelamento_exige_confirmar_rescisao`",
            "Não atesta envio ao eSocial",
            "Nunca declare esses períodos na rescisão",
        ),
    )
    assert "`confirmar_rescisao`" in read("aprovacoes")


def test_admission_carries_the_fixed_term_contract() -> None:
    guide = read("admissao")
    assert_all(
        guide,
        (
            "## Contrato a prazo determinado que não é de experiência (2.12.0)",
            "`servico_transitorio`",
            "`atividade_empresarial_transitoria`",
            "`prazo_determinado_motivo_ausente`",
            "`prazo_determinado_motivo_descricao_ausente`",
            "`prazo_determinado_termino_antes_do_inicio`",
            "`prazo_determinado_excede_dois_anos`",
            "`prazo_determinado_segunda_prorrogacao`",
            "`prazo_determinado_prorrogacao_incoerente`",
            "`prazo_determinado_inicio_diferente_da_admissao`",
            "`prazo_determinado_conflita_com_experiencia`",
            "`texto_contrato_prazo_determinado_nao_homologado`",
            "`admission_date_rectification_fixed_term_limit`",
            "`generate_documents` e `run_prepared_case_workflow`",
            "`receive_case_data`",
        ),
    )


def test_onboarding_carries_the_vacation_balance_retirement() -> None:
    guide = read("alteracao_cadastral")
    assert_all(
        guide,
        (
            "## Retirar saldo de férias gravado pela carga histórica (2.12.0)",
            "**Ferramentas novas: exigem Refresh do conector e conversa nova**",
            "`preview_onboarding_vacation_balance_retirement`",
            "`retire_onboarding_vacation_balance`",
            "`target_fact_ids`",
            "`periods_after`",
            "`period_has_vacation_use`",
            "`period_schedule_pending`",
            "`onboarding_vacation_balance_qualifies_legacy`",
            "`requires_consumer_reconciliation`",
            "`revoked_onboarding_facts`",
            "Nunca declare na rescisão",
        ),
    )


def test_plugin_mirrors_the_release() -> None:
    workflows = flat((OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8"))
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    problems = flat(PROBLEMS.read_text(encoding="utf-8"))
    capacities = flat((OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8"))
    section = workflows[workflows.index("## 2.12.0:") :]
    assert_all(
        section,
        (
            "**Refresh do conector e conversa nova**",
            NEW_ADDRESS,
            "`confirm_termination`",
            "`categoria_esocial`",
            "`razao_social_natureza_juridica_divergente`",
            "`credito_trabalhador_mapeamento_pendente`",
            "`retire_onboarding_vacation_balance`",
        ),
    )
    assert "Na 2.12.0" in skill and "Refresh do conector e conversa nova" in skill
    assert "`prazo_determinado_*`" in problems and "`onboarding_vacation_balance_*`" in problems
    assert "admissão, rescisão e férias" in capacities
    assert "retificação de data e afastamento continuam com pessoa" in capacities
    for path in (
        PLUGIN / "SKILL.md",
        PLUGIN / "skills/loki-bootstrap/SKILL.md",
        OPERATOR / "SKILL.md",
        PLUGIN / "README.md",
    ):
        assert "recadastrado nele" in flat(path.read_text(encoding="utf-8")), path


def test_domain_hashes_and_size_limit() -> None:
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name
