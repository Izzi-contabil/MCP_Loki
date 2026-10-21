# Codex — plugin Loki com atualização nativa

O plugin `loki-orientacoes@loki-equipe` usa o MCP e o OAuth já conectados.
Este roteiro substitui o timer das 07h e deixa a atualização com o próprio
Codex. Não instala leitores locais ou o kit executável Windows.

## 1. Instalar uma vez

No terminal do mesmo usuário/perfil que executa o Codex, conferir `codex --version`.
O procedimento foi verificado no Codex 0.163.0. Git e GitHub CLI precisam estar
instalados, com leitura pessoal de `T0minh0/MCP_Loki`. Se necessário, executar
`gh auth login --hostname github.com --web --git-protocol https` e
`gh auth setup-git` antes da instalação.

```text
codex plugin marketplace add https://github.com/T0minh0/MCP_Loki.git --json
codex plugin add loki-orientacoes@loki-equipe --json
codex plugin list --marketplace loki-equipe --json
```

Conferir `installed: true` e `enabled: true`. Se já estiver instalado, manter
essa instalação. Preservar a conexão MCP existente e suas credenciais.

## 2. Usar o auto-update do Codex

Manter o marketplace registrado pelo Git e o plugin habilitado. A inicialização
dos plugins no Codex 0.163.0 dispara em segundo plano a consulta e atualização
dos marketplaces Git configurados e do cache dos plugins. Não há um botão
`Enable auto-update` equivalente ao Claude para acrescentar neste roteiro.

Abrir o aplicativo normalmente e iniciar uma conversa nova para carregar as
orientações. Se uma atualização acontecer com uma conversa já aberta, iniciar
outra conversa depois de concluída. Sem agendador externo, a atualização depende
do ciclo da harness; não há promessa de consulta às 07h ou com ela fechada.

Em conversa nova, selecionar a skill `loki-bootstrap` ou invocar `$loki-bootstrap`.
Pedir que consulte `meu_acesso` e as instruções `geral`. Conferir identidade e
capacidades; a instalação no disco não comprova recarga numa conversa antiga.

## 3. Conferir ou atualizar imediatamente

Se precisar conferir uma publicação sem esperar o próximo ciclo nativo:

```text
codex plugin marketplace upgrade loki-equipe --json
codex plugin list --marketplace loki-equipe --json
```

Conferir `errors: []`, a versão instalada e `enabled: true`, depois abrir nova
conversa. Esses comandos são uma ação manual de diagnóstico, sem cron, systemd,
automação do chat ou script periódico. Falha de acesso GitHub deve ser resolvida
na credencial pessoal do Git; ela é separada do OAuth do Loki.

Quem seguiu o roteiro anterior deve [remover a agenda externa](REMOVE_EXTERNAL_SCHEDULERS.md#codex-no-linux).
O ChatGPT continua usando a conexão MCP existente no aplicativo; instalar o
plugin local não instala outro plugin na conta ChatGPT.

Referências: [OpenAI Docs — marketplaces](https://developers.openai.com/plugins/build/plugins),
[inicialização nativa no Codex 0.163.0](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core-plugins/src/manager.rs#L2823).
