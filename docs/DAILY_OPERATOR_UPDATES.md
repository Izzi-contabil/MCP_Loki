# Ana e Samuel — atualização diária pelo repositório

Ana usa **Claude Code no Mac**. Samuel usa **Claude Code no Windows e no Linux**;
configure cada máquina separadamente. O OAuth permanece na conexão MCP que já
funciona no Claude. Não remova o servidor, não troque seu nome/URL e não exporte
credenciais. O acesso pessoal ao GitHub é uma autorização separada.

Este perfil instala `loki-orientacoes`, um plugin declarativo que consulta as
instruções atuais do servidor. Não tem servidor MCP, hooks, leitores locais ou
cofre próprio. Ele complementa o kit anterior; a atualização dos leitores do kit
Windows assinado tem outro procedimento, no Project Loki.

## Antes de começar — Antônio, no servidor Linux

1. A [PR 4](https://github.com/T0minh0/MCP_Loki/pull/4) foi integrada em
   21/10/2026. O marketplace, o plugin e o atualizador estão na branch padrão
   `feature/dynamic-instructions`; os comandos abaixo já usam essa distribuição.
2. `T0minh0/MCP_Loki` já foi tornado **privado**, conforme sua decisão. Adicionar
   as contas pessoais da equipe com leitura quando desejar; nenhum convite foi
   enviado nesta implementação.
3. Para publicar novas orientações locais, revisar a alteração e aumentar a
   versão em `plugins/loki-bootstrap/.claude-plugin/plugin.json`. Manter o
   `skills/loki-bootstrap/SKILL.md` igual ao `SKILL.md` estável. O marketplace é
   distribuído por Git privado; este perfil declarativo **não usa a assinatura
   dos bundles executáveis Windows**. Não adicionar MCP, hooks ou executáveis ao
   plugin por esse canal. O código do agendador instalado uma vez fica estável;
   uma mudança nele requer repetir a configuração, após revisão.
4. Conteúdo do provider continua exigindo nova versão de wheel, promoção e deploy
   do backend pelos gates existentes. Um push neste repositório não implanta o
   serviço. O domínio, a hospedagem, o banco e o Shadow das 05h não mudam.

## Preparação comum — no computador de cada pessoa

No terminal que já abre o Claude Code, confirmar:

```text
claude --version
claude plugin --help
gh auth login --hostname github.com --web --git-protocol https
gh auth setup-git
gh repo view T0minh0/MCP_Loki --json nameWithOwner,visibility
```

Usar a conta GitHub individual que recebeu leitura. `gh auth setup-git` configura
o Git para usar a credencial pessoal já guardada pelo GitHub CLI, sem colocar
um token na tarefa. São necessários Git, GitHub CLI, Claude Code nativo e
[uv](https://docs.astral.sh/uv/getting-started/installation/). O uv instalará um
Python 3.11 isolado, sem trocar o Python do sistema. No Windows, preferir o
executável nativo `claude.exe`, evitando um wrapper npm `.cmd`.

Antes de instalar, abrir o Claude e pedir `meu_acesso`. Conferir a própria
identidade e o acesso esperado. Se o MCP ainda não funcionar, resolver essa
conexão existente antes da agenda; o atualizador não configura OAuth.

Registrar o marketplace privado e instalar somente as orientações:

```text
claude plugin marketplace add https://github.com/T0minh0/MCP_Loki.git
claude plugin install loki-orientacoes@loki-equipe --scope user
claude plugin list --json
```

Isso não substitui o MCP antigo. Não instalar novamente o kit Windows nem criar
outra conexão OAuth para seguir este guia.

## Ana — Mac

No Terminal, executar uma vez:

```bash
set -e
loki_root="$HOME/Library/Application Support/Loki-Claude-Updates"
mkdir -p "$loki_root"
git clone --branch feature/dynamic-instructions https://github.com/T0minh0/MCP_Loki.git "$loki_root/source"
uv venv --python 3.11 "$loki_root/venv"
uv pip install --python "$loki_root/venv/bin/python" --require-hashes -r "$loki_root/source/scripts/requirements-claude-updater.txt"
"$loki_root/venv/bin/python" "$loki_root/source/scripts/claude_daily.py" configure --root "$loki_root" --claude "$(command -v claude)"
"$loki_root/venv/bin/python" "$loki_root/claude_daily.py" run --root "$loki_root"
mkdir -p "$HOME/Library/LaunchAgents"
cp "$loki_root/com.themindops.loki-updates.plist" "$HOME/Library/LaunchAgents/"
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.themindops.loki-updates.plist"
launchctl print "gui/$(id -u)/com.themindops.loki-updates"
```

Ao repetir o cadastro, descarregar primeiro com `launchctl bootout` usando o
mesmo domínio `gui/$(id -u)` e arquivo plist. Não repetir `git clone` sobre uma
pasta existente: para atualizar o instalador, fazer `git -C "$loki_root/source"
pull --ff-only` e repetir `configure` após revisão.

## Samuel — Linux

No terminal da sua sessão de usuário:

```bash
set -e
loki_root="$HOME/.local/share/loki-claude-updates"
mkdir -p "$loki_root"
git clone --branch feature/dynamic-instructions https://github.com/T0minh0/MCP_Loki.git "$loki_root/source"
uv venv --python 3.11 "$loki_root/venv"
uv pip install --python "$loki_root/venv/bin/python" --require-hashes -r "$loki_root/source/scripts/requirements-claude-updater.txt"
"$loki_root/venv/bin/python" "$loki_root/source/scripts/claude_daily.py" configure --root "$loki_root" --claude "$(command -v claude)"
"$loki_root/venv/bin/python" "$loki_root/claude_daily.py" run --root "$loki_root"
mkdir -p "$HOME/.config/systemd/user"
cp "$loki_root/loki-claude-update.service" "$loki_root/loki-claude-update.timer" "$HOME/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user enable --now loki-claude-update.timer
systemctl --user list-timers loki-claude-update.timer
```

Requer systemd de usuário funcionando. Sem sessão persistente/linger, o timer
para ao sair do usuário e consulta novamente após o próximo login. Não usar
`sudo` para instalar na identidade de outra pessoa.

## Samuel — Windows

No PowerShell do mesmo usuário que já usa o Claude:

```powershell
$ErrorActionPreference = 'Stop'
$lokiRoot = Join-Path $env:LOCALAPPDATA 'Loki-Claude-Updates'
New-Item -ItemType Directory -Force $lokiRoot | Out-Null
git clone --branch feature/dynamic-instructions https://github.com/T0minh0/MCP_Loki.git (Join-Path $lokiRoot 'source')
if ($LASTEXITCODE -ne 0) { throw 'Clone falhou; agenda nao cadastrada.' }
uv venv --python 3.11 (Join-Path $lokiRoot 'venv')
if ($LASTEXITCODE -ne 0) { throw 'Python falhou; agenda nao cadastrada.' }
$lokiPython = Join-Path $lokiRoot 'venv\Scripts\python.exe'
uv pip install --python $lokiPython --require-hashes -r (Join-Path $lokiRoot 'source\scripts\requirements-claude-updater.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependencia falhou; agenda nao cadastrada.' }
& $lokiPython (Join-Path $lokiRoot 'source\scripts\claude_daily.py') configure --root $lokiRoot --claude (Get-Command claude.exe).Source
if ($LASTEXITCODE -ne 0) { throw 'Configuracao falhou; agenda nao cadastrada.' }
& $lokiPython (Join-Path $lokiRoot 'claude_daily.py') run --root $lokiRoot
if ($LASTEXITCODE -ne 0) { throw 'Consulta falhou; agenda nao cadastrada.' }
schtasks /Create /TN 'Loki-Claude-Update' /XML (Join-Path $lokiRoot 'loki-claude-update.xml') /F
if ($LASTEXITCODE -ne 0) { throw 'Cadastro da tarefa falhou.' }
schtasks /Run /TN 'Loki-Claude-Update'
if ($LASTEXITCODE -ne 0) { throw 'Disparo da tarefa falhou.' }
Get-ScheduledTaskInfo -TaskName 'Loki-Claude-Update'
```

A tarefa usa `InteractiveToken`, sem guardar senha. Requer a sessão do usuário
conectada. A consulta é compensada quando a máquina/sessão voltar.

## Horário, verificação e diagnóstico

Um disparo leve por minuto verifica o relógio em `America/Sao_Paulo`. Só depois
das **07h de Brasília** executa os dois comandos de atualização, uma vez por dia.
Com a máquina disponível, começa em até aproximadamente um minuto após 07h;
se estiver desligada ou sem sessão, consulta ao voltar depois desse horário.
O tick não chama um modelo, não envia documentos e não abre login. Falhas também
contam como uma tentativa no dia, evitando repetição de rede a cada minuto.

Em Bash, consultar estado ou repetir imediatamente:

```bash
"$loki_root/venv/bin/python" "$loki_root/claude_daily.py" status --root "$loki_root"
"$loki_root/venv/bin/python" "$loki_root/claude_daily.py" run --root "$loki_root"
claude plugin list --json
```

No Windows, usar `& $lokiPython (Join-Path $lokiRoot 'claude_daily.py') status
--root $lokiRoot` ou trocar `status` por `run` na mesma linha. `atualizado`
registra que os comandos oficiais concluíram; pode não haver versão nova.
`falha_consultar_claude` ou `iniciado` sem conclusão exige inspeção/repetição.
O comando `run` devolve código 1 em falha. Um tick posterior já consultado no dia
retorna 0 sem apagar o erro anterior de `status.json`; conferir o estado, além do
resultado da tarefa.

Para diagnosticar no terminal, executar `claude plugin marketplace update
loki-equipe` e `claude plugin update loki-orientacoes@loki-equipe --scope user`
na mesma sessão/identidade. Conferir acesso GitHub e o caminho do executável.
Se usa `CLAUDE_CONFIG_DIR`, configurar a agenda no terminal com essa variável;
o caminho e o PATH são preservados, sem copiar credenciais. Sem esse cuidado,
o cliente pode usar outro perfil. Não salvar tokens em variáveis da tarefa.

Após a atualização, iniciar nova conversa ou usar `/reload-plugins` no Claude.
Executar `/loki-orientacoes:loki-bootstrap` e confirmar `meu_acesso` e as
instruções `geral`/do domínio. Sessões abertas não comprovam recarga automática.

## Desabilitar e voltar uma orientação

Mac: descarregar e remover somente o cadastro deste job, para que não volte no
próximo login:

```bash
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.themindops.loki-updates.plist"
rm "$HOME/Library/LaunchAgents/com.themindops.loki-updates.plist"
```

Linux: `systemctl --user disable --now loki-claude-update.timer`.
Windows: `schtasks /Change /TN 'Loki-Claude-Update' /Disable`.
Isso para a agenda e preserva o MCP e o OAuth.

Se uma orientação nova estiver errada, o caminho preferencial é revertê-la por
PR e publicar uma **nova versão** do plugin. Para uma reversão local imediata,
com a agenda parada e sem conversa em andamento: no clone `source`, usar
`git checkout --detach COMMIT_VALIDADO_ANTERIOR` (SHA fornecido por Antônio),
remover apenas o plugin `claude plugin uninstall loki-orientacoes@loki-equipe
--scope user`, remover apenas esse marketplace com `claude plugin marketplace
remove loki-equipe`, adicioná-lo pelo **caminho absoluto do clone source** e
instalar `loki-orientacoes@loki-equipe` outra vez. Assim o Claude lê a versão
fixada localmente. Conferir versão com `claude plugin list --json` e nova conversa.
O rollback do plugin não faz rollback do backend nem do OAuth. A agenda fica
parada até reconciliar a versão e restaurar o marketplace remoto; não prometer
rollback automático transacional para esse perfil nativo.

## Antônio — Codex e ChatGPT

O Codex aceita o mesmo pacote declarativo pelo seu gerenciador nativo de plugins.
Seguir o [roteiro do Codex no Linux](CODEX_LINUX_SETUP.md), com instalação,
atualização diária às 07h de Brasília e diagnóstico. Ele preserva a conexão MCP
existente. Não executar os cadastros de tarefas do Claude para configurar Codex.

O ChatGPT continua usando sua conexão MCP existente; as instruções dinâmicas vêm
do serviço publicado. Conferir `meu_acesso` e as ferramentas atuais no aplicativo.
A instalação local no Codex não instala o plugin na conta ChatGPT nem executa
uma agenda nessa conta. Atualização de catálogo/conexão deve ser verificada na
interface se necessário, sem presumir novo OAuth.

## Aceite por máquina

Conferir: acesso privado pessoal, plugin/versão habilitados, mesma identidade no
MCP, orientações carregadas em conversa nova, execução manual concluída e um
disparo real do agendador registrado em `status.json`. Não enviar dados pessoais
ou tokens no recibo. Testes neste servidor não equivalem ao aceite no Mac ou
no Windows. Nenhuma máquina da equipe foi configurada remotamente nesta tarefa.

Referências: [marketplaces Claude](https://code.claude.com/docs/en/plugin-marketplaces),
[comandos oficiais de plugins](https://code.claude.com/docs/en/plugins/cli-reference).
