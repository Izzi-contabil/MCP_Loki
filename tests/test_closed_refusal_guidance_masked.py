"""Entrega das recusas com motivo fechado da 2.6.6; nao mede obediencia da harness."""

from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"


def test_closed_refusals_reach_their_domains_and_keep_the_contract() -> None:
    provider = InstructionsProvider()
    general = provider.get("geral")["instructions"]
    for required in (
        'classification: "equivalent"',
        "employee_excluded_from_current_calculation",
        "protected_consumer_equivalence_proofs",
        "import_preservation_protected_dependency",
        "import_preservation_consumer_changed",
        "reconciliation_dependencies_busy",
        'só `{"matricula"}`',
        "`{funcionario_id, matricula}` copiados da prévia",
        "provenance.field_source_keys",
        "leaf_paths(data)",
        "periodos[0].inicio",
        "field_source_coverage",
        "hypothesis_payload",
        "VersionFieldSource",
        "$.payload.<caminho>",
        "simulation_payload_incomplete",
        "simulation_process_unsupported",
        "field_source_invalid",
        "restart_requires_preparation_for_state",
        'next_action: "get_process_contract"',
        "restart_requires_adjustable_state",
        "payroll_population_rebound_requires_identifier",
        "get_process_contract.preparation.modes",
        "conciliação própria",
    ):
        assert required in general, required
    assert "`mode` e `request_ref`" not in general
    admission = provider.get("admissao")["instructions"]
    assert "employee_excluded_from_current_calculation" in admission
    assert "import_preservation_consumer_changed" in admission
    termination = provider.get("rescisao")["instructions"]
    for required in (
        "afastamento_representacao_mista",
        "afastamento_concessao_incompativel",
        "afastamento_pagadores_sobrepostos",
        "afastamento_concessoes_sobrepostas",
        "faixa_previdenciaria_exige_beneficio",
        "beneficio_previdenciario_exige_pagador_inss",
        "employee_excluded_from_current_calculation",
    ):
        assert required in termination, required
    vacation = provider.get("ferias")["instructions"]
    for required in ("related_case_ids", "related_reason", "`incomplete`", "decisão humana"):
        assert required in vacation, required
    assert provider.metadata()["mcp_contract_version"] == "2.6.3"


def test_plugin_mirrors_closed_refusals() -> None:
    workflows = (SKILLS / "operar-loki/references/WORKFLOWS.md").read_text(encoding="utf-8")
    assert "## Recusas e prévias com motivo fechado" in workflows
    for required in (
        "employee_excluded_from_current_calculation",
        "afastamento_representacao_mista",
        "simulation_process_unsupported",
        "restart_requires_preparation_for_state",
        "related_case_ids",
        "payroll_population_rebound_requires_identifier",
        "get_process_contract.preparation.modes",
    ):
        assert required in workflows, required
    capabilities = (SKILLS / "operar-loki/references/CAPACIDADES_DP.md").read_text(encoding="utf-8")
    assert "protected_consumer_equivalence_proofs" in capabilities
    assert "restart_requires_adjustable_state" in capabilities
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert "simulation_process_unsupported" in report
    assert "reconciliation_dependencies_busy" in report
