"""The packaged guide must expose the qualified consumer paths and their limits."""

from pathlib import Path

from mcp_loki_updates import InstructionsProvider

REFERENCE = (
    Path(__file__).resolve().parents[1]
    / "plugins/loki-bootstrap/skills/operar-loki/references/CAPACIDADES_DP.md"
)


def test_vacation_replacement_preserves_identity_and_requires_fresh_inputs() -> None:
    guides = [InstructionsProvider().get("ferias")["instructions"], REFERENCE.read_text()]
    for guide in guides:
        for required in (
            "preparation.supported=true",
            "loki.case-preparation-transport/1",
            "replace_process_inputs",
            "corrigir_dados",
            "input_snapshot",
            "aquisitivo",
            "gozo",
            "related_vacation_parameters_invalid",
        ):
            assert required in guide


def test_salary_extension_does_not_suggest_unqualified_calendars() -> None:
    guides = [InstructionsProvider().get("rescisao")["instructions"], REFERENCE.read_text()]
    for guide in guides:
        for required in (
            "rescisao-v42",
            "mês civil de 31 dias",
            "desligamento até o dia 30",
            "sem afastamento sobreposto",
            "divisor 30",
            "regra_nao_medida:saldo_admissao_no_mes",
        ):
            assert required in guide


def test_monthly_fgts_policy_is_contextual_and_does_not_approve_real_cases() -> None:
    guides = [InstructionsProvider().get("geral")["instructions"], REFERENCE.read_text()]
    for guide in guides:
        for required in (
            "fgts_mensal",
            "loki.fgts-mensal/1",
            "trabalhador_competencia_mensal_8pct",
            "calculo_fgts",
            "folha-v29",
            "política ausente",
            "não autoriza",
        ):
            assert required in guide
