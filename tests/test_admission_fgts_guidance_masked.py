"""Entrega do guia FGTS pelo provider; não mede obediência semântica da harness."""

import pytest

from mcp_loki_updates import InstructionsProvider


def fgts_guidance() -> str:
    guide = InstructionsProvider().get("admissao")["instructions"]
    assert "### Opção pelo FGTS" in guide
    return guide.split("### Opção pelo FGTS\n", 1)[1].split("\n### ", 1)[0]


def test_provider_delivers_fgts_derivation_with_qualified_inputs_and_primary_sources() -> None:
    text = fgts_guidance()
    for requirement in (
        "dados_admissao.contrato.fgts_opcao_em",
        "empregado CLT comum",
        "posterior a 04/10/1988",
        "episódio",
        "regime",
        "insumos",
        "Manual_SEFIP_8_4_05_2026.pdf",
        "4.11",
        "4.12",
        "nota 1",
        "REGRA_EVETRAB_VALIDA_OPCAO_FGTS",
        "vigência",
        "field_sources",
        "kind=rule",
        "foundation",
        "operandos",
        "hash",
        "localizador",
    ):
        assert requirement in text


@pytest.mark.parametrize(
    "limit",
    (
        "doméstico",
        "104",
        "diretor não empregado",
        "721",
        "anterior ou igual a 04/10/1988",
        "vínculo anterior",
        "transferência",
        "reintegração",
        "categoria incerta",
        "conflitos",
    ),
)
def test_delivered_fgts_guidance_carries_exclusions_and_pending_outcome(limit: str) -> None:
    text = fgts_guidance()
    assert limit in text
    assert "mantenha pendência" in text
    assert "regra específica" in text


def test_delivered_fgts_guidance_preserves_facts_review_snapshot_and_human_gates() -> None:
    text = fgts_guidance()
    for safeguard in (
        "não sobrescreva",
        "não marque como documento lido",
        "relatório da equipe",
        "case_type",
        "presença de uma data",
        "snapshot",
        "pacote",
        "ajuste/correção",
        "revisão humana",
        "não aplica",
        "não aprova",
    ):
        assert safeguard in text
    provider = InstructionsProvider()
    assert provider.check_version("2.0.0", "2.0.0")["compatible"] is True
    assert provider.get("admissao")["permissions"] == {
        "capabilities": ["consultar"],
        "processes": ["admissao"],
    }


def test_delivered_fgts_guidance_qualifies_verified_edition_and_current_access_limit() -> None:
    text = fgts_guidance()
    for qualification in (
        "edição de outubro/2022 conferida",
        "complemento localizado/indexado",
        "acesso integral ficou bloqueado",
        "22/10/2026",
        "regime CLT comum e episódio atual",
    ):
        assert qualification in text
