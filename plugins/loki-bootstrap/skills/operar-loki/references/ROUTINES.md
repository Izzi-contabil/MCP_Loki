# Rotina pela harness do Claude Code ou Codex

Este roteiro complementa `operar-loki` e `WORKFLOWS.md` em execuções agendadas,
filas e avaliações. Cada rodada usa a conexão MCP existente, o acesso efetivo e
os contratos do serviço. A versão do plugin não identifica o build do Loki.

## Descoberta antes da fila

Consulte `meu_acesso` (fallback: `get_operator_context`), leia as instruções
retornadas e consulte `loki_verificar_versao`, informando apenas versões de
cliente conhecidas. Obtenha as instruções geral/documentos e do domínio
autorizado quando disponível. Consulte `get_dp_capabilities` e `list_workflows`;
leia todos os blocos JSON, pois `structuredContent` pode conter só o primeiro
item. Para o processo, consulte `get_document_processing_contract` e
`get_client_readiness` com empresa/competência pertinentes.

O cadastro estar pronto informa sua consistência, não a completude do cálculo.
Lista antiga de processos não implementados não substitui a descoberta atual.
Ferramenta ausente, acesso recusado e contrato indisponível ficam registrados
separadamente; não troque identidade, amplie permissões ou remova pins.

## Seleção de insumos e histórico

Mantenha as referências estáveis da fila, pedido, caso, episódio e ocorrência.
Confirme CNPJ, CPF, admissão e corte do consumidor. Consulte
`get_company_employee_history` antes de pedir novamente um dado já fornecido.
Quando aplicável, `preview_case_input_reuse` mostra fontes, ausências e conflitos;
aplicação usa somente o plano autorizado e o hash corrente. Fixação por
`pin_company_employee_history` ou seleção do estado tipado segue o contrato.
Consulta, fixação, consumo e cálculo são evidências distintas.

Se o operador indicar um índice privado de componentes qualificados, siga
também [COMPARATIVE_TESTING.md](COMPARATIVE_TESTING.md). Confira a edição,
os hashes e as retenções antes da seleção. Um arquivo privado deste servidor
não está automaticamente disponível em outro computador.

Separe pedido do cliente, histórico interno e referência produzida pela equipe.
Congele a saída antes da comparação. Não complete entradas com o gabarito.
Ausência de folha histórica é diferente de dado ausente no pedido do cliente.
Fatos reportados, registros de pagamento e códigos impressos não definem
automaticamente fórmula, incidência, direção financeira ou política empresarial.

Leia os originais pelos leitores instalados e pela visão da harness, mantendo
hashes/localizadores. Envie somente parâmetros e CSVs conforme `WORKFLOWS.md`.
TXT, XLS e PDF podem conter referências históricas; conteúdo, empresa, episódio
e período definem o papel. Arquivo obtido não é operando qualificado. Data de
registro de reajuste retroativo não é automaticamente o dia de efeito material.
Sem esse dia, preserve a competência retroativa e a lacuna necessária ao cálculo.

## Escolha do executor

Use `execution_modes`, `available_via`, `package_kind` e `versioned_case` do
contrato corrente. A tabela indica os caminhos a confirmar, não habilita fluxos:

| Processo | Caminho versionado a conferir | Pacote e condição |
|---|---|---|
| Afastamento | `simulate_case_version` | Factual; exige cenário shadow explícito |
| Alteração cadastral | `simulate_case_version` | Proposta factual, sem aplicação canônica |
| Ocorrência | `simulate_case_version` | Factual, sem lançamento financeiro |
| Aviso de férias | `simulate_case_version` | Documental, independente do cálculo completo de férias |
| Aviso de rescisão | `simulate_case_version` | Documental, independente do cálculo completo de rescisão |
| Adiantamento | `simulate_case_version` | Financeiro, por política vigente e fonteada |

Monte o request pelo schema do processo; não transponha campos ou marcadores de
outro fluxo. Use referência estável para retomar a mesma tentativa. Um pacote
factual não exige PDF; um aviso não exige valores de TRCT ou férias para avançar
parcialmente. Adiantamento sem política/operando mantém o resultado dependente
pendente; não há percentual padrão. Registro documental não aplica cadastro,
não registra pagamento e não efetiva desligamento.

## Conferência e resultado da rodada

Nas versões, consulte `get_case_version`; baixe `receipt.json` e todos os
artefatos por `get_case_version_artifact`. Confira o contexto completo do recibo,
os bytes, os hashes e cada página de PDF. Use os checks e referências do
contrato em `submit_case_version_verification`. Nos fluxos canônicos, siga a
requisição de conferência do pacote atual. Registre PASS só para observação
efetiva. Preserve os achados anteriores e as pendências do pacote parcial.

O recibo privado da rodada identifica: executor/versão do plugin observados,
build/instruções, processo, pedido/caso/versão, corte e fontes selecionados,
executor escolhido, artefatos conferidos, pendências e resultado. Use apenas
classificações aceitas pelo schema do relatório externo; detalhe a limitação no
comentário aplicável. Não converta preparo parcial em sucesso financeiro nem
regrave julgamentos anteriores. Não aprove, publique, pague ou transmita.

## Ativação no executor real

Atualize o plugin pelo mecanismo nativo e confira a versão instalada. Recarregue
os plugins ou abra nova sessão antes de alterar o roteiro da rotina existente.
Preserve horário, referências e credenciais; não crie outra rotina para contornar
falta de acesso. Se a fila não entregar determinado tipo, registre a limitação
do mapeador. Disponibilidade no Loki não altera filtros de outro sistema.

Uma liberação registra separadamente: release publicada, versão instalada,
roteiro salvo e execução observada. Os três últimos exigem prova no ambiente
do operador; o sucesso no computador do desenvolvedor não os comprova.
