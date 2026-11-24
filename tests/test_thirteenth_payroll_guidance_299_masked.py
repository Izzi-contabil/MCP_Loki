"""Entrega das orientações da 2.9.9 (13º, folha em revisão, mês civil e fórmulas do mapa).

Contrato aditivo 2.9.9, sem ferramenta nova. Prova que os textos chegam aos domínios e ao
plugin e que as versões e os hashes do release acompanham; não mede obediência.
"""

import hashlib
import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "plugins/loki-bootstrap/skills/operar-loki"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
SECTION = (
    "## 2.9.9: 13º (cobertura, 1ª parcela já paga, horas) e folha (revisão, mês civil, fórmulas)"
)
LIMIT = 65536

THIRTEENTH = (
    "é informativo no estado: o cálculo\ndo 13º **não o lê**",
    "`thirteenth_payments`: de 01/01 do `ano` (ou da admissão, se ela for no ano) "
    "até a `data_pagamento` da etapa;",
    "`leave_occurrences`: da mesma data inicial até o corte",
    "**cobertura adjacente** (`start` 01/11, `end` 30/11",
    "**As janelas vêm só na resposta imediata**",
    "(#409, ainda não mesclada)",
    "releia a resposta imediata antes de concluir**",
    "`historical_thirteenth_first_installment_already_paid`",
    "**não pague de novo**",
    "a 2ª\nparcela compensa",
    "## Horas no 13º: só onde a norma coletiva é silente",
    "Súmula 347",
    '`horas: "valores"`',
    "`decimo_horas_vedado_pela_norma_coletiva`",
    "(backend #408,",
    '"empresas[<codigo>].decimo_terceiro_medias"',
)
PAYROLL = (
    "`restart_case` **simples** (sem `preparation`)",
    "`expected_snapshot=get_case.correction_snapshot`",
    "`case_in_review_requires_restart`",
    "(#410, aberta)",
    "## Folha pelo mês civil: `folha_divisor_mes` (backend #405)",
    '"empresas[<codigo>].folha_divisor_mes"',
    '"divisor_dias": "dias_mes_civil"',
    '"empresas[<codigo>].convencoes.dias_do_mes": "calendario"',
    "`folha_divisor_mes_retroativo`",
    "`periodo_remuneravel_diverge_do_vinculo`",
    "`ferias_calculadas_a_30_sob_a_politica`",
    "`desconto_de_faltas_acima_do_salario`",
    "**Falta sempre pela rubrica de falta**",
    "`valor_explicito`",
    "## Fórmulas do mapa: o que existe hoje e os limites",
    "**quantidade = 2 × dias**",
    '`base_composta_proporcional` com `fator: "2"`',
    "`rubricas_base`",
    "**ainda não\n  existe**",
)
STALE = (
    "`thirteenth_payment_coverage_not_certified` segue a regra de cobertura",
    "- **Abertas e em revisão** (`aberto`, `em_preparacao`, `aguardando_revisao`):",
)


def flat(value: str) -> str:
    return " ".join(value.split())


def text(name: str) -> str:
    return (DOMAINS / f"{name}.md").read_text(encoding="utf-8")


def test_thirteenth_guidance_is_delivered_and_stale_rule_is_gone() -> None:
    guide = flat(InstructionsProvider().get("decimo_terceiro")["instructions"])
    for marker in THIRTEENTH:
        assert flat(marker) in guide, marker
    assert flat(STALE[0]) not in guide
    ferias = text("ferias")
    assert "Não é a do 13º" in ferias
    assert "domínio `decimo_terceiro`" in ferias


def test_payroll_guidance_is_delivered_and_stale_review_path_is_gone() -> None:
    guide = flat(InstructionsProvider().get("folha_mensal")["instructions"])
    for marker in PAYROLL:
        assert flat(marker) in guide, marker
    assert flat(STALE[1]) not in guide


def test_plugin_mirrors_the_release_and_replaced_coverage_rule() -> None:
    workflows = (OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8")
    capacities = (OPERATOR / "references/CAPACIDADES_DP.md").read_text(encoding="utf-8")
    skill = (OPERATOR / "SKILL.md").read_text(encoding="utf-8")
    assert SECTION in workflows
    assert "**não para o cálculo do 13º** (seção 2.9.9)" in workflows
    assert workflows.index(SECTION) < workflows.index("## 2.9.8: rescisão")
    assert "## 2.9.9: 13º e folha mensal" in capacities
    assert "O 13º não segue essa regra" in capacities
    assert "Na 2.9.9" in skill
    problem = (ROOT / "plugins/loki-bootstrap/skills/registrar-problema-loki/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Na 2.9.9 não são defeito" in problem


def test_release_is_text_only_with_matching_hashes_and_size_limit() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.34"
    assert metadata["instructions_version"] == "2.9.9"
    assert metadata["mcp_contract_version"] == "2.9.9"
    assert metadata["recommended_plugin_version"] == "2.9.9"
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["backend"][-1].startswith("Contrato2.9.9 aditivo")
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.9")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.9")
    for name, hashes in release["domains"].items():
        for suffix, key in (("md", "content_sha256"), ("json", "metadata_sha256")):
            content = (DOMAINS / f"{name}.{suffix}").read_bytes()
            assert hashlib.sha256(content).hexdigest() == hashes[key], (name, suffix)
        assert len((DOMAINS / f"{name}.md").read_bytes()) <= LIMIT, name
        data = json.loads((DOMAINS / f"{name}.json").read_text(encoding="utf-8"))
        assert data["version"] == "2.9.9", name
        assert data["compatibility"]["mcp_contract_version"] == "2.9.9", name
        assert data["compatibility"]["recommended_plugin_version"] == "2.9.9", name
