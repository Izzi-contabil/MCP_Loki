# Leitores locais — plugin1.1.0

O plugin nativo mantém o nome `loki-orientacoes@loki-equipe` e inclui duas skills:
`loki-bootstrap` e `operar-loki`. As instalações1.0.2 recebem código, skill e lock
pelo mesmo auto-update Git. Não é necessário outro ZIP ou conexão MCP.

## Sistemas e dependências

Mac Intel/Apple Silicon com macOS13+, Windows10/11 x64 e Linux moderno x64/ARM64.
Git/GitHub e Claude Code ou Codex continuam sendo os da instalação existente.
Instalar uv uma vez conforme [o roteiro](DAILY_OPERATOR_UPDATES.md); Python3.11
e bibliotecas são resolvidos do lock com hashes no cache do usuário. Os binários
de PDF/renderização/imagem vêm nas wheels portáveis, sem Office/Poppler/Tesseract.
As bibliotecas não interpretam regras trabalhistas nem executam LLM/OCR remoto.

## Formatos e conferência

| Entrada | Saída local para a harness |
|---|---|
| PDF textual | Texto e PNG por página selecionada; total de páginas |
| PDF digitalizado | PNG por página; leitura visual/OCR pela própria harness |
| PNG/JPEG/TIFF/BMP/WebP | PNG por frame, mantendo conferência visual pendente |
| XLSX | Células/tipos/formatos, datas e durações; fórmulas e cache separados |
| XLS | Células/tipos e modo de data Excel, sem executar macros |
| DOCX | Parágrafos do corpo, tabelas, cabeçalhos/rodapés, notas/comentários |
| ODT/ODS | Parágrafos/títulos ou células, incluindo cabeçalhos/linhas agrupadas |
| CSV/TXT/MD/JSON/XML | Linhas/células ou texto, codificação explícita |
| ZIP | Leitura dos membros suportados em memória, sem extrair caminhos no disco |

Limites por invocação: fonte32MiB, expansão de arquivos64MiB compartilhada,
até200páginas/frames renderizados,128MiB de PNGs e200mil unidades/células.
PDF/TIFF extenso exige `--pages` em lotes e novas pastas de saída. Teto2000
páginas/frames por arquivo. Limite atingido é erro, não extração parcial aceita.
Arquivos ativos, DTD/XML, macros detectadas em contêineres e caminhos inseguros
são recusados. Formatos desconhecidos aparecem no inventário como pendência.
Arquivos legados .doc/.rtf e .xlsm não são executados/conversões automáticas.

## Operação sem novo OAuth

Após abrir conversa nova, invocar `/loki-orientacoes:operar-loki` no Claude ou
`$operar-loki` no Codex. Pedir diagnóstico local e indicar a pasta/documentos.
A harness lê a skill e executa:

```text
uv run --no-project --locked --python 3.11 --script "SCRIPT_ABSOLUTO/loki_local.py" doctor "PASTA_PRIVADA_NOVA"
```

O caminho é relativo à skill carregada, não um checkout fixo do servidor.
No Windows, a mesma invocação aceita caminhos absolutos com espaços no PowerShell.
Entradas/saídas/recibos ficam em workspace privado fora do cache do plugin.
POSIX usa0700/0600; Windows remove herança e limita ACL ao usuário e SYSTEM.
Uma saída existente é preservada; usar outra pasta em nova leitura/revisão.

A harness consulta identidade, instruções, schemas e snapshots pelo MCP já
autenticado. Os leitores só preparam arquivos: não acessam cofres, tokens,
configuração dos clientes, rede, SDK MCP ou APIs de LLM. A primeira execução uv
pode baixar Python/dependências do canal fixado; isso é distinto de ler documentos.

Os envios são **somente parâmetros e CSVs**, por chamadas MCP da harness.
Originais, ZIPs e imagens não sobem ao Loki. `source-csv` produz uma declaração
da leitura com hash/localizador do original local. `csv-request` calcula base64
do CSV real e gera pedido ainda não enviado. A resposta é salva integralmente;
`receipt` registra pedido/resposta, sem inferir sucesso/aprovação de um BLOCKED.

O ID/hash remoto é o CSV efetivamente recebido. Não atribuir a ele o hash/ID do
PDF local nem rotulá-lo como ASO/TRCT para remover pendências. O servidor atesta
integridade do CSV; não prova leitura independente do original. Staging tipado
de onboarding não aplica cadastro automaticamente. Permissões administrativas,
snapshots, decisões humanas e demais gates continuam sendo os do backend.

A [skill operacional](../plugins/loki-bootstrap/skills/operar-loki/SKILL.md) e
seu [fluxo de contratos/retomada](../plugins/loki-bootstrap/skills/operar-loki/references/WORKFLOWS.md)
orientam execução, proveniência, lote e conferência.

## Manutenção

Alterar scripts e/ou dependências exige nova versão do plugin e lock do script.
Atualizar apenas esse plugin não modifica provider/wheel/backend. O runtime
assinado antigo e seus pins não são editados; não usar seu sincronizador de
originais neste fluxo. Nenhum cron, timer, serviço ou tarefa Windows é instalado.

Os testes geram documentos sintéticos, exercitam os leitores/CLI reais e comparam
o CSV com golden produzido pelo parser/renderizador do backend. A CI inclui
matriz Ubuntu/macOS/Windows. Execução local Linux não substitui execução da
matriz nem aceite do OAuth e dos leitores nas máquinas da equipe; o diagnóstico
e ensaio individual continuam sendo a evidência desse aceite.

Referências: [dependências de skills no Codex](https://learn.chatgpt.com/docs/build-skills),
[layout do plugin Claude](https://code.claude.com/docs/en/plugins-reference),
[instalação oficial uv](https://docs.astral.sh/uv/getting-started/installation/).
