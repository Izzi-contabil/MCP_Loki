# Folha mensal

Este domínio complementa o `geral`, que continua com a prontidão, a retomada, a
população da folha e o diagnóstico do job bloqueado no cálculo. Antes de
operar, consulte `meu_acesso`, `get_dp_capabilities` e
`get_process_contract("folha_mensal")`; envie `dados_folha` pelo escritor
anunciado. Os códigos e campos abaixo valem somente quando a resposta servida
os apresentar.

## Motor folha-v32: recalcular as folhas não entregues

> **Atenção.** Quando o cálculo da folha mostrar o motor `folha-v32`: a versão
> do motor entra no hash das entradas, então **todas as folhas mensais não entregues
> ficam desatualizadas** (`calculation_stale`): as abertas, as que estão em
> revisão e as aprovadas que ainda não foram entregues. Cada uma precisa ser
> recalculada, conferida de novo e receber novo aceite antes da entrega; o
> aceite dado ao cálculo anterior não vale para o novo. As folhas já
> entregues não mudam e não são reescritas. Isso vale também para as folhas
> recalculadas na `folha-v31`.

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

Diferenças entre o cálculo anterior e o novo vêm das regras abaixo
(salário-família e VT do admitido); mostre-as à operadora na conferência. Uma
folha recalculada pode trazer pendências novas de salário-família ou de VT:
elas não são erro do recálculo. Competência já entregue só se refaz por
retificação.

**Correções registradas na v31 continuam valendo.** Se você declarou, com
`submit_operator_correction`, a cota de salário-família de um admitido no mês
como saída da pendência antiga (`salario_familia_mes_admissao_pendente_regra`),
essa correção é consumida no recálculo e **prevalece** sobre a cota
proporcional da v32. Compare o valor declarado com o calculado na memória
`operator_corrections` do cálculo novo e avise a operadora antes do aceite. Se
divergirem, a decisão de manter ou trocar a correção é dela com a DP. Sobre uma
cota pendente, a memória mostra `calculated: null`: o Loki não decidiu aquele
valor.

## Salário-família pela remuneração devida no mês (folha-v32)

Regra da DP de 19/11/2026. O Loki testa o limite da cota contra a
**remuneração que seria devida no mês, independentemente dos dias
trabalhados**:

- entra o salário-base cheio;
- os adicionais proporcionais aos dias (insalubridade sobre o mínimo,
  adicional percentual, periculosidade por dias) entram pelo valor do mês
  cheio;
- as demais verbas do mês com incidência de INSS entram pelo valor do mês
  (horas extras, produtividade, diárias);
- ficam fora faltas, DSR das faltas e atrasos, as férias do mês com o terço e
  o 13º.

Não informe o salário-família nem uma remuneração própria para o limite.
Quando a base do INSS ainda depende de um componente pendente, a cota também
fica pendente.

- **Faltas não reduzem a remuneração.** Com salário acima do limite e faltas
  no mês, não há cota, mesmo que a base do INSS caia abaixo do limite.
- **Mês de férias:** o terço não entra no limite.
- **Mês de admissão (não é mais pendência):** o limite usa o salário do mês
  cheio, e a cota sai proporcional aos dias do contrato, pelo mês comercial de
  30 dias: `30 − dia da admissão + 1`. Admissão em 16/07 dá 15 dias, em 31/07
  dá 1 e em 01/02 dá 30. A contagem está em confirmação com a DP; se o Domínio
  divergir, registre como divergência a confirmar, não como defeito. A
  pendência `salario_familia_mes_admissao_pendente_regra` não aparece mais em
  cálculos novos.

**Pendências.** O vínculo fica parcial, sem total de proventos e sem líquido;
INSS, FGTS e IRRF saem calculados. Não invente remuneração nem marque
`mes_sem_remuneracao` para destravar.

- `salario_familia_mes_transferencia_pendente_regra` (próxima ação
  `aguardar_regra_dp_do_salario_familia_no_mes_de_transferencia`): o vínculo
  entrou nesta competência por transferência entre empresas do grupo, com
  remuneração devida até o limite. A regra da DP vale só para a admissão. Não
  pague nem negue.
- `salario_familia_salario_do_mes_nao_identificado` (próxima ação
  `qualificar_rubrica_do_salario_do_mes_no_mapa`): o mapa da empresa não tem rubrica de salário reconhecível (fórmula `salario_base` ou `remuneracao_periodo`; por exemplo, o salário vem como valor informado). A saída normal é qualificar ou corrigir a rubrica de salário no mapa da empresa. `submit_operator_correction` só vale com decisão explícita da DP sobre a cota daquele caso.
- `salario_familia_adicional_mes_cheio_nao_identificado` (próxima ação
  `qualificar_adicional_do_mes_cheio_ou_declarar_cota_pela_dp`): há um
  adicional proporcional aos dias cujo valor do mês cheio o Loki não
  reconstrói. Não informe o valor cheio por conta própria.
- `salario_familia_deducao_nao_classificada` (próxima ação
  `qualificar_deducao_da_base_ou_declarar_cota_pela_dp`): um desconto da base
  do INSS que não é falta, DSR ou atraso identificável (um estorno, ou uma
  falta lançada como valor informado) decide a cota. Confira a natureza da
  rubrica com a operadora.
- `salario_familia_medias_ferias_nao_classificadas` (próxima ação
  `declarar_cota_pela_dp_com_medias_de_ferias`): as médias dentro da
  remuneração de férias decidiriam a cota.
- `salario_familia_remuneracao_zero_sem_declaracao` e
  `salario_familia_base_inss_zero_com_proventos`: sem mudança. Continuam
  lendo a base do INSS efetiva do mês. Se for benefício do INSS ou afastamento
  no mês inteiro, declare `mes_sem_remuneracao`; se forem faltas ou suspensão,
  deixe pendente e avise. Com proventos sem incidência, confira a incidência
  das rubricas no mapa.

**Saída das pendências, depois da decisão da DP.** Quando a DP informar a cota
do caso (ou zero), registre-a com `submit_operator_correction`:
`target: "calculation"`, `changes:
{"funcionarios.<matricula>.bases.salario_familia_cents": <centavos>}`, com
`expected_snapshot` atual, `idempotency_ref` estável, `human_message` com a
resposta da DP e `reason`. O Loki recalcula e o vínculo fica integral. Não use
essa rota sem a decisão da DP nem para antecipar a regra. A falta de filhos no
cadastro não usa essa rota: complete o cadastro dos dependentes.

## VT do admitido no mês (folha-v32)

Regra da DP de 19/11/2026. Isto substitui o "VT do admitido no mês: sem
mudança" da `folha-v31`.

- O desconto é o percentual da regra individual aplicado **uma vez** sobre o
  salário proporcional do mês: salário × dias do contrato no mês comercial /
  30. O limite informativo das pendências de VT também usa esse salário.
- Quando a fonte mostrar a regra valendo desde a admissão (ou antes), declare essa data; o Loki não retém mais. Não ajuste `vigente_desde` para destravar. Uma regra vigente desde antes
  do mês também passa a descontar sobre o salário proporcional. Uma regra que
  começa depois da admissão, ou termina no mês, continua
  `vale_transporte_vigencia_parcial_exige_regra`.
- **Com concessão** (`vale_transporte_concessao`):
  - admissão no dia 1: vale a fórmula de sempre, com a proporção da concessão
    aplicada;
  - admissão depois do dia 1 e proporção igual aos dias do contrato (por
    exemplo, 15/30 para admissão em 16/09): o desconto é o percentual sobre o
    salário proporcional, limitado ao custo concedido, sem reaplicar a
    proporção;
  - outra proporção (dias de uso, por exemplo): fica
    `vale_transporte_proporcao_concessao_admissao_ambigua` (próxima ação
    `confirmar_proporcao_da_concessao_ou_declarar_desconto_pela_dp`). Não
    ajuste a proporção para destravar. Com a decisão da DP, declare o desconto
    com `submit_operator_correction`, `target: "calculation"`, `changes:
    {"funcionarios.<matricula>.verbas.<rubrica de VT>.0.valor_cents":
    <centavos>}` (o caminho exato da linha de VT vem em `operator_corrections` do cálculo).
  - Se o Domínio aplicar as duas proporções, registre como divergência a
    confirmar com a DP.
- Na transferência entre empresas do grupo, a regra iniciada na entrada fica
  `vale_transporte_mes_transferencia_pendente_regra` até a regra da DP.
- Afastamento e desligamento no mês: sem mudança.

## Insalubridade no mês de admissão (desde a folha-v31)

- **Insalubridade.** O mapa precisa ter só a rubrica do grau declarado
  (`rubrica_loki`). Não acrescente a incompatível ao mapa: a ausência dela não
  bloqueia. A periculosidade segue o mesmo relaxamento do mapa. No mês da
  admissão, declare `vigente_desde` igual à data de admissão: o Loki paga
  pelos dias de `periodo_remuneravel` (ou pela quantidade lançada) sobre o
  divisor do mapa e não exige mais segmentação. Uma regra iniciada depois da
  admissão continua pendente (`insalubridade_vigencia_parcial_exige_segmentacao`).
  A periculosidade parcial continua exigindo segmentação. Se o Domínio pagar
  diferente no mês de entrada (dias ou DSR), é ponto a confirmar com a DP.

## Fila durável: um job pendente por empresa

0. **Empresa nova sem o worker.** Com a concessão automática, empresa nova
   já entra no worker sozinha (domínio `geral`, "Empresa nova e onboarding
   pela rotina"). `worker_not_authorized` com
   `reason: "worker_company_grant_missing"` ainda aparece em empresa anterior
   à política sem backfill, worker suspenso ou credencial vencida, e em
   servidor anterior; o caminho é o mesmo. A pessoa owner (ou master)
   inclui pelo conector, sem pedir à engenharia:
   1. `listar_solicitacoes_acesso`: localize a conta e anote `id` e
      `revision`. A recusa já traz `worker_account_id` e
      `worker_account_revision` para owner/master
      (`next_action: "listar_solicitacoes_acesso"`); para os demais vem
      `next_action: "ask_administrator"`: peça à pessoa owner.
   2. Prepare só o acréscimo: `receive_case_data` com `case_id: "@connector"`
      e `request: {schema_version: "loki.connector-command/1", operation:
      "prepare_authorization_addition", account_id, expected_revision,
      grants}`. Em `grants`, só as empresas que faltam, cada uma com o
      `required_grant` da recusa (`processes: ["folha_mensal"]`,
      `capabilities: ["consultar", "operar_casos"]`). O Loki conserva papel,
      status e as concessões atuais. Nunca use `preparar_autorizacao` para
      isso: ele substitui a lista inteira.
   3. Mostre o antes/depois e aplique com `aplicar_autorizacao`, com a
      confirmação literal da pessoa owner.
   4. Repita o mesmo enqueue: a recusa não grava job, então o mesmo
      `request_ref` serve.

   Sem esse `reason`, é outro problema: registre o problema e avise a
   engenharia pelo Caixa.
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

## Matrícula do eSocial na população da folha

Vale quando `get_company_onboarding_contract` citar o motivo
`adocao_matricula_esocial`; sem isso, a população segue a matrícula
registrada de hoje. Depois que a empresa adotar a matrícula do eSocial
(domínio `alteracao_cadastral`, "Adotar a matrícula do eSocial"), toda
população de folha usa a matrícula eSocial. O código Domínio não é aceito
como alias: traduza o extrato do Domínio pelo mapa de `identifiers`
(`namespace: "dominio"`, `status: "auxiliar"`) de
`get_company_employee_history`. O Loki não escolhe a pessoa.

- Folha aberta que citava o código antigo (listada em
  `adoption_effects.open_payrolls_citing_previous_code` do recibo): reenvie a
  população com as matrículas eSocial pela substituição da população.
- Pendência `matricula_coincide_com_codigo_auxiliar` (também em
  `case_candidate_diagnostics`), com `next_action`
  `resolve_payroll_employee_e_preview_payroll_population_correction_com_funcionario_id`:
  o valor do item é o código Domínio antigo de **outro** vínculo. Troque pela
  matrícula eSocial certa. A saída é `resolve_payroll_employee` com nome e CPF,
  que devolve o `funcionario_id`, e o item reenviado por
  `preview_payroll_population_correction` e a aplicação com
  `{funcionario_id, matricula}`. A confirmação vale só naquele caso: outra
  folha do mesmo mês precisa da sua.
- **Empresa com pares cruzados** (o código Domínio de um vínculo é a matrícula
  eSocial de outro): depois da adoção, mande a população pela correção da
  população com o `funcionario_id` de cada item. É o identificador da pessoa
  que o schema aceita; o item de `dados_folha` não tem CPF.
- `transitional_collisions` no recibo: outro vínculo ainda usa o mesmo valor
  como código Domínio. Adote esse vínculo também; até lá a folha recusa o
  valor como ambíguo.
- A rescisão que citar uma folha calculada antes da adoção recusa
  `termination_monthly_calculation_predates_registration_adoption`:
  recalcule essa folha.
- Folhas entregues continuam com o código antigo impresso: não reabra nem
  recalcule por causa da adoção.

## Regras comuns da operação

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Documente bases recebidas, fontes, divergências e ausências. Uma base ausente não se transforma em zero. Não invente parcelas, critérios, legislação ou datas; consulte fontes e contratos aprovados pelo responsável. Cumpra os gates humanos. Uma validação técnica não autoriza aceite, transmissão, pagamento ou publicação de resultados.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
