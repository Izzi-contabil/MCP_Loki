# Homologação técnica local — 20/10/2026

A integração está publicada no PR draft #145 do Project Loki, branch
`feature/mcp-dynamic-updates-20261019`. A suíte completa e a aplicação isolada
mediram `b963d93ce60f9f10c5db8c20e053fa1b039445ac`, sobre a base `3ff2533`.
O PR recebeu depois `aa6fe610ffd95bea743ad53069c59ae118fccaf6`: somente o teste
do subprocesso do cofre mudou; todos os arquivos de runtime continuam idênticos.
Não houve merge nem deploy em produção. O preparo de metadados no Coolify está
em [COOLIFY_PREPARATION.md](COOLIFY_PREPARATION.md).

A CI remota do backend não iniciou jobs por cobrança/limite de gastos na conta
GitHub. O usuário orientou deixá-la pendente. Nenhum check foi marcado como
aprovado, nenhum workflow foi desabilitado e nenhuma proteção foi contornada.
Os resultados abaixo são de execução local Linux, não do GitHub Actions.

## Candidato e compatibilidade

O wheel incorporado permanece imutável: `mcp-loki-updates` `0.1.0`, digest SHA256
`e8295b0da252ba4678eeeaf948c8f060e8daafdbd5fc0142ca4ea77bc80dbd08`.
Os membros do pacote conferem com o commit da fonte `c0af9ed` e com os membros do
artefato da CI da fonte. O ZIP produzido no Linux tem metadados de plataforma
diferentes do ZIP original Windows; seus arquivos internos são idênticos.
O artefato original não foi substituído nem atribuído retroativamente àquela CI.

O baseline inicial `mcp_contract_64d8e02_masked.json` foi preservado. Um segundo
snapshot captura os descritores de `3ff2533`, sem esta feature. Os testes exigem
os descritores dessa base e somente as duas consultas HTTP aditivas. A comparação
histórica distingue as evoluções upstream dos PRs #141/#142/#144. Nenhum contrato
antigo é removido por esta integração. Os 34 unitários de instruções/contratos
passaram após o rebase; alterar o tipo de `get_case.case_id` produziu duas falhas
esperadas, uma por transporte, e restaurar o descritor voltou a passar.

## Ensaios Linux do backend

Os checkouts descartáveis são criados pelo Git no Linux e fixam o candidato acima.
Antes de executar, a conferência dos 1.178 arquivos rastreados exige igualdade
byte a byte com os blobs do commit, inclusive o CMD com CRLF preservado no Git.
Cópias intermediárias vindas do Windows foram descartadas por diferenças de fim
de linha; suas execuções interrompidas não compõem o resultado final.
O ambiente tem Python 3.11, `uv`,
Poppler, `ssh-keygen` e `make`. O Postgres 16 dedicado contém somente fixtures
sintéticas. A instalação usa `uv sync --frozen --extra dev --extra mcp-updates`,
confere `uv lock --check`, carrega o provider e aplica as migrations no banco de
teste. O schema `0041` já pertence à base; esta feature não adiciona migration.

| Verificação | Resultado |
|---|---|
| Regressões PostgreSQL estruturadas, conforme workflow do candidato | 155 passaram |
| Todos os grupos de integração | 2.498 passaram, sem skips |
| Suíte completa do candidato original | 11.737 cenários: 11.723 aprovações, 13 skips e uma falha no teste legado descrito abaixo |
| Cobertura combinada, mínimo de 80% imposto ao consolidado | 93,51%: 36.603 de 39.145 instruções Python cobertas |
| Testes novos de instruções/contratos dentro da suíte completa | 47 passaram: 34 unitários e 13 de integração |
| Ruff e formatação | Passaram; 1.025 arquivos já formatados |
| Mypy | 865 arquivos sem erros |
| Gates de PII/prosa e `outputs/` | Passaram; 1.178 arquivos versionados sem achados de PII |
| Módulo do teste do cofre após correção | 24 passaram; 1 exclusivo do Windows pulado no Linux |
| Combinação prospectiva com `main` `f08206a` | 109 passaram, sem skips, nos módulos afetados e nas instruções dinâmicas |

As etapas seguem `.github/workflows/ci.yml` do candidato e usam
`uv run --no-sync`. A coleta fixou 11.737 cenários: 2.498 de integração e 9.239
unitários. A primeira execução serial foi interrompida após 500 aprovações devido
à duração; seu XML foi preservado como execução interrompida e não integra o
resultado final. A execução completa local foi distribuída em seis grupos de
arquivos de integração e um grupo unitário, sem sobreposição, com diretório e
Postgres próprios. Cada grupo produziu JUnit e dados de cobertura; o consolidado
conferiu os 11.737 node IDs sem omissão ou repetição e impôs a cobertura mínima
de 80% à combinação dos dados dos grupos e da reexecução do módulo corrigido.
Essa distribuição é uma adaptação local, não uma execução do GitHub Actions.

Os unitários originais registraram 9.225 aprovações, 13 skips e uma falha; os
2.498 testes de integração passaram. Os 13 skips correspondem a 12 testes
dependentes de Windows e um teste de bloqueio de leitura por permissões,
inaplicável ao usuário do container. Esses cenários não foram exercitados nesta
rodada Linux. Também passaram 27 subtestes internos: o JUnit os soma ao atributo
`tests`, sem criar novos elementos `testcase`. O consolidador preserva as duas
contagens e não os trata como novos node IDs da coleta.

A execução original encontrou falha no teste legado
`test_vault_lock_serializes_processes_and_releases_after_exit`: o subprocesso
não recebia o caminho Python configurado pelo pytest, falhando ao importar o kit.
O mesmo teste, com bytes idênticos, também falhou na base `3ff2533`; fornecer o
caminho ao subprocesso fez o controle passar. O ajuste em `aa6fe61` transmite
`sys.path` por `PYTHONPATH` apenas nesse teste, sem alterar o cofre ou suas
asserções de exclusão mútua e liberação após saída do processo.

O módulo completo corrigido foi reexecutado em outro clone Linux, sem
`PYTHONPATH` externo: 24 aprovações e o skip Windows esperado. Ruff passou; mypy
sem cache incremental passou nos 865 arquivos. Uma tentativa incremental havia
acusado um atributo ausente em `cli.main()`; análise fresca não reproduziu esse
erro, e essa chamada não foi modificada. Os logs das tentativas foram mantidos.
O relatório original da suíte completa não é reescrito para apagar sua falha;
a revalidação do módulo corrigido tem XML e hash próprios.
Não restaram falhas observadas após essa revalidação. A suíte inteira não foi
repetida sobre `aa6fe61`: a única diferença é o módulo de teste reexecutado,
conferido por hash; todos os outros arquivos versionados permanecem iguais.

Durante a medição, `main` avançou para `f08206a` pelo PR #146, de histórico de
férias. A combinação com `aa6fe61` não apresentou conflito e foi exercitada
somente em outro clone Linux: os três módulos de histórico afetados e os dois
módulos de instruções somaram 109 aprovações, sem skips. Lock, preflight e schema
também passaram. A árvore combinada foi
`53a1e30ebffc6a07f2194243fd3f65dcd3451b01`; seus pais e JUnit estão nos artefatos
privados. Não houve merge na branch publicada ou em `main`. Essa seleção
adicional não é uma repetição da suíte completa sobre `f08206a`.

A suíte estruturada é repetida dentro da suíte completa; não somar os dois totais
como testes distintos. Os relatórios JUnit, plano de distribuição e registro do
candidato ficam em `var/mcp-updates/pr-validation-20261020/` do worktree
consumidor, ignorados pelo Git.

## Aplicação isolada em funcionamento

A homologação técnica usa uma rede Docker própria, um Postgres novo sem porta
publicada e uma aplicação disponível somente em `127.0.0.1:55448`. A rede contém
apenas essa aplicação e seu banco. As chaves foram geradas para o ensaio; não
foram copiadas credenciais, bancos ou dados de produção. O diretório de código
e os volumes são distintos dos usados pela CI local e pelo sistema operacional.

A instalação da aplicação usa `uv sync --frozen --no-dev --extra mcp-updates`
em `/opt/venv`, preflight do provider, migrations e Uvicorn. Isso exercita o
conector real com configuração `APP_ENV=homolog`; não introduz bypass de login.
Aprovação pelo chat, publicação, notificações e onboarding estão desabilitados;
integrações externas estão em modo mock. Os cadastros Google/MCP usam identidades
e origens reservadas de teste, sem conexão com Google real.

| Leitura | Resultado observado |
|---|---|
| `/healthz` | HTTP 200, `status=ok`, build do candidato, schema `0041` |
| Instruções no health | `1.0.0`, snapshot disponível, status `ok` |
| Manifest SHA256 | `ff39a63c78b609cd4001906a17e76149c4401e3d00952b1bf98f93b3e65dc730` |
| Metadados OAuth e protected resource | HTTP 200, origem sintética correta, PKCE S256, sem cadastro dinâmico de clientes |
| Inicialização MCP sem credencial | HTTP 401, desafio de recurso presente |
| Banco de homologação | Zero empresas, funcionários, casos e contas do conector |
| Reinício do container da aplicação | Mesmos build, schema e hash; health e recusa anônima voltaram a passar |

As leituras e a inspeção de rede/portas ficaram em
`var/mcp-updates/homologacao-20261020/smoke-results.json` do consumidor.
Arquivos de ambiente e chaves ficam nesse diretório privado e nunca devem ser
anexados ao PR, publicados ou usados como configuração de produção.

Esse ensaio não representa staging no Coolify, teste do login Google real,
aceite de operadores ou refresh do catálogo das quatro contas ChatGPT.

## Pendências antes do lançamento

1. Revisar o PR e o conjunto backend/wheel/lock. Preservar o draft enquanto o
   lançamento não estiver autorizado. A CI remota continua pendente.
2. Se for necessário staging remoto com Google/ChatGPT reais, provisioná-lo como
   ambiente autorizado, com rede/banco/segredos e cliente OAuth próprios. Criar
   somente um environment no Coolify não prova isolamento de rede.
3. Obter autorização explícita de produção **antes do merge**: o auto-deploy de
   `main` já estava ativo. Registrar a imagem/build anterior para rollback do
   conjunto e conferir compatibilidade com o schema implantado, incluindo mudanças
   da base. Não fazer downgrade de banco nem alterar tokens, permissões ou dados
   como forma de voltar instruções.
4. Após o lançamento autorizado, conferir build, schema, hash e versões no health
   e em `loki_verificar_versao`, usando a identidade individual autorizada.
5. Validar uma conta piloto e depois as outras três conforme o
   [checklist por conta](MCP_UPDATES.md#checklist-das-quatro-contas-individuais).
   Primeiro observar `meu_acesso` e seu `runtime_instructions` com as tools antigas.
   Atualizar o catálogo individualmente se as tools novas não aparecerem. Atualizar
   a skill/pacote inicial somente se a instalação precisar do bootstrap novo.

Mudanças futuras de conteúdo ou backend que preservem os contratos utilizados
chegam após promoção revisada e deploy do servidor, seguidos de nova consulta.
Mudanças em skill/manifest importado, helpers locais, endereço da integração,
schema de ferramenta ou contrato incompatível podem exigir ação individual e,
conforme o pacote afetado, novo ZIP. Não há sincronização entre contas nem
garantia de que uma instrução provoque a chamada de ferramenta.
