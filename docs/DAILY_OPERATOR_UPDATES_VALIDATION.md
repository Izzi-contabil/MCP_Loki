# Validação do fluxo nativo — 21/10/2026

**Registro histórico da versão1.0.2.** O plugin completo1.1.0, incluindo leitores
locais e preparação pela harness, é descrito em [LOCAL_READERS.md](LOCAL_READERS.md).
Os números e o escopo abaixo referem-se à entrega anterior, só de orientações.

O procedimento vigente usa auto-update da harness, conforme orientação expressa
do usuário. Substitui os agendadores externos das PRs 4 e 5. Ana/macOS e
Samuel/Windows+Linux continuam no Claude Code; Antônio usa Codex neste Linux.
O plugin declarativo passa a 1.0.2; skill, provider 0.1.3, contrato e lock não
mudam. Não houve alteração no backend ou implantação de produção nesta etapa.

## Codex

O código oficial da versão instalada 0.163.0 confirma que
`maybe_start_plugin_startup_tasks_for_config` inicia, com plugins habilitados,
a atualização dos marketplaces Git em segundo plano usando o modo automático.
Esse caminho atualiza o cache dos plugins configurados, sem novo `plugin add`.

Prova com o binário real 0.163.0 em container descartável, sem rede ou credenciais:

1. Adicionado o marketplace e instalado o pacote 1.0.1.
2. Publicada versão sintética 1.0.2 num Git local. Uma URL HTTPS sintética foi
   redirecionada para ele por configuração Git restrita ao container.
3. Iniciado `codex app-server --stdio` e enviado apenas o handshake de
   inicialização. Nenhum modelo, thread de negócio ou comando de upgrade.
4. O manifesto 1.0.2 apareceu no cache pela tarefa nativa de inicialização.

Isso substitui a lacuna anterior sobre a existência de auto-update nativo. Não
promete consulta com o aplicativo fechado, periodicidade fixa ou recarga de
orientações já carregadas numa conversa. O ensaio não certifica credenciais de
outra pessoa; o acesso real deste servidor ao Git privado já foi validado nas
etapas anteriores.

No servidor, o timer `loki-codex-update` foi desabilitado/parado. Os dois arquivos
de unidade foram removidos somente após igualdade com o backup privado da
instalação anterior. Daemon systemd recarregado. A rotina `izzi-loki-feedbacks`
das 05h permaneceu ativa. Nenhuma tarefa foi removida remotamente das máquinas
da Ana ou do Samuel; o roteiro contém instruções para quem instalou a agenda.

## Claude Code

Documentação oficial confirma auto-update após início de sessão, desligado por
padrão para marketplaces particulares. O roteiro orienta `/plugin` →
Marketplaces → `loki-equipe` → Enable auto-update. O Git privado usa a credencial
pessoal já armazenada, sem prompt, configurada por `gh auth setup-git`.
Nova sessão ou `/reload-plugins` carrega a atualização concluída.

Na etapa anterior, Claude Code oficial 2.1.306 em perfil isolado Linux exerceu
instalação, atualização Git/cache, reversão e preservação de OAuth sintético.
O ajuste de auto-update na interface da Ana e do Samuel continua sendo parte
do aceite em cada máquina. Não se declara essa configuração já realizada.

## Verificações deste complemento

- `uv sync --locked --all-extras --no-editable --python 3.11`.
- `pytest -q`: **76 passaram**. Os testes exclusivos dos scripts e cadastros
  externos foram removidos junto com esses scripts, retirados da distribuição.
  A guarda existente de pacote estritamente declarativo e igualdade das skills
  foi preservada em `test_bootstrap_package_masked.py`.
- `ruff check .`, `ruff format --check .` e `mypy src scripts`: passaram.
- Fonte Python do provider, skills e lock sem diferença contra a base.
- Não houve assinatura, cópia de chave, alteração OAuth ou novo servidor MCP.

As PRs anteriores registraram 95 testes aprovados e três probes PowerShell
ignorados no host (exercidos em container real). Aqueles resultados descrevem
o procedimento anterior, não são a contagem da suíte atual. A CI hospedada
permaneceu bloqueada por cobrança/limite; verificações locais não equivalem a
CI hospedada verde. Acesso GitHub da equipe será concedido por Antônio.

Fontes: [Claude — auto-update](https://code.claude.com/docs/en/plugins/install#keep-plugins-updated),
[Git privado](https://code.claude.com/docs/en/plugins/host-marketplace#what-background-auto-update-does-with-credentials),
[OpenAI Docs](https://developers.openai.com/plugins/build/plugins),
[Codex 0.163.0 — tarefa automática](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core-plugins/src/manager.rs#L2823).
