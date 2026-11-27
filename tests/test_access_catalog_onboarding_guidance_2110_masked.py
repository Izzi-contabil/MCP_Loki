"""Entrega das orientações da 2.11.0 (acessos, catálogo de rubricas v2 e onboarding)."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "plugins/loki-bootstrap/skills/operar-loki"
PROBLEMS = ROOT / "plugins/loki-bootstrap/skills/registrar-problema-loki/SKILL.md"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
LIMIT = 65536


def flat(value: str) -> str:
    return " ".join(value.split())


def read(domain: str) -> str:
    return flat((DOMAINS / f"{domain}.md").read_text(encoding="utf-8"))


def test_general_notice_keeps_the_2110_line_in_order() -> None:
    guide = (DOMAINS / "geral.md").read_text(encoding="utf-8")
    notice = flat(guide[: guide.index("## Reaproveitar respostas e causas persistidas")])
    assert "**Continua da 2.11.0**, sem Refresh" in notice
    assert notice.index("**Continua da 2.11.0**") < notice.index("**Continua da 2.10.1:**")
    assert notice.index("**Continua da 2.10.1:**") < notice.index("**Continua da 2.10.0**")


def test_approvals_carry_addition_to_existing_company_and_removal() -> None:
    guide = read("aprovacoes")
    for marker in (
        "## Acrescentar e remover concessões em conta grande (2.11.0, backend #424)",
        "`prepare_authorization_addition` aceita empresa que a conta já tem",
        "`atualizar_por_insumo_do_cliente`",
        "`added_grants`",
        "`extends_existing_company`",
        "`added_companies`",
        "`extended_companies`",
        "`authorization_addition_nothing_to_add`",
        "`authorization_addition_duplicate_company`",
        "`prepare_authorization_removal`",
        "`removed_grants`",
        "`removed_companies`",
        "`reduced_companies`",
        "`authorization_removal_nothing_to_remove`",
        "`authorization_removal_duplicate_company`",
        "`concessao_exige_consultar`",
        "`proprietario_protegido`",
        "aceita no máximo 500 concessões",
        "`authorization_change_busy`",
        "repita a **mesma** chamada",
    ):
        assert marker in guide, marker


def test_termination_carries_catalog_v2_and_index_capabilities() -> None:
    guide = read("rescisao")
    for marker in (
        "`loki.termination-rubric-catalog/2`",
        "`parcel_table`",
        "`mapping_table`",
        "`tax_mapping_table`",
        "`caixa_table`",
        "`groups[]`",
        "`reconstruction`",
        "`resolved_map_hash`",
        "`contract_tool`",
        "`contract_hash`",
        "releia o contrato",
    ):
        assert marker in guide, marker


def test_onboarding_carries_adoption_effects_and_conflict_diagnostics() -> None:
    guide = read("alteracao_cadastral")
    for marker in (
        "`released_closed_consumers`",
        "`get_employee_identifier_state`",
        "`applied_receipts[].matricula_restoration`",
        "`nome_do_vinculo_conflitante`",
        "`identity.nome`",
        "`get_company_employee_history`",
        "`name_correction`",
        "`dated_field_value_conflict`",
        "`diagnostic.conflict`",
        "`existing_dated_conflict`",
        "`aplicacao_sequencial_por_vinculo`",
        "`snapshot_do_vinculo_desatualizado`",
        "`refusals`",
        "Junte os fatos de uma pessoa num único candidato",
    ):
        assert marker in guide, marker


def test_plugin_mirrors_the_release_without_requiring_refresh() -> None:
    workflows = flat((OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8"))
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    problems = flat(PROBLEMS.read_text(encoding="utf-8"))
    section = workflows[workflows.index("## 2.11.0: acessos") :]
    for marker in (
        "**Sem Refresh do conector**",
        "`prepare_authorization_removal`",
        "`loki.termination-rubric-catalog/2`",
        "`adoption_effects`",
        "`diagnostic.conflict`",
    ):
        assert marker in section, marker
    assert "Na 2.11.0" in skill and "Sem Refresh do conector" in skill
    for code in (
        "authorization_addition_nothing_to_add",
        "authorization_removal_nothing_to_remove",
        "nome_do_vinculo_conflitante",
        "aplicacao_sequencial_por_vinculo",
    ):
        assert code in section and code in problems, code


def test_domain_hashes_and_size_limit() -> None:
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name
