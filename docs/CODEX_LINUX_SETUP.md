# Antônio — plugin Loki no Codex do servidor Linux

Este roteiro instala `loki-orientacoes@loki-equipe`, versão `1.0.1`,
usando o repositório privado. O pacote contém a skill `loki-bootstrap`; usa as
ferramentas do MCP que você já conectou. Não cadastra outro servidor nem copia
OAuth. Leitores locais e o kit executável Windows têm distribuição separada.

O Codex 0.163.0 aceita o marketplace `.claude-plugin/marketplace.json` e o
manifest compatível já incluídos na PR 4. A instalação foi exercitada com o CLI
real antes da configuração deste servidor. Esse formato é suportado pela
[documentação oficial da OpenAI](https://developers.openai.com/plugins/build/plugins).

## Instalar uma vez

Na sessão Linux do mesmo usuário que executa o Codex, verificar Git, GitHub CLI
e `codex --version`. O Git deve conseguir ler `T0minh0/MCP_Loki` usando a conta
pessoal autorizada. Se ainda não consegue, executar `gh auth login --hostname
github.com --web --git-protocol https` e `gh auth setup-git`. Essa credencial do
GitHub é independente do OAuth já conectado ao Loki.

```bash
set -e
codex plugin marketplace add https://github.com/T0minh0/MCP_Loki.git --json
codex plugin add loki-orientacoes@loki-equipe --json
codex plugin list --marketplace loki-equipe --json
```

Conferir `installed: true`, `enabled: true` e a versão. Abrir uma conversa nova
no Codex e invocar `$loki-bootstrap`, ou selecioná-la no menu de skills. Pedir
para consultar `meu_acesso` e as instruções `geral` antes do fluxo. Conferir a
própria identidade e as capacidades retornadas, sem copiar tokens. Se o aplicativo
ainda não listar a skill, recarregar o aplicativo e conferir novamente. A
instalação no disco não comprova que uma conversa já aberta recarregou o pacote.

## Atualizar diariamente às 07h de Brasília

No Codex, o comando nativo `marketplace upgrade` atualiza o snapshot Git e o
cache do plugin instalado. Não é necessário repetir `plugin add` na agenda;
assim, um plugin desabilitado continua desabilitado. Orientações já carregadas
numa conversa podem continuar antigas até uma nova conversa.

Os comandos abaixo usam o perfil padrão `~/.codex` e o launcher estável
`~/.local/bin/codex`, como neste servidor. Conferir `command -v codex` antes;
se a instalação usar outro caminho, ajustar `ExecStart` para o launcher absoluto.
Se usa outro perfil `CODEX_HOME`, configurar e validar a agenda desse perfil
separadamente; não reutilizar este cadastro supondo que os perfis sejam iguais.

```bash
set -e
test -x "$HOME/.local/bin/codex"
mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/loki-codex-update.service" <<'EOF'
[Unit]
Description=Atualizar orientações Loki no Codex pelo Git privado

[Service]
Type=oneshot
WorkingDirectory=%h
Environment="PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin"
UMask=0077
TimeoutStartSec=10min
ExecStart=%h/.local/bin/codex plugin marketplace upgrade loki-equipe --json
EOF
cat > "$HOME/.config/systemd/user/loki-codex-update.timer" <<'EOF'
[Unit]
Description=Atualização diária Loki no Codex às 07h de Brasília

[Timer]
OnCalendar=*-*-* 07:00:00 America/Sao_Paulo
Persistent=true
AccuracySec=1min

[Install]
WantedBy=timers.target
EOF
systemd-analyze --user verify "$HOME/.config/systemd/user/loki-codex-update.service" "$HOME/.config/systemd/user/loki-codex-update.timer"
systemctl --user daemon-reload
systemctl --user start loki-codex-update.service
systemctl --user enable --now loki-codex-update.timer
systemctl --user list-timers loki-codex-update.timer
```

O disparo é às **07h de Brasília, 10h UTC** no servidor. `Persistent=true`
compensa um horário perdido quando o gerenciador de usuário voltar. Neste
servidor, o usuário `tominho` já tem `Linger=yes`; a agenda pode rodar sem uma
sessão de terminal aberta. Em outra máquina, verificar essa condição antes de
prometer execução sem login. A agenda não chama um modelo nem processa documentos.

## Verificar, repetir e desabilitar

```bash
systemctl --user show loki-codex-update.service -p Result -p ExecMainStatus
journalctl --user -u loki-codex-update.service -n 30 --no-pager
codex plugin list --marketplace loki-equipe --json
```

Conferir `Result=success`, `ExecMainStatus=0`, `errors: []` no recibo do CLI e a
versão instalada. Falha de leitura do Git privado retorna erro; corrigir o acesso
e repetir `systemctl --user start loki-codex-update.service`. Para parar a agenda:

```bash
systemctl --user disable --now loki-codex-update.timer
```

Para uma orientação incorreta, preferir uma PR de correção com nova versão do
plugin. Uma reversão local exige parar a agenda, fechar conversas que usam o
plugin e preparar um clone em `COMMIT_VALIDADO_ANTERIOR` fornecido por Antônio.
Remover somente `codex plugin remove loki-orientacoes@loki-equipe`, remover
somente `codex plugin marketplace remove loki-equipe`, adicionar o marketplace
pelo caminho absoluto desse clone e instalar o plugin outra vez. Conferir a
versão em conversa nova. Manter a agenda parada até restaurar o canal remoto.
O Codex pode substituir o cache anterior durante a atualização; esse perfil
não oferece rollback transacional automático. O OAuth e o backend não fazem
parte dessa reversão.

O plugin local não instala nada na conta ChatGPT. Nela, continuar usando a
conexão MCP existente e conferir identidade e catálogo no próprio aplicativo.
