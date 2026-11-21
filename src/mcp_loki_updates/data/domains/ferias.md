# Férias

## Parâmetros, fontes e prova da execução

Consulte o schema atual de programação, calendário, incidência, saldo e médias.
Quando oferecido pelo consumidor, use a declaração, contexto ou inferência
atribuídos à operação sem fabricar DOC, manifesto ou hash de original. Preserve
referência, localizador, fundamento e demais metadados realmente fornecidos.
Fonte documental e manifesto harness conservam suas verificações de associação
e integridade; pins históricos continuam sujeitos a identidade, corte e cobertura.

Uma prova tipada de declaração pode ter um digest próprio: isso não demonstra
leitura de arquivo nem equivale ao hash do original. Confira a prova e o consumo
na memória do cálculo e na projeção mensal, sem converter desconhecido em zero.
Use `get_case_dossier` para distinguir memória calculada e RUN recusado; uma
causa antiga não persistida não pode ser inferida da pendência atual.

## Histórico, saldo de abertura e médias de férias

Consulte `get_case_historical_state` no episódio e corte do caso e selecione
por `apply_historical_state` somente após conferir identidade, cobertura e
`state_hash`. `saldo_source` admite a referência histórica tipada anunciada
pelo schema, com `fact_ref` e `fact_hash`; não substitua por ID ou saldo inventado.
Confira período aquisitivo, corte da abertura anterior ao gozo,
`fragments_complete`, dias consumidos, abono e movimentos entre abertura e gozo.
Histórico selecionado não comprova saldo qualificado nem pagamento.

As alternativas `medias`, `componentes_medias`, `medias_importadas` e
`medias_nao_aplicaveis_source` são exclusivas conforme o schema.
Média final importada usa seleção explícita por finalidade, período de uso,
fato e hash; não é média recalculada de qualquer folha disponível.
Não troque ausência de histórico por zero ou “não se aplica”.
Siga o schema atual para programação, calendário, incidências e fontes próprias.

Releia resultado e proveniência para demonstrar consumo real; seleção e
contrato disponível são provas distintas. Não mova datas ou saldos para
forçar aceitação de uma origem incompatível.

## Data do cálculo, afastamento sem redução, gozo antecipado e abono (historical-vacation-v2)

Vale quando `get_company_onboarding_contract` trouxer
`historical_state.vacation_rules` (`rule_version: "historical-vacation-v2"`)
e o schema servido de `dados_ferias` tiver `data_calculo`. Sem isso, siga as
seções abaixo como estão e não envie os campos novos: o servidor anterior os
recusa. Regras da operação (DP), recebidas pela Caixa em 19 e 20/11/2026.

**Data do cálculo e cobertura.** Todo cálculo novo exige
`dados_ferias.data_calculo`, a data em que você calcula as férias; sem ela, o
Loki recusa `historical_vacation_calculation_date_required`. A operação
calcula até 30 dias antes do gozo, e o pagamento sai dois dias antes. A data
fica entre o fim do aquisitivo e o fim do gozo (`ferias_data_calculo_invalida`)
e não pode ser futura (`historical_vacation_calculation_date_future`, também
em simulação). Caso já calculado pela regra anterior recalcula pela regra
gravada, mas deixa de ser corrente (perde a elegibilidade de entrega) se o
Loki tiver afastamento ou gozo desse funcionário entre o início do aquisitivo
e a véspera do gozo sem espelho no histórico selecionado: lance o espelho
(abaixo) e avise a operadora antes de ela entregar.

Declare as coberturas até essa data, nunca até o fim do gozo:

- `coverage` `vacation_movements` da abertura até a data do cálculo;
- `coverage` `leave_occurrences` do início do aquisitivo até a data do
  cálculo.

Use `complete: true`, com `basis: declared` e a mensagem `CX-`, somente quando
a fonte atesta que não houve outro gozo ou afastamento no intervalo. Se o
Loki tem um afastamento ou outras férias do funcionário nesse intervalo,
lance o espelho histórico confirmado: o afastamento como `leave`, com as
mesmas datas, categoria, períodos e fontes; as férias como `vacation_use`, com
o mesmo início e fim. Sem o espelho, a recusa é
`historical_vacation_native_occurrence_not_mirrored`.

O pacote traz a ressalva `sem_afastamento_conhecido_apos_calculo` ("sem
afastamento conhecido até o cálculo (AAAA-MM-DD)") em
`ressalvas.ferias_historico` da revisão: apresente-a à operadora. Afastamento
descoberto depois do cálculo é retificação: corrija o histórico e faça um
novo cálculo.

**Afastamento que não reduz férias (`leave.vacation_effect`).** Para atestado
ou licença-maternidade, a regra da operação basta:
`"vacation_effect": {"kind": "sem_reducao", "source": {"kind":
"operation_rule", "rule": "atestado_e_licenca_maternidade_nao_sao_falta",
"message_reference": "CX-AB5EE178", "category": "atestado"}}` (`category`
`atestado` ou `licenca_maternidade`). Lance cada atestado como um `leave`
próprio, com as suas datas e o `return_on`. Afastamento com período pago pelo
INSS (`payment_periods[].responsibility: "inss"`) é benefício, não atestado:
exige a decisão do DP
(`historical_leave_vacation_effect_benefit_requires_dp_decision`). Categoria
declarada que contradiz um `category_code` tipado recusa
`historical_leave_vacation_effect_category_incompatible`. Para qualquer outra
categoria, só com a decisão do DP no caso: `{"kind": "dp_decision",
"message_reference": "CX-…"}`. Nunca deduza `sem_reducao` sem uma dessas
fontes. A ressalva `afastamento_aquisitivo_sem_reducao` vai para o aceite da
operadora. Afastamento que se sobrepõe ao gozo continua recusado.

**Afastamento documental opaco.** Se
`historical_vacation_unqualified_documentary_facts` trouxer `blocking_facts`
com `kind: afastamento`, lance um `leave` confirmado com a mesma fonte, que
comece na data do fato (`effective_on` do `blocking_facts`), com
`qualifies_legacy_fact_ids: ["<fact_id>"]` e `vacation_effect` pelas mesmas
regras. Qualificador com outra data recusa
`historical_leave_vacation_effect_target_incompatible`. Fato sem data
(`effective_on: null`) só sai com a decisão do DP no caso, e a ressalva vai
sempre para o aceite. Afastamento opaco que começou antes do aquisitivo
(`reason: leave_started_before_window`) também bloqueia e sai pela mesma
qualificação. Isso vale só para férias:
o estado e o 13º continuam listando o fato.

**Gozo antecipado (`vacation_use.advance`).** Quando o Domínio registra o gozo
no aquisitivo de origem antes do fim dele, lance o `vacation_use` com
`"advance": {"kind": "gozo_antecipado", "source": {"kind": "dominio_record",
"document_id": "<id da ficha anexada>", "content_hash": "<hash>", "locator":
"<linha>"}}` (ou a decisão do DP, `dp_decision`). A ficha tem de ser fonte do
próprio fato (`historical_vacation_advance_source_incompatible`). Não há
limite de antecedência, mas o gozo começa dentro do aquisitivo de origem;
`advance` em gozo que não é antecipado recusa
`historical_vacation_use_advance_incompatible`. O cálculo traz a ressalva
`vacation_use_advanced`. O Loki não calcula férias antecipadas. Rescisão com
gozo antecipado no aquisitivo em curso recusa
`rescisao_ferias_gozo_antecipado_pendente_regra` (domínio `rescisao`).

**Abono fora do prazo.** `data_pedido_abono` é a data em que o empregado pediu
o abono. O prazo (CLT art. 143 §1º) é até quinze dias antes do fim do
aquisitivo; pedido depois disso recusa `ferias_pedido_abono_fora_do_prazo`.
Com a concordância do empregador (normalmente o pedido do cliente), declare
`dados_ferias.abono_fora_do_prazo_source` (documento, harness ou declaração
com `foundation`). Ela vira a ressalva `clt_143_1_abono_fora_do_prazo` em
`declaracoes_dp`, para o aceite da operadora. Fonte sem pedido fora do prazo
recusa `ferias_abono_fora_do_prazo_source_sem_uso`; sem fundamento,
`ferias_abono_fora_do_prazo_source_sem_fundamento`.

## Recusas de fatos históricos do onboarding

Os códigos valem somente quando a resposta servida os apresentar. Na recusa
`declaracao_do_vinculo_invalida`, `diagnostic.details[*]` traz `path`
(relativo ao vínculo, por exemplo `facts[*].data.start`) e `type`, que é o
código da regra. Corrija o campo apontado conforme a fonte; nunca ajuste a
data só para passar. As regras não mudaram; só a recusa ficou explícita.

| Código | Significado | O que a harness corrige |
|---|---|---|
| `historical_vacation_period_inverted` | fim do aquisitivo antes do início | rever `period_start`/`period_end` na fonte |
| `historical_vacation_use_inverted` | fim do gozo antes do início | rever `start`/`end` do gozo |
| `historical_vacation_use_period_incompatible` | o gozo termina antes do fim do próprio aquisitivo (`end < period_end`). Gozo em que o fim do aquisitivo cai dentro do período (`start <= period_end <= end`, inclusive no primeiro ou no último dia) é aceito, assim como gozo que começa depois | conferir se o aquisitivo atribuído ao gozo é o correto. Se a fonte mostra gozo inteiro antes do fim do aquisitivo, não grave: pergunte à Rafa; com `vacation_rules`, o gozo antecipado registrado pelo Domínio sai por `advance` |
| `historical_vacation_use_days_incompatible` | `gozo_days_hundredths` diferente de (dias corridos de `start` a `end`) × 100 | rever `end` ou a quantidade de dias de gozo |
| `historical_leave_return_incompatible` | `return_on` não é posterior a `start` | rever `start` e a data de retorno (primeiro dia de volta ao trabalho) |
| `historical_leave_payment_outside_leave` | período de pagamento fora do afastamento (começa antes de `start` ou termina em `return_on` ou depois) | rever `start`, `return_on` e `payment_periods` |
| `historical_leave_payment_overlap` | dois períodos de pagamento se sobrepõem, inclusive quando um termina no mesmo dia em que o seguinte começa | rever `payment_periods` (o seguinte começa no dia posterior ao fim do anterior) |
| `historical_leave_payment_inverted` | período de pagamento com fim antes do início | rever `payment_periods[*].end` |
| `historical_coverage_inverted` | cobertura com fim antes do início | rever `start`/`end` da cobertura |

**Lote validado antes da atualização.** Se `apply_company_onboarding` recusar
`snapshot_desatualizado` num lote validado antes desta versão, chame
`validate_company_onboarding` de novo e aplique com o `validation_hash` novo.
O diagnóstico das linhas recusadas ficou mais detalhado e entra no hash. Não
reenvie nem altere os dados por causa disso.

**Gozo programado antes de concluir o aquisitivo** (regra da DP,
18/11/2026). Declare o `vacation_use` com o `period_end` do aquisitivo que ele
quita. O Loki aceita quando o fim do aquisitivo cai dentro do período de gozo,
do primeiro ao último dia. Gozo que termina antes do fim do aquisitivo
continua recusado (`historical_vacation_use_period_incompatible`): pergunte à
Rafa; quando o servidor tiver `vacation_rules`, o gozo antecipado registrado
pelo Domínio sai por `advance` (seção acima). Isso vale só para as férias antigas do histórico de onboarding; o
processo de férias (`ferias_gozo_antes_do_fim_do_aquisitivo`) segue a regra
anterior.

**Lote recusado antes por `historical_vacation_use_period_incompatible`.**
Depois desta versão, a próxima validação pode devolver `ready`. Chame
`validate_company_onboarding` de novo e aplique com o `validation_hash` novo.
Repetir `apply_company_onboarding` com o `validation_hash` antigo é recusado
com `snapshot_desatualizado`. Não altere as datas do gozo por causa disso.

## Cobertura desde a admissão até o corte

`leave_history_coverage_not_certified` (e
`thirteenth_payment_coverage_not_certified`) só sai do estado quando coberturas
`complete: true` do consumidor (`leave_occurrences` / `thirteenth_payments`)
cobrem, sem lacuna, **da data de admissão até o corte**. O `effective_on` de
uma cobertura é o seu `end`.

**Cobertura que termina depois do corte (estado `historical-state-v2`).** Uma
cobertura `complete: true`, lançada até o mês do corte, que começa na admissão
(ou emendada desde ela) e termina **depois** do corte limpa o gap **até o
corte**. O estado nunca certifica dia posterior ao corte. Não é mais preciso
terminar exatamente no corte; terminar no corte ou antes, emendada com outras
até ele, continua valendo. Uma cobertura que começa depois da admissão não
limpa o gap. Declare coberturas só quando a fonte atesta a completude do
intervalo inteiro.

**Versão do estado.** O estado vem `version: "historical-state-v2"` só quando
uma cobertura dessas entrou e limpou o gap. Cobertura incompleta ou que não
fecha desde a admissão não muda o estado; nesse caso, `facts` traz a cobertura
íntegra, com `effective_on` (o fim) depois de `as_of`. Sem isso, o estado
continua `historical-state-v1`, com o mesmo `state_hash` de antes.

**Seleção já feita.** Uma seleção v1 continua válida e consumível: mesmo
`state_hash`, mesmo gap e nenhum `historical_state_stale`. Nesses vínculos a
prévia pode mostrar a v2, com o gap limpo e
`selection_matches_current_state: false`. **Não reselecione se a seleção v1
for consumível.** Reselecionar (`apply_historical_state` com o `state_hash`
da prévia atual) só cabe quando o caso não consegue seguir com a seleção v1
por causa desse gap. A nova seleção vale para o próximo cálculo; cálculos já
feitos continuam ligados à seleção que consumiram. Se `apply_historical_state`
recusar `historical_state_stale` com um hash consultado antes da atualização,
consulte de novo e aplique o hash novo. Não altere coberturas já gravadas nem
regrave para casos com seleção histórica feita: isso muda o estado e exige
nova seleção.

**Afastamento antigo opaco.** Se o estado mostra um fato antigo `afastamento`
sem semântica operacional (`unqualified_documentary_facts`,
`operational_semantics_missing` ou `leave_observations_not_classified`),
**não grave um `leave` novo para o mesmo afastamento**: um `leave` paralelo
duplicaria a ocorrência. Mantenha o gap pendente e informe a operadora. A
exceção é o cálculo de férias com `vacation_rules`: o `leave` que cita o fato
em `qualifies_legacy_fact_ids` (seção "Data do cálculo…", acima) qualifica o
fato só para férias.

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

Preserve o que foi informado, suas fontes, o que falta e as divergências. Ausência não é zero. Não invente períodos, limites legais, remunerações ou prazos: use contratos e fontes operacionais aprovadas. Cumpra os gates humanos exibidos pelo runtime e diferencie conferência técnica de aprovação. Não publique, transmita ou efetive alterações automaticamente.

Programação de férias exige contrato próprio para registrar, retificar ou cancelar com pessoa/episódio, período, referência idempotente e revisão esperada. Consulte sua disponibilidade pelo HTTPS; histórico de planejamento não comprova implementação desse escritor. Quando a operação produzir apenas registro, devolva o recibo persistido e releia o registro, sem gerar PDF artificial ou exigir aceite documental. Não confunda programação, gozo confirmado e pagamento real. Nome de ferramenta ou contrato ausente permanece lacuna explícita; não improvise lançamento por outro processo.

No consumidor que oferecer `get_vacation_schedule_contract()`, siga o schema `loki.vacation-schedule/1` de `record_vacation_schedule(case_id, request)` e releia por `get_vacation_schedules(case_id)`. O request preserva `request_ref`, `expected_snapshot=correction_snapshot` atual de `get_case`, `reference`, `action` e fontes opcionais conforme o contrato. Em `register`, `data` informa `aquisitivo_inicio`, `aquisitivo_fim`, `inicio`, `fim` e `dias_abono` conforme o contrato. Registrar planejamento requer OPERAR_CASOS e não confirma gozo ou pagamento. `rectify` e `cancel` exigem pessoa autorizada com CORRIGIR_DADOS, `human_message` e `message_reference`, além do par `supersedes_id`/`supersedes_input_hash` da revisão anterior. A automação encaminha essas ações ao humano; não decide nem adapta a identidade. Preserve o recibo e a trilha anterior; releitura e retry usam a mesma referência e conteúdo. Esta candidata de instruções não comprova publicação ou adoção desses escritores.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Substituição de insumos e pins de férias

Quando `get_process_contract("ferias")` anunciar `preparation.supported=true`,
use a preparação `replace_process_inputs` no restart existente ou pelo transporte
`loki.case-preparation-transport/1` anunciado em `receive_case_data`. A pessoa
precisa das capacidades do contrato, inclusive `corrigir_dados`; o replay também
revalida a autorização. Transcreva a intenção específica e use o
`correction_snapshot` corrente. Aprovação ou efeito aplicado exigem a conciliação
própria antes do reinício.

Pessoa, empresa, vínculo, competência, aquisitivo e gozo conhecidos permanecem
âncoras. Depois da fronteira, releia `get_case.input_snapshot` e envie a seção
`dados_ferias` completa com nova referência: alternativas de médias, pins de saldo
e datas/flags precisam ser reapresentados conforme o schema. A seleção nova
continua sujeita a vigência, identidade, cobertura e integridade. O corretor
pontual conserva seu alcance; documentos e decisões anteriores permanecem.

`related_vacation_parameters_invalid` pede `get_case` do contexto relacionado
para diagnóstico, sem inventar flags ou ignorar histórico parcial. Quando a
resposta apresentar, `related_case_ids` aponta o caso de férias irmão do mesmo
funcionário e `related_reason` diz `incomplete` ou `invalid`: complete ou
corrija esse caso pelo caminho dele; se for duplicado, cancele-o somente com
decisão humana explícita. A orientação
não autoriza corrigir fatos ou reaplicar casos automaticamente. Publicação e
reteste real exigem provas próprias.

Segunda ocorrência de férias da mesma pessoa funciona em outra competência:
envie sempre `competencia` igual ao mês de início do gozo. No `create_case`,
`created: false` significa que o caso devolvido é o existente, não o novo: não
continue nele. Duas frações na mesma competência ainda não têm suporte. Nunca
cancele o primeiro caso para abrir o segundo.

## Recusa com campo e código de regra

O campo e o código valem somente quando a resposta servida os apresentar.
Quando o Loki recusar dados de férias, olhe a lista `errors`: cada item traz o
campo exato (por exemplo `dados_ferias.data_aviso`) e um código que diz qual
regra não fechou. Corrija só o campo apontado, conferindo com o documento
original, e reenvie com um novo `request_ref` e o snapshot atual do caso.
Reenviar o mesmo dado sem corrigir, com ou sem `field_sources`, vai ser
recusado de novo. Se o documento realmente traz essas datas, não force o valor:
registre a dúvida com a DP antes de reenviar.

Códigos de férias:

- `ferias_aquisitivo_29_fevereiro_exige_qualificacao`: aquisitivo em 29 de
  fevereiro precisa da qualificação do aniversário.
- `ferias_aquisitivo_incompleto`: o aquisitivo não fecha um ano completo.
- `ferias_gozo_duracao_invalida`: o gozo precisa de início antes do fim e de
  cinco a trinta dias.
- `ferias_gozo_antes_do_fim_do_aquisitivo`: o gozo começa antes de o
  aquisitivo terminar.
- `ferias_gozo_fora_do_concessivo`: gozo fora do concessivo exige o tratamento
  de dobra.
- `ferias_aviso_fora_do_prazo` e `ferias_pagamento_fora_do_prazo`: aviso ou
  adiantamento fora dos prazos.
- `ferias_abono_pedido_incoerente`: dias de abono e data do pedido de abono
  precisam vir juntos (ou nenhum dos dois).
- `ferias_pedido_abono_fora_do_prazo`: pedido de abono depois do prazo.
- `ferias_inicio_antes_de_feriado`: início nos dois dias antes de feriado,
  sem a decisão do cliente (veja "Início antes de feriado: decisão do
  cliente").
- `ferias_inicio_antes_de_feriado_source_sem_uso`: a decisão do cliente veio,
  mas o início não cai nos dois dias antes de feriado. Retire a decisão ou
  corrija a data ou os feriados.
- `ferias_inicio_antes_de_feriado_source_sem_fundamento`: a fonte da decisão
  não é documento, manifesto de harness nem declaração com `foundation`.
  Inferência e contexto são recusados.
- `ferias_inicio_antes_de_repouso`: início nos dois dias antes do repouso
  semanal, sem a declaração do DP (veja "Início antes do repouso semanal:
  declaração do DP").
- `ferias_inicio_antes_de_repouso_source_sem_uso`: a declaração veio, mas o
  início não cai nos dois dias antes do repouso. Retire a declaração ou
  corrija a data ou o repouso.
- `ferias_inicio_antes_de_repouso_source_sem_fundamento`: a fonte da
  declaração não é documento, manifesto de harness nem declaração com
  `foundation`. Inferência e contexto são recusados.
- `ferias_medias_alternativas_exclusivas`, `ferias_media_repetida` e
  `ferias_media_competencias_invalidas`: médias com alternativas que se
  excluem, média repetida ou competências da média inválidas.

## Preparação corrente: recusa por campo

O campo e o motivo valem somente quando a resposta servida os apresentar.
Numa preparação corrente (por exemplo, depois de `restart_case`),
`receive_case_data` recusa `dados_ferias` incompleto ou fora do modelo com
`vacation_preparation_requires_complete_input`, e `errors` traz um item por
campo: `{"field": "dados_ferias.data_aviso", "reason": "ferias_aviso_fora_do_prazo"}`.
`reason` é um código `ferias_...` da lista acima, `missing` (campo obrigatório
ausente) ou `extra_forbidden` (chave fora do schema, que vem como
`dados_ferias.*`, sem o nome da chave). Corrija o campo apontado conferindo com
o original e reenvie a seção `dados_ferias` completa, com novo `request_ref` e
o snapshot atual. A fonte de um campo vai no campo `*_source` do schema (ex.:
`programacao_source`, `calendario_source`), nunca numa chave própria dentro de
`dados_ferias`: essa chave volta como `extra_forbidden`.

## Início antes do repouso semanal: declaração do DP

O código e o campo valem somente quando a resposta servida e o schema de
`get_process_contract("ferias")` os apresentarem. O código antigo
`ferias_inicio_antes_de_repouso_ou_feriado` não é mais emitido; ele só aparece
em diagnósticos e recibos registrados antes.

Regra da DP da Izzi: o início de férias nos dois dias antes da folga semanal é
aceito quando o cliente pede, porque a Izzi não acompanha a escala praticada.
A véspera de feriado tem regra e fonte próprias (veja a seção seguinte): a
declaração do repouso não libera o feriado. Quando o início cai nos dois dias
antes de feriado e nos dois dias antes do repouso, as duas fontes são
exigidas e cada uma libera só a sua regra.

Para aceitar o início antes do repouso, envie em `dados_ferias` o campo
opcional `inicio_antes_de_repouso_source`. A fonte é o pedido do cliente:
documento anexado ao caso (fonte documental do schema), manifesto de harness
(`kind: "harness"`, com o EXTSRC e o mesmo `content_hash`) ou declaração
(`kind: "declaration"`, `reference`, `locator`) com `foundation` dizendo quem
pediu e onde (por exemplo, a mensagem do cliente
na conversa). Inferência, contexto, regra ou histórico são recusados com
`ferias_inicio_antes_de_repouso_source_sem_fundamento`. Sem pedido real do
cliente, não envie o campo: a recusa `ferias_inicio_antes_de_repouso` é a
resposta correta e a data volta ao cliente.

A exceção não muda valores. Ela aparece como ressalva em
`ressalvas.declaracoes_dp` da revisão, com `confirmed: false` e
`exige_aceite_humano: true`, e numa linha "Declaração do DP" do aviso e do
recibo. Só vale com o aceite explícito das ressalvas na revisão: apresente a
ressalva à pessoa e não aprove sem esse aceite.

Num caso existente, mudar `repouso_semanal` e acrescentar a declaração é uma
única correção: `submit_operator_correction` com as duas folhas juntas em
`changes` (`dados_ferias.repouso_semanal` e as folhas de
`dados_ferias.inicio_antes_de_repouso_source`). Corrigir só o repouso antes
deixa o pedido sem a declaração, e o escritor recusa com
`ferias_inicio_antes_de_repouso`.

## Início antes de feriado: decisão do cliente

O código e o campo valem somente quando a resposta servida e o schema de
`get_process_contract("ferias")` os apresentarem.

Regra da DP da Izzi (16/11/2026): a decisão é sempre do cliente. O DP informa
o passivo (CLT art. 134 §3); se o cliente decidir manter o início nos dois
dias antes de feriado, é feito. Sem essa decisão, `ferias_inicio_antes_de_feriado`
continua recusando, e o caminho é levar a data e o passivo ao cliente.

Para aceitar o início antes de feriado, envie em `dados_ferias` o campo
opcional `inicio_antes_de_feriado_source`. A fonte é a decisão do cliente:
documento anexado ao caso (fonte documental do schema), manifesto de harness
(`kind: "harness"`, com o EXTSRC e o mesmo `content_hash`) ou declaração
(`kind: "declaration"`, `reference`, `locator`) com `foundation`. Inferência,
contexto, regra ou histórico são recusados com
`ferias_inicio_antes_de_feriado_source_sem_fundamento`; fonte sem início na
janela do feriado recusa com `ferias_inicio_antes_de_feriado_source_sem_uso`.

O conteúdo da `foundation` é responsabilidade da harness e da operadora: diga
quem decidiu, onde (por exemplo, a mensagem do cliente na conversa) e que o
passivo foi informado. O Loki só exige `foundation` não vazia e não confere a
fonte. Sem decisão real do cliente, depois de informado o passivo, não envie
o campo: a recusa é a resposta correta.

Quando o início cai antes de feriado e antes do repouso, as duas fontes são
exigidas: sem a do feriado a recusa é `ferias_inicio_antes_de_feriado`; sem a
do repouso, `ferias_inicio_antes_de_repouso`. Cada fonte libera só a sua
regra.

A exceção não muda valores. Ela aparece como ressalva
`clt_134_3_vespera_feriado` em `ressalvas.declaracoes_dp` da revisão (depois
da do repouso, quando houver), com `confirmed: false` e
`exige_aceite_humano: true`, dizendo que a decisão foi do cliente, que o
passivo foi informado e que a ressalva não afasta o passivo; e numa linha
"Declaração do DP" do aviso e do recibo. Só vale com o aceite explícito das
ressalvas na revisão: apresente a ressalva à pessoa e não aprove sem esse
aceite.

Num caso existente, mudar `feriados` e acrescentar a decisão é uma única
correção: `submit_operator_correction` com as folhas juntas em `changes`
(`dados_ferias.feriados` e as folhas de
`dados_ferias.inicio_antes_de_feriado_source`). Corrigir só os feriados antes
deixa o pedido sem a decisão, e o escritor recusa com
`ferias_inicio_antes_de_feriado`.

## Recibos de componentes obsoletos depois do deploy

Cada mudança da regra de férias deixa obsoletos os recibos de componentes de
férias e de rescisão e as consolidações de médias emitidos antes do deploy
dela, inclusive os emitidos depois da mudança anterior (2.6.11):
`get_case` mostra o recibo como `OBSOLETO`, uma nova consolidação sobre o
recibo antigo é recusada (`recibo_componentes_obsoleto`) e o recálculo da
rescisão com consolidação recusa com `medias_rescisao_obsoletas`. Isso não é
defeito e não pede reinício do caso.

Caminho de recuperação de um caso aberto, nesta ordem: nova qualificação dos
componentes, nova consolidação (médias de férias ou de rescisão), novo
cálculo, depois geração, conferência e revisão. Casos aprovados ou entregues
não mudam: decisão, pacote e bytes registrados ficam como estão. O Loki não
recalcula nada sozinho.

A descrição da ressalva do repouso mudou: agora diz que a véspera de feriado
tem regra e declaração próprias. Revisões já preparadas com essa ressalva
precisam ser preparadas de novo; casos aprovados ou entregues não mudam.
