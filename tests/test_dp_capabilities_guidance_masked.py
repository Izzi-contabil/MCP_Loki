"""Discovery guidance does not certify deployment, adoption, or DP accuracy."""

import re
from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "plugins/loki-bootstrap/skills/operar-loki"


def test_dp_reference_is_reachable_before_preparation_and_routine_execution() -> None:
    reference = OPERATOR / "references/CAPACIDADES_DP.md"
    for entry in (OPERATOR / "SKILL.md", OPERATOR / "references/ROUTINES.md"):
        targets = {
            (entry.parent / link).resolve()
            for link in re.findall(r"\]\(([^)]+\.md)\)", entry.read_text(encoding="utf-8"))
        }
        assert reference.resolve() in targets
    assert reference.is_file()


@pytest.mark.parametrize(
    ("domain", "required"),
    [
        ("geral", ("pronto_folha", "folha_avaliada", "prontidão por funcionário", "98%")),
        (
            "geral",
            (
                "get_operational_batch_contract",
                "apply_historical_state",
                "loki.case-workflow-command/1",
                "loki.payroll-population-preview/1",
                "reset_financial_inputs=true",
                "loki.case-cancellation/1",
            ),
        ),
        ("ferias", ("saldo_source", "medias_importadas", "fragments_complete")),
        (
            "afastamento",
            (
                "leave.categoria",
                "correcao nao pode alterar identidade ou escopo do caso",
                "submit_operator_correction",
            ),
        ),
        (
            "rescisao",
            (
                "credito_trabalhador_rescisao",
                "loki.pension-rule/2",
                "Dataprev",
                "saldo_admissao_no_mes",
                "regra_nao_medida",
            ),
        ),
        ("decimo_terceiro", ("loki.pension-rule/2", "acumulada_com_compensacao", "etapas")),
        (
            "alteracao_cadastral",
            (
                "credito_trabalhador_contratos",
                "pensao_alimenticia_regra",
                "additional_policies",
                "inherit_future_hires",
            ),
        ),
    ],
)
def test_runtime_distributes_consumer_specific_paths_and_limits(
    domain: str, required: tuple[str, ...]
) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for item in required:
        assert item in guide, (domain, item)


def test_reference_keeps_missing_contract_and_known_refusals_visible() -> None:
    guide = (OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8")
    for required in (
        "contrato servido",
        "não oferece endpoint bulk",
        "STARTED",
        "Sem essa ferramenta no catálogo",
        "consultas e seleções individuais",
        "não mede acurácia",
        "correcao nao pode alterar identidade ou escopo do caso",
        "regra_nao_medida",
        "não comprova publicação",
        "não baixar o acervo",
    ):
        assert required in guide, required


def test_leave_preparation_is_discoverable_without_relaxing_the_generic_corrector() -> None:
    provider = InstructionsProvider()
    guides = [
        provider.get("afastamento")["instructions"],
        (OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8"),
    ]
    for guide in guides:
        assert "preparation.supported=true" in guide
        assert "replace_process_inputs" in guide
        assert "loki.case-preparation-transport/1" in guide
        assert "corrigir_dados" in guide
        assert "efeito aplicado" in guide


def test_same_month_salary_guidance_keeps_the_qualified_calendar_scope() -> None:
    provider = InstructionsProvider()
    guides = [
        provider.get("rescisao")["instructions"],
        (OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8"),
    ]
    for guide in guides:
        assert "mês civil de 30 dias" in guide
        assert "divisor 30" in guide
        assert "inferência técnica" in guide
        assert "saldo_admissao_no_mes" in guide
