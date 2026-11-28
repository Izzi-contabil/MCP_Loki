"""Entrega das orientações da 2.13.0 (categoria eSocial na folha e no cadastro, por alteração
cadastral e por onboarding, e recusa de caso de quem não é empregado)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/loki-bootstrap"
OPERATOR = PLUGIN / "skills/operar-loki"
PROBLEMS = PLUGIN / "skills/registrar-problema-loki/SKILL.md"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
LIMIT = 65536
PROCESSES = ("admissao", "rescisao", "ferias", "decimo_terceiro")
# O reinício em lote por correção é da 2.14.0: nenhum texto da categoria (2.13.0) o menciona.
# Os marcadores são montados aqui para que a busca por eles no repositório não os encontre.
RESTART = ("restart" + "_batch", "correction" + "_restart", "case-restart" + "-authorized")


def section_of(guide: str, title: str) -> str:
    """A seção `title` até o próximo `## `: onde a categoria vive, sem o texto da 2.14.0."""
    start = guide.index(title)
    found = re.search(r"\s## ", guide[start + len(title) :])
    return guide[start:] if found is None else guide[start : start + len(title) + found.start()]


def flat(value: str) -> str:
    return " ".join(value.split())


def read(domain: str) -> str:
    return flat((DOMAINS / f"{domain}.md").read_text(encoding="utf-8"))


def assert_all(body: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        assert flat(marker) in body, marker


def test_general_notice_keeps_the_2130_no_refresh_line_and_the_2120_one() -> None:
    guide = (DOMAINS / "geral.md").read_text(encoding="utf-8")
    assert "## O que mudou nesta versão (2.13.0)" not in guide
    assert "## O que mudou nesta versão (2.12.0)" not in guide
    notice = flat(guide[: guide.index("## Reaproveitar respostas e causas persistidas")])
    assert_all(
        notice,
        (
            "**Continua da 2.13.0:**",
            "sem ferramenta nova nem Refresh do conector",
            "a categoria eSocial (seções 2.13.0) já está publicada",
            "Releia `get_process_contract` de `alteracao_cadastral` antes de declará-la",
            "**Continua da 2.12.0:**",
            "**Refresh do conector e conversa nova**",
        ),
    )
    order = (
        "**Exige ação da operadora (2.14.0):**",
        "**Vale quando o Loki for publicado:**",
        "**Continua da 2.13.0:**",
        "**Continua da 2.12.0:**",
        "**Continua da 2.11.0**",
        "**Continua da 2.10.1:**",
        "**Continua da 2.10.0**",
        "**Continua da 2.9.9**",
        "**Continua da 2.9.8:**",
    )
    positions = [notice.index(marker) for marker in order]
    assert positions == sorted(positions)
    # A regra do consignado não pode ficar mais larga do que a 2.12.0 a escreveu.
    assert (
        "Folha com pessoa que confirma 2 ou mais contratos de consignado no mês "
        "(`-worker-credit-allocation-v1`)"
    ) in notice
    assert len((DOMAINS / "geral.md").read_bytes()) <= LIMIT


def test_payroll_carries_non_employee_category_and_the_cadastre_rules() -> None:
    guide = read("folha_mensal")
    assert_all(
        guide,
        (
            "## Categoria eSocial que não é de empregado e categoria no cadastro (2.13.0)",
            "**Categoria que não começa com `1`**",
            "723 sócio com pró-labore, 901 estagiário",
            "`vinculo_nao_suportado`",
            "`categoria_esocial_nao_suportada`",
            "`retirar_categoria_nao_clt_da_folha_mensal`",
            "**não calcula pró-labore nem bolsa de estágio**",
            "O `111` segue com o código próprio",
            "**Memória dentro do caso.**",
            "só dentro do caso da competência",
            "O cadastro vence a memória",
            "**(a) alteração cadastral**",
            "**(b) fato `parametrizacao` do onboarding**",
            "**Data de efeito: o início da pessoa naquela categoria**",
            "**nunca a data do envio**",
            "folha sem o campo usa a do cadastro",
            "`categoria_esocial_divergente`",
            "`alinhar_categoria_esocial_folha_e_cadastro`",
            "Quem não é empregado exige só `dependentes_irrf`",
            "sindicato, escala, VT e salário-família",
            "ANTES de rodar a folha",
        ),
    )
    # A seção do intermitente da 2.12.0 não afirma mais que nenhum cadastro guarda a categoria.
    assert "nenhum cadastro guarda a categoria" not in guide
    assert "não recebem o fato de categoria hoje" not in guide
    assert "**Declare em TODA competência.**" in guide
    # A seção da categoria não menciona o reinício em lote (que é da 2.14.0).
    categoria = section_of(
        guide, "## Categoria eSocial que não é de empregado e categoria no cadastro (2.13.0)"
    )
    assert not any(token in categoria for token in RESTART)
    assert not any(token in section_of(guide, "## Vínculo intermitente") for token in RESTART)


def test_cadastre_domain_says_how_to_declare_the_category_by_both_paths() -> None:
    guide = read("alteracao_cadastral")
    section = guide[guide.index("## Categoria eSocial do vínculo no cadastro (2.13.0)") :]
    assert_all(
        section,
        (
            "`employee_parameters.data_schema`",
            "`^[0-9]{3}$`",
            '`get_process_contract("alteracao_cadastral")`',
            "não há Refresh do conector",
            "**Data de efeito: o início da pessoa naquela categoria**",
            "**nunca a data do envio**",
            "a folha calcula a pessoa como empregada",
            "**Caminho 1: alteração cadastral**",
            "`dados_alteracao_cadastral.changes`",
            "`get_documentary_profile(case_id, funcionario_id, as_of)`",
            "`profile_hash`",
            "`expected_profile_hash`",
            'changes: {"categoria_esocial": "723"}}`',
            "`apply_case_effects`",
            "`correction_snapshot` de `get_case`",
            "`effect_snapshot_changed`",
            "a rotina não aplica",
            "`prior_value_missing`",
            "`data_efeito`",
            "`occurrence_ref` **nova a cada declaração ou correção**",
            "`effect_reference_already_applied`",
            "**mesma `effective_on` da declaração errada**",
            "`effect_before_admission`",
            "`reference` (do chunk, obrigatório)",
            "**Caminho 2: fato `parametrizacao` do onboarding**",
            "`create_company_onboarding(cliente_slug, empresa_cnpj, reference)`",
            "`submit_company_onboarding_chunk(onboarding_id, declaration)`",
            '"loki.company-onboarding/1"',
            "`reference`, `cpf`, `nome` e `data_admissao`",
            "`existing_employee_id`",
            "`validate_company_onboarding(onboarding_id)`",
            "`apply_company_onboarding(onboarding_id, validation_hash)`",
            "`import_documentary_profile`",
            "Valor sem 3 dígitos é recusado",
            "`replaces_fact_id`",
            "**antes** de rodar folha",
            "`categoria_esocial_divergente`",
            "o cadastro vence a memória do caso",
            "exige só os dependentes de IRRF",
            "`categoria_sem_regime_clt`",
        ),
    )
    assert "não aceita `categoria_esocial` hoje" not in guide
    assert not any(token in guide for token in RESTART)


def test_other_processes_refuse_the_case_with_the_exact_code_and_its_limits() -> None:
    for domain in PROCESSES:
        guide = read(domain)
        assert_all(
            guide,
            (
                "## Categoria eSocial que não é de empregado no cadastro (2.13.0)",
                "`create_case` recusa antes de gravar",
                "`categoria_sem_regime_clt`",
                "`HUMAN_DECISION`",
                "O caso não é criado.",
                "vale só na criação",
                "`vinculo_nao_clt_*`",
                "competência do próprio processo",
                "o mês corrente (America/Sao_Paulo)",
                "e recriar o caso). O caso não é criado.",
                "com a data de efeito do início da pessoa naquela categoria",
                "Sem vínculo conhecido",
                "o caso segue",
                "`folha_mensal` e `alteracao_cadastral`",
            ),
        )
        # A divergência do texto servido acabou: a alteração cadastral aceita o campo.
        assert "o campo vai pelo onboarding" not in guide
        categoria = section_of(
            guide, "## Categoria eSocial que não é de empregado no cadastro (2.13.0)"
        )
        assert not any(token in categoria for token in RESTART)
        if domain in {"ferias", "decimo_terceiro"}:
            assert not any(token in guide for token in RESTART)
    thirteenth = read("decimo_terceiro")
    assert_all(
        thirteenth,
        (
            "o `ano` de `dados_decimo_terceiro` (vale como dezembro)",
            "uma data completa (`AAAA-MM-DD`)",
        ),
    )
    assert "a competência ou o ano de `dados_decimo_terceiro`" not in thirteenth
    termination = read("rescisao")
    assert_all(
        termination,
        (
            "A simulação de rescisão recusa pela mesma regra",
            "`code` `case_simulation_refused`",
            "`reason` `categoria_sem_regime_clt`",
            "na simulação sem caso de origem, a do desligamento hipotético",
        ),
    )


def test_plugin_mirrors_the_release() -> None:
    workflows = flat((OPERATOR / "references/WORKFLOWS.md").read_text(encoding="utf-8"))
    skill = flat((OPERATOR / "SKILL.md").read_text(encoding="utf-8"))
    problems = flat(PROBLEMS.read_text(encoding="utf-8"))
    section = section_of(workflows, "## 2.13.0:")
    assert_all(
        section,
        (
            "**Não há ferramenta nova e não há Refresh do conector**",
            "PRs #441 e #444",
            "`categoria_esocial_nao_suportada`",
            "`categoria_esocial_divergente`",
            "`categoria_sem_regime_clt`",
            "`case_simulation_refused`",
            "`get_documentary_profile`",
            "`apply_case_effects`",
            "`create_company_onboarding`",
            "`apply_company_onboarding`",
            "**Data de efeito (`effective_on`):**",
            "nunca a data do envio",
            "o `ano`, que vale como dezembro, ou uma data completa",
        ),
    )
    assert "Na 2.13.0" in skill and "Sem ferramenta nova e sem Refresh do conector" in skill
    assert "nunca a do envio" in skill
    for code in (
        "categoria_esocial_nao_suportada",
        "categoria_esocial_divergente",
        "categoria_sem_regime_clt",
    ):
        assert code in problems, code
    assert not any(token in section for token in RESTART)
    # Os parágrafos 2.13.0 de operar-loki e de registrar-problema-loki não citam o reinício.
    skill_2130 = skill[skill.index("Na 2.13.0") : skill.index("Na 2.14.0")]
    problems_2130 = problems[problems.index("Na 2.13.0") : problems.index("Na 2.14.0")]
    assert not any(token in skill_2130 + problems_2130 for token in RESTART)


def test_release_history_keeps_the_2130_entry() -> None:
    updates = (ROOT / "docs/MCP_UPDATES.md").read_text(encoding="utf-8")
    entry = section_of(updates, "## Candidata 0.4.39 / contrato, instruções e plugin 2.13.0")
    assert "PR #441" in entry and "PR #444" in entry and "nem Refresh do conector" in entry
    assert not any(token in entry for token in RESTART)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "**provider 0.4.39 / contrato, instruções e plugin 2.13.0**" in readme
