# Décimo terceiro

As regras de etapas, competência, envio e recusas abaixo valem somente quando a
resposta servida e o contrato de `get_process_contract("decimo_terceiro")` as
apresentarem.

## Etapas e meses

- `primeira`: `data_pagamento` de fevereiro a novembro do `ano`; `meses` de 1
  até o mês anterior ao pagamento (pagamento em 20/11 → meses 1 a 10). Sem
  referências anteriores (`casos_anteriores=[]`, sem `historical_payments`).
- `segunda`: `data_pagamento` entre 01/12 e 20/12 do `ano`; `meses` de 1 a 12.
  A variável da segunda é a média de janeiro a novembro (÷ 11): dezembro pode
  ir com `variavel_cents: null`.
- `ajuste`: `numero_ajuste ≥ 1`, `data_pagamento` entre 01/01 e 10/01 do ano
  seguinte; `meses` de 1 a 12, dezembro com valor.
- Sem `medias_importadas`, cada mês exigido leva `variavel_cents`. Zero só
  quando a fonte disser zero; ausência não vira zero.

## Competência do caso

`create_case` do 13º exige `competencia` no dia 1 do mês do pagamento da
parcela (1ª paga em novembro → `AAAA-11-01`; 2ª → `AAAA-12-01`; ajuste →
`(AAAA+1)-01-01`). Competência fora do dia 1 ou ausente é recusada na criação
(`thirteenth_competence_required`, campo `competencia`); repetir a criação de
um caso antigo sem competência também é recusado, em vez de devolver o caso
existente. Competência diferente do mês de `data_pagamento` é recusada
(`thirteenth_competence_mismatch`, `next_action=cancel_case`). A competência
não se corrige no caso: cancele o caso antigo com `cancel_case` e só depois
recrie com a competência certa. Não envie `occurrence_ref` no 13º operacional
(`occurrence_ref_requires_shadow_scenario`).

## Envio por partes

A seção pode ir em mais de uma chamada de `receive_case_data`, cada uma com o
`expected_snapshot` atual e um `request_ref` próprio. Por exemplo: primeiro os
obrigatórios com `casos_anteriores=[]`, depois `historical_payments`. Uma regra
que depende de `historical_payments`, `numero_ajuste`, `afastamento_source` ou
`medias_importadas` só é cobrada no cálculo quando esse campo ainda não foi
enviado. As demais regras são cobradas no receive. Caso cancelado ou fora de
preparação é recusado pelo estado (`caso_fora_de_estado_gravavel`) antes de
qualquer erro de campo.

## Parcelas pagas fora do Loki

Caso operacional não usa `casos_anteriores` (recusa
`thirteenth_prior_cases_require_shadow`). A 2ª parcela e o ajuste leem o que já
foi pago por `historical_payments`, com os IDs `ONBFACT-…` de fatos de
onboarding `kind=historico_operacional` (`data.version=historical-state-v1`):

- `type=thirteenth_payment` com `occurrence`, `year`, `installment`
  (1 = adiantamento, 2 = segunda), `paid_on`, `gross_cents`, `inss_cents`,
  `irrf_cents`, `fgts_cents` (INSS/IRRF em zero na 1ª, **nunca nulos**) e
  `confirmed: true`;
- `type=coverage`, `complete: true`, para `consumer=thirteenth_payments` (de
  01/01, ou da admissão, até a data de pagamento desta parcela) e
  `consumer=leave_occurrences` (até o corte da etapa).

A cadeia traz todas as parcelas anteriores (1..N-1), confirmadas e pagas até a
data desta parcela. Fluxo:

1. Envie a seção com `casos_anteriores=[]`, sem `historical_payments`. O
   recibo avisa, em `pending_rules`, o que ainda falta. É só aviso: não é
   recusa, e o reenvio do mesmo `request_ref` devolve o recibo sem ele. Quem
   cobra é o cálculo.
2. Consulte `get_case_historical_state` do próprio caso e leia os ids
   `ONBFACT-…` dos fatos `thirteenth_payment`.
3. Envie `historical_payments` com esses ids.
4. Aplique o estado (`apply_historical_state`) e calcule.

O corte do estado depende só de `ano`, `etapa` e `data_pagamento`.
`thirteenth_payment_coverage_not_certified` segue a regra de cobertura do
domínio `ferias` ("Cobertura desde a admissão até o corte"): com o estado
`historical-state-v2`, uma cobertura completa desde a admissão que termina
depois do corte também limpa o gap, só até o corte.

**Recusa de cobertura.** `historical_thirteenth_coverage_incomplete` (campo
`historical_state`, próxima ação `get_case_historical_state`) traz
`required_windows` e `missing_intervals`, cada um com `consumer`
(`leave_occurrences` ou `thirteenth_payments`), `start` e `end`. Declare na
carga histórica uma cobertura completa (`type: coverage`, `complete: true`) do
consumidor indicado que feche cada lacuna, selecione o estado de novo e
recalcule. Se a recusa vier sem janelas, a admissão do estado histórico é
posterior à referência salarial ou ao pagamento: confira a admissão e as
datas do 13º antes de declarar cobertura. Não presuma ausência de afastamento
ou de pagamento só porque falta cobertura.

## Médias

Para bater com o Domínio, use `medias_importadas` (média final do Domínio,
finalidade `decimo_terceiro`). Ela é exclusiva com `variavel_cents` mensal:
com ela, nenhum mês leva valor. A média por quantidade × valor atual e a
produtividade ainda dependem de confirmação da DP; até lá, use a média
importada.

**`final_average` é a média mensal integral do Domínio.** Envie essa média
inteira, como veio, em `medias_importadas={fact_id}`, sem `variavel_cents`
mensal. Nunca envie uma média já proporcional aos avos: o Loki aplica
`média × avos ÷ 12` em todas as etapas, e uma média já dividida sairia
dividida duas vezes. Na 1ª parcela, a média só entra inteira quando a pessoa
foi admitida antes do ano e tem todos os avos até o mês-limite, que é quando a
parte fixa também entra inteira. Para conferir com o Domínio, compare
`variavel_cents` com média × avos ÷ 12.

Os campos de seis casas (`horas_micros`, `valor_micros`, `vantagens_micros`)
e o `bloco` das médias, quando o contrato servido os apresentar, valem só nas
férias da rescisão (domínio `rescisao`). O 13º continua com os centavos e não
rateia por bloco. A DP informou (18/11/2026) que o Domínio soma as médias de
todas as empresas do grupo, sem separar por empresa, também no 13º: envie uma
média com a soma das empresas, sem `bloco`.

## 13º com média importada que já estava em revisão

Um caso em `aguardando_revisao` calculado antes desta versão perde o cálculo
atual, e os pacotes gerados ficam obsoletos de propósito: eles usavam a média
inteira. O caminho é:

1. registrar a decisão `ajustar`, com intenção humana explícita. O caso volta
   a `em_preparacao` com o payload intacto, sem reenviar nada;
2. `calculate_case`;
3. gerar os documentos de novo;
4. fazer nova conferência do pacote e levar à revisão.

`restart_case` com `preparation` também serve, mas obriga a reenviar a seção
`dados_decimo_terceiro` inteira. Casos `aprovado` ou `publicado` continuam com
o cálculo que gerou o pacote aprovado.

## Reiniciar um 13º

Se um campo já gravado estiver errado (mês, variável, dedução, fonte), use
`restart_case` com
`preparation={schema_version:"loki.case-preparation/1", mode:"replace_process_inputs", request_ref:<novo>}`
e `expected_snapshot=get_case.correction_snapshot`. Isso exige intenção humana
explícita, mas não exige a capacidade `corrigir_dados`. A seção volta só com
`ano`, `etapa` e `numero_ajuste`. Depois, mande a seção completa e corrigida
por `receive_case_data`, aplique de novo o estado histórico
(`apply_historical_state`), se for o caso, e recalcule. Ano, etapa e número do
ajuste não mudam no reinício (`preparation_identity_changed`); se um deles
estiver errado, cancele o caso e crie outro. Repetir o mesmo `request_ref`
devolve o recibo original. Casos aprovados ou publicados continuam fora do
reinício (`restart_requires_adjustable_state`).

## Dependentes de IRRF

O perfil documental é lido no corte da etapa: último dia do mês anterior ao
pagamento na 1ª (pagamento em novembro → 31/10) e 31/12 na 2ª e no ajuste. O
dependente precisa estar vigente nessa data. A 1ª parcela dispensa
dependentes, salvo pensão `interdependente` no 13º; a 2ª e o ajuste exigem
(`thirteenth_irrf_dependents_required` quando o valor é necessário).

## Recusas

`calculate_case`/`run_prepared_case_workflow` devolvem `BLOCKED` com `code`
(`thirteenth_parameters_invalid` ou `thirteenth_competence_mismatch`),
`fields`, `errors` e `months` (número dos meses apontados).
`receive_case_data` devolve `invalid_case_data` com `{field, reason, mes}`.
Nos dois, o código da regra é fechado `thirteenth_...` (ex.:
`thirteenth_months_incomplete_for_stage`,
`thirteenth_second_payment_date_invalid`,
`thirteenth_imported_average_exclusive`); `thirteenth_month_variable_required`
depende de `medias_importadas` e por isso só aparece no cálculo, já com campo e
mês. Corrija o campo apontado e reenvie a seção. `thirteenth_stage_duplicated` e
`thirteenth_peer_section_invalid` trazem `related_case_ids` e
`next_action=get_case`: veja o outro caso com `get_case` e cancele o que
sobrou, se for rascunho. Reenviar o mesmo pedido (mesmo `request_ref`) depois
da preparação devolve o recibo original.

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

Documente bases recebidas, fontes, divergências e ausências. Uma base ausente não se transforma em zero. Não invente parcelas, critérios, legislação ou datas; consulte fontes e contratos aprovados pelo responsável. Cumpra os gates humanos. Uma validação técnica não autoriza aceite, transmissão, pagamento ou publicação de resultados.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
