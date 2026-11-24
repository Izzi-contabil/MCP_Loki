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
`thirteenth_payment_coverage_not_certified` é informativo no estado: o cálculo
do 13º **não o lê** e não segue a regra de cobertura do domínio `ferias`
("Cobertura desde a admissão até o corte"). Quem decide é a janela que o
próprio cálculo exige:

- `thirteenth_payments`: de 01/01 do `ano` (ou da admissão, se ela for no
  ano) até a `data_pagamento` da etapa;
- `leave_occurrences`: da mesma data inicial até o corte (a referência
  salarial da etapa).

O cálculo confere essas janelas, não o gap do estado: limpar o gap não basta.
Cobertura `complete: true` que termina antes do fim da janela exigida (por
exemplo, pagamentos até 31/10 com pagamento em 30/11) recusa com
`historical_thirteenth_coverage_incomplete`; declare a **cobertura adjacente** (`start` 01/11, `end` 30/11, mesmo
consumidor) sem alterar a cobertura que já existe, selecione o estado de novo
e recalcule. O `effective_on` de uma cobertura é o seu `end`.

**Recusa de cobertura.** `historical_thirteenth_coverage_incomplete` (campo
`historical_state`, próxima ação `get_case_historical_state`) traz
`required_windows` e `missing_intervals`, cada um com `consumer`
(`leave_occurrences` ou `thirteenth_payments`), `start` e `end`. Declare na
carga histórica uma cobertura completa (`type: coverage`, `complete: true`) do
consumidor indicado que feche cada lacuna, selecione o estado de novo e
recalcule. **As janelas vêm só na resposta imediata** do
`run_prepared_case_workflow` (ou de `calculate_case`). `get_case` e o dossiê só
passam a trazê-las quando o backend publicar a correção "13º 1ª parcela já
paga" (#409, ainda não mesclada); até lá, o
registro gravado mostra a recusa sem `required_windows` nem
`missing_intervals`. Por isso, **releia a resposta imediata antes de concluir**
que a admissão é posterior: recusa sem janelas só significa admissão
posterior à referência salarial ou ao pagamento quando a resposta imediata
também vier sem elas. Nesse caso, confira a admissão e as datas do 13º antes
de declarar cobertura. Não presuma ausência de afastamento ou de pagamento só
porque falta cobertura.

**13º já adiantado no ano.** Vale quando a resposta servida trouxer
`historical_thirteenth_first_installment_already_paid` (backend #409,
aberta). Na etapa `primeira`, o estado
selecionado tem um `thirteenth_payment` confirmado do ano para o vínculo, pago
até a `data_pagamento` (por exemplo, o adiantamento pago em julho com as
férias). A recusa traz `fields: ["historical_state"]`,
`next_action=cancel_case`, `year` e `installment` (a parcela já paga) e
`guidance`; nunca valor, fato ou fonte. Significa que já houve adiantamento de
13º: **não pague de novo** a 1ª parcela (Lei 4.749/1965, arts. 1º e 2º); a 2ª
parcela compensa o adiantamento. Cancele o caso da 1ª parcela e siga para a
2ª na data dela. Não apague nem reclassifique o pagamento para passar. Sem a
recusa no servidor, confira `thirteenth_payments` do ano no estado antes de
calcular a 1ª parcela.

## Fatos documentais não qualificados

Quando a resposta servida apresentar `blocking_facts`: `calculate_case` ou o
workflow devolvem `BLOCKED` com
`code=historical_thirteenth_unqualified_documentary_facts`, campo
`historical_state`, `next_action=get_case_historical_state`, `blocking_facts`
(no máximo 32 linhas) e `blocking_facts_total` (a contagem bruta). Servidor
anterior devolve só `{"erro": "<código>"}`, sem a lista. Cada linha tem
`origin`, `kind`, um identificador (`fact_id`, `event_seq` ou `case_id`),
`effective_on` (data ou `null`), `reason` e `path`, sem texto nem referência
da ficha. Não recalcule, não reinicie o caso e não troque o fato por zero ou
"irrelevante" por conta própria.

- `path=qualify_legacy_fact` (`outro` ou `decimo_terceiro`; com a 2.9.8 e o
  sinal servido, também `afastamento` e `transferencia`, cujos `allowed_types`
  trazem `thirteenth_fact_assessment`, seção "Fatos opacos do 13º qualificados
  pelo id"): releia a ficha original. Se a ficha mostrar o que o fato é para o 13º, envie pela carga da
  empresa um `historico_operacional` de um dos `allowed_types` da linha (só
  esses; o escritor aceita outros tipos, como férias e `final_average`, que
  também retiram o fato da lista, mas não dizem nada sobre o 13º), com a
  **mesma fonte** (`document_id` e `content_hash`) do fato e
  `qualifies_legacy_fact_ids=[<fact_id>]`. Para declarar que o fato não
  altera o 13º, reenvie a cobertura `thirteenth_payments` já declarada a
  partir daquela ficha, com os mesmos dados, `replaces_fact_id=<id da
  cobertura>` e `qualifies_legacy_fact_ids` com todos os fatos daquela fonte.
  Não crie cobertura nova nem intervalo que a ficha não certifique. Fatos de
  outra ficha precisam da cobertura daquela ficha. Se nada na ficha sustentar
  a cobertura, o fato continua pendente: pergunte à DP. Depois rode
  `apply_historical_state` no caso e calcule de novo.
- **Antes de qualificar**, veja se o empregado tem outros casos abertos
  (férias, rescisão, simulação, outro 13º). A qualificação muda o
  `history_hash` e o `state_hash` dele: as seleções já aplicadas nesses casos
  ficam desatualizadas e exigem novo `apply_historical_state`. **Não
  qualifique quem tem outros casos abertos sem alinhar com a DP.** A
  qualificação só vale em cortes a partir do `effective_on` da cobertura, que
  é o fim dela.
- `path=no_typed_exit` (afastamento opaco da carga, servidor anterior à
  2.9.8): o afastamento pode afetar avos e continua pendente, e reenviar a
  ficha estruturada não remove o fato opaco. Registre a pendência
  (`registrar_problema`) com o `fact_id` e as datas que a ficha mostrar. Não
  invente datas. Com `thirteenth_rules.fact_assessment` servido, o afastamento
  opaco vem como `path=qualify_legacy_fact` e sai por
  `thirteenth_fact_assessment`.
- `path=dp_rule_pending` (rescisão da carga; antes da 2.9.8, também a
  transferência): não existe qualificação tipada que valha para o 13º.
  `final_average` com `qualifies_legacy_fact_ids` tira a rescisão da lista, mas
  **não deve ser usado para qualificar fato do 13º**: média final não diz nada
  sobre o 13º do ano. Registre a pendência. A transferência da carga tem
  caminho próprio quando o contrato servido apresentar
  `thirteenth_rules.fact_assessment` (`path=qualify_legacy_fact`, seção "Fatos
  opacos do 13º qualificados pelo id", abaixo).
- `path=episode_reconciliation`: concilie o evento ou o caso do vínculo
  indicado.
- `reason=effective_date_missing`: o fato não tem data e por isso não pode ser
  posto fora do ano. Um fato datado depois do fim da janela, ou um `outro` ou
  `decimo_terceiro` datado antes do ano, não aparece na lista. Os outros
  motivos são `inside_thirteenth_window`, `leave_started_before_window` e
  `episode_change_before_window`.

## Médias

Para bater com o Domínio, use `medias_importadas` (média final do Domínio,
finalidade `decimo_terceiro`). Ela é exclusiva com `variavel_cents` mensal:
com ela, nenhum mês leva valor. A produtividade não é calculada pelo Loki: use
a média importada. A média por quantidade das horas (Súmula 347) passou a ser
calculada, com `meses[].horas` ("Horas no 13º", abaixo), mas é exclusiva com a
média importada (`decimo_horas_com_media_importada`): uma ou outra.

**`final_average` é a média mensal integral do Domínio.** Envie essa média
inteira, como veio, em `medias_importadas={fact_id}`, sem `variavel_cents`
mensal. Nunca envie uma média já proporcional aos avos: o Loki aplica
`média × avos ÷ 12` em todas as etapas, e uma média já dividida sairia
dividida duas vezes. Na 1ª parcela, a média só entra inteira quando a pessoa
foi admitida antes do ano e tem todos os avos até o mês-limite, que é quando a
parte fixa também entra inteira. Para conferir com o Domínio, compare
`variavel_cents` com média × avos ÷ 12.
Esse uso da média em `medias_importadas` não muda; o que não vale é usar
`final_average` para qualificar fato da carga ("Fatos documentais não
qualificados").

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

## Janela da média por empresa (decimo-v5)

Vale quando o schema servido do cadastro da empresa apresentar
`empresas[].decimo_terceiro_medias` (`get_company_onboarding_contract`:
`thirteenth_rules.average_window`). O padrão é `jan_nov_11`: a 2ª parcela usa
janeiro a novembro ÷ 11 e o ajuste de janeiro usa janeiro a dezembro ÷ 12.
`dez_nov_12` usa dezembro do ano anterior a novembro ÷ 12 na 2ª parcela e no
ajuste; a 1ª parcela segue a regra de sempre nas duas janelas, e a média
importada não usa janela.

- A política é por empresa, com `id`, `valid_from`, `janela` e `fonte`. Vale a
  vigência que contém a referência salarial da etapa; vigências sobrepostas
  recusam (`decimo_terceiro_medias_vigencias_sobrepostas`). `jan_nov_11`
  declarado equivale a não declarar.
- `dez_nov_12` é configuração do cliente: não tem base no art. 77 do Decreto
  10.854/2021. Só aplique com a decisão da DP registrada na `fonte` (CX-…) e o
  aceite dela para os efeitos: quem entrou no meio do ano divide por 12 em vez
  de 11, e o primeiro ano da troca pode contar dezembro duas vezes se o ano
  anterior foi apurado no padrão. Não ative por conta própria nem presuma a
  janela de outro cliente.
- Com `dez_nov_12`, a 2ª parcela e o ajuste exigem
  `dados_decimo_terceiro.dezembro_anterior` (`variavel_cents` e `source`) para
  quem já tinha vínculo em dezembro (`thirteenth_prior_december_variable_required`).
  O campo é recusado quando a admissão é posterior
  (`thirteenth_prior_december_before_hire`), na janela padrão
  (`thirteenth_prior_december_outside_window`), junto com `medias_importadas`
  (`thirteenth_prior_december_exclusive`) e na 1ª parcela
  (`thirteenth_prior_december_stage_incompatible`).
- O motor vira `decimo-v5` só com `dez_nov_12` ativa; sem ela segue
  `decimo-v3`/`decimo-v4`. Caso aprovado ou publicado conserva o cálculo que
  gerou o pacote; em preparação ou revisão, o caso passa a exigir
  `dezembro_anterior` e novo cálculo. A simulação continua no padrão.

## Horas no 13º: só onde a norma coletiva é silente

Vale quando o schema servido de `dados_decimo_terceiro` apresentar
`meses[].horas` (backend #404, em `main`). A média por quantidade (Súmula 347
do TST: média física das horas × valor da hora na data do pagamento) é o
critério **no silêncio da norma coletiva**. Onde a CCT ou o ACT manda somar os
valores recebidos, não há horas: a média segue pelos valores.

- Norma silente: envie `meses[].horas` (e `dezembro_anterior.horas` na janela
  `dez_nov_12`), `salario_hora_base` e, se houver repouso, `dsr_fator`, mais
  `variavel_exclui_rubricas_de_horas` (a declaração de que `variavel_cents`
  não repete o valor dessas rubricas). Motor `decimo-v3+horas-347-v1`
  (`decimo-v5+horas-347-v1` com `dez_nov_12`). Sem horas, o motor e os hashes
  são os de antes. O schema e as recusas fechadas `decimo_horas_*` vêm de
  `get_process_contract("decimo_terceiro")`.
- Norma manda somar valores: **não envie horas** (`meses[].horas`,
  `dezembro_anterior.horas`). Envie só `variavel_cents` por mês, que é a média
  pelos valores.
- Não decida pela cláusula por conta própria: leia a norma coletiva da empresa
  e registre na `fonte` a decisão da DP ou a cláusula. Norma ilegível ou
  ambígua vai à DP, não ao silêncio presumido.

**Política `horas` da empresa** (backend #408,
aberta; vale quando `empresas[].decimo_terceiro_medias` mostrar o campo
`horas` no schema servido de `get_client_config`/`validate_client_config`).
Declare no mesmo cadastro da janela (um `validate_client_config` e depois
`apply_client_config`), com vigência e fonte:

```json
"empresas[<codigo>].decimo_terceiro_medias": [
  {"id": "media-13-valores-2026", "valid_from": "2026-01-01", "horas": "valores",
   "fonte": {"reference": "CX-…", "foundation": "<cláusula da norma coletiva>"}}
]
```

- `horas` aceita `valores` ou `quantidade_347`. Ausente ou `quantidade_347`
  mantém o comportamento de antes (horas aceitas quando enviadas). Uma política
  só com `horas: "valores"` vale, com a janela padrão `jan_nov_11`; com
  `janela: "dez_nov_12"` no mesmo registro, as duas regras valem juntas.
- Com `valores` vigente na referência salarial da etapa, enviar horas recusa
  com `decimo_horas_vedado_pela_norma_coletiva`: `fields` aponta
  `dados_decimo_terceiro.meses` e/ou `dados_decimo_terceiro.dezembro_anterior`,
  a resposta traz `politica_id` e a `fonte` da política, e a próxima ação é
  enviar só os valores. Reenvie a seção sem `horas`, com `variavel_cents`.
- A política só entra por declaração com fonte; nenhuma empresa a tem por
  padrão. Sem a política, o Loki aceita as horas e **não** descobre a cláusula:
  a conferência com a norma é da harness.
- Servidor sem o campo `horas` no schema recusa o cadastro: não o declare.

## Fatos opacos do 13º qualificados pelo id

Vale quando o contrato servido apresentar `thirteenth_rules.fact_assessment`.
O fato opaco da carga (`outro`, afastamento ou transferência) é qualificado
por um `historico_operacional` confirmado `thirteenth_fact_assessment`, da
mesma fonte do fato, citando o id em `qualifies_legacy_fact_ids`. A avaliação
vale só para o 13º; o fato continua no estado para os outros consumidores.

| `effect` | alvos | fonte |
|---|---|---|
| `sem_efeito` | `outro`, `afastamento` | `dp_decision` (CX-…) |
| `afastamento_tipado` | `afastamento` sem data, junto com o `leave` tipado que também o cita | `dp_decision` |
| `transferencia_mesmo_grupo` | `transferencia` | `legal_rule` (`transferencia_grupo_economico_continuidade`) ou `dp_decision` |

- `decided_on` é o `effective_on` e nada retroage: a avaliação só vale em
  cortes a partir dessa data. Uma decisão posterior ao fim da janela da etapa
  não entra no estado daquele corte.
- Afastamento opaco com data também sai por um `leave` tipado confirmado que
  comece na data do fato; sem data, só sai com a decisão da DP.
- `transferencia_mesmo_grupo` declara `direction`. Na `saida`, exige
  `destination_company_cnpj`: o 13º do ano é da empresa de destino, e a origem
  recusa com `historical_thirteenth_transfer_out_destination_company`
  (`next_action=cancel_case`): cancele o caso da origem. Na `entrada`, exige a
  `qualificacao_vinculo` aplicada, com `current_company_entry` igual à data da
  transferência e `original_admission` igual à admissão do estado; sem ela, a
  recusa é `historical_thirteenth_transfer_entry_unproven`. Os avos contam o
  contrato todo e as médias somam as empresas (envie a soma). As coberturas
  `thirteenth_payments` e `leave_occurrences` continuam exigidas.
- O escritor recusa alvo de outro tipo
  (`historical_legacy_qualification_kind_incompatible`), outra fonte
  (`historical_legacy_qualification_source_incompatible`), avaliação sem alvo
  (`historical_thirteenth_assessment_target_required`) e `legal_rule` fora da
  transferência (`historical_thirteenth_assessment_requires_dp_decision`).
- Antes de qualificar, valem os mesmos cuidados da seção anterior: outros
  casos abertos do empregado ficam com a seleção histórica desatualizada.

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
