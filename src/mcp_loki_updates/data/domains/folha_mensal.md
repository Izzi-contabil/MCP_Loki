# Folha mensal

Este domínio complementa o `geral`, que continua com a prontidão, a retomada, a
população da folha e o diagnóstico do job bloqueado no cálculo. Antes de
operar, consulte `meu_acesso`, `get_dp_capabilities` e
`get_process_contract("folha_mensal")`; envie `dados_folha` pelo escritor
anunciado. Os códigos e campos abaixo valem somente quando a resposta servida
os apresentar.

## Motor folha-v31: recalcular as folhas não entregues

> **Atenção.** O motor da folha mensal passou a `folha-v31`. A versão do motor
> entra no hash das entradas, então **todas as folhas mensais não entregues
> ficam desatualizadas** (`calculation_stale`): as abertas, as que estão em
> revisão e as aprovadas que ainda não foram entregues. Cada uma precisa ser
> recalculada, conferida de novo e receber novo aceite antes da entrega; o
> aceite dado ao cálculo anterior não vale para o novo. As folhas já
> entregues não mudam e não são reescritas.

Nada é recalculado, reaberto ou decidido automaticamente. Não cancele o caso
para isso.

- **Abertas e em revisão** (`aberto`, `em_preparacao`, `aguardando_revisao`):
  recalcule pelo mesmo fluxo da folha (`enqueue_case_workflow`, uma folha por
  empresa na fila), com `input_snapshot` e `expected_snapshot` atuais e novo
  `request_ref`, gere o pacote corrente e confira de novo.
- **Aprovadas e não entregues:** a aprovação pertence ao pacote anterior; a
  entrega exige novo cálculo, conferência e aceite humano. O enqueue recusa
  caso aprovado (`case_not_preparable`). Siga a próxima ação servida e, se
  não houver caminho para recalcular, não entregue o pacote antigo: avise a
  operadora e registre o problema.

Diferenças entre o cálculo
anterior e o novo vêm das regras abaixo (salário-família e insalubridade no
mês de admissão); mostre-as à operadora na conferência. Uma folha recalculada
pode trazer as pendências novas de salário-família: elas não são erro do
recálculo. Competência já entregue só se refaz por retificação.

## Salário-família pelo limite da base do INSS (folha-v31)

O Loki testa o limite da cota contra a **base do INSS do mês que ele mesmo
calcula** (regra da DP: a remuneração reúne as verbas de natureza salarial).
Até a v30 o teste usava a soma dos proventos, que incluía verbas sem
incidência e o abono de férias. Não informe o salário-família nem uma
remuneração própria para o limite. Quando a base do INSS ainda depende de um
componente pendente, a cota também fica pendente: uma base subestimada nunca
paga cota a quem está acima do limite.

Pendências novas no diagnóstico do dossiê, com a próxima ação servida:

- `salario_familia_mes_admissao_pendente_regra` (próxima ação
  `aguardar_regra_dp_do_salario_familia_no_mes_de_admissao`): o vínculo
  entrou na empresa nesta competência com base até o limite. A entrada é
  `inicio_empresa_em` ou, sem ela, `admitido_em`; a transferência entre
  empresas do grupo hoje também conta como entrada. A regra é da DP: o Loki
  não paga nem nega. Enquanto ela não responder, o vínculo fica parcial, sem
  total de proventos e sem líquido; INSS, FGTS e IRRF saem calculados. Não
  invente remuneração nem marque `mes_sem_remuneracao` para destravar. Com a
  base parcial acima do limite a cota é zero, sem pendência.
- `salario_familia_remuneracao_zero_sem_declaracao` (próxima ação
  `declarar_mes_sem_remuneracao_ou_regra_de_salario_familia_do_afastamento`):
  base do INSS zero com filhos. Se for benefício do INSS ou afastamento no mês
  inteiro, declare o contexto `mes_sem_remuneracao`. Se forem faltas ou
  suspensão, deixe pendente e avise a operadora.
- `salario_familia_base_inss_zero_com_proventos` (próxima ação
  `qualificar_incidencia_inss_das_rubricas_do_mes`): a base do INSS deu zero,
  mas há proventos sem incidência (abono, por exemplo). Confira a incidência
  das rubricas no mapa. Não declare `mes_sem_remuneracao`.

**Saída das três pendências, depois da decisão da DP.** Quando a DP informar a
cota do caso (ou zero), registre-a com `submit_operator_correction`:
`target: "calculation"`, `changes:
{"funcionarios.<matricula>.bases.salario_familia_cents": <centavos>}`, com
`expected_snapshot` atual, `idempotency_ref` estável, `human_message` com a
resposta da DP e `reason`. O Loki recalcula e o vínculo fica integral. Não
use essa rota sem a decisão da DP nem para antecipar a regra. A falta de
filhos no cadastro não usa essa rota: complete o cadastro dos dependentes.
Uma correção registrada antes da v31 continua consumida no recálculo.

**Em consulta à DP, sem mudança agora:** o terço de férias do mês entra na base
do limite; faltas que reduzem a base podem levá-la para baixo do limite e
permitir a cota; no mês de admissão, se o limite usa a remuneração do mês
parcial ou do mês cheio (e se a cota é proporcional aos dias); e se a
transferência entre empresas do grupo deve contar como entrada. Se a equipe
divergir do Loki nesses pontos, registre como divergência a confirmar com a
DP, não como defeito.

## Insalubridade e VT no mês de admissão (folha-v31)

- **Insalubridade.** O mapa precisa ter só a rubrica do grau declarado
  (`rubrica_loki`). Não acrescente a incompatível ao mapa: a ausência dela não
  bloqueia. A periculosidade segue o mesmo relaxamento do mapa. No mês da
  admissão, declare `vigente_desde` igual à data de admissão: o Loki paga
  pelos dias de `periodo_remuneravel` (ou pela quantidade lançada) sobre o
  divisor do mapa e não exige mais segmentação. Uma regra iniciada depois da
  admissão continua pendente (`insalubridade_vigencia_parcial_exige_segmentacao`).
  A periculosidade parcial continua exigindo segmentação. Se o Domínio pagar
  diferente no mês de entrada (dias ou DSR), é ponto a confirmar com a DP.
- **VT do admitido no mês: sem mudança.** O desconto continua retido com
  `vale_transporte_vigencia_parcial_exige_regra` até a regra da DP. Não
  declare vigência desde o dia 1 para destravar.

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
3. **Enfileire em série na mesma empresa, em paralelo entre empresas.** Para
   várias folhas da mesma empresa, envie uma, espere o estado terminal e só
   então envie a próxima. Folhas de **empresas diferentes** rodam ao mesmo
   tempo no worker, no máximo uma por empresa: para várias empresas,
   enfileire uma folha de cada sem esperar as outras; o tempo total deixa de
   ser a soma. Consultas Dataprev mensais podem demorar mais enquanto houver
   folhas em execução, porque só rodam com a fila de folha vazia; acompanhe
   pelo recibo, sem reenviar. Depois da recusa, releia `get_case` do caso recusado
   antes de repetir o enqueue; a mesma referência pode ser usada, porque nada
   foi gravado. O replay de um `request_ref` já aceito devolve o recibo
   original.
4. **Não grave em outro caso da empresa durante o job.** Enquanto houver job
   `queued` ou `running`, não chame `receive_case_data`, `update_case_payload`,
   `complement_payroll_items`, anexos ou outras escritas em **outro** caso da
   mesma empresa, nem no cadastro dela. O job confere a empresa inteira e
   termina `BLOCKED` com `job_sources_changed`. Leituras são seguras, e gravar
   em casos de **outras** empresas também é seguro. A recusa
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

## Janela de publicação e a fila de folha

- **Na janela que publica esta versão** (a primeira com a re-fixação de
  jobs), a fila de folha ainda precisa estar vazia antes da janela: jobs
  aceitos na versão anterior não são retomados.
- **A partir das janelas seguintes**, não é mais preciso esvaziar a fila.
  Durante a janela avisada, só pare de gravar dados (`receive_case_data`,
  correções, anexos) e de iniciar jobs novos (`enqueue_case_workflow`). Jobs
  que estavam na fila e ainda não tinham começado são retomados depois da
  janela, no build novo, sem reenfileirar. A trilha do caso registra
  `case_job_build_repinned`. O aviso de que pode voltar a usar o Loki chega
  assim que a publicação libera a operação, antes do fim da janela.
- Depois da janela, acompanhe cada job com `get_case_workflow_job`. Ainda pode
  vir `BLOCKED` com:
  - `job_build_changed`: o job já tinha começado antes da janela;
  - `job_snapshot_changed` / `job_sources_changed`: dados do caso ou da
    empresa mudaram depois do enqueue;
  - `job_fingerprint_snapshot_changed`: a versão nova mudou o que o cálculo
    confere.

  Nesses casos, confira o caso com `get_case` e reenfileire com um
  `request_ref` novo e o `expected_snapshot` atual. Não reenfileire um job
  que ainda esteja `queued` ou `running`.

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

## Contexto do mês por pessoa e hashes dos lançamentos

Folha com afastamento ou gozo no mês: depois de `enqueue_case_workflow` e
`get_case_workflow_job`, chame `get_case_dossier(case_id)`. Em
`calculations[]`, pegue a entrada `kind=folha_mensal` cujo `calculation_id` é
o do job. Em `diagnostics.employees[]`, cada pessoa com pendência de contexto
tem `payroll_context`.

1. Se `payroll_context.available=false`, informe o `reason` e não qualifique o
   mês daquela pessoa. Não invente hash.
2. Se `leave_qualification.next_action=qualificar_afastamento_na_origem`,
   qualifique primeiro o afastamento na origem. Depois recalcule e leia o
   dossiê de novo, porque o `context_hash` muda.
3. Com o pacote em `aguardando_revisao`, os lançamentos saem
   `payroll_effective_launches_not_read`. Com o aceite humano, faça
   `restart_case` e leia o dossiê de novo. Só o cálculo mais recente traz
   lançamentos.
4. Use o `context_hash` só com `context_current=true`. Com `false` e
   `payroll_context_changed_since_calculation`, recalcule antes. Com `null`,
   informe o `context_current_reason`.
5. Monte `history_qualifications.payroll_context`: o envelope
   `{version: qualification_version, competencia, funcionarios: [...]}`; por
   pessoa, `funcionario_id` e `context_hash` copiados do bloco; os `periodos`
   remunerados com fonte; `encargos_afastamento` ou `mes_sem_remuneracao`,
   quando há período não pago pelo empregador.
6. Confira que `lancamentos.calculation_id` é o do job. Se
   `lancamentos.available=true`, coloque cada item de `lancamentos.items` em
   `lancamentos_conciliados`, com o mesmo `codigo` e `lancamento_hash` e os
   `periodos` datados com fonte documental. Todos os códigos da pessoa
   entram; cada período precisa caber nos `periodos` remunerados; não calcule
   o hash você mesma.
7. Motivos de `lancamentos` indisponível:
   - `payroll_effective_inputs_changed_since_calculation`: recalcule e leia
     de novo;
   - `payroll_effective_launches_busy`: tente de novo mais tarde, sem
     reiniciar nada;
   - `payroll_effective_launch_codes_repeated`: a pessoa tem dois lançamentos
     com o mesmo código. Hoje o Loki não concilia esse caso; registre o
     problema e não qualifique os lançamentos dela;
   - `payroll_effective_launches_unavailable`: informe e não concilie.
8. Envie por `receive_case_data`, com `expected_snapshot`/`request_ref`, e
   recalcule. Se vier `payroll_context_qualification_stale`, o contexto
   mudou: leia o dossiê de novo.

O bloco não traz CPF, nome, referência nem descrição. Também não atesta
paridade nem aceite de DP.

## Rescisão declarada no onboarding e a população do mês

Em `get_company_employee_history` com `process_type=folha_mensal`, uma
rescisão **declarada no onboarding** aparece em `unqualified_facts` com
`kind: "rescisao"`, `effective_on` e `constraint_hash`, sem os detalhes de RH.
A ausência dessa restrição **não** prova que o vínculo está ativo: a recusa
que vale é a da população mensal, `desligamento_anterior_ao_mes`. Quando ela
aparecer, leve a restrição à operadora em vez de insistir em incluir a pessoa
na folha do mês. Se a operadora confirmar que o contrato segue ativo, o
caminho é a revogação auditada do desligamento (domínio
`alteracao_cadastral`, "Revogar desligamento gravado pelo onboarding").
Depois da revogação, nada é recalculado sozinho: cada folha aberta da
empresa a partir do mês recebe `populacao_desatualizada_por_revogacao`;
refaça a preparação incluindo a pessoa e refaça as seleções históricas.

A leitura também traz `identifiers.matricula` e
`identifiers.matricula_operacional`; a regra da matrícula no `create_case`
está no domínio `geral`. Depois de uma restauração ou troca auditada do
código Domínio (domínio `alteracao_cadastral`), a folha aberta com o código
antigo no payload fica `vinculo_nao_identificado_na_competencia` até você
reenviar a população com o código novo.

## Regras comuns da operação

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Documente bases recebidas, fontes, divergências e ausências. Uma base ausente não se transforma em zero. Não invente parcelas, critérios, legislação ou datas; consulte fontes e contratos aprovados pelo responsável. Cumpra os gates humanos. Uma validação técnica não autoriza aceite, transmissão, pagamento ou publicação de resultados.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
