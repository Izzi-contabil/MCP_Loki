# Folha mensal

Este domínio complementa o `geral`, que continua com a prontidão, a retomada, a
população da folha e o diagnóstico do job bloqueado no cálculo. Antes de
operar, consulte `meu_acesso`, `get_dp_capabilities` e
`get_process_contract("folha_mensal")`; envie `dados_folha` pelo escritor
anunciado. Os códigos e campos abaixo valem somente quando a resposta servida
os apresentar.

## Fila durável: um job pendente por empresa

1. **Uma folha por empresa na fila.** O Loki aceita um único job pendente
   (`queued` ou `running`) por empresa. O contrato anuncia isso em
   `durable_workflow.admission: "one_pending_job_per_company"`. Se outro caso
   da mesma empresa já tem job pendente, `enqueue_case_workflow` devolve
   `BLOCKED` com `code: "company_job_pending"` (HTTP 409) e não grava nada. A
   resposta traz `pending_job: {case_id, job_id, request_ref}`,
   `retry: "after_pending_job_terminal"` e um `next_action`. Cada identificador
   só aparece quando a conta consegue usá-lo: `case_id` quando o caso pendente
   está no escopo `consultar`; `job_id` para quem iniciou o job ou um owner
   pessoa; `request_ref` só para quem iniciou.
2. **Acompanhar o job pendente.**
   - Com `pending_job.job_id` (`next_action: "get_case_workflow_job"`),
     consulte `get_case_workflow_job` pelo `job_id` (ou pelo `request_ref`,
     quando vier preenchido) até um estado terminal: `completed`, `blocked`
     ou `failed`.
   - Com `job_id` e `request_ref` `null` (`next_action: "retry_enqueue_later"`,
     `retry_after_seconds: 60`), o job é de outra pessoa e você não consegue
     consultá-lo. A única forma de acompanhar é repetir o mesmo enqueue, com
     a mesma referência, a cada `retry_after_seconds`, até ser aceito. Não
     tente consultá-lo e não troque de `request_ref` por causa de um
     `job_not_found`: isso não libera a fila.
   - O job pendente pode reter a empresa por até cerca de 60 minutos
     (tentativas máximas × lease) se o worker cair. Passado esse tempo, avise
     a engenharia pelo Caixa em vez de insistir.
3. **Enfileire em série.** Para várias folhas da mesma empresa, envie uma,
   espere o estado terminal e só então envie a próxima. Empresas diferentes
   podem ir em paralelo. Depois da recusa, releia `get_case` do caso recusado
   antes de repetir o enqueue; a mesma referência pode ser usada, porque nada
   foi gravado. O replay de um `request_ref` já aceito devolve o recibo
   original.
4. **Não grave em outro caso da empresa durante o job.** Enquanto houver job
   `queued` ou `running`, não chame `receive_case_data`, `update_case_payload`,
   `complement_payroll_items`, anexos ou outras escritas em **outro** caso da
   mesma empresa, nem no cadastro dela. O job confere a empresa inteira e
   termina `BLOCKED` com `job_sources_changed`. Leituras são seguras. A recusa
   no enqueue só avisa da fila; ela não protege o job de uma escrita
   concorrente.
5. **Em 524 ou timeout, não reenvie às cegas.** Consulte
   `get_case_workflow_job` com o **mesmo** `request_ref` do seu pedido. Se o
   recibo existir, siga por ele. Se vier `job_not_found`, repita o enqueue com
   o mesmo `request_ref` e o mesmo corpo: o replay é idempotente.
6. **Em `BUSY` ou HTTP 429, respeite `retry_after_seconds`** (ou o cabeçalho
   `Retry-After`) antes de tentar de novo, com a mesma referência. 429 quer
   dizer que o pedido não foi aceito. `company_job_pending` não é `BUSY`:
   repetir depois de alguns segundos não resolve; siga o item 2.

## Diagnóstico da folha no dossiê

**Onde ler.** Use `get_case_dossier(case_id)`, em `calculations[].diagnostics`.
`get_case_calculation` só lê cálculo rescisório (`CALC-`). Um `CALCF-` é
recusado pelo formato, sem consulta, com `calculation_kind_unsupported` e
`next_action: "get_case_dossier"`: vá ao dossiê. A recusa não diz se o cálculo
existe.

**Afastamento não qualificado: causa primária.** Na issue
`contexto_operacional_pendente`, `leave_qualification_incomplete` é a causa
primária. Leia três coisas:

- `missing_fields`: as causas a tratar. As que restarem além da primária são
  causas próprias (por exemplo, de outro afastamento já qualificado ou de um
  gozo de férias) e seguem o fluxo normal.
- `dependent_fields`: consequências do afastamento sem qualificação. Não trate
  essas agora e não monte `history_qualifications.payroll_context` para elas;
  elas serão reavaliadas depois que o afastamento for qualificado.
- Ação: `next_action: "qualificar_afastamento_na_origem"` vem sempre primeiro,
  porque qualificar o afastamento muda o contexto do mês e invalida
  qualificações de contexto feitas antes. Se houver outras causas,
  `next_action_after_primary` traz a ação delas, para fazer **depois** de
  qualificar o afastamento e recalcular. Com `missing_fields_complete: false`,
  há causas que o diagnóstico não reconhece: trate-as depois, sem inferi-las.

**Onde qualificar.** Cada funcionário traz `leave_qualification`:

- Com `available: true`: traz `primary_reason`, `dependent_reasons`,
  `next_action` e `origins`. Cada origem diz onde completar e, em
  `missing_fields`, o que falta: `leave.categoria`, `leave.policy_version` ou
  `leave.periodos[N].responsabilidade`.
  - `origin: "company_onboarding"` (`onboarding_id`, `fact_id`): no lote de
    onboarding, revise a declaração `historico_operacional` do tipo `leave`
    desse fato com a **categoria fechada** (`category_code` do catálogo), a
    `policy_version` e os `payment_periods` (início, fim e responsabilidade:
    `empregador`, `inss` ou `sem_remuneracao`). Valide e aplique o lote e fixe
    de novo o histórico na folha.
  - `origin: "operational_effect"` (`effect_id`, `case_id`): no caso de
    afastamento `case_id`, complete categoria, `policy_version` e a
    responsabilidade de cada período pela nova preparação desse caso, quando o
    contrato oferecer (domínio `afastamento`). Efeito já aplicado exige a
    conciliação própria.
- Com `available: false` e `reason: "leave_qualification_not_recognized"`: a
  origem não pôde ser reconhecida com segurança. Nada foi separado; trate as
  causas como estão e registre o problema.
- Não infira categoria nem pagador: são dados da DP.

**Fonte.** Um `EXTSRC` registrado em **outro** caso (por exemplo, no caso de
afastamento) não serve como fonte da folha. Cada caso usa as próprias fontes
registradas.

Depois de qualificar, recalcule a folha e releia o dossiê. As causas antes
dependentes podem então aparecer como causas próprias.

**Salário-base ausente.** `salario_base_ausente` é reconhecido no dossiê. Siga
primeiro `next_action`, que é a ação gravada pelo cálculo.
`code_next_action: "qualify_payroll_salary"`, quando aparece (só quando difere
de `next_action`), é a alternativa própria do código: qualificar o salário do
vínculo na competência por `qualify_payroll_salary`.

**Recibo do restart com `replace_payroll_population`.** Em
`population_correction`, o recibo traz `population_count` e `population_hash`
(`canonical_hash(population)`), não a lista. `added`, `removed`, `rebound` e
`preview_id` continuam. A prévia (`preview_payroll_population_correction`)
continua devolvendo a `population` completa com `funcionario_id` e também
`population_hash`, com o mesmo valor do recibo. Compare os dois para confirmar
que a população aplicada é a da prévia.

**Recurso ocupado.** `payroll_population_dependencies_busy` traz
`retryable: true`, `dependency` (`empresa` ou `funcionarios`) e
`next_action: "get_case"`, sem identificadores: outra operação usava esses
registros e nada foi gravado. Releia o caso (`get_case`) e repita o mesmo
pedido, com o mesmo `request_ref`, depois de alguns instantes. Se o snapshot
tiver mudado, gere uma prévia nova.

## Rescisão declarada no onboarding e a população do mês

Em `get_company_employee_history` com `process_type=folha_mensal`, uma
rescisão **declarada no onboarding** aparece em `unqualified_facts` com
`kind: "rescisao"`, `effective_on` e `constraint_hash`, sem os detalhes de RH.
A ausência dessa restrição **não** prova que o vínculo está ativo: a recusa
que vale é a da população mensal, `desligamento_anterior_ao_mes`. Quando ela
aparecer, leve a restrição à operadora em vez de insistir em incluir a pessoa
na folha do mês. A leitura também traz `identifiers.matricula` e
`identifiers.matricula_operacional`; a regra da matrícula no `create_case`
está no domínio `geral`.

## Regras comuns da operação

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Documente bases recebidas, fontes, divergências e ausências. Uma base ausente não se transforma em zero. Não invente parcelas, critérios, legislação ou datas; consulte fontes e contratos aprovados pelo responsável. Cumpra os gates humanos. Uma validação técnica não autoriza aceite, transmissão, pagamento ou publicação de resultados.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
