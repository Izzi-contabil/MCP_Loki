# Loki — leitores locais e operação pela harness

Versão1.1.5. O nome instalado `loki-orientacoes@loki-equipe` foi mantido para
quem já instalou receber o plugin completo pelo auto-update nativo Git.

O pacote inclui `loki-bootstrap` e `operar-loki`, leitores de PDF/imagem,
planilhas, documentos de texto e arquivos estruturados, preparação de CSV e
parâmetros e recibos locais. Os scripts/lock estão dentro da skill operacional.
A harness interpreta e confere os documentos e chama o MCP já conectado.
O Loki recebe somente parâmetros e CSVs; originais e renderizações ficam locais.

A skill [investigar-regras-dp](skills/investigar-regras-dp/SKILL.md) integra a
operação quando faltar dado, fórmula ou parâmetro, ou houver divergência
recorrente. Pode ser invocada como `/loki-orientacoes:investigar-regras-dp`
no Claude ou `$investigar-regras-dp` no Codex. Use normas e holerites para
qualificar parâmetros, testar hipóteses e retomar tarefas com consumo comprovado.
A skill distingue correção de dados/configuração de correção do produto;
nenhuma instrução concede acesso de desenvolvimento ou decisão.

Na operação real, o cadastro, histórico e parâmetros consumidos ficam no Loki.
O roteiro de rotina inclui investigação de regras por normas e histórico e
acompanhamento por tarefa de todas as finalidades do DP. O índice de componentes
abaixo é opcional, sem exigir recadastro de informações já existentes no servidor.

O [roteiro de comparação](skills/operar-loki/references/COMPARATIVE_TESTING.md)
orienta o uso de índices privados de componentes qualificados: edição/hashes,
seleção por empresa/episódio/competência, retenções, unidades reportadas e recibo
do consumo. Dados do cliente ficam fora do plugin e do Git.

Nenhum servidor MCP, hook, token, runtime Windows ou código do backend é
instalado. O OAuth permanece no aplicativo que já está conectado. Não há
agendador externo ou ZIP novo. Python3.11/dependências com hashes são gerenciados
pelo uv; dados privados ficam fora do cache atualizado pelo Git.

- [Claude Code: Mac/Windows/Linux](../../docs/DAILY_OPERATOR_UPDATES.md).
- [Codex no Linux](../../docs/CODEX_LINUX_SETUP.md).
- [Leitores, requisitos e validação](../../docs/LOCAL_READERS.md).

Depois da atualização, use `/loki-orientacoes:operar-loki` no Claude ou
`$operar-loki` no Codex. O bootstrap antigo continua disponível. O kit legado
assinado conserva seus próprios pins/preflight; esta distribuição não o altera
nem importa seu cofre. ChatGPT mantém seu conector remoto e não executa esses
leitores locais.

Para achados, erros ou sugestões ao suporte, use
`/loki-orientacoes:registrar-problema-loki` no Claude ou
`$registrar-problema-loki` no Codex. A skill também é descoberta pelos guias
de operação e rotina. Ela prepara relato sanitizado e usa `registrar_problema`
na conexão MCP existente, dentro da autorização de suporte. Atualizar o plugin
não atualiza o catálogo remoto: confira a ação e seu recibo antes de declarar
entrega ao Discord. O webhook permanece no servidor.

Rotinas agendadas usam o [roteiro incluído no plugin](skills/operar-loki/references/ROUTINES.md),
consultado pelo bootstrap e pela skill operacional. Ele seleciona os executores
pelo contrato corrente e preserva históricos, pendências e recibos de execução.
Para vincular uma rotina existente no Claude Code, siga o
[roteiro de ativação](../../docs/ANA_ROUTINE_ACTIVATION.md). Publicação pelo Git
não comprova instalação ou alteração do agendamento na máquina do operador.
