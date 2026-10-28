# Rotina pela harness do Claude Code ou Codex

Este roteiro complementa `operar-loki` e `WORKFLOWS.md` em execuções agendadas,
filas e avaliações. Cada rodada usa a conexão MCP existente, o acesso efetivo e
os contratos do serviço. A versão do plugin não identifica o build do Loki.

Ao fechar a rodada ou uma execução com falha técnica persistente/bloqueio
inesperado, carregue [registrar-problema-loki](../../registrar-problema-loki/SKILL.md).
Com autorização vigente de suporte no mesmo escopo, registre automaticamente
o relato sanitizado e inclua UUID/recibo no resumo da rodada; não delegue a
redação ao humano. Pendência prevista não é erro automático. Agregue sintomas
da mesma ocorrência e preserve UUID/conteúdo nas retomadas; falha do suporte
não gera novo relato recursivo. Sem autorização, prepare e aguarde a escrita.

O objetivo é reproduzir o trabalho real da equipe em todas as finalidades do DP.
Cadastro, histórico, parâmetros, regras e fontes consumidos devem ser registrados
nos contratos nativos do Loki; arquivos externos orientam a leitura e não formam
um banco operacional paralelo. Não espere um kit de dados para começar uma tarefa
que já tenha fontes suficientes. Documentos de clientes usam o Drive autorizado
da organização, nunca uma conta pessoal indicada em referência histórica.

## Descoberta antes da fila

Consulte `meu_acesso` (fallback: `get_operator_context`), leia as instruções
retornadas e consulte `loki_verificar_versao`, informando apenas versões de
cliente conhecidas. Obtenha as instruções geral/documentos e do domínio
autorizado quando disponível. Consulte `get_dp_capabilities` e `list_workflows`;
leia todos os blocos JSON, pois `structuredContent` pode conter só o primeiro
item. Para o processo, consulte `get_process_contract` e
`get_client_readiness` com empresa/competência pertinentes.

O cadastro estar pronto informa sua consistência, não a completude do cálculo.
Lista antiga de processos não implementados não substitui a descoberta atual.
Ferramenta ausente, acesso recusado e contrato indisponível ficam registrados
separadamente; não troque identidade, amplie permissões ou remova pins.

## Seleção de insumos e histórico

Mantenha as referências estáveis da fila, pedido, caso, episódio e ocorrência.
Confirme CNPJ, CPF, admissão e corte do consumidor. Consulte
`get_company_employee_history` antes de pedir novamente um dado já fornecido.
Consulte também `get_company_historical_state` no corte do consumidor quando
precisar de saldos, ocorrências e coberturas tipados. Histórico opaco não vira
automaticamente um fato tipado, e consulta não comprova consumo pelo cálculo.
Quando aplicável, `preview_case_input_reuse` mostra fontes, ausências e conflitos;
aplicação usa somente o plano autorizado e o hash corrente. Fixação por
`pin_company_employee_history` ou seleção do estado tipado segue o contrato.
Consulta, fixação, consumo e cálculo são evidências distintas.

Se o operador indicar um índice privado de componentes qualificados, siga
também [COMPARATIVE_TESTING.md](COMPARATIVE_TESTING.md). Confira a edição,
os hashes e as retenções antes da seleção. Um arquivo privado deste servidor
não está automaticamente disponível em outro computador.
Sem esse índice, continue pelo cadastro, histórico e fontes autorizadas existentes.

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

## Investigar e qualificar regras

Ao encontrar falta de dado, fórmula, parâmetro ou divergência recorrente, leia e
aplique [investigar-regras-dp](../../investigar-regras-dp/SKILL.md) como parte da
rodada. Retome a investigação existente, consulte o acervo e qualifique hipóteses
por normas e histórico antes de pedir complemento. Configuração do ERP é uma
fonte possível, não um requisito universal quando outras fontes são suficientes.

O registro distingue calibração, validação reservada, regra gravada e consumo
pelo executor. Regra não expressável no contrato/motor segue reprodução e fluxo
autorizado de correção de produto; as partes independentes continuam. Preserve
retenções e registre a próxima ação concreta no recibo da rodada. O avanço só
encerra o bloqueio após execução e conferência pertinentes.

## Execução e resultado

Siga `get_process_contract` e envie a seção estruturada e fontes por
`receive_case_data`, com referência estável e snapshot corrente. Depois execute
`run_prepared_case_workflow` ou cálculo, geração e revisão do contrato. A empresa
de teste usa esse mesmo fluxo; versões internas preservam auditoria.

Afastamento, alteração cadastral e ocorrência conservam fatos e efeitos
qualificados; não deduza pagamento, classificação ou efeito financeiro de um
registro isolado. Avisos autônomos não exigem completar o cálculo do processo
pai. Adiantamento exige política vigente e operandos fonteados. Parcial útil
mantém os resultados dependentes desconhecidos e os conflitos existentes.

Confira externamente recibos, bytes/hashes e páginas dos PDFs; comparação com a
equipe também é externa. O resumo privado identifica executor/plugin observado,
build/instruções, processo/caso, snapshot, fontes consumidas, artefatos e
pendências. Separe recebido, calculado, gerado, revisado e entregue. Entrega ao
solicitante usa acesso autenticado e recibo; Drive é opção futura explícita.
Não crie outra agenda, altere a fila da Ana ou classifique conferência como entrega.

## Cobertura e acerto das tarefas

Mantenha uma linha por pedido e finalidade, inclusive quando o tipo não chega à
fila ou não possui executor disponível. Para cada processo, acompanhe recebidos,
executados, conferidos, comparáveis, coincidentes, parciais e bloqueados, com
período, denominador e exclusões explícitos. Registre campos e parcelas para
diagnosticar diferenças, mantendo separado o acerto da tarefa completa.

Use a meta autorizada para priorizar divergências e ampliar cobertura de todas
as finalidades descobertas nos contratos. Tipos sem amostra continuam no mapa.
Pacote parcial, cadastro pronto, teste técnico e percentual de campos de uma só
finalidade não comprovam a meta geral. Preserve o indicador existente e acrescente
o recorte por tarefa sem alterar contadores do sistema externo.

## Achados para o suporte

Para erro, bloqueio ou sugestão, siga
[registrar-problema-loki](../../registrar-problema-loki/SKILL.md). Separe defeito
reproduzido, divergência observada e falta de informação. Se a rotina já tiver
autorização humana para avisar o suporte, envie o relato sanitizado pela ação
`registrar_problema`; caso contrário, preserve-o para autorização. Registre ID,
estado e identificador da mensagem quando houver entrega confirmada. Retomadas
usam o mesmo ID/conteúdo; não repita execução de negócio para relatar um erro.

## Ativação no executor real

Atualize o plugin pelo mecanismo nativo e confira a versão instalada. Recarregue
os plugins ou abra nova sessão antes de alterar o roteiro da rotina existente.
Preserve horário, referências e credenciais; não crie outra rotina para contornar
falta de acesso. Se a fila não entregar determinado tipo, registre a limitação
do mapeador. Disponibilidade no Loki não altera filtros de outro sistema.

Uma liberação registra separadamente: release publicada, versão instalada,
roteiro salvo e execução observada. Os três últimos exigem prova no ambiente
do operador; o sucesso no computador do desenvolvedor não os comprova.

Fontes `kind=document` exigidas como evidência nativa usam `document.reference` com o ID do anexo retornado por `attach_source_document` e `content_hash` igual ao retorno. O upload arquiva o original como bytes opacos; o Loki não extrai nem interpreta seu conteúdo. Não invente DOC com caminho local, ID do Drive ou hash avulso. Leitura externa declarada pode usar `kind=declaration`, referência/localizador/fundamento honestos e seus limites; isso não atesta verificação documental nativa. Quando identidade, efeito ou qualificação exigir fonte nativa, arquive o original opacamente ou selecione a fonte nativa já persistida/pinnada indicada pelo contrato. Não troque a classificação da origem para fabricar qualificação.
