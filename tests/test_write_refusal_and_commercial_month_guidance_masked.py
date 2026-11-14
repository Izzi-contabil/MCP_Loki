"""Entrega das orientações da 2.6.7; nao mede obediencia da harness."""

from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
CAPACITIES = SKILLS / "operar-loki/references/CAPACIDADES_DP.md"


def test_package_equivalence_replaces_live_recalculation_wording() -> None:
    provider = InstructionsProvider()
    for domain in ("geral", "admissao", "rescisao"):
        text = provider.get(domain)["instructions"]
        assert "o cálculo de onde saiu" in text, domain
        assert "calculo_desatualizado" in text, domain
        assert "cálculo vigente\nancorado" not in text, domain
    general = provider.get("geral")["instructions"]
    assert "gravação em andamento em casos da\nmesma empresa" in general
    assert "não recalcula a folha viva" in general


def test_commercial_month_salary_balance_and_pending_scenarios() -> None:
    guides = [InstructionsProvider().get("rescisao")["instructions"], CAPACITIES.read_text()]
    for guide in guides:
        for required in (
            "trinta_fixo",
            "rescisao-v43",
            "rescisao-v44",
            "não informe dias nem troque o divisor",
            "no dia 31 agora calcula",
            "licença-maternidade",
            "divisor pelo calendário",
            "nova\nrevisão",
        ):
            assert required in guide, required
        assert "não são habilitados" not in guide


def test_connector_write_refusal_and_payroll_map_batch_in_general() -> None:
    general = InstructionsProvider().get("geral")["instructions"]
    for required in (
        "## Conector: conexão fechada ou tempo esgotado",
        "/healthz",
        "Refresh do conector",
        "Caixa",
        "nunca sem `request_ref`",
        "campo_fora_do_schema",
        "campo_ja_preenchido_exige_sobrescrever",
        "dados_ferias_fora_do_schema",
        "afastamentos_representacao_invalidos",
        "vacation_preparation_requires_complete_input",
        "caso_fora_de_estado_gravavel",
        "`reason` igual a `case_write_constraints`",
        "loki.company-payroll-map-policy-patch/1",
        "payroll_map_policy_patch_transport.policies.arredondamento_monetario.accepted",
        '"half_up" | "half_even" | "exigir_qualificacao"',
        "`fonte` é obrigatória",
        "payroll_policy_patch_rounding_verba_missing",
        "payroll_policy_patch_rounding_verba_ambiguous",
        "payroll_policy_patch_rounding_formula_incompatible",
        "harness não\nescolhe",
    ):
        assert required in general, required
    assert InstructionsProvider().metadata()["mcp_contract_version"] == "2.6.3"


def test_second_vacation_occurrence_guidance() -> None:
    guides = [InstructionsProvider().get("ferias")["instructions"], CAPACITIES.read_text()]
    for guide in guides:
        for required in (
            "mês de início do gozo",
            "`created: false`",
            "Duas frações na mesma competência",
            "Nunca\ncancele o primeiro caso",
        ):
            assert required in guide, required


def test_plugin_mirrors_267_guidance() -> None:
    workflows = (SKILLS / "operar-loki/references/WORKFLOWS.md").read_text(encoding="utf-8")
    assert "## Recusas de gravação, conector, saldo comercial e lote de mapas" in workflows
    for required in (
        "caso_fora_de_estado_gravavel",
        "/healthz",
        "trinta_fixo",
        "`created: false`",
        "arredondamento_monetario",
        "calculo_desatualizado",
    ):
        assert required in workflows, required
    skill = (SKILLS / "operar-loki/SKILL.md").read_text(encoding="utf-8")
    assert "Recusas de gravação, conector, saldo comercial e lote de mapas" in skill
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert "loki.company-payroll-map-policy-patch/1" in capacities
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert "`reason` igual ao próprio código" in report
    assert "/healthz" in report
