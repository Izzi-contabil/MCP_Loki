# Ana e Samuel — instalar uma vez e receber atualizações pelo Claude


Contrato operacional vigente: plugin/instruções2.0.1 e provider0.2.1.
Consulte `get_process_contract` e envie `receive_case_data` com fontes, referência
estável e o `input_snapshot` atual de `get_case`. Leitura e comparação são externas;
a empresa de teste usa o mesmo fluxo e gates. Atualização, catálogo e execução
no operador exigem comprovação própria; preserve OAuth e a agenda existente.

**Ana:** Claude Code no Mac. **Samuel:** Claude Code no Windows e no Linux;
repetir a configuração em cada máquina. O plugin usa o MCP e o OAuth que vocês
já têm. A atualização fica por conta do próprio Claude Code.

**A partir da versão1.1.0, o mesmo plugin inclui os leitores locais.** A harness
lê/confere os documentos e envia dados estruturados e fontes pela conexão existente.
Originais e imagens ficam no computador. O nome `loki-orientacoes` foi mantido
para atualizar instalações anteriores sem reinstalar ou refazer OAuth.

## Pré-requisito dos leitores: uv

Instalar `uv` uma única vez, se `uv --version` não funcionar. Não é necessário
instalar Python nem clonar o backend: o uv prepara Python3.11 e as dependências
fixadas pelo lock do plugin na primeira execução.

Mac, se já usa Homebrew:

```text
brew install uv
```

Windows, no PowerShell:

```text
winget install --id astral-sh.uv -e
```

Linux, ou Mac sem Homebrew (instalador oficial):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reabrir o terminal/Claude depois da instalação. Requisitos e formatos:
[leitores locais](LOCAL_READERS.md). O helper usa bibliotecas portáveis; não
depende de Poppler, Office, LibreOffice ou Tesseract instalado no sistema.

## 1. Confirmar acesso ao GitHub

Depois que Antônio liberar a leitura do repositório privado `T0minh0/MCP_Loki`,
abrir o terminal que já usa para o Claude Code. São necessários Git, GitHub CLI
(`gh`) e Claude Code atualizado. Executar com sua conta pessoal:

```text
gh auth login --hostname github.com --web --git-protocol https
gh auth setup-git
gh repo view T0minh0/MCP_Loki --json nameWithOwner,visibility
```

Se a conta já estiver autenticada, basta conferir o acesso e executar
`gh auth setup-git`. O Git usa a credencial pessoal armazenada pelo `gh`.
Esse login no GitHub é separado do OAuth do Loki. Não colar tokens no chat.

## 2. Instalar o plugin

No mesmo terminal, executar uma vez:

```text
claude plugin marketplace add https://github.com/T0minh0/MCP_Loki.git
claude plugin install loki-orientacoes@loki-equipe --scope user
claude plugin list --json
```

Conferir `loki-orientacoes` habilitado. Se já estiver instalado, manter a
instalação e seguir para a etapa 3. Preservar o nome, a URL e o OAuth da conexão
MCP existente. O plugin acrescenta orientações e leitores; não cadastra outro servidor.

## 3. Ligar o auto-update do Claude

Abrir o Claude Code e seguir:

1. Digitar `/plugin`.
2. Abrir a aba **Marketplaces** e selecionar **loki-equipe**.
3. Selecionar **Enable auto-update**. Se aparecer **Disable auto-update**, já
   está ligado e não é preciso mudar.

Esse ajuste é necessário uma vez por máquina/perfil: marketplaces particulares
vêm com auto-update desligado. O Claude consulta o Git em segundo plano após
iniciar uma sessão e atualiza os plugins instalados. Novas orientações entram
na próxima sessão ou com `/reload-plugins` depois do aviso de atualização.

O repositório privado precisa continuar acessível pela credencial do GitHub.
Depois do pré-requisito uv, não é necessário instalar Python, clonar o repositório manualmente ou
cadastrar tarefas no sistema operacional. Não há horário fixo às 07h nem
consulta agendada com o Claude fechado.

## 4. Conferir o Loki

A versão1.1.7 atualiza `/loki-orientacoes:registrar-problema-loki` para relatos,
backlog Slack e propostas de correção.
Use-a para relatos sanitizados de achados, erros e sugestões, com autorização
de suporte já existente ou obtida antes de enviar. Confira `registrar_problema`
no catálogo MCP; instalar a skill não atualiza ferramentas da conexão. Entrega
real exige recibo `sent` e `message_id`, conforme a skill. Guarde `report_id` e
`problem_id` quando retornado e acompanhe sem reenviar. A decisão do proprietário
OAuth sobre a versão exata, a publicação e a confirmação humana da solução são
etapas distintas. O backend conserva o caminho Discord com suporte novo desligado.

Abrir uma conversa nova e executar:

```text
/loki-orientacoes:loki-bootstrap
```

O Claude deve consultar `meu_acesso` (ou `get_operator_context`) e as instruções
atuais do servidor. Conferir a própria identidade e o acesso esperado. Não
refazer OAuth se a conexão já funciona. A instalação por Git não concede
permissões no Loki nem altera o catálogo de ferramentas automaticamente.

Para iniciar o fluxo completo, executar na conversa:

```text
/loki-orientacoes:operar-loki
```

Pedir: **“Confira os leitores com o diagnóstico local, mantendo minha conexão
OAuth. Depois leia os documentos que eu indicar e envie ao Loki somente os
dados e fontes pela conexão existente.”** A harness resolve o caminho do
script instalado, executa o diagnóstico e conduz os comandos. O operador
permanece na conversa; não precisa invocar os leitores manualmente.

O diagnóstico local não valida a conta remota. Conferir identidade/permissão
pelo MCP e realizar um ensaio autorizado antes de trabalho real. Onboarding
continua sujeito ao papel administrativo exigido no backend; o plugin não
amplia permissões. Scripts não enviam PDFs, imagens ou ZIPs.

Se uma atualização não chegar, executar no terminal:

```text
claude plugin marketplace update loki-equipe
claude plugin update loki-orientacoes@loki-equipe --scope user
claude plugin list --json
```

Depois, usar `/reload-plugins` ou iniciar nova conversa. Conferir o acesso
GitHub se houver erro de autenticação; não remover o MCP para resolver Git.

Quem já tinha1.0.2 usa esses mesmos comandos e confere2.0.1 ou superior em
`claude plugin list --json`. Não desinstalar a conexão antiga para atualizar.

Para a rotina existente no Claude Code, use a
[ativação do roteiro de rotina](ANA_ROUTINE_ACTIVATION.md). A versão1.1.2 inclui
`references/ROUTINES.md` no plugin, com descoberta dos executores atuais,
seleção de histórico e recibo por rodada. Atualização do plugin não altera
o horário, o texto de uma tarefa agendada ou filtros de fila de outro sistema.

## Operação real e comparação opcional

Na versão1.1.4, a rotina usa cadastro, histórico, regras e fontes do Loki e dos
canais autorizados. Investiga parâmetros deriváveis por normas e passado e
acompanha execução, comparação e pendências por tarefa e finalidade do DP.
O índice de componentes abaixo é opcional, para comparações expressamente
pedidas com esse material; sua ausência não bloqueia fontes nativas suficientes.

Na versão1.1.1, `operar-loki` inclui o [roteiro de comparação privada](../plugins/loki-bootstrap/skills/operar-loki/references/COMPARATIVE_TESTING.md).
O índice e os dados do cliente ficam em local privado indicado pelo operador,
fora do repositório/cache. Informe essa localização na rotina existente:

> Use operar-loki e o roteiro COMPARATIVE_TESTING.md da instalação carregada.
> Leia o índice privado que indiquei, confira edição e hashes e concilie os
> componentes com o histórico nativo do Loki. Aplique as retenções por empresa,
> episódio e competência. Execute os componentes permitidos pelos contratos
> atuais e registre linhas consumidas, fontes, pendências e versão do resultado.
> Fixe o resultado do Loki antes de consultar o resultado da equipe e comparar.
> Prepare somente o pacote privado para revisão, com as ressalvas preservadas.

Esse texto pode ser incorporado ao pedido já autorizado no Claude Code; não
cria nem altera agenda. O índice orienta seleção, não é contrato MCP ou fonte
primária. Dados reportados não viram regra executável. Atualização no Git não
comprova instalação ou execução no computador de outro operador: conferir
versão, skill carregada, MCP e recibo de um ensaio real nesse ambiente.

## Quem seguiu o roteiro anterior

O procedimento atual substitui os agendadores externos publicados nas PRs 4 e 5.
Antes de usar somente o auto-update, seguir a [remoção da agenda antiga](REMOVE_EXTERNAL_SCHEDULERS.md)
para seu sistema. Quem ainda não configurou uma tarefa pode ignorar essa etapa.

## Antônio — Codex no servidor Linux

Seguir o [roteiro do Codex](CODEX_LINUX_SETUP.md), também sem agendador externo.
O ChatGPT continua com a conexão MCP configurada no próprio aplicativo.

Para publicar uma orientação nova, Antônio revisa e integra a alteração com
nova versão em `plugins/loki-bootstrap/.claude-plugin/plugin.json`, mantendo as
duas cópias do bootstrap iguais. Esse canal distribui também a skill operacional,
os scripts e o lock dos leitores. Mudanças do provider/backend continuam com
seus gates de build e publicação; o kit Windows legado não é modificado.

Referências: [auto-update no Claude](https://code.claude.com/docs/en/plugins/install#keep-plugins-updated),
[credenciais do repositório privado](https://code.claude.com/docs/en/plugins/host-marketplace#what-background-auto-update-does-with-credentials).

## Investigação durante a operação — 1.1.5

`/loki-orientacoes:investigar-regras-dp` também é descoberta pelos guias normais
quando houver lacuna ou divergência. O método e o registro de qualificação
acompanham a skill; dados ficam fora do cache. Confira versão instalada1.1.5,
recarregue a sessão e registre uma execução observada antes de declarar adoção.
Ver [ativação da rotina](ANA_ROUTINE_ACTIVATION.md).

Na1.1.7, ao concluir execução com falha inesperada, a IA carrega a skill de
suporte e registra quando já houver autorização no escopo. Pendência prevista
não é defeito automático; falha de suporte não gera recursão. O leitor retorna
support_handoff, sem enviar dados. [Escopo e limites](SUPPORT_COLLABORATION_20261027.md).
