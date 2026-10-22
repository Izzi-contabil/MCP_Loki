# Loki — leitores locais e operação pela harness

Versão1.1.2. O nome instalado `loki-orientacoes@loki-equipe` foi mantido para
quem já instalou receber o plugin completo pelo auto-update nativo Git.

O pacote inclui `loki-bootstrap` e `operar-loki`, leitores de PDF/imagem,
planilhas, documentos de texto e arquivos estruturados, preparação de CSV e
parâmetros e recibos locais. Os scripts/lock estão dentro da skill operacional.
A harness interpreta e confere os documentos e chama o MCP já conectado.
O Loki recebe somente parâmetros e CSVs; originais e renderizações ficam locais.

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

Rotinas agendadas usam o [roteiro incluído no plugin](skills/operar-loki/references/ROUTINES.md),
consultado pelo bootstrap e pela skill operacional. Ele seleciona os executores
pelo contrato corrente e preserva históricos, pendências e recibos de execução.
Para vincular uma rotina existente no Claude Code, siga o
[roteiro de ativação](../../docs/ANA_ROUTINE_ACTIVATION.md). Publicação pelo Git
não comprova instalação ou alteração do agendamento na máquina do operador.
