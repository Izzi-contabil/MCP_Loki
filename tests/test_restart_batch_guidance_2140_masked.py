"""Entrega das orientações da 2.14.0 (reinício autorizado em lote por correção, ADR-041)."""

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
ROUTINE_TITLE = "## Reinício em lote autorizado por correção (rotina, 2.14.0)"


def flat(value: str) -> str:
    return " ".join(value.split())


def read(domain: str) -> str:
    return flat((DOMAINS / f"{domain}.md").read_text(encoding="utf-8"))


def assert_all(body: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        assert flat(marker) in body, marker


def routine_section(domain: str) -> str:
    guide = read(domain)
    return guide[guide.index(flat(ROUTINE_TITLE)) :]


def test_general_notice_leads_with_the_2140_refresh_only_for_the_owner() -> None:
    guide = (DOMAINS / "geral.md").read_text(encoding="utf-8")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.14.0)")
    assert "## O que mudou nesta versão (2.13.0)" not in guide
    notice = flat(guide[: guide.index("## Reaproveitar respostas e causas persistidas")])
    assert_all(
        notice,
        (
            "**Exige ação da operadora (2.14.0):** atualizar o plugin instalado",
            "só para quem autoriza reinício em lote",
            "**Refresh do conector e conversa nova**",
            "variante `restart_batch` de `preparar_autorizacao`",
            "a rotina não precisa",
            "o reinício em lote já está publicado",
            "**Continua da 2.13.0:**",
            "sem ferramenta nova nem Refresh do conector",
            "a categoria eSocial (seções 2.13.0) já está publicada",
            "Releia `get_process_contract` de `alteracao_cadastral` antes de declará-la",
        ),
    )
    # O reinício em lote já está publicado: o aviso não o condiciona à publicação futura.
    assert "reinício em lote (seções 2.14.0) quando" not in notice
    order = (
        "**Exige ação da operadora (2.14.0):**",
        "**Vale quando o Loki for publicado:**",
        "**Continua da 2.13.0:**",
        "**Continua da 2.12.0:**",
        "**Continua da 2.11.0**",
        "**Continua da 2.10.1:**",
        "**Continua da 2.10.0**",
        "**Continua da 2.9.9**",
        "**Continua da 2.9.8:**",
    )
    positions = [notice.index(marker) for marker in order]
    assert positions == sorted(positions)
    assert len((DOMAINS / "geral.md").read_bytes()) <= LIMIT


def test_approvals_carry_the_owner_side_with_the_published_state() -> None:
    guide = read("aprovacoes")
    assert_all(
        guide,
        (
            "## Reinício autorizado em lote por correção: `restart_batch` (2.14.0, ADR-041)",
            "O backend já está publicado (schema 0069)",
            "**Refresh do conector e conversa nova** só na conta de quem autoriza",
            "a rotina não precisa de Refresh",
            "Não é ferramenta nova nem capacidade nova",
            "uma lista **fechada** de casos de **uma** empresa",
            "`atualizar_por_insumo_do_cliente` não serve para isso",
            "`somente_proprietario_autoriza_reinicio`",
            "`reinicio_exige_conta_de_rotina_ativa`",
            "`versao_desatualizada`",
            "`correction_restart_requires_routine`",
            "`preparation.correction_restart`",
            '"loki" | "harness"',
            "support_candidate_id (só `loki`)",
            "`publication_receipt`",
            "`manifest_hash`",
            "case_ids (1 a 100, sem repetir)",
            "(1 a 72, padrão 72)",
            "daily_limit (1 a 200, padrão 50)",
            "vale 15 minutos",
        ),
    )
    assert_all(
        guide,
        (
            "Só `restart_batch_refused` e o `BUSY` são resposta tipada",
            "`somente_proprietario_autoriza_reinicio`",
            "`restart_authorization_not_found`, `restart_authorization_already_revoked`",
            "chegam como erro de ferramenta",
        ),
    )
    # Recusa tipada: lista por caso, inclusive `case_snapshot_changed` no apply, e `case_id` nulo.
    assert_all(
        guide,
        (
            '"restart_batch_refused"',
            "refusals: [{case_id, code}]",
            "refusal_count",
            "`case_not_found`",
            "`case_other_company`",
            "`case_process_not_supported`",
            "`case_is_simulation`",
            "`case_retired_execution_context`",
            "`case_not_in_review`",
            "`routine_scope_missing`",
            "`case_has_effects`",
            "`case_already_authorized`",
            "só no apply, `case_snapshot_changed`",
            "nada foi concedido, prepare de novo",
            "Com `case_id` nulo:",
            "`support_candidate_not_approved_and_published`",
            "quando outra concessão ganha a corrida",
        ),
    )
    # Erros de ferramenta do apply, com a chave real de cada um.
    assert_all(
        guide,
        (
            "Erros de ferramenta, nada gravado:",
            "`confirmacao_humana_obrigatoria` (mensagem vazia ou com mais de 4000 caracteres",
            "na concessão e na revogação",
            "`alteracao_invalida`",
            "`versao_desatualizada_ou_alteracao_expirada` (a revisão da rotina mudou depois da "
            "prévia, ou passaram os 15 minutos",
            "`restart_batch_message_requires_code`",
            "`CL-1` não casa em `CL-12`",
            "`authorization_change_busy`",
            "`retry_after_seconds`",
            "`authorization_id` (`rst-` e 32 hex)",
            "limite diário por autorização (até 200)",
            "por conta da rotina (200, ajustável no servidor)",
            "**consumo único por caso**",
        ),
    )


def test_revocation_is_bound_to_the_authorization_and_reauthorizing_needs_it() -> None:
    guide = read("aprovacoes")
    assert_all(
        guide,
        (
            '`action: "revoke"`',
            "fecha **todos** os itens ainda abertos (`items_closed`)",
            "A mensagem não precisa nomear o `CL-N`",
            "A revogação não confere a revisão da rotina",
            "`expected_revision` segue como argumento, mas não é comparado",
            "vale com a rotina suspensa",
            "`account_id` tem de ser a rotina da própria autorização",
            "`restart_authorization_not_found`",
            "`restart_authorization_already_revoked`",
            "**Autorizar de novo exige revogar antes**",
            "`restart_batch_refused` e `case_already_authorized`",
            "A proprietária revoga a autorização inteira e depois autoriza de novo só os casos "
            "que ainda valem",
            "Autorização revogada ou vencida, e item já consumido, não bloqueiam a concessão nova",
        ),
    )
    # A conduta é por código, não um genérico "autorize de novo".
    assert "a proprietária autoriza de novo)" not in guide
    assert_all(
        guide,
        (
            "`correction_restart_snapshot_mismatch`: a rotina reenvia com o `expected_snapshot` "
            "do recibo da concessão (não o atual do caso)",
            "`correction_restart_message_requires_code`: a rotina corrige a mensagem",
            "`correction_restart_authorization_daily_limit`, "
            "`correction_restart_account_daily_limit`: esperar o dia seguinte",
            "`correction_restart_authorization_revoked` (itens fechados pela revogação)",
            "`correction_restart_authorization_expired` (vencida: o item não vale mais e não "
            "bloqueia nova concessão): autorize de novo, sem nada a revogar",
            "`correction_restart_requires_review_state`: o caso saiu de `aguardando_revisao`",
            "o item só volta a valer se o snapshot voltar a ser o autorizado",
            "do contrário vem `case_snapshot_changed`",
            "revogue a autorização inteira e autorize de novo os casos que ainda valem",
            "`correction_restart_candidate_not_published`",
            "`correction_restart_grantor_not_owner`",
            "`restart_requires_effect_reconciliation`",
            "o caso sai do reinício em lote; uma autorização nova também seria recusada",
            "`case_has_effects`",
            "`case_simulation_refused` com `reason` `simulation_context_invalid`",
            "`correction_restart_case_mismatch`",
            "`lifecycle_authorization_revoked`",
            "`caso_inexistente_ou_nao_autorizado`",
            "só aparece se a rotina tem escopo nas duas empresas",
        ),
    )


def test_audit_limits_and_the_publication_window_come_from_the_adr() -> None:
    guide = read("aprovacoes")
    assert_all(
        guide,
        (
            "`operational_case_restart`",
            "`authority=correction_restart_authorization`",
            "Uma recusa de execução não deixa linha de auditoria",
            "a expiração só é gravada quando o mesmo caso recebe nova concessão",
            "item vencido que ninguém reautoriza fica aberto, recusado por `expires_at`",
            "**Não rode a rotina de correção durante uma janela de publicação do executor "
            "anterior**",
            "falha fechada",
        ),
    )
    assert "Casos `aberto` e `em_preparacao` a rotina recalcula sem este ato (ADR-041)" in guide


def test_routine_scripts_are_self_sufficient_and_do_not_depend_on_approvals() -> None:
    for domain in ("folha_mensal", "admissao", "rescisao"):
        section = routine_section(domain)
        assert_all(
            section,
            (
                "`authorization_id` (`rst-` e 32 hex)",
                '"loki.case-restart-authorized/1"',
                "`human_message` que nomeia o `CL-N`",
                "requires_case_data",
                "`correction_restart_snapshot_mismatch`",
                "`correction_restart_message_requires_code`",
                "`authorization_change_busy`",
                "`case_snapshot_changed`",
                "`restart_requires_effect_reconciliation`",
                "`case_simulation_refused`",
                "`caso_inexistente_ou_nao_autorizado`",
                "pare e avise a proprietária",
            ),
        )
        # A rotina não lê `aprovacoes` (exige `decidir_chat`): o texto dela não a manda ler.
        assert "códigos em `aprovacoes`" not in section
    assert_all(routine_section("folha_mensal"), ("`enqueue_case_workflow`",))
    for domain in ("admissao", "rescisao"):
        section = routine_section(domain)
        assert_all(
            section,
            (
                "`run_prepared_case_workflow`",
                "sem `replace_process_inputs`",
                "`replayed: true`",
                "Não rode a rotina de correção durante uma janela de publicação",
                "`correction_restart_authorization_daily_limit`",
                "`correction_restart_account_daily_limit`",
                "`lifecycle_authorization_revoked`",
            ),
        )
    payroll = read("folha_mensal")
    assert "só a proprietária abre a exceção (seção da 2.14.0)" in payroll
    assert "(#410, mesclada)" in payroll


def test_category_sections_of_2130_stay_untouched_by_the_restart_text() -> None:
    for domain in ("alteracao_cadastral", "ferias", "decimo_terceiro"):
        guide = read(domain)
        for token in ("restart" + "_batch", "correction" + "_restart", "case-restart"):
            assert token not in guide, (domain, token)


def test_plugin_mirrors_the_release() -> None:
    workflows = flat((OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8"))
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    problems = flat(PROBLEMS.read_text(encoding="utf-8"))
    capacities = flat((OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8"))
    section = workflows[workflows.index("## 2.14.0:") :]
    assert_all(
        section,
        (
            "**Não há ferramenta nova nem capacidade nova.**",
            "O backend já está publicado",
            "**Refresh do conector e conversa nova** só na conta de quem autoriza",
            "a rotina não precisa de Refresh",
            "O `tools/list` mudou só nesse ponto",
            "`restart_batch_message_requires_code`",
            "`confirmacao_humana_obrigatoria`",
            "`restart_batch_refused` com `refusals[].code`",
            "inclusive `case_snapshot_changed` no apply",
            "não confere a revisão da rotina",
            "`restart_authorization_not_found`",
            "só recebe nova concessão depois que a proprietária revoga a autorização inteira",
            "`case_already_authorized`",
            "`loki.case-restart-authorized/1`",
            "`correction_restart_requires_routine`",
            "`correction_restart_snapshot_mismatch`",
            "Não rode a rotina durante uma janela de publicação do executor anterior",
        ),
    )
    assert (
        "Na 2.14.0" in skill and "Refresh do conector e conversa nova só na conta de quem" in skill
    )
    assert "revoga a autorização inteira antes" in skill
    assert "`restart_batch`, 2.14.0" in capacities
    assert "só `consultar` e `operar_casos`" in capacities
    for code in (
        "restart_batch_refused",
        "restart_batch_message_requires_code",
        "confirmacao_humana_obrigatoria",
        "versao_desatualizada_ou_alteracao_expirada",
        "correction_restart_*",
        "case_snapshot_changed",
        "restart_requires_effect_reconciliation",
        "case_already_authorized",
        "caso_inexistente_ou_nao_autorizado",
    ):
        assert code in problems, code
    # A conduta por código, não um "peça nova autorização" para tudo.
    assert "peça nova autorização à proprietária" not in problems
    assert "revogue a autorização inteira" in problems
    assert "esperar o dia seguinte" in problems


def test_release_versions_hashes_and_current_history() -> None:
    metadata = InstructionsProvider().metadata()
    assert metadata["provider_version"] == "0.4.40"
    assert metadata["instructions_version"] == "2.14.0"
    assert metadata["mcp_contract_version"] == "2.14.0"
    assert metadata["recommended_plugin_version"] == "2.14.0"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "2.14.0"
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["updated_at"] == "2026-11-28"
    for category, prefix in (
        ("backend", "Contrato2.14.0"),
        ("instructions", "Instruções2.14.0"),
        ("plugin", "Plugin2.14.0"),
    ):
        entries = release["changes"][category]
        assert len(entries) == 2 and "docs/MCP_UPDATES.md" in entries[0], category
        assert entries[1].startswith(prefix), category
    backend = release["changes"]["backend"][1]
    assert "já publicado" in backend and "restart_batch" in backend
    assert "só em preparar_autorizacao" in backend
    assert "ainda fora de" not in json.dumps(release["changes"])
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name
    updates = (ROOT / "docs/MCP_UPDATES.md").read_text(encoding="utf-8")
    assert updates.startswith("# Atualizações MCP Loki — contrato 2.14.0")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert readme.startswith("# MCP Loki — contrato operacional 2.14.0")
    assert "ainda fora de" not in readme and "ainda fora de" not in updates
