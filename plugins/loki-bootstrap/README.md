# Bootstrap estável do Loki

`SKILL.md` é o guia mínimo para obter identidade e instruções atuais pelo servidor. Pode orientar a configuração de um cliente que aceite instruções/skills. Não é um instalador ChatGPT e não comprova que o aplicativo carregou o texto.

Não foi encontrada fonte verificável de um pacote/manifest ChatGPT do Loki; por isso esta pasta não declara esse formato. O administrador configura a conexão OAuth existente pelo aplicativo e verifica as ferramentas visíveis. Um cliente que ainda não enxergue as ferramentas novas pode usar `runtime_instructions` retornado por `meu_acesso` ou `get_operator_context`, quando a integração do backend estiver implantada.

O bootstrap não substitui o kit desktop: leitura de arquivos locais, venv, cofre Windows, checkpoint, assinatura de release e preflight continuam nas implementações existentes. Não copie tokens ou credenciais para esta pasta ou para instruções do chat.

## Claude Code

O marketplace privado instala somente orientações, sem declarar servidor MCP ou hooks:

```text
claude plugin marketplace add https://github.com/T0minh0/MCP_Loki.git
claude plugin install loki-orientacoes@loki-equipe --scope user
```

Depois, em nova conversa, use `/loki-orientacoes:loki-bootstrap`.
Veja o [agendamento para Mac, Windows e Linux](../../docs/DAILY_OPERATOR_UPDATES.md).

## Codex no Linux

O Codex aceita este mesmo pacote pelo gerenciador nativo:

```text
codex plugin marketplace add https://github.com/T0minh0/MCP_Loki.git --json
codex plugin add loki-orientacoes@loki-equipe --json
```

Abrir conversa nova e usar `$loki-bootstrap`. O [roteiro do servidor Linux](../../docs/CODEX_LINUX_SETUP.md)
inclui atualização diária às 07h de Brasília. A conexão MCP existente continua
responsável pelo OAuth e pelas ferramentas; este plugin entrega orientações.
