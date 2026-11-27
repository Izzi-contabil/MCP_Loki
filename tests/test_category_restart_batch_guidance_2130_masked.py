"""Entrega das orientações da 2.13.0 (categoria eSocial na folha e no cadastro, recusa de
caso de quem não é empregado e reinício autorizado em lote por correção)."""

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
PROCESSES = ("admissao", "rescisao", "ferias", "decimo_terceiro")


def flat(value: str) -> str:
    return " ".join(value.split())


def read(domain: str) -> str:
    return flat((DOMAINS / f"{domain}.md").read_text(encoding="utf-8"))


def assert_all(body: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        assert flat(marker) in body, marker


def test_general_notice_leads_with_the_2130_refresh_and_keeps_the_2120_one() -> None:
    guide = (DOMAINS / "geral.md").read_text(encoding="utf-8")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.13.0)")
    assert "## O que mudou nesta versão (2.12.0)" not in guide
    notice = flat(guide[: guide.index("## Reaproveitar respostas e causas persistidas")])
    assert_all(
        notice,
        (
            "**Exige ação da operadora (2.13.0):** atualizar o plugin instalado",
            "**Refresh do conector e conversa nova**",
            "variante `restart_batch` de `preparar_autorizacao`",
            "sem ferramenta nova",
            "`categoria_sem_regime_clt`",
        ),
    )
    order = (
        "**Exige ação da operadora (2.13.0):**",
        "**Vale quando o Loki for publicado:**",
        "**Continua da 2.12.0:**",
        "**Continua da 2.11.0**",
        "**Continua da 2.10.1:**",
        "**Continua da 2.10.0**",
        "**Continua da 2.9.9**",
        "**Continua da 2.9.8:**",
    )
    positions = [notice.index(marker) for marker in order]
    assert positions == sorted(positions)
    # A regra do consignado não pode ficar mais larga do que a 2.12.0 a escreveu.
    assert (
        "Folha com pessoa que confirma 2 ou mais contratos de consignado no mês "
        "(`-worker-credit-allocation-v1`)"
    ) in notice
    assert len((DOMAINS / "geral.md").read_bytes()) <= LIMIT


def test_payroll_carries_non_employee_category_and_the_cadastre_rules() -> None:
    guide = read("folha_mensal")
    assert_all(
        guide,
        (
            "## Categoria eSocial que não é de empregado e categoria no cadastro (2.13.0)",
            "**Categoria que não começa com `1`**",
            "723 sócio com pró-labore, 901 estagiário",
            "`vinculo_nao_suportado`",
            "`categoria_esocial_nao_suportada`",
            "`retirar_categoria_nao_clt_da_folha_mensal`",
            "**não calcula pró-labore nem bolsa de estágio**",
            "O `111` segue com o código próprio",
            "**Memória dentro do caso.**",
            "só dentro do caso da competência",
            "O cadastro vence a memória",
            '`kind: "parametrizacao"`',
            '`data: {"categoria_esocial": "723"}`',
            "`workers[].existing_employee_id`",
            "`import_documentary_profile`",
            "Folha sem o campo usa a do cadastro",
            "`categoria_esocial_divergente`",
            "`alinhar_categoria_esocial_folha_e_cadastro`",
            "Quem não é empregado exige só `dependentes_irrf`",
            "sindicato, escala, VT e salário-família",
            "ANTES de rodar a folha",
        ),
    )
    # A seção do intermitente da 2.12.0 não afirma mais que nenhum cadastro guarda a categoria.
    assert "nenhum cadastro guarda a categoria" not in guide
    assert "não recebem o fato de categoria hoje" not in guide
    assert "**Declare em TODA competência.**" in guide
    # O reinício em lote não é mais descrito como inexistente sem a exceção da proprietária.
    assert "Só a proprietária abre a exceção" in guide


def test_cadastre_domain_says_how_to_declare_the_category() -> None:
    guide = read("alteracao_cadastral")
    assert_all(
        guide,
        (
            "## Categoria eSocial do vínculo no cadastro (2.13.0)",
            "`employee_parameters.data_schema`",
            "`^[0-9]{3}$`",
            '`kind: "parametrizacao"`',
            "`existing_employee_id`",
            "`import_documentary_profile`",
            "Valor que não tenha 3 dígitos é recusado",
            "`replaces_fact_id`",
            "**antes** de rodar folha",
            "`categoria_esocial_divergente`",
            "o cadastro vence a memória do caso",
            "exige só os dependentes de IRRF",
            "`categoria_sem_regime_clt`",
        ),
    )


def test_other_processes_refuse_the_case_with_the_exact_code_and_its_limits() -> None:
    for domain in PROCESSES:
        guide = read(domain)
        assert_all(
            guide,
            (
                "## Categoria eSocial que não é de empregado no cadastro (2.13.0)",
                "`create_case` recusa antes de gravar",
                "`categoria_sem_regime_clt`",
                "`HUMAN_DECISION`",
                "O caso não é criado.",
                "vale só na criação",
                "`vinculo_nao_clt_*`",
                "competência do próprio processo",
                "o mês corrente (America/Sao_Paulo)",
                "Sem vínculo conhecido",
                "o caso segue",
                "`folha_mensal` e `alteracao_cadastral`",
            ),
        )
    termination = read("rescisao")
    assert_all(
        termination,
        (
            "A simulação de rescisão recusa pela mesma regra",
            "`code` `case_simulation_refused`",
            "`reason` `categoria_sem_regime_clt`",
            "na simulação sem caso de origem, a do desligamento hipotético",
        ),
    )


def test_approvals_carry_the_owner_side_of_the_restart_batch() -> None:
    guide = read("aprovacoes")
    assert_all(
        guide,
        (
            "## Reinício autorizado em lote por correção: `restart_batch` (2.13.0, ADR-041)",
            "**exige Refresh do conector e conversa nova**",
            "não é ferramenta nova nem capacidade nova",
            "uma lista **fechada** de casos de **uma** empresa",
            "`aguardando_revisao`",
            "`somente_proprietario_autoriza_reinicio`",
            "`reinicio_exige_conta_de_rotina_ativa`",
            "`versao_desatualizada`",
            "`correction_restart_requires_routine`",
            'correction_kind:\n            "loki" | "harness"',
            "support_candidate_id (só `loki`)",
            "`publication_receipt`",
            "`manifest_hash`",
            "case_ids (1 a 100",
            "ttl_hours (1 a 72, padrão 72)",
            "daily_limit (1 a 200, padrão 50)",
            "vale 15 minutos",
            "`restart_batch_refused`",
            "`case_not_in_review`",
            "`routine_scope_missing`",
            "`case_has_effects`",
            "`case_already_authorized`",
            "`support_candidate_not_approved_and_published`",
            "**nomeia o `CL-N`**",
            "`restart_batch_message_requires_code`",
            "`case_snapshot_changed`",
            "`authorization_change_busy`",
            "`authorization_id` (`rst-` e 32 hex)",
            "limite diário por autorização (até 200)",
            "por conta da rotina (200, ajustável no servidor)",
            "**consumo único por caso**",
            "`correction_restart_grantor_not_owner`",
            '`action: "revoke"`',
            "`restart_authorization_already_revoked`",
            "`correction_restart_snapshot_mismatch`",
            "`correction_restart_wrong_account`",
            "`correction_restart_item_not_found`",
            "`correction_restart_requires_review_state`",
            "`correction_restart_authorization_expired`",
            "`correction_restart_account_daily_limit`",
            "`restart_requires_effect_reconciliation`",
            "`simulation_context_invalid`",
            "`caso_inexistente_ou_nao_autorizado`",
            "só aparece se a rotina tem escopo nas duas empresas",
            "`operational_case_restart`",
            "`authority=correction_restart_authorization`",
        ),
    )


def test_routine_scripts_carry_the_envelope_in_payroll_admission_and_termination() -> None:
    for domain in ("folha_mensal", "admissao", "rescisao"):
        guide = read(domain)
        assert_all(
            guide,
            (
                "## Reinício em lote autorizado por correção (rotina, 2.13.0)",
                "`authorization_id` (`rst-` e 32 hex)",
                "`atualizar_por_insumo_do_cliente` nem é exigida nem basta",
                '"loki.case-restart-authorized/1"',
                "`expected_snapshot` igual ao repassado",
                "`human_message` que nomeia o `CL-N`",
                "`requires_case_data`",
                "`replayed: true`",
                "Toda recusa deixa o item sem consumir",
                "códigos em `aprovacoes`",
            ),
        )
    assert "`enqueue_case_workflow`" in read("folha_mensal")
    assert "`run_prepared_case_workflow`" in read("admissao")
    assert "sem `replace_process_inputs`" in read("admissao")


def test_plugin_mirrors_the_release() -> None:
    workflows = flat((OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8"))
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    problems = flat(PROBLEMS.read_text(encoding="utf-8"))
    capacities = flat((OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8"))
    section = workflows[workflows.index("## 2.13.0:") :]
    assert_all(
        section,
        (
            "**Não há ferramenta nova.**",
            "**Refresh do conector e conversa nova**",
            "`restart_batch`",
            "`categoria_esocial_nao_suportada`",
            "`categoria_esocial_divergente`",
            "`categoria_sem_regime_clt`",
            "`case_simulation_refused`",
            "`loki.case-restart-authorized/1`",
            "`correction_restart_requires_routine`",
        ),
    )
    assert "Na 2.13.0" in skill and "Sem ferramenta nova" in skill
    for code in (
        "categoria_esocial_nao_suportada",
        "categoria_sem_regime_clt",
        "restart_batch_refused",
        "restart_batch_message_requires_code",
        "correction_restart_*",
    ):
        assert code in problems, code
    assert "`restart_batch`, 2.13.0" in capacities
    assert "só `consultar` e `operar_casos`" in capacities


def test_release_versions_hashes_and_current_history() -> None:
    metadata = InstructionsProvider().metadata()
    assert metadata["provider_version"] == "0.4.39"
    assert metadata["instructions_version"] == "2.13.0"
    assert metadata["mcp_contract_version"] == "2.13.0"
    assert metadata["recommended_plugin_version"] == "2.13.0"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "2.13.0"
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    for category, prefix in (
        ("backend", "Contrato2.13.0"),
        ("instructions", "Instruções2.13.0"),
        ("plugin", "Plugin2.13.0"),
    ):
        entries = release["changes"][category]
        assert len(entries) == 2 and "docs/MCP_UPDATES.md" in entries[0], category
        assert entries[1].startswith(prefix), category
    assert "só valem depois da publicação do backend" in release["changes"]["backend"][1]
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name
