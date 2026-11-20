"""Entrega das orientações da 2.9.4 (backend #374 e #375).

Prova só que os textos chegam aos domínios e ao plugin; não mede obediência.
"""

import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
OPERATOR = SKILLS / "operar-loki"
WORKFLOWS = OPERATOR / "references/WORKFLOWS.md"
CAPACITIES = OPERATOR / "references/CAPACIDADES_DP.md"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"
SECTION_294 = "## 2.9.4: folha v32 (salário-família, VT do admitido) e empresa nova no worker"

NOTICE = (
    "## O que mudou nesta versão (2.9.4)",
    "> **Atenção: recalcular as folhas mensais não entregues.**",
    "Quando `loki_verificar_versao` ou o cálculo da folha mostrar o motor `folha-v32`",
    "`calculation_stale`",
    "inclusive as já recalculadas na `folha-v31`",
    "Uma correção de salário-família registrada na v31 continua valendo e prevalece",
    "**Exige ação da operadora:** o recálculo acima e atualizar o plugin instalado",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
    "o limite usa a remuneração devida no mês",
    "o percentual incide uma vez sobre o salário proporcional",
    "Empresa nova: a pessoa owner (ou master) inclui a empresa no worker de folha pelo "
    "comando aditivo `prepare_authorization_addition`; a recusa "
    "`worker_not_authorized` diz o que falta",
)
RECALC = (
    "## Motor folha-v32: recalcular as folhas não entregues",
    "**todas as folhas mensais não entregues ficam desatualizadas** (`calculation_stale`)",
    "o aceite dado ao cálculo anterior não vale para o novo",
    "Nada é recalculado, reaberto ou decidido automaticamente",
    "**Correções registradas na v31 continuam valendo.**",
    "**prevalece** sobre a cota proporcional da v32",
    "Compare o valor declarado com o calculado na memória `operator_corrections`",
    "a memória mostra `calculated: null`",
)
FAMILY = (
    "## Salário-família pela remuneração devida no mês (folha-v32)",
    "**remuneração que seria devida no mês, independentemente dos dias trabalhados**",
    "entra o salário-base cheio",
    "entram pelo valor do mês cheio",
    "ficam fora faltas, DSR das faltas e atrasos, as férias do mês com o terço e o 13º",
    "**Faltas não reduzem a remuneração.**",
    "`30 − dia da admissão + 1`",
    "A contagem está em confirmação com a DP",
    "não aparece mais em cálculos novos",
    "`salario_familia_mes_transferencia_pendente_regra`",
    "`aguardar_regra_dp_do_salario_familia_no_mes_de_transferencia`",
    "`salario_familia_salario_do_mes_nao_identificado`",
    "`qualificar_rubrica_do_salario_do_mes_no_mapa`",
    "`salario_familia_adicional_mes_cheio_nao_identificado`",
    "`qualificar_adicional_do_mes_cheio_ou_declarar_cota_pela_dp`",
    "`salario_familia_deducao_nao_classificada`",
    "`qualificar_deducao_da_base_ou_declarar_cota_pela_dp`",
    "`salario_familia_medias_ferias_nao_classificadas`",
    "`declarar_cota_pela_dp_com_medias_de_ferias`",
    '{"funcionarios.<matricula>.bases.salario_familia_cents": <centavos>}',
    "A falta de filhos no cadastro não usa essa rota",
    "A saída normal é qualificar ou corrigir a rubrica de salário no mapa da empresa. "
    "`submit_operator_correction` só vale com decisão explícita da DP sobre a cota "
    "daquele caso.",
)
TRANSPORT = (
    "## VT do admitido no mês (folha-v32)",
    'Isto substitui o "VT do admitido no mês: sem mudança" da `folha-v31`',
    "aplicado **uma vez** sobre o salário proporcional do mês",
    "admissão no dia 1: vale a fórmula de sempre",
    "sem reaplicar a proporção",
    "`vale_transporte_proporcao_concessao_admissao_ambigua`",
    "`confirmar_proporcao_da_concessao_ou_declarar_desconto_pela_dp`",
    '{"funcionarios.<matricula>.verbas.<rubrica de VT>.0.valor_cents":',
    "`vale_transporte_mes_transferencia_pendente_regra`",
    "Afastamento e desligamento no mês: sem mudança",
    "Quando a fonte mostrar a regra valendo desde a admissão (ou antes), declare essa "
    "data; o Loki não retém mais. Não ajuste `vigente_desde` para destravar.",
    "o caminho exato da linha de VT vem em `operator_corrections` do cálculo",
)
STALE_V31 = (
    "## Salário-família pelo limite da base do INSS (folha-v31)",
    "**VT do admitido no mês: sem mudança.**",
    "**Em consulta à DP, sem mudança agora:**",
    "a transferência entre empresas do grupo hoje também conta como entrada",
    "## Motor folha-v31: recalcular as folhas não entregues",
)
WORKER = (
    "## Empresa nova: acesso do worker e da rotina",
    '`reason: "worker_company_grant_missing"`',
    '"prepare_authorization_addition"',
    "`aplicar_autorizacao`",
    "`preparar_autorizacao` substitui a lista inteira de concessões",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    lines = (line.removeprefix(">").strip() for line in value.splitlines())
    return " ".join(" ".join(lines).split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def assert_none(guide: str, stale: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in stale:
        assert flat(item) not in body, item


def test_versions_follow_the_additive_contract_patch() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.29"
    assert metadata["instructions_version"] == "2.9.4"
    assert metadata["mcp_contract_version"] == "2.9.4"
    assert metadata["recommended_plugin_version"] == "2.9.4"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.9.2", "2.9.3", "2.9.4"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.9.4", "2.9.5")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    backend = release["changes"]["backend"][-1]
    assert backend.startswith("Contrato2.9.4 aditivo")
    assert "as 96 ferramentas são as mesmas" in backend
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.4")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.4")
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.9.4", path.name


def test_general_notice_highlights_the_v32_recalculation_and_worker() -> None:
    guide = text("geral")
    end = guide.index("## Reaproveitar respostas e causas persistidas")
    notice = guide[:end]
    assert_all(notice, NOTICE)
    current = notice[: notice.index("**Continua da 2.8.0**")]
    assert current.index("recalcular as folhas mensais") < current.index("**Não exige nada**")
    assert "## O que mudou nesta versão (2.9.3)" not in guide
    assert_all(guide, WORKER)
    assert len(guide.encode("utf-8")) <= 65536


def test_payroll_domain_carries_v32_guidance() -> None:
    payroll = text("folha_mensal")
    assert_all(payroll, (*RECALC, *FAMILY, *TRANSPORT))
    assert_none(payroll, STALE_V31)
    first = payroll.index("\n## ")
    assert payroll[first:].startswith("\n## Motor folha-v32")
    assert_all(
        payroll,
        (
            "**Empresa nova sem o worker.**",
            "A pessoa owner (ou master) inclui pelo conector",
            "registre o problema e avise a engenharia pelo Caixa",
            '`reason: "worker_company_grant_missing"`',
        ),
    )


def test_plugin_mirrors_294_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_294 in workflows
    section = workflows[workflows.index(SECTION_294) :]
    section = section[: section.index("\n## ", 1)]
    assert_all(
        section,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "Quando o cálculo mostrar o motor `folha-v32`",
            "A saída normal é qualificar ou corrigir a rubrica de salário no mapa da empresa",
            "só vale com decisão explícita da DP sobre a cota daquele caso",
            "Não ajuste `vigente_desde` para destravar",
            "o caminho exato da linha de VT vem em `operator_corrections` do cálculo",
            "a pessoa owner (ou master) inclui a empresa",
            "**Correção da v31 prevalece.**",
            "`salario_familia_mes_admissao_pendente_regra` não aparece mais",
            "`salario_familia_mes_transferencia_pendente_regra`",
            "`salario_familia_deducao_nao_classificada`",
            "`vale_transporte_proporcao_concessao_admissao_ambigua`",
            "`prepare_authorization_addition`",
        ),
    )
    assert_all(
        CAPACITIES.read_text(encoding="utf-8"),
        (
            "## 2.9.4: folha v32, VT do admitido e empresa nova no worker",
            "Uma correção de salário-família registrada na v31 prevalece",
            "Substituída em parte pela 2.9.4: salário-família e VT do admitido.",
        ),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.4: folha v32 (salário-família, VT do admitido) e empresa nova no worker”",
            "correções de salário-família da v31 prevalecem e devem ser conferidas",
            "Substituída em parte pela 2.9.4: salário-família e VT do admitido.",
        ),
    )
    assert_all(
        (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"),
        (
            "Na 2.9.4 não são defeito",
            "`calculation_stale` depois da troca para `folha-v32`",
            "`salario_familia_salario_do_mes_nao_identificado` é problema do mapa",
            "`vale_transporte_mes_transferencia_pendente_regra` e",
            "iniciada depois da admissão ou encerrada no mês",
        ),
    )
