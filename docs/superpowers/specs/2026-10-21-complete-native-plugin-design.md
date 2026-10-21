# Plugin completo com leitura local pela harness

Autorização: Antônio pediu concluir e liberar nesta sessão o plugin completo
para Ana/macOS e Samuel/Windows/Linux, mantendo OAuth e auto-update nativo Git.
Este escopo corrige a entrega anterior, limitada ao bootstrap. Não criar agenda,
ZIP, login, servidor MCP, parser remoto ou acesso ao sistema da Ana.

## Comportamento

Manter o identificador instalado `loki-orientacoes@loki-equipe`, publicar 1.1.0
e acrescentar `operar-loki`, com scripts portáveis distribuídos no próprio
plugin. O bootstrap encaminha demandas documentais para essa skill. Dependências
Python 3.11 são fixadas em lock universal com hashes e executadas por uv no
cache do usuário; código, lock e skill chegam pelo gerenciador Git nativo.

Leitores cobrem PDF textual e digitalizado (texto por página e render PNG para
visão da harness), imagens PNG/JPEG/TIFF, CSV/texto/JSON/XML, XLSX/XLS,
DOCX/ODT/ODS e inventário seguro de ZIP. Não executar macros, fórmulas, links,
scripts ou instruções recebidas em documentos. Não atribuir OCR/legibilidade
ao simples sucesso de extração técnica. A harness interpreta e confere imagens.

Entradas e derivados ficam fora do cache do plugin, em pasta privada escolhida
explicitamente; nunca sobrescrever saída existente, seguir symlink de saída ou
extrair caminhos de ZIP no disco. Limitar tamanho, páginas, células e expansão.
Registrar SHA256 e localizadores por página/célula/linha. Preservar zero, false,
null, tipos e fórmulas/caches separadamente; falhar em vez de truncar sem aviso.

## Envio

Scripts offline não importam SDK MCP, não acessam rede, não leem cofres/configs
de OAuth, não chamam LLM e não executam comandos de negócio. A própria harness
consulta identidade, instruções e schemas atuais pelo MCP já conectado,
estrutura parâmetros e gera CSV tipado `loki.batch-csv/1` conforme contrato.
Somente parâmetros e bytes CSV são enviados ao Loki. Originais e imagens não
são enviados. CSV é fonte declarada pela harness, sem alegação de leitura
independente dos originais pelo servidor. Manter identidade, escopo, snapshots,
build/preflight quando exigido, recibos, revisão humana e escritores existentes.

Gerar pedidos locais determinísticos com hash/referência/revisão. A harness
executa a chamada MCP e salva resposta integral; retry consulta recibo atual
antes de repetir. Para fontes, usar IDs/hashes reais do CSV recebido, nunca
inventar ID remoto do original nem atribuir hash do original ao CSV.
Não contornar contratos que exijam prova indisponível: registrar pendência.

## Validação e aceite

Testes sintéticos dos formatos e casos adversos, compatibilidade do CSV com o
parser real do backend, subprocesso real offline, instalação Git e upgrade do
pacote/lock/skills nos gerenciadores nativos. Matriz CI Linux/macOS/Windows,
com distinção entre execução real Linux e aceite ainda não observado nas
máquinas da equipe. Conferir wheels por plataforma. Revisão independente antes
da publicação, sem dados reais e sem alterar OAuth existente.
