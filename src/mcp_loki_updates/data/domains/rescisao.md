# Rescisão

## Episódio de afastamento e faixa de responsabilidade

No schema servido, `representacao=episodio_integral` conserva a interpretação
legada do episódio, incluindo a partição inicial do empregador quando aplicável.
`representacao=faixa_pagador` é opt-in para intervalo já dividido por responsável;
não desconta novamente os primeiros15dias da faixa declarada como INSS.
Essa indicação não presume concessão, espécie, continuidade clínica ou vínculo
entre intervalos vizinhos. Coleção mista, sobreposição ou responsabilidade
conflitante precisam ser conciliadas pelos dados reais e pelo contrato.

`retorno_episodio` informa o retorno efetivo quando a faixa não encerra o episódio.
Não deduza esse fato do último dia do pagador. Sem retorno necessário conhecido,
somente o efeito dependente permanece pendente. Ausência dos campos novos
preserva o formato e a interpretação legados; entrada, versão, seleção e memória
do cálculo precisam comprovar consumo antes de afirmar destrave financeiro.

## Faltas mensais e elegibilidade do 13º

Consulte `get_process_contract` antes de preparar `faltas_decimo_terceiro`.
Quando o schema oferecer `loki.thirteenth-absences/1`, informe janela, corte,
competências, completude e ocorrências com a natureza e os dias realmente
conhecidos. Uma declaração atribuída ao pedido pode bastar; fontes por campo
são opcionais. Ausência de competência ou cobertura não significa zero faltas.
Preserve faltas justificadas, partição patronal/INSS e conflitos entre fontes;
não some novamente a mesma ocorrência do pedido e do histórico.

Confira `elegibilidade_decimo_terceiro` no resultado, quando persistida, e
confronte avos informados e derivados. Não altere o inteiro para vencer uma
recusa. Dados que já determinam a elegibilidade podem sustentar a parcela sem
redigitação; uma competência indeterminada retém somente os dependentes.
O 13º sobre aviso tem escopo próprio. Memórias e políticas de centavos devem
ser conferidas por cálculo e versão, sem aplicar retroativamente o cadastro.

Pensão/IR interdependentes só usam o regime explicitamente oferecido no schema,
qualificado por ato, base, dedutibilidade, percentual, processo e vigência.
Não use um regime pós-impostos como aproximação; incerteza do ato ou do imposto
permanece limitada aos resultados dependentes e não vira autorização de pagamento.

## Consignado: contrato, competência e rescisão

Consulte `get_company_onboarding_contract` e os parâmetros efetivamente
oferecidos. `credito_trabalhador_contratos` registra revisões de contrato,
número como string, instituição, vigência, parcela em centavos e
`rubrica_loki` explícita. Encerramento/cancelamento é outra revisão;
não altere revisões antigas nem presuma rubrica por código numérico global.

Na folha, `credito_trabalhador_competencia` identifica os contratos/versões
confirmados no mês e as qualificações exigidas pelo schema. Declaração atribuída
pode ser aceita, sem documento/hash universal. Cronograma não comprova desconto
pago ou repasse; confira memória, limites, operandos e pendências.

Na rescisão, `credito_trabalhador_rescisao` é snapshot próprio da consulta,
com data do desligamento/consulta, identidade, completude, contratos, saldos e
garantias informados. Parcela mensal não vira saldo devedor.
Consulta automática Dataprev exige acesso corporativo e contrato técnico próprio;
importação estruturada disponível não comprova integração automática ativa.
Sem dados/qualificação específicos, preserve o resultado dependente pendente.

## Pensão por finalidade

Analise o ofício/decisão na harness antes de preparar
`pensao_alimenticia_regra`, pelo contrato de onboarding/parâmetros autorizado.
Originais permanecem na harness; a regra extraída conserva referência, vigência
e autoria, sem anexação ou hash por campo universal.
Quando oferecido, `loki.pension-rule/2` define aplicações explícitas para
`folha_mensal`, `ferias`, `decimo_terceiro` e `rescisao`, com situação,
rubrica, percentual, base, deduções, tratamento do IRRF e critério temporal.
Não estenda regra mensal a outra finalidade nem conclua “não beneficiário”
a partir de ausência. Política desconhecida retém parcelas dependentes.

No décimo terceiro, confira `apuracao` (`parcela` ou
`acumulada_com_compensacao`), `etapas` e retenção anterior efetivamente qualificada;
retenção omitida não é zero. Nas férias e na folha, confira a proveniência
da retenção já calculada para evitar consumo duplicado. Persistência do parâmetro
não demonstra consumo: releia a seleção e a memória do cálculo correspondente.


Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Registre valores ausentes como pendências, nunca como zero; mantenha divergências e origens para revisão. Não derive legislação, verbas, datas ou prazos a partir deste guia. As regras válidas e os gates de decisão devem vir do contrato operacional e das fontes aprovadas. O responsável humano deve cumprir os gates antes de qualquer efeito externo; não transmita nem publique resultados automaticamente.

## Pedido, aviso e anexos

Procure os originais e o histórico na tarefa correspondente ao fluxo de aviso trabalhado, indenizado ou pedido de demissão, usando somente acesso e canais já autorizados. O aviso pode ter sido emitido pela contabilidade ou pelo cliente; uma carta de demissão pode ser documento distinto. Registre origem, datas, localizador e eventual orientação posterior. Não deduza modalidade ou datas pela simples ausência do arquivo.

Anexo que não abriu é falha de acesso, não prova de inexistência. Preserve a falha e peça o original ou sua localização no canal autorizado, sem repetir pedido já pendente e sem buscar senhas ou contornar permissões. A explicação geral do fluxo não localiza automaticamente um anexo de um caso específico.

Se o cliente tiver comunicado o desligamento sem encaminhar documento, registre os fatos efetivamente informados e a orientação específica com sua origem. Só avance no que o contrato permitir, com pendências e revisão; não fabrique aviso, assinatura, carta ou ciência do empregado para completar o processo. Comunicação relatada não substitui aceite humano nem prova documental ausente.

## Histórico e médias

Consulte o contrato e os estados históricos correntes antes de afirmar que folha importada sustenta o cálculo. Cadastro importado, matrícula presente, histórico carregado, identidade qualificada, estado selecionado e consumo pelo calculador são etapas distintas. Não prometa que fatos antigos viram automaticamente médias, faltas aquisitivas ou saldo de FGTS. Qualifique empregado/vínculo, competência, rubricas, bases e fontes e preserve lacunas de cobertura; “não se aplica” só é válido se sustentado pelo caso e aceito pelo contrato, nunca como substituto de verba dependente de dado ausente.

Recusa de acesso técnico à carga histórica não autoriza conceder capacidades humanas, usar identidade de pessoa por automação ou criar canal de envio alternativo. Preserve o pedido para a operação administrativa correspondente; estas instruções não habilitam processos ou importadores.

Com raiz mínima válida, ausência de operandos não deve ser completada com zero nem impedir por orientação da harness as parcelas independentes admitidas pelo contrato. Dependentes desconhecidos mantêm IRRF e totais dependentes desconhecidos; saldo FGTS ausente pode reter a guia correspondente. Dado contraditório conserva conflito e não equivale a mera ausência. Não prometa cálculo integral nem documento condicionado sem os insumos próprios.

Consulte `get_case_historical_state` e selecione somente o estado tipado aceito por `apply_historical_state` no caso e corte correntes. A seleção e as qualificações de `receive_case_data` não são a fixação legada de um histórico opaco. Confira recibo de carga, releitura, identidade, cobertura, seleção, hash/operandos e consumo efetivo nos resultados de rescisão e folha. Episódio errado, competência/corte errado, fonte adulterada, revisão superada ou cobertura insuficiente impedem a seleção correspondente; preserve as parcelas independentes disponíveis sem contaminar seu cálculo. Não declare consumo apenas porque o histórico existe.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Complemento de identidade ausente

`funcionario.nome` é identidade do caso, não um campo de `dados_rescisao` ou da
seção de cálculo. Consulte `get_process_contract` e `get_case` atuais. Somente se
o contrato oferecer `identity_completion_schema` e a rota autorizada, prepare o
request `loki.case-identity-completion/1` com `request_ref` estável,
`expected_snapshot=get_case.correction_snapshot`, `input_snapshot` corrente,
`expected_company_id`, `expected_employee_id`, `expected_admission_date` e `nome`
observado/declarado com origem honesta. Valide offline por `parameters` usando
`--schema contract.json --schema-pointer /identity_completion_schema`.

Use `complete_case_identity(case_id, request)` quando descoberto; se o contrato
anunciar `receive_case_data` como rota compatível para esse discriminador, envie
exatamente o mesmo request por essa rota, sem envelope `loki.case-data/1` e sem
misturar o nome à seção financeira. Rota ausente é lacuna de distribuição HTTPS;
não improvise escritor. Esse complemento só preenche nome antes vazio da mesma
empresa, pessoa e episódio. Nome já preenchido, divergência de identidade ou
snapshots antigos conservam recusa/pendência; não substitua nome nem cadastro.
Preserve recibo e replay idêntico, releia nome e ambos os snapshots antes de
retomar geração. A operação não cria decisão humana nem efeito financeiro.

Na automação, o caminho concreto é `get_case_historical_state(case_id)` →
conferir identidade, corte, cobertura e `state_hash` →
`apply_historical_state(case_id, expected_state_hash)` → reler recibo/estado →
conferir consumo no cálculo. Pin legado pode exigir pessoa; não troque identidade
para contornar a recusa. Seleção não comprova pagamento ou ocorrência aplicada.
Não use meses tocados como avos devidos nem copie avos do TRCT comparado para
completar a entrada. Dados ausentes mantêm parcelas dependentes pendentes;
este guia não oferece fórmula universal de avos.

## Saldo de salário na rescisão

Quando o calculador servido oferecer o alcance qualificado, admissão e
rescisão no mesmo mês civil de 30 dias, com divisor 30 e sem afastamento
sobreposto, usam o intervalo contratual inclusivo das datas
reais de admissão e desligamento. É uma inferência técnica documentada das
fontes aplicáveis e da semântica temporal, não medição histórica nem regra
universal de calendário. A harness informa fatos; os dias e centavos são derivados
pelo motor, sem entrada livre para coincidir com a referência.

O consumidor `rescisao-v42` estende o alcance ao mesmo mês civil de 31 dias,
com divisor 30, desligamento até o dia 30 e sem afastamento sobreposto. A versão
nova é selecionada somente nesse predicado. Mês30 e contratos anteriores
permanecem no alcance próprio; fevereiro, desligamento no dia31 e outros
divisores não são habilitados por essa extensão. Releia dias, seleção e memória;
`regra_nao_medida:saldo_admissao_no_mes` continua um diagnóstico possível fora
do alcance qualificado. Não adapte a data ou o divisor para coincidir com o comparador.

`regra_nao_medida:saldo_admissao_no_mes` pode continuar pendente fora desse alcance; fevereiro,
dia31, divisores e afastamentos seguem suas guardas próprias. Atualização de
instruções não corrige o calculador publicado nem certifica o caso completo.
Confira versão do motor, dias, memória e bases; não reutilize memorial parcial
antigo ou aceite anterior como resultado da regra nova. Parcelas independentes
permanecem disponíveis conforme o contrato, sem preencher ausência com zero.
