# Preparação no Coolify Trabalho — 20/10/2026

O pacote está publicado em [T0minh0/MCP_Loki](https://github.com/T0minh0/MCP_Loki),
branch padrão `feature/dynamic-instructions`, commit inicial `c0af9ed`.
A [CI desse commit](https://github.com/T0minh0/MCP_Loki/actions/workflows/ci.yml)
terminou com sucesso. A integração do consumidor foi publicada no PR draft #145
do Project Loki, agora em `aa6fe61`, sobre a base `3ff2533`. Esse commit posterior
altera somente um teste; o runtime continua igual ao candidato `b963d93`.
Não houve merge.
O [relatório de homologação](HOMOLOGATION.md) registra a validação local posterior.

## Organização escolhida

A preparação reutiliza a aplicação **Project Loki**, dentro do projeto **Izzi**,
na instância **trabalho** do Coolify. `MCP_Loki` é uma biblioteca incorporada ao
backend; seu repo não contém servidor independente, porta HTTP ou banco.

Não foi criada uma aplicação fictícia apontando o Nixpacks para essa biblioteca.
O código implantável continua em `T0minh0/Project-loki`, branch `main`, com build
Nixpacks e comandos delegados ao `nixpacks.toml` versionado. Depois de incorporar a
integração revisada, esse arquivo instala o extra `mcp-updates` e valida o snapshot
antes das migrations.

## Configuração aplicada e verificada

Foi usado o cliente/API local já configurado para o contexto `trabalho`. O MCP
Coolify não estava exposto no catálogo desta sessão; não foi necessário instalar
outro plugin ou copiar credenciais para o projeto.

| Campo | Resultado conferido pela API |
|---|---|
| Descrição da aplicação | Identifica `Project Loki + MCP_Loki` e o repo da biblioteca |
| `health_check_path` | `/healthz` |
| `include_source_commit_in_build` | `true`, para incluir a origem no próximo build |
| `instant_deploy` enviado no PATCH | `false` |

O healthcheck nativo permanece desabilitado, conforme a configuração existente.
Alterar o caminho não comprova monitoramento nativo ou saúde do serviço. O efeito
da opção de commit deverá ser conferido no próximo build autorizado e na resposta
de versão; não se atribui uma nova versão ao container já existente.

Depois do PATCH, as leituras da API confirmaram que repositório, branch, domínio,
porta, comandos, status, rede e configurações de preview/auto-deploy permaneceram
iguais. Os valores de variáveis de produção e preview também permaneceram iguais;
nenhum valor sensível foi impresso ou incluído neste documento. O histórico de
deploy da aplicação não mudou. Não houve start, restart ou deploy.

Um registro privado em `var/mcp-updates/coolify-preparation-20261020.json` no
worktree consumidor conserva os campos anteriores e posteriores e o payload de
rollback. Essa pasta é ignorada pelo Git; o registro não contém tokens ou valores
de variáveis. O helper privado admite somente consultas GET e PATCH dessa
aplicação, sem endpoint de deploy.

## Pendências para ativar as instruções

1. Revisar o PR consumidor #145, wheel, proveniência e lock. Não apontar a aplicação
   para o repo da biblioteca. O artefato atual foi
   construído antes do commit inicial da fonte; sua proveniência registra esse
   fato e não deve ser reescrita como se tivesse sido produzida pela CI publicada.
2. A CI remota do backend não iniciou as etapas por cobrança/limite de gastos da
   conta GitHub. Por orientação explícita do usuário, ela fica pendente; o workflow
   e suas proteções foram preservados. O ensaio isolado posterior usa Docker local,
   rede e banco novos, chaves próprias e OAuth sintético. Não criou staging no
   Coolify, não copiou banco e não validou login Google ou contas ChatGPT reais.
   Conferir os resultados e os limites em [HOMOLOGATION.md](HOMOLOGATION.md).
3. Obter autorização explícita antes de integrar/deployar em produção.
   **O auto-deploy da branch `main` já estava ativo e foi preservado:** um merge
   no consumidor pode disparar o webhook existente. A autorização precisa vir
   antes desse merge, não somente antes de apertar um botão no Coolify.
4. No lançamento autorizado, verificar build, `/healthz`, `release_sha256` e
   versões pela ferramenta autenticada. O último deploy observado durante o PATCH
   de preparação era `64d8e02`; isso é um registro daquele instante, não uma leitura
   atual de produção. A feature deste PR não foi implantada por esta tarefa.
5. Validar uma conta ChatGPT piloto e depois as outras três, conforme o
   [checklist individual](MCP_UPDATES.md#checklist-das-quatro-contas-individuais).
   Refresh de catálogo e atualização inicial da skill continuam condicionados ao
   que for observado em cada instalação.

## Recuperação da configuração

O registro privado contém o `rollback_patch` anterior para descrição, caminho de
healthcheck e opção de commit no build. Se necessário, aplicar somente esses
campos com `instant_deploy=false` e reler a aplicação. Esse rollback de metadados
não restaura código nem imagens. O [rollback de release](MCP_UPDATES.md#rollback)
continua restaurando o conjunto backend/wheel/lock, sem alterar OAuth ou dados.
