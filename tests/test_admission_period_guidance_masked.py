"""Entrega do criterio de periodo salarial; nao mede obediencia semantica da harness."""

from mcp_loki_updates import InstructionsProvider


def test_explicit_pay_period_is_delivered_with_its_source_and_output_check() -> None:
    guide = InstructionsProvider().get("admissao")["instructions"]
    assert "### Período salarial" in guide
    assert "contrato.periodo_salario" in guide
    assert "Mensalista" in guide
    assert "valor integral" in guide
    assert "localizador" in guide
    assert "não confirma o período" in guide
    assert "categoria do vínculo" in guide
    assert "branco" in guide
    assert "missing_fields" in guide
    assert "overflow" in guide
