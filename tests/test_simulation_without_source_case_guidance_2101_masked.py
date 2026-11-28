"""Entrega das orientações da 2.10.1 (simulação de rescisão de quem segue empregado).

Contrato aditivo, sem Refresh do conector: `create_case` recebe o payload genérico. Prova que
os textos chegam ao domínio de rescisão e ao plugin e que versões e hashes acompanham; não
mede obediência.
"""

import hashlib
import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "plugins/loki-bootstrap/skills/operar-loki"
PROBLEMS = ROOT / "plugins/loki-bootstrap/skills/registrar-problema-loki/SKILL.md"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
LIMIT = 65536
SPEC = "loki.termination-simulation-create/2"
REFUSALS = (
    "simulation_history_changed",
    "simulation_employment_not_active",
    "simulation_source_not_supported",
    "simulation_cancelled",
)


def flat(value: str) -> str:
    return " ".join(value.split())


def test_general_notice_needs_no_refresh_and_keeps_the_previous_one() -> None:
    guide = (DOMAINS / "geral.md").read_text(encoding="utf-8")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.14.0)")
    notice = flat(guide[: guide.index("## Reaproveitar respostas e causas persistidas")])
    # 2.14.0: avisos anteriores à 2.12.0 aposentados (sem objeto depois do recadastro dos
    # conectores no endereço novo); cada regra que eles apontavam segue no domínio próprio.
    for retired in ("**Continua da 2.10.1:**", "**Continua da 2.10.0**", "**Continua da 2.9.9**"):
        assert retired not in notice, retired
    # A regra do aviso da 2.10.1 (simulação sem caso de origem) segue no domínio da rescisão.
    rescisao = flat((DOMAINS / "rescisao.md").read_text(encoding="utf-8"))
    assert "## Simulação de quem segue empregado, sem caso de origem (2.10.1)" in rescisao
    assert "Refresh do conector e conversa nova" in notice


def test_termination_domain_carries_the_employee_simulation_script() -> None:
    guide = flat((DOMAINS / "rescisao.md").read_text(encoding="utf-8"))
    for marker in (
        "## Simulação de quem segue empregado, sem caso de origem (2.10.1)",
        SPEC,
        "`get_company_employee_history`",
        "`expected_history_hash`",
        "`kind=declaration`",
        "`locator = $.payload.<caminho da folha>`",
        "Não mande `documentos_origem`",
        "`run_prepared_case_workflow`",
        "`get_case_version`",
        "dizem que o histórico não entrou no cálculo",
        "`requires_source_case_by_version`",
        "Só a pessoa descarta, com `cancel_case`",
        "A rotina técnica não cancela",
        "use outra `simulation_ref`",
        "não cria funcionário, evento de vínculo ou pin",
        "fica isolada: não entra no 13º, no fechamento do mês nem na conciliação",
    ):
        assert marker in guide, marker
    for code in REFUSALS[:3] + ("simulation_cancelled",):
        assert code in guide, code


def test_plugin_mirrors_the_simulation_without_requiring_refresh() -> None:
    workflows = flat((OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8"))
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    problems = flat(PROBLEMS.read_text(encoding="utf-8"))
    section = workflows[workflows.index("## 2.10.1: simulação de rescisão") :]
    for marker in (
        SPEC,
        "**Sem Refresh do conector**",
        "`cancel_case`",
        "`requires_source_case_by_version`",
    ):
        assert marker in section, marker
    assert "Na 2.10.1" in skill and SPEC in skill and "Sem Refresh do conector" in skill
    for code in REFUSALS:
        assert code in section and code in problems, code


def test_release_versions_and_hashes() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.40"
    assert metadata["instructions_version"] == "2.14.0"
    assert metadata["mcp_contract_version"] == "2.14.0"
    assert metadata["recommended_plugin_version"] == "2.14.0"
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name
