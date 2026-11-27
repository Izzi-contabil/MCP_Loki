# Folha mensal

Este domínio complementa o `geral`, que continua com a prontidão, a retomada, a
população da folha e o diagnóstico do job bloqueado no cálculo. Antes de
operar, consulte `meu_acesso`, `get_dp_capabilities` e
`get_process_contract("folha_mensal")`; envie `dados_folha` pelo escritor
anunciado. Os códigos e campos abaixo valem somente quando a resposta servida
os apresentar.

## Motor folha-v33: recalcular as folhas não entregues

> **Atenção.** Quando o cálculo da folha mostrar o motor `folha-v33` (ou
> `folha-v33-historical-vacation-v1`): **todas as folhas mensais não entregues
> ficam desatualizadas**, inclusive as recalculadas na `folha-v32`. Cada uma
> precisa ser recalculada, conferida de novo e receber novo aceite antes da
> entrega, pelo mesmo procedimento da seção da `folha-v32` abaixo. As folhas
> já entregues não mudam. Nada é recalculado ou decidido automaticamente.

Sem `folha-v33` no cálculo, siga as seções da `folha-v32` como estão. As
diferenças do recálculo vêm das regras abaixo; mostre-as à operadora.

**VT do admitido no mês (v33).** Com admissão depois do dia 1, o percentual da
regra individual incide sobre a **linha de salário calculada do mês** (o
período remunerável enviado), não mais sobre o salário × `(30 − dia + 1)/30`.
São linhas de salário: `remuneracao_periodo` sem fator,
`salario_base_proporcional`, membros de partição e, para horista,
`salario_horario` com fator 1.

- Admissão no dia 1 é mês cheio: vale a fórmula da v32. Faltas ou 31 dias
  enviados não mudam o VT.
- Envie em `periodo_remuneravel` o período da fonte; ele não pode passar dos
  dias de contrato: o maior entre os dias corridos desde a admissão e
  `30 − dia + 1` (admissão em 02/02 dá 29, em 20/02 dá 11). A base também
  nunca passa do salário cheio. Acima disso, o VT fica em
  `vale_transporte_salario_do_mes_acima_do_contrato` (campo
  `periodo_remuneravel`, próxima ação `confirmar_periodo_remuneravel_enviado`):
  confira o período enviado com a fonte; não o reduza para destravar.
- Linha de salário pendente deixa o VT pendente pela mesma causa. Sem linha
  de salário identificável no mapa (salário em `salario_base` cheio ou em
  valor informado), o VT fica em
  `vale_transporte_salario_do_mes_nao_identificado` (campo `folha_rubricas`,
  próxima ação
  `qualificar_rubrica_do_salario_do_mes_no_mapa_ou_declarar_desconto_pela_dp`).
  A saída normal é qualificar a rubrica de salário no mapa
  (`salario_base_proporcional` ou `remuneracao_periodo`). Se não for possível,
  com a decisão da DP, declare o desconto com `submit_operator_correction`,
  `target: "calculation"`, no caminho
  `funcionarios.<matricula>.verbas.<rubrica de VT>.0.valor_cents` (o caminho
  exato vem em `operator_corrections` do cálculo). O limite informativo
  mostra a regra antiga. Um mapa com salário em `salario_base` cheio que
  calculava na v32 passa a ficar pendente.
- A concessão segue os três ramos da v32, lidos pelo mês comercial: num mês
  de 31 dias, a concessão 25/30 continua ambígua. Vigência parcial e
  desligamento no mês: sem mudança.
- Em `fontes_insumos` da linha de VT, `base_percentual`
  (`linha_de_salario_do_mes` ou `desconto_declarado_pelo_operador`),
  `linhas_de_salario` e `salario_do_mes_cents` mostram a base: apresente-os à
  operadora.

**Salário-família do admitido (v33).** Regra da DP: as faltas não reduzem a
cota. No mês de admissão, a cota é proporcional aos dias de vínculo desde a
admissão, na base de dias da linha de salário do mapa:

- linha por mês civil (divisor igual aos dias do mês): dias desde a admissão
  sobre os dias do mês. Admissão no dia 7 de um mês de 31 dias dá 25/31,
  mesmo com faltas no período enviado;
- linha comercial (divisor 30) ou sem linha do período: `30 − dia + 1`, como
  na v32.

O período enviado não muda a cota. Se o Domínio divergir, registre como
divergência a confirmar, não como defeito.

**Férias calculadas pelo Loki no contexto do mês.** Para o mês de gozo ou de
pagamento, envie em `funcionarios[].ferias` o efeito do caso de férias do
Loki, com o `case_id` e o `result_hash` do cálculo corrente dele. O Loki lê do
próprio caso o gozo, o efeito e o pagamento; não anexe documento para isso. O
caso precisa ser da mesma empresa e do mesmo vínculo, estar calculado e em
`aguardando_revisao`, `aprovado` ou `publicado`. Pagamento observado e
declarado em `pagamentos_ferias` prevalece; sem ele, conta a `data_pagamento`
do caso até o fim do mês, e `vacation_loki_payments[].payment_basis` diz a
evidência: `entrega_registrada`, `caso_publicado` ou
`data_pagamento_programada`. Recusas:

- `loki_vacation_case_not_found`: outro vínculo, outra empresa ou caso que
  não é de férias;
- `loki_vacation_case_cancelled` e `loki_vacation_case_state_unsupported`:
  o caso não pode alimentar a folha nesse estado;
- `loki_vacation_result_hash_incompatible`: as férias foram recalculadas; use
  o hash novo;
- `confirmed_vacation_calculation_stale`: o caso de férias não tem cálculo
  corrente; recalcule as férias antes;
- `vacation_effect_differs_from_loki_calculation`: copie o efeito exatamente
  como o Loki calculou;
- `loki_vacation_effect_reference_invalid`: falta `case_id` ou `result_hash`.

Gozo no mês inteiro do vínculo dá também o período zero. Gozo parcial
continua pedindo `periodos`, contados na mesma base de dias da linha de
salário do mapa.

**Afastamento do INSS no mês inteiro.** Um afastamento já qualificado
(categoria, política e responsabilidade de cada período), com INSS o mês
inteiro e iniciado antes da competência, qualifica sozinho o mês como
`sem_remuneracao_empregador`, com período zero. Não anexe documento nem
declare `mes_sem_remuneracao` para esse mês, e não envie lançamentos nele
(`payroll_launches_in_inss_full_month`). Continua como antes: o mês em que o
afastamento começa (a cota do mês é da empresa), o mês com retorno ou com
dias do empregador, o acidentário, a maternidade, `outro_comprovado`,
afastamento não qualificado, admissão ou desligamento no mês e afastamento de
caso cancelado ou rejeitado.

**Dossiê da folha.** `missing_fields` lista todas as causas do contexto do
mês, e `context_fields` (com `context_fields_complete`) diz quais campos de
entrada faltam, por exemplo `ferias`, `pagamentos_ferias` ou `periodos`.
Quando a issue trouxer `retroactive_actions`, `missing_fields` também lista
as pendências da diferença retroativa do reajuste (`diferenca_*`,
`politica_diferenca_retroativa_ausente`, `instrumento_reajuste_divergente`),
que não tornam `context_fields_complete` falso. A ação de cada código e o
detalhe por regra (`retroactive_detail`) estão no domínio `reajuste_salarial`,
"Pendências da diferença no dossiê da folha".
Motivos dos lançamentos não lidos:

- `payroll_case_workflow_running`: o job do caso está na fila ou rodando;
  aguarde o fim;
- `payroll_effective_launches_case_not_in_preparation`: o caso saiu da
  preparação (em revisão); use `restart_case` se precisar qualificar o
  contexto;
- `payroll_effective_launches_case_being_written`: outro processo grava o
  caso; tente de novo.

**Pensão alimentícia do admitido.** No mês de admissão, o contrato começa na
admissão: declare a `pensao_alimenticia_regra` (ou "não beneficiário") com
`vigente_desde` na data de admissão, ou antes, e sem fim no mês; assim o mês
não fica pendente. Regra iniciada depois da admissão ou encerrada no mês, mês
de transferência e mês sem admissão continuam em
`pensao_vigencia_parcial_exige_regra`, que agora aponta os campos
`pensao_alimenticia_regra.vigente_desde` e `pensao_alimenticia_regra.vigente_ate`:
corrija o que a fonte mostrar. Em empresa cujo mapa tem a rubrica de pensão, todo vínculo precisa da
declaração; a ausência não vale como não beneficiário
(`pensao_regra_individual_pendente`).

**Crédito do Trabalhador.** Em
`credito_trabalhador_competencia.descontos_compulsorios_sem_incidencia`, liste
só descontos sem incidência de INSS do mapa, pelo nome Loki ou pelo código do
Domínio da rubrica. Não liste proventos (gorjeta estimada, adicional noturno e
reflexos), o VT (é opção do empregado, não é compulsório), o próprio crédito
nem INSS/IRRF. Desconto da lista sem linha no mês vale zero para aquele
vínculo. Recusas: `credito_trabalhador_compulsorio_nao_identificado` (próxima
ação `listar_somente_descontos_sem_incidencia_do_mapa`; o item está em
`verbas`: corrija a lista) e `credito_trabalhador_tributos_do_mes_pendentes`
(resolva antes a pendência de INSS/IRRF do mês). A consulta Dataprev não é
exigida para a lista.

## Correções calculadas atravessam o reinício da folha

Vale quando a resposta do `restart_case` trouxer `corrections_carried`. Sem
isso, as correções calculadas se perdem no reinício e precisam de nova
declaração da DP, como antes.

Ao reiniciar uma folha mensal com `restart_case` e
`preparation.mode=replace_process_inputs`, as correções de valor calculado já
declaradas pela DP (`submit_operator_correction`, `target=calculation`)
continuam no caso. A resposta (e o replay idempotente) traz:

- `corrections_carried`: correções levadas para o recálculo, com
  `correction_id`, `path`, `declared` e o status
  `reaplicada_no_proximo_calculo_se_caminho_e_natureza_iguais`. Não repita
  essas correções e não peça à identidade técnica para refazê-las;
- `corrections_not_carried`: correções que ficaram de fora já no reinício,
  com o motivo: `funcionario_fora_da_populacao`,
  `populacao_substituida_no_reinicio` (modo `replace_payroll_population`:
  nada é levado), `caminho_posicional_de_verba` (verba calculada
  `verbas.<verba>.<índice>`), `pendencia_indeterminada_no_reinicio` ou
  `processo_sem_reaplicacao_automatica` (outro processo que não a folha).

O recálculo só reaplica a correção sobre o mesmo valor que a DP viu: a mesma
pessoa, o mesmo número calculado ou a mesma pendência com os mesmos operandos
(no salário-família, a mesma quantidade de filhos; no VT do admitido, o mesmo
salário, proporção e custo). Depois do reenvio e do recálculo, confira
`operator_corrections` na memória do cálculo corrente: `carried` lista o que
foi reaplicado; `not_carried` lista o que não foi, com o motivo
`valor_calculado_mudou`, `pendencia_mudou`, `valor_calculado_mudou_de_natureza`,
`caminho_inexistente_no_calculo` ou `funcionario_fora_da_populacao`.

Correção declarada antes do registro de operandos (legado) só é levada quando
o cadastro do cálculo corrente é o mesmo do cálculo da declaração; senão, e
sempre no VT legado, fica `pendencia_indeterminada_no_reinicio`. Uma correção
declarada na v31 sobre a pendência antiga do salário-família do admitido
continua prevalecendo sem reinício; depois de um reinício, ela não volta se o
motor calcular a cota e aparece em `operator_corrections.not_carried` ou, se o
cadastro mudou, em `corrections_not_carried`
(`pendencia_indeterminada_no_reinicio`).

Na revisão, cada item de `ressalvas.correcoes_humanas` traz
`estado_no_calculo_corrente`, com `estado` e `caminhos` (estado por caminho):
`aplicada`, `levada_do_reinicio` (com o `preparation_id`; sem cálculo
corrente, `reaplicacao: aguardando_calculo_corrente`), `nao_levada` (com o
`motivo`), `aposentada` (`preparacao_anterior` ou
`substituida_por_correcao_posterior`) ou `parcial`, quando os caminhos
divergem. Mostre esse estado à operadora na conferência.

Não há descarte: uma correção levada só é trocada por nova correção humana no
mesmo caminho, que prevalece. Uma correção não levada só volta com nova
declaração da DP; manter o valor do motor ou declarar de novo é decisão dela.

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

- **Abertas** (`aberto`, `em_preparacao`): recalcule pelo mesmo fluxo da folha
  (`enqueue_case_workflow`, uma folha por empresa na fila), com
  `input_snapshot` e `expected_snapshot` atuais e novo `request_ref`, gere o
  pacote corrente e confira de novo.
- **Em revisão** (`aguardando_revisao`): o cálculo não aceita escrita nesse
  estado; tirar o caso da fila de revisão é ato humano. O caminho é
  `restart_case` **simples** (sem `preparation`), com
  `expected_snapshot=get_case.correction_snapshot` e `human_message`, pela
  conta pessoal da operadora; depois `enqueue_case_workflow` com o
  `input_snapshot` e o `expected_snapshot` novos e novo `request_ref`; depois
  o pacote corrente, a conferência e o novo aceite. O reinício simples não
  reenvia os insumos (o `preparation` com `replace_process_inputs` arquiva-os e
  exige reenviar tudo; não o use só para trocar o motor). A rotina com a capacidade
  `atualizar_por_insumo_do_cliente` (2.10.0; a Ana concede por empresa, só pela
  autorização: `preparar_autorizacao` ou o acréscimo `prepare_authorization_addition`) faz o `restart_case` simples (sem `preparation`, com
  `human_message`) e depois o `enqueue_case_workflow` com os snapshots novos;
  sem a capacidade, ela para e avisa a Ana. O aceite continua humano e a
  capacidade não abre cancelamento nem `preparation` na folha. Não há reinício em lote:
  `restart_case` não está no `execute_operational_batch`; são uma chamada por
  caso e um enqueue por empresa. Só a proprietária abre a exceção, por correção
  `CL-N` e lista fechada de casos (seção da 2.13.0 abaixo). Enquanto o servidor aceitava o enqueue em
  revisão, o job nascia e terminava em `job_preparation_failed`. Com a
  correção do backend (#410, mesclada), o
  enqueue recusa na hora, sem criar job, com `case_in_review_requires_restart`
  e `next_action=restart_case`; ao ver esse código, faça o reinício simples
  acima. Não tente contornar com novo `request_ref`, cancelamento ou outro
  caso.
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
  Com `folha-v33`, a contagem segue a base de dias da linha de salário
  ("Salário-família do admitido (v33)", acima).

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
  no mês inteiro, declare `mes_sem_remuneracao` (com `folha-v33`, o INSS já
  qualificado e iniciado antes da competência qualifica o mês sozinho); se forem faltas ou suspensão,
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
Com `folha-v33` no cálculo, a base e a saída sem linha de salário mudam
("VT do admitido no mês (v33)", acima).

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

## Folha pelo mês civil: `folha_divisor_mes` (backend #405)

Vale quando o contrato de onboarding servido mostrar
`payroll_rules.month_divisor` e o schema do cadastro apresentar
`empresas[].folha_divisor_mes`. Por padrão a folha divide por 30 (CLT, art.
64). O mês civil (28, 29, 30 ou 31) é convenção da empresa ou da norma
coletiva: só entra por pedido do cliente ou decisão da DP, **com a fonte**
(CX-…), por empresa. Não ative por conta própria nem estenda a outra empresa
do grupo. Sem a política, nada muda: mapa, resultado e hashes são os de antes.

**O que muda sob a política** (marca `-divisor-mes-v1` no motor, só na
vigência):

- Toda linha em dias com divisor 30 passa a dividir pelos dias do mês:
  `remuneracao_periodo` (com ou sem fator), `salario_base_proporcional`,
  `base_composta_proporcional` em dias e `salario_minimo_proporcional`, como
  provento ou desconto. Também as partições de remuneração e as compensações
  com teto 30.
- VT e salário-família do admitido: dias de vínculo sobre os dias do mês
  (admissão em 07/10: 25/31). Faltas e DSR das faltas: no mesmo divisor do
  salário, limitados ao salário do período; se passarem, a folha fica
  pendente (`desconto_de_faltas_acima_do_salario`), em vez de cortar.
- **O que não muda:** `valor_explicito`, linhas em horas (`salario_horario`,
  divisor 220 ou outro explícito) e `base_composta_razao_quantidades`.
- **Falta sempre pela rubrica de falta**, nunca embutida no período: falta
  embutida não é detectável (28 dias com 2 faltas em fevereiro). Envie o
  período pelos dias de vínculo do mês (31 em outubro, mês cheio) e a ausência
  real na rubrica de falta, não um período reduzido a 30.

**Como ligar**, num único `validate_client_config` seguido de
`apply_client_config`, por empresa, com a mesma fonte nos três campos:

```json
{
  "empresas[<codigo>].folha_divisor_mes": [
    {"id": "folha-calendario-1", "valid_from": "AAAA-MM-01", "divisor": "calendario",
     "fonte": {"kind": "external_reference", "reference": "CX-…"}}
  ],
  "empresas[<codigo>].ferias_recibo": [
    {"id": "ferias-civil-1", "valid_from": "AAAA-MM-01", "divisor_dias": "dias_mes_civil",
     "fonte": {"kind": "external_reference", "reference": "CX-…"}}
  ],
  "empresas[<codigo>].convencoes.dias_do_mes": "calendario"
}
```

- `valid_from` no dia 1 de um mês, **depois da última folha fechada** da
  empresa; `valid_until`, se houver, no último dia de um mês. Vigências
  sobrepostas ou ids repetidos recusam. Valor já existente exige
  `sobrescrever=true`.
- O recibo de férias civil tem de cobrir toda a vigência; as bases não se
  misturam (20 dias a /30 e 11 a /31 pagariam cerca de 102% das férias). Sem
  `convencoes.dias_do_mes: calendario` (da empresa ou do cliente), o saldo da
  rescisão sairia /30 e a folha /31.

**Recusas e pendências:**

- Cadastro: `folha_divisor_mes_retroativo` (mudança que altera a política em
  mês até a última folha fechada; declare no mês seguinte),
  `folha_divisor_mes_exige_ferias_recibo_mes_civil`,
  `folha_divisor_mes_ferias_recibo_divisor_30_vigente` e
  `folha_divisor_mes_exige_convencao_dias_do_mes_calendario`.
- Mapa ambíguo: sob a política, mapa sem `remuneracao_periodo` (sem fator) e
  com duas ou mais linhas provento `salario_base_proporcional` em dias, fora
  de partição, é recusado ("mapa ambiguo"). O mapa precisa de uma única linha
  de salário por dias, ou da partição, ou de uma `remuneracao_periodo` sem
  fator: o salário e o feriado declarados no mesmo tipo (veja "Fórmulas do
  mapa") ficam ambíguos. Acerte o mapa antes de ligar a política.
- Folha: `periodo_remuneravel_diverge_do_vinculo` (período diferente dos dias
  de vínculo no mês menos as férias; o detalhe traz esperado e recebido: reenvie
  o período e lance a ausência pela falta), `ferias_calculadas_a_30_sob_a_politica`
  (efeito de férias calculado com o recibo /30: recalcule as férias com o recibo
  civil), `ferias_cruzam_o_inicio_da_politica`, `quantidade_dias_acima_do_mes`,
  `particao_periodo_acima_do_mes` e `desconto_de_faltas_acima_do_salario`.
  Nenhuma é resolvida por ajustar número para passar. Folha em revisão que
  precise recalcular segue "Em revisão", na seção da `folha-v32`.

## Fórmulas do mapa: o que existe hoje e os limites

São escolhas do mapa de rubricas da empresa (política do mapa, lote de
políticas). O Loki valida a coerência da fórmula declarada; não infere a
verba.

- **Dobro de feriado e domingo trabalhados sem folga** (Lei 605/1949, art.
  9º; backend #414): `salario_base_proporcional` aceita `fator` **1 ou 2**
  (outro valor recusa com `formula_day_factor_invalid`). Declare a verba como
  `salario_base_proporcional`, unidade em dias, divisor 30, `fator: "2"`, e o
  cliente lança os **dias** trabalhados. O valor é salário ÷ 30 × dias × 2,
  sobre o salário contratual. Membro de partição e `afastamento_empregador` não
  aceitam fator. Sob `folha_divisor_mes`, a linha com fator não é linha de
  salário do período: o mapa precisa de outra linha de salário do período, sem
  fator (`MapaFolhaInvalido`). Essa linha pode contar na base do VT e na cota
  do salário-família do admitido; avise a operadora na conferência. **Não**
  use `base_composta_proporcional` com `fator: "2"` e a linha de salário em
  `rubricas_base`: a base é o valor da linha **já calculado no mês**, e com
  admissão, férias ou afastamento no mês o dobro sai menor.
- **Divisor por linha sob `folha_divisor_mes`**
  (`formula.divisor_sob_calendario: "30" | "dias_do_mes"`, #414). A medição da
  DP (CX-D0D4F1EF) mostrou que o divisor depende da verba. Com `"30"`, a linha
  fica ÷30 mesmo com a política (faltas e DSR de faltas no Abençoado; feriado
  em dobro onde o Domínio mede ÷30); sem o campo ou com `"dias_do_mes"`, segue
  os dias do mês; **fora da política o campo não tem efeito**. Recusas: `"30"`
  na linha de salário do período, em `remuneracao_periodo`, em membro de
  partição e em `afastamento_empregador`; e mudança retroativa do campo ou do
  `fator` até a última folha fechada (`folha_divisor_mes_retroativo`; vale a
  partir do mês seguinte).
- **Base da hora com outras verbas** (Súmulas 264 e 132 do TST):
  `salario_horario` não aceita `rubricas_base`. Quem soma verbas é
  `base_composta_proporcional`, com `unidade_quantidade: horas`, `divisor`
  literal e `rubricas_base` (por exemplo, salário e periculosidade). Limites:
  o divisor é **literal no mapa** (220 para todos), não o divisor individual
  da pessoa; e a base é o **valor do mês** das linhas citadas, não o do mês
  cheio. Num mês com admissão, férias ou afastamento a hora sai menor que a das
  súmulas. Serve a quem tem jornada única e mês cheio; fora disso, não declare
  e registre a limitação.
- **Percentual individual por pessoa** (quinquênio, 5/10/15%): **ainda não
  existe**. O `parametro_individual` aceita só insalubridade, periculosidade,
  pensão alimentícia e vale-transporte, e o cadastro não tem percentual por
  tempo de serviço. Lance o valor calculado em `valor_explicito`, que o Loki
  não valida; declare a limitação na conferência. Não use a unidade
  `percentual` em `base_composta_proporcional`: não tem uso nem prova.

## Fila durável: um job pendente por empresa

0. **Worker de folha sem concessão por empresa.** O worker não precisa de
   concessão na empresa da folha e ninguém o inclui nela (domínio `geral`,
   "Empresa nova e onboarding pela rotina"). Não use
   `prepare_authorization_addition` nem `preparar_autorizacao` para o worker.
   `worker_not_authorized` (com ou sem `reason:
   "worker_company_grant_missing"`, este de servidor anterior) e
   `worker_service_not_authorized` não gravam job e não são da operadora:
   registre o problema e avise a engenharia pelo Caixa. Depois da correção,
   repita o mesmo enqueue com o mesmo `request_ref`.
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
   `payroll_effective_launches_not_read` (com `folha-v33`, também
   `payroll_effective_launches_case_not_in_preparation` ou
   `payroll_case_workflow_running`; veja "Dossiê da folha"). Com o aceite humano, faça
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
  matrícula eSocial certa. A saída é `resolve_payroll_employee` com nome completo (CPF e admissão só para homônimos),
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

## Afastamento pago pela empresa: rubrica marcada no mapa (2.9.8)

Vale quando o mapa da empresa tiver uma rubrica com `afastamento_empregador` e
o cálculo mostrar o sufixo `-employer-leave-v1`. Sem a rubrica, o mês de
afastamento segue como antes.

- **Marcar a rubrica** (patch completo do mapa, `loki.company-payroll-map-patch/1`):
  `afastamento_empregador` é `doenca` (atestado de até 15 dias e os 15 primeiros
  dias do auxílio previdenciário) ou `acidente_trabalho` (15 primeiros dias do
  acidentário). A rubrica tem de ser provento comparável com código do Domínio,
  fórmula `salario_base_proporcional` em dias com divisor 30, INSS, FGTS e IRRF
  `adicionar`, sem `automatica` nem `parametro_individual`; senão recusa com
  `afastamento_empregador_mapeamento_incompativel`. Uma rubrica por natureza.
- Marcar muda o hash do mapa e desatualiza as folhas abertas da empresa:
  marque antes de calcular o mês.
- O Loki deriva os dias da empresa do afastamento qualificado e os lança na
  rubrica marcada; a linha de salário paga só os dias trabalhados. Envie
  `periodo_remuneravel` ausente, 30 ou o derivado. Se vier 30, a troca fica
  registrada em `afastamento_mes.periodo_enviado`; outro valor fica com
  `payroll_salary_periods_not_qualified`. **Não lance a rubrica marcada nem
  outra rubrica de dias para o mesmo atestado.**
- Pendências (os dias não voltam em silêncio ao salário):
  - `afastamento_empregador_rubrica_nao_mapeada` (próxima ação
    `mapear_rubrica_de_afastamento_pago_pela_empresa`): a natureza do mês não
    tem rubrica;
  - `afastamento_empregador_lancamento_conflitante`
    (`retirar_lancamento_da_rubrica_de_afastamento_derivada_do_contexto`): a
    rubrica marcada também veio como lançamento;
  - `afastamento_empregador_lancamento_em_rubrica_sem_marca`
    (`conferir_se_o_lancamento_e_o_mesmo_atestado_e_retira_lo_ou_qualificar_os_periodos`):
    dias lançados em outra rubrica, que podem ser o mesmo atestado;
  - `afastamento_mes_exige_salario_pelo_mes_comercial`
    (`qualificar_periodos_do_mes_de_afastamento_pelo_historico`): a linha de
    salário não lê o período pelo mês de 30 dias.
- Regras individuais que leem `rubricas_base=["salario_base"]` passam a ler só
  os dias trabalhados: inclua a rubrica de afastamento em `rubricas_base` das
  regras que devem cobrir esses dias; o Loki não a acrescenta.

## Regras da DP para declarar o cadastro e os descontos (2.9.8)

São regras da DP aplicadas pela harness ao ler o cadastro e o lançamento. O
Loki não as deriva sozinho: ele recebe a quantidade declarada por pessoa e a
valida com a coerência interna.

- **Salário-família.** Depende da flag no cadastro do Domínio. Com a flag
  desmarcada, a quantidade de filhos para o salário-família é 0, mesmo que o
  empregado tenha dependente cadastrado. Declare 0 no campo `salario_familia`
  do cadastro em vez de contar os dependentes; o dependente de IRRF é outro
  dado.
  Ausência da quantidade continua pendência, nunca zero presumido.
- **DSR das faltas.** Faltas em semanas distintas descontam 2 DSR. O período
  corrido já engloba o DSR: não acrescente desconto de DSR por cima dele. Não crie falta nem desconto de DSR
  para fazer o total coincidir com o Domínio.
- **VT.** O percentual vem da escala da pessoa: 3% na 12x36 e 6% na 6x1. A
  harness declara o percentual por pessoa em `vale_transporte_regra`
  (`percentual_basis_points`: 300 ou 600). O Loki não deduz a taxa da escala,
  do sindicato nem de referência livre: sem a regra declarada, o Loki não
  aplica taxa pela escala.

## Vínculo intermitente: `categoria_esocial` (2.12.0)

Vale quando `get_process_contract("folha_mensal")` listar `categoria_esocial` em
`dados_folha.funcionarios[*]` (backend #434). O Loki **ainda não calcula
contrato intermitente** (CLT art. 452-A: convocação, horas por período e
parcelas proporcionais não existem no motor); ele só impede que a pessoa seja
calculada como mensalista.

- **Declare o fato.** `categoria_esocial` é opcional, com três dígitos
  (`"101"`, `"111"`), lido da fonte pela harness. O Loki não infere o regime
  por salário, jornada ou cargo.
- **Com `"111"`** a pessoa vai para `nao_calculados` (motivo
  `vinculo_nao_suportado`, código `vinculo_intermitente_nao_suportado`, próxima
  ação `retirar_vinculo_intermitente_da_folha_mensal`, `missing_fields` vazio) e
  abre a pendência agregada de mesmo código (evidência `competencia` e
  `matriculas`). Os demais calculam normalmente e a cobertura fica parcial. A
  checagem vem antes de rubrica e de alocação: rubrica não mapeada de um
  intermitente não derruba a folha.
- **Declare em TODA competência.** Sem a categoria no cadastro (seção da 2.13.0
  abaixo), a memória do intermitente vale só dentro do caso da competência e não
  atravessa competências. Folha de outro mês, sem `categoria_esocial = "111"`
  na folha nem no cadastro, calcula a pessoa como mensalista. Dentro do mesmo
  caso, a pendência aberta lembra as matrículas e mantém a pessoa fora do
  cálculo mesmo se `restart_case` ou nova escrita deixarem a categoria de fora.
- **Fecha** (`auto_resolve` na reavaliação mensal) só quando cada matrícula
  marcada saiu da folha ou foi declarada com outra categoria; campo ausente não
  fecha.
- **O que fazer.** Retire o intermitente da folha mensal e apure a competência
  dele fora do Loki; se a categoria foi declarada por engano, corrija a fonte e
  recalcule. Nunca calcule intermitente como mensalista nem tente reproduzir a
  convocação por lançamentos.

## Categoria eSocial que não é de empregado e categoria no cadastro (2.13.0)

Vale quando `get_company_onboarding_contract` listar `categoria_esocial` em
`employee_parameters.data_schema` (padrão `^[0-9]{3}$`); sem o sinal, siga a seção
do intermitente acima. O Loki só calcula empregado (categoria `1xx`, e dentre elas
não a `111`).

- **Categoria que não começa com `1`** (723 sócio com pró-labore, 901 estagiário):
  a pessoa **não é calculada**. Vai para `nao_calculados` (motivo
  `vinculo_nao_suportado`, código `categoria_esocial_nao_suportada` em
  `issues[].code`, `detalhe` com a categoria recebida, próxima ação
  `retirar_categoria_nao_clt_da_folha_mensal`) e abre a pendência agregada de mesmo
  código (evidência `competencia` e `matriculas`); os demais calculam e a cobertura
  fica parcial. O Loki ainda **não calcula pró-labore nem bolsa de estágio**. O `111`
  segue com o código próprio da seção acima; `1xx` e campo ausente, como sempre. A
  checagem vem antes de rubrica: rubrica não mapeada dessa pessoa não derruba a folha.
- **O que fazer.** Retire a pessoa da folha mensal e apure a competência dela fora do
  Loki; se a categoria foi declarada por engano na folha, corrija a fonte e
  recalcule; se a do cadastro está errada, corrija-a no cadastro (fato
  `parametrizacao`, abaixo). Nunca calcule sócio ou estagiário como empregado.
- **Fecha** (`auto_resolve`) quando nenhuma matrícula marcada segue com categoria que
  não é de empregado: saiu da folha, ou a folha (ou o cadastro, se a folha omite o
  campo) passou a trazer `1xx`. Declarar `1xx` na folha de quem tem 723 ou 901 no
  cadastro fecha esta pendência, mas abre `categoria_esocial_divergente` e a pessoa
  segue sem cálculo.
- **Memória dentro do caso.** A pendência aberta lembra matrícula e categoria e
  mantém a pessoa fora do cálculo mesmo se `restart_case` ou nova escrita deixarem
  o campo de fora. Limites: só dentro do caso da competência e só o que a folha
  declarou; o campo ausente não fecha a pendência. O cadastro vence a memória:
  matrícula com categoria cadastrada não herda a lembrada (cadastro corrigido para
  101 e folha reenviada sem o campo calcula como 101).
- **Categoria no cadastro do vínculo.** `categoria_esocial` (3 dígitos, opcional) é
  parâmetro individual, declarado como os demais (pensão, VT, adicionais): fato
  `kind: "parametrizacao"` com `effective_on`, referência, fonte e
  `data: {"categoria_esocial": "723"}`, no trabalhador do lote de onboarding
  (`workers[].existing_employee_id` quando o vínculo já existe) ou, em caso
  aberto, pelo perfil documental
  (`import_documentary_profile`, `parametrizacao` com a fonte do campo). Valor que
  não tenha 3 dígitos é recusado. Folha sem o campo usa a do cadastro, inclusive
  `111`, 723 e 901.
- **Folha e cadastro divergentes** (qualquer diferença, até entre duas `1xx`): a
  pessoa não é calculada (`nao_calculados`, código `categoria_esocial_divergente`,
  próxima ação `alinhar_categoria_esocial_folha_e_cadastro`) e a pendência agregada
  de mesmo código fica aberta até nenhuma matrícula divergir. Se a folha está certa,
  atualize o cadastro (fato `parametrizacao`); se o cadastro está certo, declare
  na folha a mesma categoria (ou omita o campo) e recalcule. Nunca escolha em
  silêncio.
- **Exigência de cadastro.** Quem não é empregado exige só `dependentes_irrf`:
  sindicato, escala, VT e salário-família deixam de ser cobrados
  (`cadastro_mestre_campo_ausente`). Cadastro sem o campo: mesma saída, mesmos
  hashes e mesma versão do motor, e nenhuma folha fica desatualizada por isso.
- **Recomendação.** Declare a categoria no cadastro de todo sócio, estagiário e
  intermitente ANTES de rodar a folha: sem ela no cadastro nem na folha, a pessoa
  é calculada como mensalista.
- Criar caso de 13º, férias, rescisão ou admissão (e simulação de rescisão) de
  quem tem categoria que não é de empregado no cadastro é recusado
  (`categoria_sem_regime_clt`): `rescisao`, `admissao`, `ferias` e `decimo_terceiro`.

## Reinício em lote autorizado por correção (rotina, 2.13.0)

Vale quando a proprietária repassar um `authorization_id` (`rst-` e 32 hex) e o
`expected_snapshot` de cada caso, depois de uma correção `CL-N` (a autorização
está em `aprovacoes`). A rotina (conta de automação com `consultar` e `operar_casos`
em `folha_mensal`; `atualizar_por_insumo_do_cliente` nem é exigida nem basta)
reinicia **uma vez cada caso listado**, em `aguardando_revisao`, de forma simples
(payload preservado): `receive_case_data(case_id, request={schema_version:
"loki.case-restart-authorized/1", authorization_id, case_id, expected_snapshot,
human_message})`, com `case_id` igual ao argumento, `expected_snapshot` igual ao
repassado e `human_message` que nomeia o `CL-N`. O recibo traz `requires_case_data`: `true`
em caso legado (reenvie os dados pelo `receive_case_data` comum). Depois, `enqueue_case_workflow`
com os snapshots novos; o pacote novo exige nova revisão e novo aceite humanos.
Repetir o mesmo pedido devolve o recibo (`replayed: true`). Toda recusa deixa o item
sem consumir: pare e avise a proprietária, sem laço (códigos em `aprovacoes`); só
`BUSY` (`authorization_change_busy`) pede repetir a mesma chamada.

## Consignado sem linha no mapa de verbas (2.12.0)

Sintoma: o contrato de consignado (`credito_trabalhador_contratos`) declara
`rubrica_loki`, mas o mapa de verbas da empresa não tem linha utilizável para
esse nome. A folha da pessoa sai **parcial** (`funcionarios_parciais`), com o
componente pendente `credito_trabalhador_mapeamento_pendente` (próxima ação
`configurar_mapeamento_empresarial_do_credito`) e sem a verba do crédito; os
proventos e os demais descontos dela e a folha dos outros seguem. Um número de
rubrica como 220 nunca identifica o crédito sem esse vínculo explícito.

Acrescente ao mapa da empresa, pelo patch completo do mapa
(`loki.company-payroll-map-patch/1`, o mesmo caminho da seção de afastamento),
uma linha que o Loki aceite como vínculo do crédito:

- `loki` igual à `rubrica_loki` do contrato (nunca `vale_transporte`, `inss`,
  `irrf`, `fgts` nem `salario_familia`);
- `natureza` desconto e ao menos um código do Domínio em `dominio_codes`;
- sem `parametro_individual` (a linha de VT e de pensão tem outra função);
- incidência `sem_efeito` em INSS, FGTS e IRRF (cada uma com `fonte`); qualquer
  outro efeito faz o vínculo ser recusado e a pendência persistir;
- `disposition`, `formula` e `fonte` como em qualquer linha do mapa.

O código do Domínio e a fonte vêm da DP, nunca de palpite. Como em toda mudança
de mapa, o hash dele muda e as folhas abertas da empresa ficam desatualizadas:
acrescente a linha antes de calcular o mês e, nas já calculadas, `restart_case`
e novo cálculo. Não crie lançamento manual da parcela para o total fechar.

## Razão social do caso x cadastro (2.12.0)

Vale quando a resposta servida mostrar o código ou o aviso abaixo. Na geração
dos holerites o Loki confere de novo a razão social do caso contra a do
cadastro (binding) da empresa. Detalhe das regras em `admissao` ("Razão social
da empresa"). Aqui, o que muda a folha:

- natureza jurídica diferente (LTDA x S.A. x EIRELI) recusa a geração com
  `razao_social_natureza_juridica_divergente` no início da mensagem da recusa. Diferença só
  de tipo societário com `codigo_dominio` do caso diferente do cadastro também
  recusa (a tolerância exige CNPJ e código conferidos). A conferência roda de
  novo na geração, contra o cadastro vigente nela; divergência ali recusa com
  "razao social do caso diverge do binding da empresa": confira a empresa e o
  cadastro, nunca ajuste o nome só para silenciar;
- só o tipo societário diferente, ou só o porte (ME, EPP) ou o tipo ausente de
  um lado, não recusa: o holerite sai com o nome do cadastro e o pacote traz o
  aviso `razao_social_tipo_societario` (sem reter documento, sem exigir ciência).

## Regras comuns da operação

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Documente bases recebidas, fontes, divergências e ausências. Uma base ausente não se transforma em zero. Não invente parcelas, critérios, legislação ou datas; consulte fontes e contratos aprovados pelo responsável. Cumpra os gates humanos. Uma validação técnica não autoriza aceite, transmissão, pagamento ou publicação de resultados.

Toda operação usa o conector HTTPS `https://loki.izzicontabil.com.br/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
