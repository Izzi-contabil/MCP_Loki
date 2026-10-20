# Entrega local — MCP Loki

A entrega inicial preparou a implementação em dois repositórios locais, sem
implantação, alteração de contas ou uso de dados reais. Em 20/10/2026, o remoto da
fonte já está publicado e a CI de `c0af9ed` passou; os metadados do recurso existente foram
preparados no Coolify conforme [o registro específico](COOLIFY_PREPARATION.md).
O PR consumidor #145 foi integrado, após autorização explícita, no build
`c91c145` e publicado pelo Coolify. O [registro de produção](PRODUCTION_RELEASE.md)
confirma health e acesso autenticado; login no outro dispositivo e aceite das
quatro instalações continuam pendentes. A validação
posterior está registrada em [HOMOLOGATION.md](HOMOLOGATION.md); a CI remota do
backend fica pendente por orientação do usuário.

## Onde está o trabalho

| Local | Estado |
|---|---|
| `Izzi/MCP_Loki` | Git independente publicado em `T0minh0/MCP_Loki`, branch `feature/dynamic-instructions`, commit inicial `c0af9ed` |
| `<perfil-do-operador>/.local/izzi-worktrees/mcp-dynamic-updates-20261019` | Integração no Loki, branch `feature/mcp-dynamic-updates-20261019`, PR #145 integrado em `c91c145`; candidato preservado `aa6fe61` |
| `Izzi/Project_loki` | Checkout original em `0742bfcb`; alterações preexistentes preservadas |

O checkout original era anterior ao conector atual. Por isso, a integração foi
feita em worktree registrado, a partir de `origin/main`, sem transplantar código
novo para a branch de rescisão antiga. Os arquivos de orientação da raiz IZZI
receberam o link para `MCP_Loki`.

## Arquitetura entregue

`MCP_Loki` é uma biblioteca Python de dados e metadados, incorporada ao conector
existente por wheel local revisado e fixado no `uv.lock`. Não é outro servidor,
banco ou serviço OAuth. Git versiona a fonte; revisão e deploy do backend levam
o snapshot até o servidor; chamadas MCP autenticadas consultam o conteúdo atual.

O provider atende os domínios `geral`, `admissao`, `rescisao`, `ferias`,
`decimo_terceiro`, `afastamento`, `documentos` e `aprovacoes`. Markdown contém
orientação técnica e aponta os contratos do runtime para processos incompletos.
JSON declara versão, data, compatibilidade e requisitos de acesso. O manifest
fixa hashes dos arquivos. O carregamento valida o snapshot inteiro antes de
aceitá-lo e conserva a última versão válida em memória se um reload falhar.

O conector conserva Google OAuth/PKCE, sessões e autorização persistida. A cada
consulta, relê a conta e confere empresa, processo e capacidade na mesma combinação
de escopo. Instruções não autorizam operações, aprovação, publicação ou pagamentos.
O domínio geral não exige capacidade operacional; instruções restritas e suas
versões são filtradas. Metadados não incluem empregados, tokens ou URLs assinadas.

| Superfície | Resultado |
|---|---|
| `loki_obter_instrucoes(dominio="geral", empresa_id=None)` | Conteúdo autorizado, versão, data, compatibilidade e requisitos; domínio inválido ou acesso recusado gera erro explícito |
| `loki_verificar_versao(client_plugin_version=None, client_contract_version=None)` | Backend/build, contrato, instruções, versões autorizadas por domínio, alterações e comparação das versões declaradas |
| `meu_acesso` e `get_operator_context` HTTP | Campos antigos preservados; novo campo aditivo `runtime_instructions` leva conteúdo e versão a clientes que já consultam essas ferramentas |
| `/healthz`, com conector habilitado | Campo aditivo `dynamic_instructions`; snapshot degradado resulta em HTTP 503 |

Sem versão conhecida do cliente, compatibilidade e necessidade de atualização
manual permanecem desconhecidas. O servidor não detecta instalação nem refresh
do catálogo ChatGPT. A fixture de contrato anterior compara os descritores das
ferramentas HTTP e stdio; assinaturas antigas foram preservadas.

O provider fica nos extras `mcp-updates` e `dev`. A instalação base, o exportador
assinado desktop e o stdio não dependem dele. Nixpacks conserva seu bootstrap
Python com `...`, depois instala o extra remoto. A CI instala os extras com lock
congelado e usa `uv run --no-sync`. Não há migration nova nem mudança de OAuth.

## Arquivos entregues

Na fonte `MCP_Loki`:

- `src/mcp_loki_updates/provider.py`, `__init__.py` e `py.typed`;
- `src/mcp_loki_updates/data/release.json` e os pares JSON/Markdown dos domínios;
- `scripts/promote.py`, para promoção local validada, sem executar código do wheel;
- `plugins/loki-bootstrap/SKILL.md` e `README.md`, com orientação mínima;
- `tests/test_provider.py`, `test_versions.py`, `test_release_masked.py` e
  `test_repository_masked.py`;
- `pyproject.toml`, `uv.lock`, `.gitattributes`, `.gitignore`, `AGENTS.md`,
  `.github/workflows/ci.yml` e `README.md`;
- `docs/IMPLEMENTATION.md`, `docs/MCP_UPDATES.md`, `docs/COOLIFY_PREPARATION.md`,
  `docs/HOMOLOGATION.md`, `docs/PRODUCTION_RELEASE.md` e este relatório.

No worktree do Project Loki:

- `src/loki/connector/instructions.py` — integração, ferramentas e autorização;
- `src/loki/connector/operations.py` — fallback aditivo nas consultas antigas;
- `src/loki/connector/server.py` — bootstrap curto e registro aditivo;
- `src/loki/main.py` — health condicionado ao conector;
- `pyproject.toml`, `uv.lock`, `nixpacks.toml` e `.github/workflows/ci.yml`;
- `vendor/mcp_loki_updates-0.1.0-py3-none-any.whl` e seu `.provenance.json`;
- `tests/fixtures/mcp_contract_64d8e02_masked.json` e
  `tests/fixtures/mcp_contract_3ff2533_masked.json`, preservando o baseline inicial;
- `tests/unit/test_dynamic_instructions_masked.py`;
- `tests/integration/test_dynamic_instructions_masked.py`;
- `tests/integration/test_connector_http_masked.py` — expectativa de catálogo
  pendente atualizada para incluir somente as novas consultas de metadados;
- `tests/unit/test_kit_https_auth_masked.py` — transmite o caminho Python ao
  subprocesso do teste legado de exclusão mútua do cofre;
- `docs/MCP_UPDATES.md` — runbook no consumidor.

## Identidade do artefato

| Item | Valor |
|---|---|
| Pacote | `mcp-loki-updates` `0.1.0` |
| Instruções / primeiro contrato formal | `1.0.0` / `1.0.0` |
| Plugin mínimo / recomendado | `0.4.0` / `0.5.0` |
| SHA256 do wheel | `e8295b0da252ba4678eeeaf948c8f060e8daafdbd5fc0142ca4ea77bc80dbd08` |
| SHA256 do manifest de instruções | `ff39a63c78b609cd4001906a17e76149c4401e3d00952b1bf98f93b3e65dc730` |

O recomendado `0.5.0` não é alegação de pacote ChatGPT publicado. A proveniência
registra HEAD/tree nulos e árvore suja porque o artefato foi construído antes do
primeiro commit da fonte; a publicação posterior não reescreve essa evidência.
Hash e proveniência local não são assinatura de release nem prova de implantação.

## Validação inicial executada

Os testes usaram fixtures sintéticas e Postgres descartável dedicado. Nenhum
teste apontou para o banco operacional ou alterou funcionário/processo real.

| Escopo | Resultado observado |
|---|---|
| Provider, versões, promoção e snapshot dos bytes do índice Git — Linux | 74 passaram |
| Mesma suíte — Windows | 73 passaram; 1 pulado por falta de privilégio de symlink, coberto no Linux |
| Conector — Linux: unit novo, integração nova e regressões OAuth/acesso/HTTP/operações/versões/onboarding | 124 passaram |
| Gerador assinado desktop — Linux | 96 passaram; teste de Makefile passou em execução posterior após instalar `make` no container descartável |
| Unit novo após separação dos extras — Windows | 30 passaram |
| Regressões selecionadas de configuração, MCP/principal, compatibilidade e distribuição do plugin, browser, arquivos, intake e UI de versão — Windows | 345 passaram |
| Ruff no consumidor | Lint e formatação da árvore inteira passaram |
| Mypy no consumidor | 852 arquivos passaram |
| Ruff e Mypy na fonte | Lint/formatação e tipos de `src`/`scripts` passaram |
| Gates de repositório | PII: nenhum achado no consumidor ou na fonte; prosa do consumidor sem contradição derivável; verificação de `outputs/` sem vazamento |
| Ablações do host | Guardas exercitadas produziram RED antes/restauraram GREEN após correção; inclui escopo, revogação, fallback, versão, health e configuração |
| Plano Nixpacks e instalação real dos comandos gerados | Nixpacks `1.41.0`, uv `0.4.30`, venv `/opt/venv`: instalação base + extra e smoke do provider passaram |

A execução Linux combinada registrou `187 passed, 34 skipped`; as recusas de
execução eram falta de `ssh-keygen`/`make` na imagem de teste. Depois de instalar
essas ferramentas somente no container descartável, a repetição registrou
`126 passed, 1 skipped` (incluindo novamente as 30 unit do conector), seguida de
`1 passed` para o teste de Makefile. Não somar essas execuções como casos distintos.

Comandos principais na fonte: `uv sync --locked --all-extras --no-editable`,
`uv run --no-sync pytest`, `uv run --no-sync ruff check .`,
`uv run --no-sync ruff format --check .`, `uv run --no-sync mypy src scripts`,
`uv build --wheel`, instalação do wheel em venv isolado e smoke fora do fonte.

No consumidor, o ensaio Linux executou:

```text
uv sync --frozen --extra dev --extra mcp-updates
uv run --no-sync pytest -q
  tests/unit/test_dynamic_instructions_masked.py
  tests/unit/test_operator_release.py
  tests/integration/test_dynamic_instructions_masked.py
  tests/integration/test_connector_access_masked.py
  tests/integration/test_connector_oauth_masked.py
  tests/integration/test_connector_http_masked.py
  tests/integration/test_connector_operations_masked.py
  tests/integration/test_connector_operational_versions_masked.py
  tests/integration/test_company_onboarding_connector_masked.py
```

Esse bloco enumera argumentos de uma única chamada, quebrados por legibilidade.
XMLs completos ficaram no clone descartável de validação, fora do repo entregue.
O teste do deploy executa o preflight com snapshot válido e inválido antes de
qualquer migration. O ensaio real Nixpacks executou apenas instalação e smoke;
não executou start, migrations ou implantação.

Na entrega inicial, a suíte completa do Project Loki com cobertura mínima e a CI
consumidora estavam pendentes. A retomada de 20/10/2026 está registrada em
[HOMOLOGATION.md](HOMOLOGATION.md). A CI GitHub da fonte publicada passou, conforme
o registro do preparo Coolify. As suítes selecionadas não certificam produção.
Regressões com leitura segura POSIX falharam no Windows e passaram no ensaio Linux;
não foi enfraquecido o leitor seguro para fazê-las passar no Windows.

Na primeira conferência de 20/10/2026, os membros do pacote no wheel coincidiram
com a fonte, o digest do arquivo conferiu com a proveniência e o snapshot carregou
os domínios esperados com health `ok`. Os XMLs dos ensaios anteriores foram relidos.
Docker estava indisponível naquele momento e voltou posteriormente. Os resultados
Linux desta seção são históricos; as novas execuções e a homologação local estão
em [HOMOLOGATION.md](HOMOLOGATION.md), sem atestar disponibilidade de produção.

## Atualizações futuras e lançamento

O [runbook](MCP_UPDATES.md) contém atualização de conteúdo, hashes, SemVer,
adição de domínio, evolução de ferramentas, tabela deploy/ZIP/ação do usuário,
rollback e checklist individual das quatro contas.

Para as próximas releases:

1. Revisar o PR consumidor e os resultados locais registrados. A CI remota
   ficou pendente por orientação do usuário. Não criar pull de código não revisado
   no servidor; observar o auto-deploy de `main` antes de integrar o PR.
2. Promover o wheel validado, versionado e imutável para `vendor/`; manter pin e
   lock correspondentes no consumidor. Releases futuras precisam de versão nova.
3. Usar o ensaio técnico local como evidência delimitada; validar login Google e
   conexão ChatGPT reais em ambiente autorizado. Conferir build real, health,
   hashes e ferramenta de versão autenticada.
4. Somente após autorização explícita, implantar com o Coolify existente e
   preservar o build anterior para rollback do conjunto backend/wheel/lock.
5. Validar uma conta piloto e depois as demais. Observar chamadas antigas,
   conteúdo dinâmico, escopo permitido e recusa fora dele, sem remover conexões ou
   revogar credenciais como parte desta migração.

Para mudanças de texto ou backend remoto que preservem contratos, futuras
atualizações exigem nova release/deploy do servidor e nova consulta, sem novo ZIP.
Ferramenta/schema novo pode exigir Refresh individual e nova conversa. Alterar
skill importada, manifest, endereço, helpers locais ou runtime desktop pinado
segue atualização manual do pacote e sua política de assinatura.

A fonte do manifest/pacote ChatGPT instalado nas quatro contas não foi encontrada.
O bootstrap foi preparado como guia mínimo; não foi inventado um manifest nem
alterado o kit desktop para simular atualização ChatGPT. Clientes que já consultam
as ferramentas antigas podem receber o conteúdo por elas sem redistribuição.
Se a orientação estática da instalação precisar mudar, poderá ser necessária uma
atualização manual inicial. Essa necessidade deve ser observada na conta piloto.
Não há sincronização entre contas, refresh comprovado ou garantia de invocação
automática de ferramentas nesta entrega.
