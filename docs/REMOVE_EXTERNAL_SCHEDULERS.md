# Remover os agendadores do roteiro anterior

Somente para quem configurou as tarefas externas das PRs 4 ou 5. Quem vai
instalar o plugin agora pode seguir diretamente o [roteiro nativo](DAILY_OPERATOR_UPDATES.md).
Parar apenas a tarefa indicada para o seu aplicativo e manter o plugin, o
servidor MCP e o OAuth existentes. Habilitar o auto-update do Claude conforme
o roteiro antes de encerrar a migração.

## Claude Code no Mac — Ana

No Terminal:

```bash
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.themindops.loki-updates.plist"
rm -f "$HOME/Library/LaunchAgents/com.themindops.loki-updates.plist"
```

Se o job já estiver descarregado, `bootout` pode informar que não foi encontrado.
Remover o plist instalado impede que a tarefa volte no próximo login.

## Claude Code no Linux — Samuel

```bash
systemctl --user disable --now loki-claude-update.timer
systemctl --user stop loki-claude-update.service
```

Se as unidades não existirem, essa máquina não tem essa agenda para parar.

## Claude Code no Windows — Samuel

No PowerShell do mesmo usuário:

```powershell
schtasks /Change /TN 'Loki-Claude-Update' /Disable
```

Ou abrir o Agendador de Tarefas, localizar **Loki-Claude-Update** e selecionar
**Desabilitar**. Se uma execução já estiver em andamento, aguardar sua conclusão.

## Codex no Linux

```bash
systemctl --user disable --now loki-codex-update.timer
systemctl --user stop loki-codex-update.service
```

Se as unidades não existirem, não há essa agenda para parar. No servidor de
Antônio, o timer foi desativado durante a migração para o fluxo nativo.

Os arquivos de configuração das tarefas e os antigos diretórios de suporte
podem permanecer inativos. Não executar os instaladores antigos para atualizar
o plugin. Nenhum comando deste roteiro para a rotina independente das 05h.
