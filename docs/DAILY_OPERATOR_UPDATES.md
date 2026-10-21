# Ana e Samuel — instalar uma vez e receber atualizações pelo Claude

**Ana:** Claude Code no Mac. **Samuel:** Claude Code no Windows e no Linux;
repetir a configuração em cada máquina. O plugin usa o MCP e o OAuth que vocês
já têm. A atualização fica por conta do próprio Claude Code.

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
MCP existente. O plugin acrescenta orientações; não cadastra outro servidor.

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
Não é necessário instalar Python, uv, clonar o repositório manualmente ou
cadastrar tarefas no sistema operacional. Não há horário fixo às 07h nem
consulta agendada com o Claude fechado.

## 4. Conferir o Loki

Abrir uma conversa nova e executar:

```text
/loki-orientacoes:loki-bootstrap
```

O Claude deve consultar `meu_acesso` (ou `get_operator_context`) e as instruções
atuais do servidor. Conferir a própria identidade e o acesso esperado. Não
refazer OAuth se a conexão já funciona. A instalação por Git não concede
permissões no Loki nem altera o catálogo de ferramentas automaticamente.

Se uma atualização não chegar, executar no terminal:

```text
claude plugin marketplace update loki-equipe
claude plugin update loki-orientacoes@loki-equipe --scope user
claude plugin list --json
```

Depois, usar `/reload-plugins` ou iniciar nova conversa. Conferir o acesso
GitHub se houver erro de autenticação; não remover o MCP para resolver Git.

## Quem seguiu o roteiro anterior

O procedimento atual substitui os agendadores externos publicados nas PRs 4 e 5.
Antes de usar somente o auto-update, seguir a [remoção da agenda antiga](REMOVE_EXTERNAL_SCHEDULERS.md)
para seu sistema. Quem ainda não configurou uma tarefa pode ignorar essa etapa.

## Antônio — Codex no servidor Linux

Seguir o [roteiro do Codex](CODEX_LINUX_SETUP.md), também sem agendador externo.
O ChatGPT continua com a conexão MCP configurada no próprio aplicativo.

Para publicar uma orientação nova, Antônio revisa e integra a alteração com
nova versão em `plugins/loki-bootstrap/.claude-plugin/plugin.json`, mantendo as
duas cópias da skill iguais. Esse canal distribui somente orientações. Mudanças
do provider e do backend continuam exigindo os gates de build e publicação;
leitores do kit Windows seguem seu canal assinado.

Referências: [auto-update no Claude](https://code.claude.com/docs/en/plugins/install#keep-plugins-updated),
[credenciais do repositório privado](https://code.claude.com/docs/en/plugins/host-marketplace#what-background-auto-update-does-with-credentials).
