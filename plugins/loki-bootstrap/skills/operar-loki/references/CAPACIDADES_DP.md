# Recursos de DP: descobrir, preparar e conferir

Leia antes de preparar folha com muitas pessoas, retomar caso ou qualificar
férias, afastamento, consignado, pensão e adicionais. Este roteiro descreve
recursos condicionados ao contrato servido, sem corrigir defeitos de cálculo.

## Descobrir prontidão e medir acurácia

Consulte `meu_acesso`, `get_dp_capabilities`, `list_workflows` e
`get_process_contract` no serviço autenticado. Fonte no Git, plugin instalado,
catálogo do aplicativo e contrato servido são observações separadas. Uma rota
nova só pode ser usada quando anunciada pelo contrato servido; instrução local
não comprova publicação, acesso ou instalação no executor.

Para folha, consulte `get_client_readiness` com `process_type=folha_mensal`,
`empresa_cnpj` e `competencia` exatos. `pronto` é cadastral;
`folha_avaliada`, `pronto_folha` e `mapa_folha` mostram a avaliação mensal,
com hash/grupo/origem. Sem contexto mensal, `pronto_folha=null` e
`mapa_folha_nao_avaliado` conservam a lacuna. Essa leitura não mede acurácia
nem comprova completude ou prontidão por funcionário.

O contrato atual não oferece endpoint bulk específico de prontidão por pessoa.
Quando o catálogo/contrato não oferecer esse recurso, registre a lacuna sem
inventar nomes ou concluir que uma tabela da harness seja estado do Loki.
Consulte população/identidade no caso, histórico e pendências por pessoa.
Uma tabela de cobertura é diagnóstico da harness, com data e fontes explícitas.

Para histórico em lote, somente quando o catálogo HTTPS oferecer
`get_operational_batch_contract`, consulte esse contrato e confira as operações
permitidas. Sem essa ferramenta no catálogo, registre pendência de distribuição
e use consultas e seleções individuais anunciadas e autorizadas. Não invente
alias, dispatcher ou rota de lote em `receive_case_data`.
O lote existente, quando disponível, pode encadear leituras
`get_case_historical_state` e seleções `apply_historical_state` por caso,
com o `state_hash` retornado, identidade/episódio e corte conferidos.
Isso continua sendo execução sequencial por item, sem endpoint bulk novo.
Use dependências/referências de resultado somente no formato do contrato;
releia recibos e consumo por calculador. `SUCCEEDED` da linha não comprova
consumo financeiro; `STARTED` ambíguo exige conciliação antes de repetir.

A meta de98% usa casos completos corretos / casos elegíveis, com coorte,
finalidade, período e elegibilidade definidos antes da rodada. Falha, parcial
e abstenção não são acerto; não exclua casos após conhecer o resultado.
Sem referência ou completude necessárias, declare percentual não aferido.
Registre também comparáveis, coincidências por campo, bloqueios e motivos,
sem substituir o indicador principal. Prontidão, testes de software e seleção
de histórico não comprovam acurácia geral. Separe defeito reproduzido,
parâmetro/dado pendente, regra ainda não medida e diferença de recepção da harness.

## Retomada, nova preparação e seleção da folha

Na folha, siga `preferred_execution` e `durable_workflow` do contrato.
Quando `available=true`, use os jobs duráveis
`enqueue_case_workflow`/`get_case_workflow_job`, inclusive pela rota declarada
`receive_case_data` com `loki.case-workflow-command/1`.
Preserve `request_ref` e `job_id`; resposta perdida exige consulta do mesmo
job, não outro cálculo. `exception_type`, `phase` e `reference` são diagnóstico
técnico, sem provar correção dos dados ou autorizar restart.

Quando o contrato anunciar `durable_workflow.admission:
"one_pending_job_per_company"`, a fila aceita um job pendente por empresa.
`company_job_pending` (HTTP 409, nada gravado) traz `pending_job` e
`next_action`: com `job_id`, acompanhe por `get_case_workflow_job` até
`completed`, `blocked` ou `failed`; com `retry_enqueue_later`, repita o mesmo
enqueue, com a mesma referência, a cada `retry_after_seconds`. Enfileire em
série na mesma empresa e não grave em outro caso nem no cadastro da empresa
durante o job (`job_sources_changed`). Em 524, consulte o mesmo `request_ref`;
em `BUSY`/429, respeite `retry_after_seconds`. Retenção acima de cerca de 60
minutos vai à engenharia pelo Caixa. Roteiro em “Fila da folha: um job
pendente por empresa” de [WORKFLOWS.md](WORKFLOWS.md).

O diagnóstico da folha fica em `get_case_dossier`
(`calculations[].diagnostics`); `CALCF-` em `get_case_calculation` recusa com
`calculation_kind_unsupported`. Afastamento não qualificado é causa primária:
`qualificar_afastamento_na_origem` primeiro, `dependent_fields` depois da
qualificação, `next_action_after_primary` para as causas próprias, e
`leave_qualification.origins[*]` diz onde completar (onboarding ou caso de
afastamento). `salario_base_ausente` segue `next_action` (alternativa
`code_next_action`); o restart da população traz `population_count` e
`population_hash`, iguais ao da prévia; `payroll_population_dependencies_busy`
é `retryable`. Roteiro em “Diagnóstico da folha no dossiê” de
[WORKFLOWS.md](WORKFLOWS.md) e no domínio `folha_mensal`.

Quando a resposta servida apresentar, job da folha `blocked` em `calculate`
traz `diagnostic.errors` com `{"field": ..., "index": N, "reason": ...}`:
`reason` é código fechado e `index` é a posição do funcionário em
`dados_folha.funcionarios` do payload enviado, contando do zero. `field`
aponta o lançamento (`...lancamentos.M`, `.valor`, `.quantidade`,
`.divisor_quantidade`, `.fatos_datados.K.alocacao`) ou o dado do funcionário
(`.salario_base`, `.periodo_remuneravel`, `.parcelas_salariais`,
`.matricula`). Lançamento além dos enviados é efeito operacional acrescentado
pelo Loki: corrija o efeito ou o mapa. `verba_nao_mapeada` traz `codigo`, a
rubrica do layout sem mapeamento: peça o mapeamento no mapa da empresa.
`dados_folha.valorizacao` sem `index` é recusa da competência;
`operational_pending_employee_out_of_scope`/`cadastro_pending_employee_out_of_scope`
indicam contexto de matrícula fora do payload (confira a população) e
`tabela_legal_fora_da_competencia`/`fgts_mensal_...`, configuração. A
matrícula nunca volta. O diagnóstico não prova o resto nem autoriza
recomeçar: corrija pelo fluxo normal com novo `expected_snapshot`.

Recomeçar exige pessoa autorizada, intenção específica e
`expected_snapshot=get_case.correction_snapshot`. Siga `preparation` do
contrato; `loki.case-preparation-transport/1` em `receive_case_data` só é rota
quando anunciada. `replace_process_inputs` abre nova preparação e exige novos
dados financeiros; documentos, decisões e eventos anteriores permanecem.
Preservar imports de admissão/rescisão exige a prévia `preview_import_preservation`
e o plano/hash/dependências correntes em `preserve_imports`; não escolha eventos
de memória. Aprovação ou efeito pode exigir conciliação prévia.
Folha mensal protegida (`aguardando_revisao`, `aprovado`, `publicado`) deixa de
bloquear a preservação só com `consumer_impact.protected_consumers[]` em
`classification: "equivalent"` e
`reason: "employee_excluded_from_current_calculation"` (contrato declara
`protected_consumer_equivalence_proofs`): o cálculo de onde saiu o pacote da
folha (em revisão ou aprovado) está ancorado e não inclui o funcionário; a
prévia não recalcula a folha viva. `"unknown"` continua bloqueando com
`import_preservation_protected_dependency`. No restart,
`import_preservation_consumer_changed` pede refazer a prévia;
`reconciliation_dependencies_busy` (gravação em andamento em casos da mesma
empresa) pede tentar depois, sem forçar. Pacote envelhecido continua barrado na
revisão (`calculo_desatualizado`).

Quando o serviço informar o motivo, a recusa de `restart_case`/`cancel_case`
por efeitos conserva `restart_requires_effect_reconciliation` ou
`case_lifecycle_action_refused` e traz `blocking_refs` (`ref` e `kind` entre
`vinculo_event`, `documentary_approval`, `chat_review` e `operational_effect`;
eventos também `origin` e `event_type`), `blocking_ref_count` (lista limitada
a 50). `next_action` vem somente em `restart_case`:
`preview_import_preservation` quando todos os refs são imports documentais, só
em admissão e rescisão; `preview_admission_reconciliation` nos demais casos de
admissão; ausente nos outros processos. As duas prévias habilitam nova
preparação (reinício), não cancelamento: `cancel_case` recusado por efeitos
nunca traz `next_action` e não tem caminho pelo acesso da operadora. Nele,
`blocking_refs` e `blocking_ref_count` só vêm quando o estado permitiria
cancelar sem os efeitos (`aberto`, `em_preparacao`, `aguardando_revisao`,
`rejeitado`); fora deles `case_lifecycle_action_refused` vem sem esses campos
e a recusa é de estado. Nenhuma proteção mudou. Siga somente o `next_action`
recebido; sem ele, pare, guarde a resposta e relate pelo fluxo de problema com
`case_id` e refs, sem dado pessoal. Não contorne, não cancele nem recrie o
caso. Blockers da prévia de conciliação, Beneficiários da ficha e nome
diferente só em caixa/espaços estão no domínio `admissao`.

`restart_case` em `aberto`/`em_preparacao` sem `preparation` recusa com
`restart_requires_preparation_for_state` (`next_action: "get_process_contract"`):
envie `preparation` com `schema_version: "loki.case-preparation/1"`,
`request_ref` e, em `mode`, um dos modos de
`get_process_contract.preparation.modes`; efeitos persistidos ainda podem
exigir conciliação própria. Nos demais estados, `restart_requires_adjustable_state` não tem
reinício por esse caminho.
Depois de `restart_case`, quando a resposta servida apresentar, `get_case`
lista de novo `harness_sources` e os anexos nativos em `documentos`:
reutilize os mesmos EXTSRC e anexos, sem registrar nem anexar de novo.

Correção da população da folha depende de
`preparation.population_correction` no contrato servido. Quando oferecido,
prepare a lista final completa de `funcionario_id`+`matricula`, consulte
`preview_payroll_population_correction` ou a rota anunciada
`loki.payroll-population-preview/1` e apresente diferenças ao humano.
A prévia aceita item só `{"matricula"}` e devolve `funcionario_id` em
`population`. Matrícula que passou a apontar para outra pessoa recusa o item
só com `{"matricula"}` (`payroll_population_rebound_requires_identifier`) até o
`funcionario_id` novo vir no item; confirme antes com o humano que é outra
pessoa. A aplicação exige `{funcionario_id, matricula}` copiados da prévia e o
`preview_id`.
Quando a resposta servida apresentar, `payroll_population_identity_changed`
da prévia traz `next_action: "preview_payroll_population_correction"` e
`errors` com `{"field": "population[*]", "index": N, "reason": ...}`: `index`
é a posição do item na lista enviada, contando do zero; motivos
`admissao_posterior_ao_mes`, `entrada_empresa_posterior_ao_mes`,
`desligamento_anterior_ao_mes`, `matricula_sem_vinculo_operacional`,
`matricula_ambigua_na_competencia`, `funcionario_id_diverge_da_matricula` e
`vinculo_fora_da_competencia`. Remova ou corrija esses itens e peça a prévia
de novo; `{"field": "population"}` sem `index` não aponta item.
A aplicação usa `loki.case-preparation/1`, `mode=replace_payroll_population`,
`preview_id`, `reason`, `request_ref` e `reset_financial_inputs=true`,
no restart autorizado ou seu transporte tipado anunciado. Não é complemento
incremental: exige repor dados/qualificações financeiras e nova revisão.
Prévia não aplica; seleção antiga, valores e aceite não migram por presunção.
Sem esse bloco/rota, preserve a pendência; plugin novo não publica a PR240.

Cancelamento usa `cancellation` do contrato. Quando anunciado,
`loki.case-cancellation/1` pode seguir em `receive_case_data`, com
`expected_snapshot=correction_snapshot` e `human_message` específico.
Releia estado e trilha; cancelamento não exclui registros nem libera a chave
natural para criar outro caso. Automação não recebe autoridade humana.

Para publicação, smoke ou comparação de versões, não baixar o acervo nem
rebaixar todos os documentos. Confira fatos, eventos, decisões e metadados/hashes
pelo conector; integridade dos bytes usa provas do servidor/storage/backup.
Baixe somente o documento necessário à demanda expressa. Metadados não são
bytes lidos; checks de um pacote documental exigem a conferência correspondente.

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

Quando a resposta servida apresentar, `declaracao_do_vinculo_invalida` traz em
`diagnostic.details[*]` o `path` e o código da regra em `type`
(`historical_vacation_...`, `historical_leave_...`,
`historical_coverage_inverted`): corrija conforme a fonte, sem ajustar data
para passar; gozo em que o fim do aquisitivo cai dentro do período é aceito
(DP, 18/11/2026), e o que termina antes dele vai à Rafa. Lote validado
antes da atualização pode recusar `snapshot_desatualizado`: valide de novo e
aplique com o `validation_hash` novo. `leave_history_coverage_not_certified` e
`thirteenth_payment_coverage_not_certified` só saem quando a cobertura vai da
admissão até o corte; com o estado `historical-state-v2`, a que termina depois
do corte também limpa o gap, só até o corte, e uma seleção v1 consumível não
se refaz. Não altere coberturas de casos com seleção histórica feita. Afastamento antigo opaco não recebe `leave`
duplicado. Roteiro em “Recusas de fatos históricos e cobertura até o corte” de
[WORKFLOWS.md](WORKFLOWS.md).

## 13º por etapas

Quando a resposta servida apresentar, o 13º exige `competencia` no dia 1 do
mês do pagamento (`thirteenth_competence_required`); competência divergente de
`data_pagamento` (`thirteenth_competence_mismatch`) pede cancelar e recriar.
A seção pode ir por partes, com `pending_rules` como aviso; a 2ª parcela e o
ajuste leem as parcelas pagas fora do Loki por `historical_payments`
(`ONBFACT-…` de `thirteenth_payment`), sem `casos_anteriores`.
`medias_importadas` exclui a variável mensal; a 1ª parcela dispensa
dependentes, salvo pensão `interdependente`. `thirteenth_stage_duplicated` e
`thirteenth_peer_section_invalid` trazem `related_case_ids`. `final_average` é a
média mensal integral do Domínio e nunca vai proporcional aos avos: o Loki
aplica `média × avos ÷ 12`. 13º em `aguardando_revisao` com média importada
segue a decisão `ajustar`, `calculate_case`, geração e nova conferência; o
reinício usa `restart_case` com `replace_process_inputs`, sem `corrigir_dados`.
Roteiro no domínio `decimo_terceiro`.

## Matrícula no `create_case`

Quando a resposta servida apresentar, omita `funcionario.matricula` por padrão;
`matricula_funcionario_divergente` e `matricula_funcionario_nao_qualificada`
não gravam nada e pedem reenvio sem a matrícula. Se o documento divergir da
registrada, avise a operadora: a correção combinada com ela segue a
restauração ou a troca auditada do código Domínio (domínio
`alteracao_cadastral`), e `registrar_problema` fica para quando não há caminho
automático. Matrícula vazia é recusada. Roteiro no domínio `geral`.

## Onda 2: dossiê da folha, rescisão e cadastro

Quando a resposta servida apresentar: folhas de empresas diferentes rodam em
paralelo, no máximo uma por empresa; o dossiê da folha traz `payroll_context`
por pessoa (`context_hash`, `lancamentos.items` com `lancamento_hash`) para
montar `history_qualifications.payroll_context`; o mapa de rescisão aceita
`add`/`replace` de uma parcela por `loki.company-termination-map-patch/1`.
Nada disso exige Refresh.

Exigem Refresh do conector e conversa nova, todos no domínio
`alteracao_cadastral` e só depois de combinar com a operadora: restauração de
matrícula (`restoration_declaration`), troca de código Domínio
(`motivo: "troca_de_codigo_dominio"`, `message_reference` `CX-…` obrigatória)
e revogação de desligamento gravado pelo onboarding
(`preview_onboarding_termination_revocation`, `revoke_onboarding_termination`,
`revoga_com_rescisao_aberta`; antes do Refresh, pelo transporte
`receive_case_data(case_id="@connector")`). Roteiro em “Cadastro: matrícula,
código Domínio e desligamento do onboarding” de [WORKFLOWS.md](WORKFLOWS.md).

## 2.9.0: método do Domínio na rescisão, reajuste e simulação

Quando a resposta servida apresentar: a política
`arredondamento_proporcionais` da empresa aceita, por opção medida e citada
em `fonte`, `metodo_ferias: valor_dia_6_casas`, `terco: por_parcela`,
`saldo: valor_dia_6_casas` (exige `trinta_fixo`) e `medias_por_bloco: true`;
as médias aceitam `horas_micros`, `valor_micros`, `vantagens_micros` e
`bloco`, só nas férias da rescisão. No reajuste, a linha recusada traz
`folha_bloqueante` e `cliente_config_incompleta` fecha no apply. Na
simulação, `operational_context_changed` traz `subreason`, e
`selection_matches_current_state` aparece também para pessoa. Nada disso
exige Refresh; a operadora só atualiza o plugin. Roteiro em “2.9.0: reajuste,
rescisão, simulação e admissão” de [WORKFLOWS.md](WORKFLOWS.md).

## 2.9.1: regras da DP de 18/11/2026

Quando a resposta servida apresentar: no reajuste, admitido no próprio dia da
data-base com o salário novo fica `sem_reajuste`
(`admitido_na_data_base_com_salario_novo`), o VT não entra na diferença nem
no pago declarado e o salário novo já registrado na data-base é o próprio
reajuste; nas férias antigas do onboarding, gozo em que o fim do aquisitivo
cai dentro do período é aceito, e o lote recusado antes se valida de novo
(`validation_hash` novo); no afastamento, um registro por atestado e
licença-maternidade não é falta; nas médias, o Domínio soma as empresas do
grupo, em férias e no 13º, e `medias_por_bloco` não se liga sem conferência
com a DP; a matrícula do eSocial é o identificador oficial, e matrícula nova
por `identifier_only` só depois de falar com a engenharia. Nada disso exige
Refresh; a operadora só atualiza o plugin. Roteiro em “2.9.1: regras da DP de
18/11/2026” de [WORKFLOWS.md](WORKFLOWS.md).

## 2.9.2: política do mapa de rescisão e fatos do 13º

Quando a resposta servida apresentar: no mapa de rescisão, troca-se só a
política `arredondamento_proporcionais` pelo patch
`loki.company-termination-map-policy-patch/1`, em várias empresas numa
versão, substituindo a política atual inteira, com o
`termination_policy_preview` mostrado à operadora antes do apply e
`medias_por_bloco` desligada sem conferência da DP; no 13º, a recusa
`historical_thirteenth_unqualified_documentary_facts` traz `blocking_facts`,
e o `outro` se qualifica pela cobertura `thirteenth_payments` da mesma ficha,
o que muda o `state_hash` do empregado e desatualiza as seleções dos outros
casos abertos dele. Nada disso exige Refresh; a operadora só atualiza o
plugin. Roteiro em “2.9.2: política do mapa de rescisão e fatos do 13º” de
[WORKFLOWS.md](WORKFLOWS.md).

## Nova preparação de afastamento

Consulte `get_process_contract("afastamento")`. Quando o contrato anunciar
`preparation.supported=true`, a pessoa autorizada pode usar
`replace_process_inputs` pelo transporte `loki.case-preparation-transport/1`
em `receive_case_data`, com `correction_snapshot`, mensagem humana e referência
idempotente. Exige `operar_casos`, `decidir_chat` e `corrigir_dados`; automação não recebe
essas capacidades humanas. Siga o schema anunciado, sem inventar parâmetros.

A nova preparação conserva caso, empresa, funcionário, CPF/CNPJ, admissão e
referência da ocorrência; arquiva os fatos anteriores e exige nova recepção
completa de categoria, início, períodos e retorno coerentes. Releia o recibo,
os fatos recebidos e a nova revisão. Não reenvie o payload antigo sem conferir
suas âncoras e os parâmetros corretos. Histórico e decisões permanecem.

Aprovação ou efeito aplicado impedem essa recuperação até a conciliação própria;
não use restart para reescrever um episódio efetivo. O corretor genérico
`submit_operator_correction` mantém
a recusa `correcao nao pode alterar identidade ou escopo do caso` para
`leave.categoria`. Essa recusa não impede a nova preparação quando o contrato
a oferecer. Sem o suporte anunciado, conserve a pendência do caminho e sua
reprodução; o plugin não publica a capacidade nem altera a conta do operador.

Quando a resposta servida apresentar, a recusa de dados de afastamento traz em
`errors` o campo exato (ex.: `leave.retorno`) e um código de regra:
`afastamento_inicio_antes_da_admissao`,
`afastamento_inicio_diverge_do_primeiro_periodo`,
`afastamento_periodos_descontinuos`, `afastamento_fonte_de_retorno_sem_data`,
`afastamento_retorno_fora_da_vespera` (retorno = dia seguinte ao fim do último
período) ou `afastamento_periodo_invertido`. Corrija só o campo apontado,
conferindo com o original, e reenvie com novo `request_ref` e o snapshot atual.
Reenviar o mesmo dado sem corrigir, com ou sem `field_sources`, vai ser recusado
de novo. Se o documento realmente traz essas datas, não force o valor: registre
a dúvida com a DP antes de reenviar.

Numa preparação corrente, quando a resposta servida apresentar,
`leave_preparation_requires_complete_input` traz `errors` por campo (ex.:
`{"field": "leave.retorno", "reason": "afastamento_retorno_fora_da_vespera"}`,
`leave.periodos[*].fim`), com código de regra, `missing` ou `extra_forbidden`.
Corrija o campo e reenvie a seção `leave` completa; fonte vai em
`retorno_source`/`identity_source`, nunca numa chave própria dentro de `leave`.

## Reajuste coletivo com efeito retroativo

Somente quando `get_process_contract("reajuste_salarial")` servir
`loki.salary-adjustment/1`, siga [REAJUSTE_SALARIAL.md](REAJUSTE_SALARIAL.md).
Não há ferramenta nova: prévia (`loki.salary-adjustment-preview/1`), exclusão
(`loki.salary-adjustment-exclusion/1`) e reabertura
(`loki.salary-adjustment-reopen/1`) são transportes de `receive_case_data`.
A conta precisa de `reajuste_salarial` e `alteracao_cadastral` na mesma
empresa, com `consultar`, `decidir_chat` e `corrigir_dados` em
`alteracao_cadastral` (`salary_adjustment_requires_employee_change_scope`).
A harness lê e confere o instrumento e monta a população; o Loki só valida a
coerência interna e nunca confere a fonte. Mês sem folha do Loki pede o pago
declarado com `sem_outras_verbas_dependentes_do_salario`. Regras da DP de
17/11/2026: reajuste por competência, ano anterior sem RRA, desligados fora
por padrão (`excluidas_automaticamente`), admitidos depois da data-base pelo
`salario_base_anterior_cents`, sem reajuste proporcional
(`reajuste_proporcional_nao_praticado`) e arredondamento meio centavo para
cima. Salário novo já registrado no cadastro vira a ressalva
`salario_novo_ja_registrado_no_cadastro`. Regras da DP de 18/11/2026:
admitido no próprio dia da data-base fica `sem_reajuste`, o VT não entra na
diferença e o salário novo já registrado na data-base é o próprio reajuste.
A rescisão complementar dos desligados abrangidos e o admitido no mesmo mês,
antes do dia da data-base, ficam pendentes até a DP decidir.

## Consignado: contrato, competência e rescisão

Para a consulta automática mensal, siga
[DATAPREV_MENSAL.md](DATAPREV_MENSAL.md), somente quando o contrato servido
anunciar `loki.dataprev-monthly/1`. Consulta completa exige aplicação separada;
retomada usa a referência durável original antes de repetir comandos.

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

## Adicionais por pessoa e cargo

Consulte o contrato de parâmetros e o cadastro empresarial vigente.
`insalubridade_regra` e `periculosidade_regra` são escolhas individuais
explícitas, com `recebe`, vigência, rubrica e operandos do schema; ausência não
é `recebe=false`. Regra individual qualificada prevalece sobre política por cargo.

`additional_policies` só atribui por cargo quando houver política explícita
com CNPJ, estabelecimento, cargos, período e população de admissões.
`inherit_future_hires` exige escolha e corte de admissão explícitos;
o nome do cargo isolado não cria direito. Sobreposição, cargo/unidade desconhecidos
e vigência parcial conservam pendência/necessidade de segmentação.

Elegibilidade difere de valoração: base, percentual, divisor, quantidade e
incidências dependem do mapa/regra qualificados; não invente fórmula universal.
Aplique cadastro somente por `validate_client_config`/`apply_client_config`
autorizados, com CAS e releitura. Parâmetros individuais seguem onboarding próprio.
Fonte informal atribuída pode ser aceita; confira consumo na memória por pessoa.

## Saldo de salário na rescisão

Quando o calculador servido oferecer o alcance qualificado, admissão e
rescisão no mesmo mês civil de 30 dias, com divisor 30 e sem afastamento
sobreposto, usam o intervalo contratual inclusivo das datas
reais de admissão e desligamento. É uma inferência técnica documentada das
fontes aplicáveis e da semântica temporal, não medição histórica nem regra
universal de calendário. A harness informa fatos; os dias e centavos são derivados
pelo motor, sem entrada livre para coincidir com a referência.

O consumidor `rescisao-v42` estende o alcance ao mesmo mês civil de 31 dias,
com divisor 30, desligamento até o dia 30 e sem afastamento sobreposto. Mês30
e contratos anteriores permanecem no alcance próprio. Releia dias, seleção e
memória. Não adapte a data ou o divisor para coincidir com o comparador.

Mês comercial (divisor 30, `trinta_fixo`), quando a resposta servida o
apresentar (`rescisao-v43`/`rescisao-v44`): os dias do saldo são calculados
pelo Loki; não informe dias nem troque o divisor. Desligamento em fevereiro ou
no dia 31 agora calcula; mês inteiro trabalhado conta 30 dias; admissão no mesmo
mês conta os dias corridos desde a admissão, incluindo atestado pago pela
empresa. Continuam `regra_nao_medida:saldo_admissao_no_mes` até a DP responder:
admissão no mês (depois do dia 1) com saída no dia 31 ou no último dia de
fevereiro; afastamento pelo INSS ou licença-maternidade no mês da saída; empresa
com divisor pelo calendário. Nesses casos não altere datas nem divisor;
registre a dúvida com a DP. Cálculo novo exige gerar o pacote de novo e nova
revisão; versões congeladas antigas desses cenários passam a exigir nova versão.
Atualização de instruções não corrige o calculador publicado nem certifica o
caso completo.
Confira versão do motor, dias, memória e bases; não reutilize memorial parcial
antigo ou aceite anterior como resultado da regra nova. Parcelas independentes
permanecem disponíveis conforme o contrato, sem preencher ausência com zero.

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
para diagnóstico, sem inventar flags ou ignorar histórico parcial. A orientação
não autoriza corrigir fatos ou reaplicar casos automaticamente. Publicação e
reteste real exigem provas próprias.

Segunda ocorrência de férias da mesma pessoa funciona em outra competência:
envie sempre `competencia` igual ao mês de início do gozo. No `create_case`,
`created: false` significa que o caso devolvido é o existente, não o novo: não
continue nele. Duas frações na mesma competência ainda não têm suporte. Nunca
cancele o primeiro caso para abrir o segundo.

Quando a resposta servida apresentar, a recusa de dados de férias traz em
`errors` o campo exato (ex.: `dados_ferias.data_aviso`) e um código de regra:
`ferias_aquisitivo_29_fevereiro_exige_qualificacao`,
`ferias_aquisitivo_incompleto`, `ferias_gozo_duracao_invalida`,
`ferias_gozo_antes_do_fim_do_aquisitivo`, `ferias_gozo_fora_do_concessivo`,
`ferias_aviso_fora_do_prazo`, `ferias_pagamento_fora_do_prazo`,
`ferias_abono_pedido_incoerente`, `ferias_pedido_abono_fora_do_prazo`,
`ferias_inicio_antes_de_feriado`,
`ferias_inicio_antes_de_feriado_source_sem_uso`,
`ferias_inicio_antes_de_feriado_source_sem_fundamento`,
`ferias_inicio_antes_de_repouso`,
`ferias_inicio_antes_de_repouso_source_sem_uso`,
`ferias_inicio_antes_de_repouso_source_sem_fundamento`,
`ferias_medias_alternativas_exclusivas`, `ferias_media_repetida` ou
`ferias_media_competencias_invalidas`. Corrija só o campo apontado, conferindo
com o original, e reenvie com novo `request_ref` e o snapshot atual. Reenviar o
mesmo dado sem corrigir, com ou sem `field_sources`, vai ser recusado de novo.
Se o documento realmente traz essas datas, não force o valor: registre a dúvida
com a DP antes de reenviar.



Numa preparação corrente, quando a resposta servida apresentar,
`vacation_preparation_requires_complete_input` traz `errors` por campo (ex.:
`{"field": "dados_ferias.data_aviso", "reason": "ferias_aviso_fora_do_prazo"}`),
com código de regra, `missing` ou `extra_forbidden` (chave fora do schema, como
`dados_ferias.*`). Corrija o campo e reenvie a seção `dados_ferias` completa;
fonte vai nos campos `*_source` do schema, nunca numa chave própria dentro de
`dados_ferias`.

Quando a resposta servida e o schema apresentarem,
`ferias_inicio_antes_de_repouso_ou_feriado` não é mais emitido.
`ferias_inicio_antes_de_repouso` recusa sem a declaração do DP: a
DP da Izzi aceita o início antes da folga semanal quando o cliente pede,
porque não acompanha a escala praticada. A declaração vai em
`dados_ferias.inicio_antes_de_repouso_source`, com o pedido do cliente como
fonte: documento anexado, manifesto de harness ou declaração
(`kind: "declaration"`, `reference`, `locator`) com `foundation` dizendo quem
pediu e onde. Inferência e contexto são recusados
(`ferias_inicio_antes_de_repouso_source_sem_fundamento`); fonte sem início na
janela do repouso recusa com `ferias_inicio_antes_de_repouso_source_sem_uso`.
A exceção não muda valores: aparece em `ressalvas.declaracoes_dp` e numa
linha "Declaração do DP" do aviso e do recibo, e só vale com o aceite
explícito das ressalvas na revisão. Num caso existente, mudar o repouso e
acrescentar a declaração é uma única correção (`submit_operator_correction`
com as duas folhas juntas em `changes`).

Quando a resposta servida e o schema apresentarem,
`ferias_inicio_antes_de_feriado` recusa sem a decisão do cliente. Regra da DP
da Izzi: a decisão é sempre do cliente; o DP informa o passivo e, se o
cliente decidir, é feito. A decisão vai em
`dados_ferias.inicio_antes_de_feriado_source`, com a decisão do cliente como
fonte: documento anexado, manifesto de harness ou declaração com
`foundation`. O conteúdo da `foundation` (quem decidiu, onde e que o passivo
foi informado) é responsabilidade da harness e da operadora; o Loki só exige
`foundation` não vazia e não confere a fonte. Inferência e contexto são
recusados (`ferias_inicio_antes_de_feriado_source_sem_fundamento`); fonte sem
início na janela do feriado recusa com
`ferias_inicio_antes_de_feriado_source_sem_uso`. Quando o início cai antes de
feriado e antes do repouso, as duas fontes são exigidas e cada uma libera só
a sua regra. A exceção não muda valores: aparece como ressalva
`clt_134_3_vespera_feriado` em `ressalvas.declaracoes_dp` (`confirmed: false`,
`exige_aceite_humano: true`), dizendo que a decisão foi do cliente, que o
passivo foi informado e que a ressalva não afasta o passivo, e numa linha
"Declaração do DP" do aviso e do recibo; só vale com o aceite explícito das
ressalvas na revisão. Num caso existente, mudar os feriados e acrescentar a
decisão é uma única correção (`submit_operator_correction` com as folhas
juntas em `changes`).

Depois do deploy, recibos de componentes de férias e de rescisão e
consolidações de médias emitidos antes ficam obsoletos de novo, inclusive os
emitidos depois da 2.6.11 (`OBSOLETO` em `get_case`;
`medias_rescisao_obsoletas` no recálculo da rescisão). A recuperação é nova
qualificação, nova consolidação, novo cálculo, depois geração, conferência e
revisão. A descrição da ressalva do repouso mudou: revisões já preparadas com
ela precisam ser preparadas de novo. Casos aprovados ou entregues não mudam.

## Política contextual do FGTS mensal

Quando o consumidor oferecer `folha-v29`, o mapa selecionado pode declarar
`fgts_mensal` com `policy_version=loki.fgts-mensal/1`, método, fonte e
`escopo=trabalhador_competencia_mensal_8pct`. Confira empresa, competência e
vigência do mapa efetivamente selecionado. Política ausente conserva o cálculo
legado; política ausente não comprova configuração ou validação do critério.
A memória `calculo_fgts` por empregado distingue método, fonte, pin, base,
valor da fórmula e valor final; uma base pendente não vira zero.

Confronte a memória com persistência, materialização, documentos e soma dos
encargos individuais. Apuração sobre base agrupada e FGTS rescisório têm
contratos próprios. Disponibilidade da política não autoriza alterar configuração
real, corrigir valores, aprovar casos ou transmitir. Uma diferença relatada de
centavo só é conferida com os operandos e a referência daquele cálculo.

Lote de políticas de mapa: quando `get_client_config` anunciar
`payroll_map_policy_patch_transport`, o envelope
`loki.company-payroll-map-policy-patch/1` (`validate_client_config` →
`apply_client_config`, argumento `alteracoes`) aplica `fgts_mensal` e, se
`payroll_map_policy_patch_transport.policies.arredondamento_monetario.accepted`
aparecer, `arredondamento_monetario` (`verbas` do `rounding_context`, `metodo`
`half_up`/`half_even`/`exigir_qualificacao`, `fonte` obrigatória) a todos os
mapas selecionados, sem reenviar `mapa` nem `mappings`, com seletores exatos e
`expected_hash` atual. Uma única versão; verba ausente ou sem fórmula
`remuneracao_periodo` recusa o lote inteiro. Método é decisão humana/DP.
Roteiro completo no domínio `geral`.
