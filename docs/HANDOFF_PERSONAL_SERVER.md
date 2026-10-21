# Retomada do MCP Loki no servidor pessoal — 20/10/2026

Este é o checkpoint da transferência do desenvolvimento do PC Windows para o
servidor pessoal. Não autoriza nova implantação nem migração de hospedagem,
banco, DNS ou sistema financeiro. A produção existente permanece no Coolify
Trabalho. Caminhos privados, credenciais e evidências operacionais ficam fora
deste repositório público.

## Começar pelo estado existente

No servidor, ler primeiro o `AGENTS.md` da raiz IZZI, o mapa operacional já
preparado em `operacao/` e as instruções de cada checkout. O backend pode se
chamar `Project-loki`, enquanto no PC o checkout original se chama
`Project_loki`. Localizar os diretórios reais; não reproduzir caminhos Windows.

Antes de atualizar qualquer checkout, registrar `git status --short --branch`,
HEAD, remotos, upstream e `git worktree list`. Preservar mudanças de outras
sessões. Não executar reset, clean, checkout forçado ou pull sobre trabalho local
sem conciliação. As referências abaixo são checkpoints históricos, não uma
afirmação de que o servidor ou a produção ainda estão nesses commits.

| Repositório | Referência de retomada |
|---|---|
| [MCP_Loki](https://github.com/T0minh0/MCP_Loki) | Branch `feature/dynamic-instructions`; checkpoint anterior a este handoff `d94dbd70eced0a2fad5625cde317c7ce9e1151ab` |
| [Project Loki](https://github.com/T0minh0/Project-loki) | Integração [PR #145](https://github.com/T0minh0/Project-loki/pull/145), **MERGED** |
| Backend integrado e implantado | `c91c145985c2d2bd092486ff01a75ad97fb092ad` |
| Branch histórica de implementação | `feature/mcp-dynamic-updates-20261019`, HEAD `aa6fe610ffd95bea743ad53069c59ae118fccaf6` |
| Build anterior para avaliação de rollback | `f08206ae60f295dce0654343463818978c59758a` |

Os dois checkouts usados por esta tarefa estavam limpos e sem commits adiante
do upstream antes do handoff. O checkout original do backend no PC pertence a
outra frente e possui trabalho próprio; ele não foi substituído ou incorporado.
Não reaplicar o PR #145: a integração já está em `main`.

Para recuperar somente este registro no servidor, depois de conferir o estado:

```bash
git -C MCP_Loki fetch origin feature/dynamic-instructions
git -C MCP_Loki show origin/feature/dynamic-instructions:docs/HANDOFF_PERSONAL_SERVER.md
```

Esse fetch não altera arquivos de trabalho. Se a branch local estiver limpa,
na mesma branch e somente atrás do remoto, atualizar por fast-forward. Caso
contrário, conciliar primeiro. Não trocar a branch de uma sessão em atividade.

## Arquitetura que já existe

O `MCP_Loki` é um pacote Python incorporado ao backend, sem servidor, banco ou
OAuth próprios. O wheel versionado em `vendor/` e o `uv.lock` do Project Loki
fixam a release. O deploy usa o Nixpacks/Coolify existente. Alterar apenas os
Markdowns neste repositório não muda um processo já implantado.

O provider valida Markdown/JSON, hashes, versões e a allowlist de oito domínios:
`geral`, `admissao`, `rescisao`, `ferias`, `decimo_terceiro`, `afastamento`,
`documentos` e `aprovacoes`. Não há pull de Git em runtime nem execução do texto.
Reload inválido conserva o último snapshot válido e sinaliza degradação; sem
snapshot inicial válido, a candidata falha no preflight.

O backend continua responsável por identidade, autorização por conta, empresa,
processo e capacidade, além dos gates humanos. A integração preserva ferramentas
antigas e acrescenta `runtime_instructions` às respostas HTTP de `meu_acesso` e
`get_operator_context`. Acrescenta as ferramentas somente de leitura:

- `loki_obter_instrucoes(dominio="geral", empresa_id=None)`;
- `loki_verificar_versao(client_plugin_version=None, client_contract_version=None)`.

| Identidade da release | Valor |
|---|---|
| Pacote / instruções / contrato de aplicação MCP | `0.1.0` / `1.0.0` / `1.0.0` |
| Wheel SHA256 | `e8295b0da252ba4678eeeaf948c8f060e8daafdbd5fc0142ca4ea77bc80dbd08` |
| Manifest de instruções SHA256 | `ff39a63c78b609cd4001906a17e76149c4401e3d00952b1bf98f93b3e65dc730` |
| Árvore integrada validada | `53a1e30ebffc6a07f2194243fd3f65dcd3451b01` |

A provenance original registra HEAD/tree nulos e `dirty=true`, pois o wheel foi
construído antes do primeiro commit do pacote. Preservar esse registro honesto.
Não reconstruir bytes diferentes sob a versão `0.1.0`. A versão mostrada na
listagem do plugin ChatGPT não comprova a versão do cliente deste contrato;
sem versão declarada, compatibilidade e necessidade de atualização são `null`.

## Evidências e limites dos testes anteriores

| Validação | Resultado observado |
|---|---|
| Provider, Linux | 74 passaram |
| Suíte completa do backend em `b963d93` | 11.737 node IDs únicos: 11.723 passaram, 13 skips, 1 falha |
| Integração PostgreSQL, incluída no total acima | 2.498 passaram, nenhum skip |
| Falha do harness legado do cofre | Reproduzida na base; subprocesso não recebia caminho de importação do kit |
| Módulo corrigido em `aa6fe61` | 24 passaram, 1 skip Windows, sem `PYTHONPATH` externo |
| Combinação com `main` em `f08206a` | 109 passaram, nenhum skip; árvore igual à integrada em `c91c145` |
| Cobertura combinada do backend | 93,51%; mínimo de 80% atendido |
| Ruff / formato / mypy do backend | 1.025 arquivos / 1.025 arquivos / 865 arquivos; gates de PII e prosa passaram |
| Novos testes de instruções no backend, incluídos na suíte | 47: 34 unitários e 13 de integração |

Os 27 subtests registrados no JUnit não são outros 27 node IDs. Não somar
reexecuções e seleções ao total da suíte. O XML original que contém a falha foi
preservado. Não restaram falhas observadas depois da correção e reexecução do
módulo, mas **a suíte completa não foi repetida sobre `aa6fe61` ou `c91c145`**.
A seleção de 109 testes não substitui essa medição. Consulte
[HOMOLOGATION.md](HOMOLOGATION.md) para o contexto dos candidatos.

A sessão de preparação do servidor informou adicionalmente 74 testes do MCP e
100 testes selecionados do Loki aprovados, além do build do MCP. Esses números
são de outro ensaio e não se somam à suíte acima; conferir seus registros no
servidor. A CI remota do backend ficou pendente por orientação do usuário devido
ao bloqueio de billing. Não tratá-la como aprovada, não contornar proteções e
não reabrir essa cobrança como pré-requisito desta retomada.

## Publicação e piloto observados

A implantação autorizada terminou em 20/10/2026 às 20:23:05 UTC. O health
posterior confirmou `c91c145`, schema `0041`, calculador `rescisao-v22` e
snapshot válido das instruções `1.0.0`. Ambiente e OAuth foram preservados;
esta feature não adicionou migration. A conta autenticada já era proprietária e
ativa, sem necessidade de concessão de acesso. Não houve operação em empregados,
casos ou documentos. O healthcheck nativo do Coolify continuou desabilitado;
a conferência foi externa. Detalhes em [PRODUCTION_RELEASE.md](PRODUCTION_RELEASE.md).

Depois, o usuário relatou este resultado real no outro dispositivo:

```json
{
  "backend_build": "c91c145985c2d2bd092486ff01a75ad97fb092ad",
  "instructions_version": "1.0.0"
}
```

Relatou também leitura das instruções `rescisao`, versão `1.0.0`, pelo fallback
de `meu_acesso`, sem alteração de dados. **`loki_obter_instrucoes` não estava
disponível naquela conexão.** Isso valida, conforme relato do piloto, o caminho
aditivo antigo; não comprova atualização do catálogo nem aceite das quatro
contas. Não registrar o login Google como observado diretamente pelo agente.

## Próximo trabalho: catálogo e migração individual

1. Reconferir o estado atual dos repositórios e, por leitura, build/schema/hash
   implantados. Comparar com este checkpoint sem rebaixar uma release posterior.
2. Identificar o tipo real de instalação em **Gerenciar** no ChatGPT e a fonte
   do pacote. A captura recebida mostra apenas nome, autor e versão da listagem;
   não mostra a configuração. A fonte do ZIP/manifest ChatGPT não foi localizada.
3. Usar o mecanismo apropriado ao tipo de conexão: atualização de catálogo de
   MCP direto ou nova varredura/revisão do servidor no portal do plugin. Consultar
   a documentação oficial atual e a interface real antes de orientar cliques.
   Não há comando de refresh/rescan disponível nas ferramentas de gerenciamento
   expostas nesta sessão. Não desinstalar a conexão funcional para experimentar.
4. Em conversa nova, selecionar o Loki e testar somente leituras: `meu_acesso`,
   versão, instruções gerais e `rescisao`, quando autorizada. Se as ferramentas
   novas continuarem ausentes, registrar a ausência e usar o fallback existente;
   não simular sua invocação nem exigir outro deploy sem diagnóstico.
5. Registrar cada uma das quatro contas separadamente em evidência privada:
   identidade autorizada, escopo, build, versão/hash, catálogo e consultas.
   Validar recusas em ambiente sintético; não criar casos reais para o aceite.
   Ausência de acesso não autoriza ampliar permissões.
6. Atualizar pacote/skill somente se a instalação realmente precisar do novo
   bootstrap. Preferir uma única atualização inicial, se necessária, seguida
   de instruções centralizadas. Não inventar manifest nem declarar sincronização
   entre contas individuais.

Não há justificativa técnica observada para um novo deploy apenas porque uma
ferramenta nova ainda não apareceu no catálogo do cliente. O fallback já obtém
conteúdo do servidor quando a consulta antiga é invocada. Nenhuma instrução
garante que o modelo chamará uma ferramenta.

## Atualizações futuras e limites da transferência

Procedimento: editar domínio/metadados/hashes, subir versões apropriadas,
validar, construir e promover novo wheel imutável para o backend, revisar o
lock e a integração, testar e preparar PR. O fluxo detalhado e a tabela de
ações manuais estão em [MCP_UPDATES.md](MCP_UPDATES.md). Texto e comportamento
compatíveis chegam por deploy e nova consulta, sem novo ZIP. Mudança de
schema, skill/manifest instalado, helper ou contrato incompatível pode exigir
atualização individual. O rollback restaura backend/wheel/lock compatíveis com
o schema; não restaura permissões nem reescreve dados para voltar instruções.

A `main` do backend possui auto-deploy existente. Preparar/revisar alterações
não autoriza merge, push em `main`, nova implantação ou rollback em produção.
Nunca copiar tokens, `.env`, cookies, clientes OAuth ou documentos do PC para
Git/chat. Provisionar acessos no servidor pelo mecanismo seguro já adotado.

As evidências originais do PC ficam em `var/mcp-updates/` no worktree de
integração, ignoradas pelo Git. Há arquivos de ambiente nesse diretório:
**não copiá-lo inteiro**. Um pacote privado com lista explícita de relatórios,
JUnit e hashes pode preservar a auditoria; ele não é necessário para obter o
código ou este handoff pelo Git. Recebimento de conversa não transfere arquivos,
volumes Docker ou credenciais automaticamente. Conferir qualquer cópia por hash.

Os serviços locais de homologação não são produção. Não apagar volumes ou
parar recursos de outras sessões. Não ativar o runner Shadow legado, agendas
ou integrações ao sistema financeiro como parte desta retomada do MCP; essas
frentes têm suas próprias sessões e instruções no servidor.
