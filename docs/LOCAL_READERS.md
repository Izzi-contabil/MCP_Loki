# Leitores externos — plugin2.2.0

O plugin nativo mantém o nome `loki-orientacoes@loki-equipe` e inclui bootstrap, operação, investigação de regras e suporte. As instalações1.0.2 recebem código, skill e lock
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

Para um caso, a harness prepara dados estruturados e fontes no contrato
`loki.case-data/1`, usando `get_process_contract` e `get_case.input_snapshot`.
`case-request` valida/prepara o pedido offline para `receive_case_data`; o helper
não envia. Leitura, preparação e comparação são externas. Originais permanecem
na harness; ao Loki seguem parâmetros e, opcionalmente, proveniência estruturada pelo
HTTPS. Se o contrato exigir original novo, registre lacuna contratual, sem
fabricar DOC ou reclassificar documento como declaração. Fonte já registrada
pode ser selecionada pelo contrato autorizado.
`receipt` preserva pedido e resposta, sem transformar BLOCKED em sucesso.

`source-csv` pode produzir evidência externa de leitura. `csv-request` só prepara
CSVs de onboarding nos contratos específicos autorizados; staging não aplica
cadastro nem transforma a leitura em conferência independente do servidor.
Permissões, snapshots, decisões e demais gates continuam no backend.

Para operações em lote, `render-operational-csv` e `operational-batch-request`
preparam o schema de `get_operational_batch_contract()` para
`execute_operational_batch`: CSV UTF-8 tipado em `csv_content`, até100linhas/8MiB,
JSON estrito por linha, allowlist corrente e dependências anteriores. Sem upload,
SDK ou transporte no leitor. A harness chama o conector e consulta
`get_operational_batch(batch_id)`; lote é sequencial/não atômico e STARTED ambíguo
exige conciliação. Preparação offline não comprova execução nem efeito aplicado.

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


`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Extensão eSocial2.2.0

Provider0.3.1, contrato/instruções/plugin2.2.0 preservam o mínimo2.0.0 e a
compatibilidade declarada de2.0/2.1; cliente desconhecido continua desconhecido.
A allowlist e as permissões dos domínios permanecem: consulte `geral` e
`alteracao_cadastral` para as cinco ferramentas HTTPS de modo fiscal e parâmetros.
Veja o roteiro nativo [ESOCIAL.md](../plugins/loki-bootstrap/skills/operar-loki/references/ESOCIAL.md). A configuração de homologação
pode persistir por intenção de administrador humano; não transmite. Operação
permanece PENDING/recusada sem fila/executor fiscal, assinatura, representação
e recibo de homologação verificados. S-1005 local não comprova transmissão.
Perfis por estabelecimento/data usam os escritores empresariais com CAS,
origem opcional e releitura; seleção não comprova consumo financeiro.

Esta distribuição não provisiona acesso fiscal, não emite eventos pelo catálogo
HTTPS e não instala o plugin no operador. Wheels anteriores, inclusive0.3.0,
permanecem imutáveis; promoção/publicação exigem revisão e gates do consumidor.

O helper `loki_local.py --version` informa a edição local declarada do plugin.
Para perfis empresariais, `parameters perfil.json SAIDA_NOVA --schema contrato-esocial.json
--schema-pointer /company_parameters_schema` usa o schema retornado por
`get_company_esocial_contract`; `validated_not_sent` não comprova autorização,
CAS, semântica do perfil, envio ou prontidão fiscal. Script e lock permanecem
juntos; dependências dos leitores não mudaram nesta extensão.
