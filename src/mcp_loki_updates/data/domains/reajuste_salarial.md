# Reajuste salarial coletivo com efeito retroativo

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato. Este processo não gera documento: `document_outputs=[]` e o retorno é recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

## Quando usar e o que o contrato oferece

Use o processo `reajuste_salarial` para reajuste de CCT, ACT, termo aditivo,
sentença normativa ou pedido do cliente com vigência (data-base Y) anterior à
competência em que ele é lançado e pago (X). O desenho vale somente quando
`get_process_contract("reajuste_salarial")` servir a interface
`loki.salary-adjustment/1`. Não há ferramenta nova: o processo vem por
`get_process_contract`, e a prévia, a exclusão e a reabertura são transportes
de `receive_case_data` (`loki.salary-adjustment-preview/1`,
`loki.salary-adjustment-exclusion/1` e `loki.salary-adjustment-reopen/1`).
Por isso não é preciso Refresh do conector para este processo; atualizar o
plugin instalado continua sendo outra etapa.

A conta precisa dos processos `reajuste_salarial` e `alteracao_cadastral` na
mesma empresa. Em `alteracao_cadastral`, ela precisa de `consultar`,
`decidir_chat` e `corrigir_dados`, porque o lote cria casos de alteração
cadastral e grava um efeito por funcionário. Sem isso, `apply_case_effects`
no caso coletivo, a reabertura e a exclusão recusam com
`salary_adjustment_requires_employee_change_scope`. Peça a autorização pelo
fluxo administrativo; não contorne pelo caso de alteração cadastral.

## Quem confere o quê

A harness lê o instrumento no original, confere com a operadora e monta a
população. O Loki só valida a coerência interna (data-base até X, salário
novo coerente com a regra declarada, origens dentro do intervalo) e o estado
do próprio cadastro (salário anterior, admissão, desligamento, folhas
fechadas). O Loki nunca confere a fonte: a prévia e o `validate_case` trazem
`conferencia_das_fontes: "harness"`. Coerência aceita não prova que o
instrumento foi lido certo. O que o instrumento não diz vira pergunta à DP;
não invente convenção.

## Passo a passo

1. Leia o instrumento no original e registre a fonte. Confira com a
   operadora o tipo (`kind`: `cct`, `act`, `termo_aditivo`,
   `sentenca_normativa` ou `cliente`), a referência, a data-base
   (`data_base`), a competência de lançamento (`competencia_lancamento`,
   `AAAA-MM`), a regra (`regra.percentual_bp` em pontos-base, 550 = 5,50%,
   e/ou `regra.piso_cents`) e a abrangência de desligados
   (`abrange_desligados_no_intervalo`). O padrão da DP é `nao`. Use `sim`
   só quando o instrumento ou o cliente pedir expressamente. Se o
   instrumento não diz, não envie o campo: ausente ou `pendente` valem
   `nao`. Com regra percentual, declare em
   `regra.salario_base_anterior_cents` o salário-base (piso) da categoria
   antes do reajuste. Se o instrumento tem mais de um piso, declare o da
   pessoa em `linhas.<matricula>.salario_base_anterior_cents`. Isso decide
   o reajuste de quem foi admitido depois da data-base.
2. `create_case` com `case_type=reajuste_salarial`, `competencia` no dia 1
   de X e `occurrence_ref` igual à referência do instrumento, sem
   funcionário.
3. `get_process_contract("reajuste_salarial")` para o schema atual da seção
   `dados_reajuste_salarial`.
4. Envie o `instrumento` por `receive_case_data`.
5. Monte a população pela matrícula, em `linhas` (um mapa por matrícula):
   `salario_anterior_esperado_cents` sempre; `salario_novo_cents` só quando
   a regra não bastar, com `motivo_salario_novo` (veja "Salário fora da
   regra"); `source`; `origens_declaradas` para os meses sem folha do Loki;
   e `exclusao` com `motivo` para quem não entra no lote. Envie em blocos de
   até 100 matrículas por chamada (mais que isso recusa com
   `salary_adjustment_block_too_large`); o lote CSV existente
   (`get_operational_batch_contract`) pode levar os blocos, um
   `receive_case_data` por bloco. Antes da decisão, reenviar a linha ou o
   instrumento substitui o valor enviado; valor enviado não some sozinho:
   para tirar a pessoa do lote, use `exclusao`.
6. `validate_case`, com `cliente.slug` e `empresa.cnpj` no payload para usar
   a admissão do cadastro. `reajuste_salarial.linhas_divergentes` lista a
   divergência interna por matrícula, com os códigos.
7. Prévia: `receive_case_data` com
   `{"schema_version": "loki.salary-adjustment-preview/1"}`, só leitura.
   Ela é paginada: até 500 matrículas por página (`limite`); siga
   `proximo_inicio` em `inicio` até vir `null`. `resumo_total` conta o lote
   inteiro; `resumo_pagina`, só a página. Por matrícula: situação
   (`pronta`, `divergente`, `sem_reajuste`, `excluida`, `pendente` ou
   `aplicada`), salário novo, vigência `max(data-base, admissão)`, origem de
   cada mês, ressalvas e meses pendentes. No lote: `decidido`,
   `decisao.request_ref`, `casos_filhos_sem_efeito` e o `expected_snapshot`.
   O salário anterior contra o cadastro é conferido na aplicação
   (`salario_anterior_conferido: "na_aplicacao"`).
8. Conferência da operadora: mostre o resumo total, as ressalvas, os meses
   pendentes e as linhas divergentes. A conferência das fontes é sua e da
   operadora.
9. Lote ainda não decidido (`decidido=false`): só com o aceite explícito da
   operadora para o lote inteiro, chame `apply_case_effects` no caso
   coletivo com o `expected_snapshot` da prévia, `request_ref` estável e a
   decisão humana explícita transcrita em `human_message`, com
   `message_reference`.
   - `BLOCKED` (`salary_adjustment_lines_divergent`, `decidido=false`,
     `effects_written=false`): nenhum efeito foi gravado e não há decisão.
     Corrija ou exclua as linhas apontadas em `pendentes`, refaça a prévia e
     peça o aceite de novo.
   - `VALIDATING` (`retry: "mesmo_pedido"`): a conferência por linha
     continua; repita o mesmo pedido, com o mesmo `request_ref`. Ainda não
     há efeito.
   - `effect_snapshot_changed`: o caso mudou depois da prévia; refaça a
     prévia e o aceite.
10. Lote já decidido (`decidido=true`, ou recibo `IN_PROGRESS` ou
    `PARTIAL`): não peça nova decisão. Retome pelo mesmo `request_ref`,
    repetindo `apply_case_effects` no caso coletivo até `APPLIED` ou
    `PARTIAL`; a prévia mostra o pedido da decisão em
    `decisao.request_ref`. Pode retomar quem decidiu ou outra pessoa com
    `decidir_chat` e `corrigir_dados` no escopo; os efeitos usam a mensagem
    humana gravada na decisão. Depois da decisão a seção não muda
    (`salary_adjustment_already_decided`,
    `salary_adjustment_input_changed_after_decision`).
11. Depois de `APPLIED`, siga o `next_action` (`enqueue_case_workflow`):
    calcule a folha X. A diferença sai na verba 19 com a política de
    diferença retroativa do mapa.

Não há job durável para o lote: a harness repete o pedido. O plano mede cerca
de 0,01 s por linha e a conferência mais a execução cerca de 0,2 s por linha
no banco sintético; cada chamada tem 20 s depois do plano. Depois de
`APPLIED`, o caso coletivo continua `aberto`, com a seção imutável e os
eventos de decisão, exclusão e aplicação; não há pacote documental.
`external_payment_executed: false`: nada é pago nem transmitido.

## Recibo PARTIAL e saídas

O recibo `PARTIAL` (`code: salary_adjustment_partially_applied`) mostra o
estado real do lote: `decidido=true`, `aplicadas` (matrícula, caso filho e
efeito), `pendentes` (matrícula e códigos) e `effects_written=true` quando já
houve efeito. Relate esse estado à operadora: quantas aplicadas, quais
pendentes e por quê. Nunca diga "nada foi gravado" quando já houve efeito; só
o `BLOCKED` antes da decisão garante que nenhum efeito foi gravado. Mesmo
nele, casos filhos e marcadores de conferência sem efeito podem existir
(`casos_filhos_sem_efeito`).

- Linha pendente sem `saida` teve tentativa transitória (tempo ou capacidade,
  snapshot que mudou): volta sozinha; repita o pedido. Na terceira tentativa
  vira falha registrada (`tentativas_transitorias_esgotadas`).
- Linha com falha registrada traz `saida: ["reabertura", "exclusao"]` e não
  é tentada de novo nesta decisão. Decida com a operadora:
  - reabertura (`loki.salary-adjustment-reopen/1`) quando a causa foi
    resolvida: o Loki apaga a falha, reconfere o cadastro com o perfil atual
    antes de aplicar, e a próxima repetição de `apply_case_effects` aplica;
  - exclusão (`loki.salary-adjustment-exclusion/1`) quando a pessoa fica fora
    do lote, com `motivo` fechado: `nao_aplicavel_apos_decisao`,
    `decisao_da_dp` ou `outro_declarado`. A exclusão fecha o lote quando não
    resta pendência; repetir a mesma exclusão devolve o mesmo recibo.
  - As duas vão por `receive_case_data` com `request_ref`, o
    `expected_snapshot` da prévia atual, `matriculas` (até 100),
    `human_message` com a decisão humana e `message_reference`. São
    recusadas em lote cancelado (`effect_case_incompatible`) e sem o escopo
    de `alteracao_cadastral`.
- Linha já aplicada sai pela retirada no caso filho: `apply_case_effects` no
  caso filho com `withdraw:true`. No caso coletivo, a retirada é recusada
  (`salary_adjustment_withdraw_per_employee`). A reabertura vale só para
  linha com falha registrada (`salary_adjustment_reopen_invalid`) e a
  exclusão recusa linha aplicada (`salary_adjustment_exclusion_invalid`):
  nenhuma das duas corrige linha `APPLIED`. Para corrigir uma pessoa já
  aplicada (por exemplo, o pago declarado de um mês), veja "Corrigir o pago
  declarado de lote já aplicado".
- `caso_filho_cancelado`: o caso filho foi cancelado e não é reaproveitado;
  exclua a linha ou declare outro instrumento.
- Os casos filhos são `alteracao_cadastral` com `occurrence_ref` iniciado por
  `reajuste:`, prefixo reservado (`reserved_occurrence_ref`).
  `apply_case_effects` direto num caso filho é recusado
  (`salary_adjustment_child_requires_collective`); a retirada continua
  permitida.
- `cancel_case` do caso coletivo é recusado enquanto algum caso filho tiver
  efeito ativo. Não cancele o lote para destravar a folha.
- `salary_adjustment_line_key_changed`: o segredo do servidor mudou com o
  lote em curso. Não é erro da operadora e não se resolve excluindo,
  reabrindo ou recomeçando: relate com `registrar-problema-loki`; a única
  saída é a engenharia restaurar o segredo usado na decisão.

Códigos de linha (fechados, por matrícula): `salario_novo_diverge_da_regra`,
`salario_novo_nao_superior_ao_anterior`, `salario_novo_ausente_sem_regra`,
`origem_declarada_fora_do_intervalo`, `origem_declarada_com_folha_do_loki`,
`funcionario_nao_encontrado`, `funcionario_ambiguo`,
`salario_anterior_divergente`, `admissao_posterior_ao_lancamento`,
`desligado_antes_da_vigencia`, `reajuste_proporcional_nao_praticado`,
`salario_base_nao_declarado_para_admitido_apos_data_base`,
`salario_anterior_abaixo_do_salario_base`,
`reajuste_retroativo_ja_lancado_na_competencia`,
`folha_do_lancamento_em_revisao_ou_fechada`,
`perfil_do_funcionario_indisponivel`, `secao_interna_ja_gravada_divergente`,
`aplicacao_do_efeito_recusada`, `caso_filho_cancelado` e
`tentativas_transitorias_esgotadas`. O recibo nunca ecoa valor: corrija pelo
original e pela operadora, não pelo código.

## Pago declarado para os meses sem folha do Loki

Para cada mês da vigência efetiva até X-1 sem folha do Loki
(`diferenca_origem_sem_base`), ou com folha aprovada sem a linha da pessoa
(`diferenca_origem_sem_linha`), transcreva da ficha financeira ou do holerite
o que foi pago, em `origens_declaradas["AAAA-MM"]`:
`salario_pago_cents`, `verbas` (de 1 a 30, sem repetir código:
`codigo_origem`, `valor_pago_cents` e `quantidade` em dias ou horas quando a
fórmula do mapa exigir), `sem_outras_verbas_dependentes_do_salario` e
`source`. Inclua todas as verbas do mês, não só o salário (o desconto de VT
fica de fora; veja abaixo).

- O pago recalculado pela fórmula do mapa tem de bater com o declarado; senão
  o mês fica `diferenca_pago_divergente`.
- Verba declarada que depende do salário e não é revalorizada aqui (hora
  extra, DSR, adicional) vira reflexo não calculado, no blocker
  `diferenca_reflexos_nao_calculados`. Verba independente do salário é
  ignorada.
- Descontos que dependem do salário, como o VT (6%), não entram na diferença
  (regra da DP, 18/11/2026): o VT vale só sobre o salário do mês. Não declare
  VT em `origens_declaradas.<mês>.verbas`. Ele não impede a afirmação
  `sem_outras_verbas_dependentes_do_salario: true`, que trata das verbas de
  provento (hora extra, DSR, adicionais). Na folha fechada do Loki, o VT
  também não vira parcela de diferença nem reflexo, qualquer que seja a
  fórmula do mapa (`declared_origins.transport_discount` no contrato).
- Confirme `sem_outras_verbas_dependentes_do_salario: true` só depois de
  conferir que nenhuma verba dependente do salário ficou de fora. Sem essa
  afirmação, o mês fica `diferenca_origem_declarada_incompleta`.
- Sem declaração, o mês fica `diferenca_origem_sem_base`. Não invente o pago
  e não declare zero.
- Mês com folha do Loki não leva declaração (`origem_declarada_com_folha_do_loki`;
  na folha, `diferenca_origem_invalida`). Mês fora do intervalo da pessoa
  recusa a linha (`origem_declarada_fora_do_intervalo`).

**`quantidade` segue a fórmula do mapa da competência de origem**, não o
holerite:

- Verba com fórmula `salario_base`: nunca envie `quantidade`, mesmo que o
  holerite mostre 30 dias. Com `quantidade`, o mês fica
  `diferenca_origem_invalida` (regra `salario_base_nao_aceita_quantidade`).
- Verba com fórmula `remuneracao_periodo` (salário pelos dias do período):
  `quantidade` obrigatória, na unidade do mapa. Quando o `retroactive_detail`
  mostrar a regra `remuneracao_periodo_quantidades_divergentes`, pode haver
  mais de uma no mesmo mês (o salário do período e uma produtividade ou
  adicional com fator sobre ele): todas com a mesma `quantidade`, a do
  período pago no holerite, porque o Loki revaloriza todas sobre o mesmo
  período. A `quantidade` é a do período em dias, a mesma para todas as
  verbas do período (por exemplo, 30); não é a referência que o holerite
  mostra para a produtividade (por exemplo, "5,00"). Usar essa referência, ou
  quantidades ou unidades diferentes no mesmo mês, dá
  `diferenca_origem_invalida` (`remuneracao_periodo_quantidades_divergentes`).
  O detalhe traz em `codigo_origem` a verba que diverge e em `codigo_periodo`
  a que fixou o período (a primeira declarada); a ordem não diz qual está
  errada: confira as duas no holerite. Código de verba repetido no mesmo mês
  é recusado, mesmo com zeros à esquerda (por exemplo, "8" e "008").
  Sem esse sinal (servidor anterior, regra `remuneracao_periodo_repetida`),
  declare uma única por mês.
- Verbas proporcionais (as demais fórmulas que dependem de dias ou horas):
  `quantidade` obrigatória (`formula_exige_quantidade`). Verba proporcional
  automática do mapa não é revalorizada no pago declarado
  (`diferenca_revalorizacao_pendente`, `verba_proporcional_automatica`).
- Na dúvida sobre a fórmula de uma verba, leia o mapa da competência de
  origem em `get_client_config`; não deduza pelo holerite.

## Corrigir o pago declarado de lote já aplicado

Depois de `APPLIED`, a seção do lote não muda
(`salary_adjustment_input_changed_after_decision`), a reabertura só vale para
linha com falha e a exclusão recusa linha aplicada. Para corrigir o pago
declarado (ou a linha) de quem já tem o efeito aplicado, com a confirmação da
operadora:

1. Retire o efeito: `apply_case_effects` no caso filho `alteracao_cadastral`
   da matrícula (`occurrence_ref` iniciado por `reajuste:`), com
   `withdraw: true` e `supersedes_effect_id`; exige `corrigir_dados`.
2. Abra um novo caso `reajuste_salarial` com o mesmo instrumento (mesmo tipo,
   data-base, regra e competência de lançamento) e outra `reference`, em
   `occurrence_ref` e em `dados_reajuste_salarial.instrumento.reference`. A
   mesma referência recusa a pessoa
   (`reajuste_retroativo_ja_lancado_na_competencia`).
3. Envie só as linhas corrigidas, com o pago em
   `linhas.<matricula>.origens_declaradas.<AAAA-MM>`, e siga o passo a passo
   (prévia, aceite, `apply_case_effects`). A folha X não pode estar em
   `aguardando_revisao`, `aprovado` ou `publicado`
   (`preview.blocking_payroll`).

Depois, recalcule a folha X e releia o dossiê.

## Salário fora da regra: motivos fechados

Com regra declarada, o Loki calcula o salário novo sobre o salário anterior:
percentual com arredondamento meio para cima em centavos; com percentual e
piso, vale o maior. Um `salario_novo_cents` diferente da regra só é aceito
com `motivo_salario_novo` fechado:

- `acima_do_piso_mantido`, só para quem já ganha o piso ou mais, com salário
  novo igual ao anterior; abaixo do piso a linha recusa com
  `salario_novo_diverge_da_regra`;
- `outro_declarado`, com `motivo_texto` obrigatório.

A DP não pratica reajuste proporcional à admissão. `proporcional_admissao`
recusa a linha (`reajuste_proporcional_nao_praticado`). Arredondamento: meio
centavo para cima, igual ao Domínio.

O motivo vira ressalva por matrícula (`salario_novo_fora_da_regra`). Com
regra só de piso, quem já ganha o piso ou mais fica `sem_reajuste`: não tem
diferença e não é recusado. Sem regra, o salário novo é obrigatório
(`salario_novo_ausente_sem_regra`). As outras ressalvas por matrícula são
`alteracao_salarial_no_intervalo` (outra alteração salarial entre Y e X) e
`rescisao_complementar_pendente`. Ressalva não recusa o lote; leve-a à
operadora antes do aceite.

## Admitidos depois da data-base

O reajuste é por competência (regra da DP de 18/11/2026). Vale quando
`rule.admitted_after_base_date` do contrato servido disser
`applies_to_admission: "competencia posterior a da data-base"`; sem esse
sinal, admitido no mesmo mês depois do dia da data-base ainda é tratado como
posterior.

Com regra percentual, declare o salário-base em
`regra.salario_base_anterior_cents` (só com `percentual_bp`) ou em
`linhas.<matricula>.salario_base_anterior_cents`. Quem foi admitido em
competência posterior à da data-base, no salário-base da categoria, recebe o
reajuste integral desde a admissão. Quem foi admitido acima do salário-base não
tem reajuste: a prévia mostra `sem_reajuste` com
`motivo_sem_reajuste = admitido_apos_data_base_acima_do_salario_base`, e o
piso novo ainda prevalece. Sem salário-base declarado, a linha recusa com
`salario_base_nao_declarado_para_admitido_apos_data_base`. Salário anterior
abaixo do salário-base recusa com `salario_anterior_abaixo_do_salario_base`.
Nos dois casos, confira o original e pergunte à DP. Não declare o reajuste
por linha para contornar.

## Admitido no mês da data-base

Regra da DP (18/11/2026: quem entrou no mês da data-base já deve entrar com o
salário correto), em `rule.admitted_on_base_date` do contrato. Quando o
contrato servido descrever "admitido na competência da data-base", vale para
qualquer dia do mês, antes, no dia ou depois do dia da data-base:

- O salário de admissão já é o salário novo. Envie a linha com
  `salario_anterior_esperado_cents` igual ao salário de admissão e sem
  `salario_novo_cents`. O Loki devolve `sem_reajuste` com
  `motivo_sem_reajuste = admitido_na_data_base_com_salario_novo`, e isso não
  é divergência. Se o piso novo for maior, vale o piso.
- Não informe percentual nem salário novo para essa pessoa:
  `salario_novo_cents` maior sem motivo diverge da regra
  (`salario_novo_diverge_da_regra`).
- Linha desse tipo aplicada antes desta regra continua `aplicada` e a prévia
  mostra o salário gravado no efeito.
- Sem o sinal (servidor anterior), só o próprio dia da data-base tem essa
  regra: o admitido no mês antes desse dia não entra na linha, e o admitido
  depois dele segue "Admitidos depois da data-base". A regra da DP já existe e
  só falta a publicação; avise a operadora em vez de perguntar à DP.

## Salário novo já registrado no cadastro

- **Como declarar a linha.** Quando o histórico já tem o salário novo da CCT
  com vigência na data-base, declare a linha normalmente.
  `salario_anterior_esperado_cents` é o salário **antes** da data-base (o da
  véspera). `salario_novo_cents` é o reajustado, ou fica vazio para a regra
  calcular. Não tente corrigir o fato de onboarding, não declare o anterior
  igual ao novo (quem tem véspera no vínculo) e não exclua a pessoa por
  isso. Admitido no mês da data-base segue a seção anterior.
- **Na prévia.** A linha pode trazer
  `salario_novo_provavelmente_registrado: a_confirmar_na_aplicacao`. É só um
  aviso: a conferência é feita na aplicação.
- **Na aplicação.** O Loki aceita a linha com a ressalva
  `salario_novo_ja_registrado_no_cadastro:<fonte>` se o cadastro tiver
  exatamente esse salário novo na data-base e o anterior na véspera. A fonte é
  `fato_onboarding`, `alteracao_cadastral` ou `evento_vinculo`. Apresente a
  ressalva à operadora no recibo. A DP confirmou (18/11/2026): o salário novo
  já registrado com vigência na data-base é o próprio reajuste da CCT, e a
  diferença ainda não foi paga. Envie a linha normalmente. Só se o original
  mostrar a diferença dos meses desde a data-base já paga no sistema de
  origem (Domínio ou outro), não siga com a diferença em X: leve o caso à DP
  antes de calcular a folha.
- **Diferença.** Sai na folha de lançamento, contra o salário efetivamente
  pago em cada mês de origem. Se algum mês de origem já foi pago com o
  salário novo, a diferença daquela pessoa fica pendente
  (`diferenca_salario_pago_divergente`) e nada é pago de novo.
- **Retirada do efeito.** Retirar o efeito do lote não desfaz o fato de
  onboarding: o salário na data-base continua sendo o novo registrado.
- **Recusas.** Se o cadastro tiver na data-base um valor que não é nem o
  anterior nem o novo, ou se a véspera não tiver o anterior, a recusa
  continua `salario_anterior_divergente`. Admitido depois da data-base é
  conferido só na vigência.

## Desligados

Padrão da DP: desligados não são abrangidos. Quem foi desligado até o fim de
X sai do lote sozinho (`situacao = excluida`,
`exclusao_automatica = desligado_nao_abrangido_pelo_instrumento`), sem
recusar o lote e sem efeito. O recibo lista essas pessoas em
`excluidas_automaticamente` e `resumo_total.excluidas` as conta. Mostre a
lista à operadora. Com `sim` explícito, rescisão antes da vigência recusa a
linha (`desligado_antes_da_vigencia`). Nas demais linhas o efeito é gravado e
a folha X mostra a ressalva `diferenca_rescisao_complementar_pendente`.

## O que a operadora vê na folha X

- `reajuste_coletivo_em_execucao`: enquanto o lote decidido de X não fecha
  (`APPLIED`, ou todas as linhas aplicadas, excluídas ou sem reajuste), o
  cálculo da folha X da empresa é recusado; o blocker nomeia os casos.
  Retome o caso coletivo até o fechamento; nunca calcule com o lote pela
  metade nem cancele o lote para destravar a folha.
- `diferenca_reflexos_nao_calculados` (por matrícula): reflexos não
  revalorizados (férias no período, DSR, hora extra, adicionais). Decida com
  a DP no aceite das ressalvas; nunca trate como zero.
- `diferenca_funcionario_fora_da_folha`: matrícula ativa com reajuste
  lançado em X fora da população da folha. Inclua a pessoa na folha ou
  registre o desligamento; nunca a omita.
- `diferenca_rescisao_complementar_pendente`: desligado até o fim de X com
  reajuste lançado. A diferença dessa pessoa não é paga na folha nem na
  rescisão. A ressalva não impede a aprovação, mas exige a decisão da DP
  sobre cada matrícula registrada no aceite das ressalvas; nunca considere a
  diferença paga.
- Pendências `diferenca_*` por matrícula, na revisão da folha:
  `diferenca_origem_aberta` (folha de origem ainda aberta),
  `diferenca_origem_sem_base`, `diferenca_origem_sem_linha`,
  `diferenca_origem_declarada_incompleta`, `diferenca_origem_invalida`,
  `diferenca_mapa_origem_divergente`, `diferenca_salario_pago_divergente`,
  `diferenca_pago_divergente`, `diferenca_revalorizacao_pendente`,
  `diferenca_reajustes_sobrepostos` e `diferenca_retroativa_nao_positiva`;
  também `politica_diferenca_retroativa_ausente` e
  `instrumento_reajuste_divergente`. A diferença dessas pessoas não entra.
  Siga a ação de cada código no dossiê ("Pendências da diferença no dossiê
  da folha"); o que for decisão leve à DP, e nunca as zere nem informe a
  diferença à mão em `dados_folha` (recusa `retroactive_difference_informed`).
- A verba 19 e a política `diferenca_retroativa` do mapa (INSS, FGTS e IRRF
  em `competencia_pagamento`) entram numa vigência nova do mapa a partir de
  X. Editar a vigência que cobre um mês já fechado muda o hash e deixa a
  diferença em `diferenca_mapa_origem_divergente`. A verba 19 fica fora das
  médias de férias e 13º. Com a política ausente
  (`politica_diferenca_retroativa_ausente`), faça um `add` de vigência nova
  com `vigente_desde` no dia 1 da competência de lançamento, pelo
  `loki.company-payroll-map-patch/1` (`validate_client_config` e
  `apply_client_config`, em `entry.mapa.diferenca_retroativa` e
  `entry.mapa.mappings`); nunca um `replace` numa vigência que cubra mês de
  origem fechado. Quando o `envelope_schema` de
  `get_client_config.payroll_map_patch_transport` trouxer
  `diferenca_retroativa` em `MapaFolha`, monte a política por ele.

## Pendências da diferença no dossiê da folha

Vale quando a issue `contexto_operacional_pendente` de
`get_case_dossier(case_id)` (`calculations[].diagnostics`) trouxer
`retroactive_actions`. Os códigos acima aparecem em `missing_fields`, e
`retroactive_actions` traz uma ação por código: `code`, `next_action` e,
quando há, `next_operation`, `fields`, `steps` ou `alternatives`.
`diferenca_funcionario_fora_da_folha` não tem ação própria: inclua a pessoa
na folha ou registre o desligamento. Quando a ação é
`escolher_pela_regra_em_retroactive_detail` (`diferenca_origem_invalida`,
`diferenca_revalorizacao_pendente`, `diferenca_pago_divergente`), a regra do
detalhe decide.

`retroactive_detail` é uma leitura atual, sem valores, e só é feita com a
folha em preparação. Fora dela vem `available: false` com
`retroactive_detail_case_not_in_preparation`; com o caso ocupado,
`retroactive_detail_busy` (tente de novo); sem leitura possível,
`retroactive_detail_unavailable`. Com `available: true`, cada item traz
`codigo`, `regra`, `competencia`, `origem` (`declarada` ou
`folha_loki_fechada`), `codigo_origem` e `formula` quando há, e a ação da
regra. `codigo_origem_available: false` (ou outro `*_available: false`)
quer dizer que o valor não tem a forma esperada e não foi copiado. No pago
declarado, todas as verbas que falham são listadas, não só a primeira.

- Regra de declaração (`salario_base_nao_aceita_quantidade`,
  `formula_exige_quantidade`, `remuneracao_periodo_quantidades_divergentes`,
  `pago_declarado_fora_do_schema`, `pago_declarado_com_folha_do_loki`,
  `verba_proporcional_automatica`, as falhas de verba com `origem:
  declarada`): `retirar_efeito_no_caso_filho_e_relancar_reajuste_com_origem_corrigida`,
  com os três passos de "Corrigir o pago declarado de lote já aplicado".
- `verba_fora_do_mapa_da_competencia` com `origem: declarada`: o mesmo
  relançamento, ou incluir a verba na vigência do mapa da origem, só para
  mês sem folha do Loki fechada.
- Origem fechada no Loki que não se reproduz, histórico inválido ou folha de
  origem ilegível: `registrar_problema`. Nunca edite o mapa de um mês
  fechado.
- Política ausente: o `add` de vigência nova descrito acima, nunca `replace`.
- Mapa da origem divergente: restaurar a vigência original ou abrir uma
  vigência que comece depois dos meses de origem.

`retroactive_proof` traz o hash da prova gravada de cada efeito no cálculo,
e `matches_calculation` diz se a leitura atual ainda bate com ela. Com
`matches_calculation: false`, o detalhe já não descreve o cálculo gravado
(efeito, mapa ou origem mudaram depois): recalcule a folha antes de agir.
`retroactive_proof_not_recognized`: registre o problema. O detalhe não muda
o cálculo nem o hash da folha.
- O reajuste é por competência: o mês da vigência inteiro leva o salário
  novo, qualquer que seja o dia da data-base. Competências de ano anterior a
  X entram na verba 19 de X e são tributadas em X, como as demais (sem RRA).
  O 13º desse ano não é recalculado: aparece em
  `diferenca_reflexos_nao_calculados` como `decimo_terceiro`. Decida com a
  DP; nunca o trate como zero.

## Folha que bloqueia a linha e pendência de cadastro

Quando a resposta servida apresentar, a linha da prévia com
`folha_do_lancamento_em_revisao_ou_fechada` traz
`folha_bloqueante: {competencia: "AAAA-MM", estado}`. A regra não mudou e
está em `get_process_contract("reajuste_salarial").preview.blocking_payroll`:
bloqueia a `folha_mensal` da empresa de competência X **ou qualquer
competência posterior**, em `aguardando_revisao`, `aprovado` ou `publicado`,
que tenha a matrícula em `dados_folha.funcionarios`. Com mais de uma, vem a
de menor competência. O histórico importado não conta: só folhas do Loki
bloqueiam.

- Diga à operadora qual folha é (competência e estado). Não tente contornar
  a recusa.
- As saídas são duas: devolver essa folha para ajuste, se a DP quiser, ou
  lançar o reajuste em outra competência. Lance na primeira competência
  depois da última folha do Loki da empresa em revisão ou fechada, com a DP
  confirmando o mês. A competência do caso coletivo é a do lançamento
  (`salary_adjustment_instrument_case_mismatch` se divergirem): antes da
  decisão, cancele o caso e crie outro com `competencia` no dia 1 do novo X
  e o instrumento com a nova `competencia_lancamento`.
- Use sempre o `expected_snapshot` da prévia mais recente.

A pendência `cliente_config_incompleta` do caso de reajuste agora **fecha no
apply** (`decision.config_pending_reconciled` no contrato): depois da decisão
gravada (recibo `IN_PROGRESS`, `PARTIAL` ou `APPLIED`), quando o cadastro do
cliente está pronto. Antes da decisão e na prévia (só leitura) ela não muda.
Ela não impede o `apply_case_effects`. Se o motivo for
`processo_nao_habilitado_no_cliente`, o apply segue, mas o certo é habilitar
o processo no cadastro do cliente com a DP: avise a operadora; habilitar é
decisão da DP.

## Pendente até a DP decidir

A DP respondeu em 17/11/2026 a vigência fora do dia 1, o RRA, a abrangência
de desligados, os admitidos depois de Y e o arredondamento, e em 18/11/2026 o
admitido na data-base (pelo mês inteiro, com o sinal da seção "Admitido no
mês da data-base"), o VT e o salário novo já registrado (regras acima).
Fica pendente:

- O cálculo da rescisão complementar dos desligados abrangidos (`sim`) ainda
  não existe: a ressalva continua exigindo a decisão da DP no aceite.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
