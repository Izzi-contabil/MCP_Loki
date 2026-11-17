# Reajuste salarial coletivo com efeito retroativo

Este roteiro orienta o caso coletivo `reajuste_salarial`, da leitura do
instrumento à folha X. É o mesmo texto do domínio `reajuste_salarial` servido
por `loki_obter_instrucoes`. Distribuir este guia ou preparar um wheel não
comprova publicação do backend, instalação no operador, escopo ativado na
conta, homologação contra o Domínio ou aceite de DP.

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
   e/ou `regra.piso_cents`) e se o instrumento abrange desligados no
   intervalo (`abrange_desligados_no_intervalo`: `sim`, `nao` ou
   `pendente`). Se o instrumento não diz, use `pendente` e pergunte à DP.
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
  (`salary_adjustment_withdraw_per_employee`). Para corrigir uma pessoa já
  aplicada, retire o efeito no caso filho e abra um caso coletivo com nova
  referência do instrumento; o mesmo instrumento não é reaplicado à pessoa
  (`reajuste_retroativo_ja_lancado_na_competencia`).
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
`desligado_antes_da_vigencia`, `desligado_nao_abrangido_pelo_instrumento`,
`abrangencia_de_desligados_pendente`,
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
`source`. Inclua todas as verbas do mês, não só o salário.

- O pago recalculado pela fórmula do mapa tem de bater com o declarado; senão
  o mês fica `diferenca_pago_divergente`.
- Verba declarada que depende do salário e não é revalorizada aqui (hora
  extra, DSR, adicional) vira reflexo não calculado, no blocker
  `diferenca_reflexos_nao_calculados`. Verba independente do salário é
  ignorada.
- Confirme `sem_outras_verbas_dependentes_do_salario: true` só depois de
  conferir que nenhuma verba dependente do salário ficou de fora. Sem essa
  afirmação, o mês fica `diferenca_origem_declarada_incompleta`.
- Sem declaração, o mês fica `diferenca_origem_sem_base`. Não invente o pago
  e não declare zero.
- Mês com folha do Loki não leva declaração (`origem_declarada_com_folha_do_loki`;
  na folha, `diferenca_origem_invalida`). Mês fora do intervalo da pessoa
  recusa a linha (`origem_declarada_fora_do_intervalo`).

## Salário fora da regra: motivos fechados

Com regra declarada, o Loki calcula o salário novo sobre o salário anterior:
percentual com arredondamento meio para cima em centavos; com percentual e
piso, vale o maior. Um `salario_novo_cents` diferente da regra só é aceito
com `motivo_salario_novo` fechado:

- `proporcional_admissao`;
- `acima_do_piso_mantido`, só para quem já ganha o piso ou mais, com salário
  novo igual ao anterior; abaixo do piso a linha recusa com
  `salario_novo_diverge_da_regra`;
- `outro_declarado`, com `motivo_texto` obrigatório.

O motivo vira ressalva por matrícula (`salario_novo_fora_da_regra`). Com
regra só de piso, quem já ganha o piso ou mais fica `sem_reajuste`: não tem
diferença e não é recusado. Sem regra, o salário novo é obrigatório
(`salario_novo_ausente_sem_regra`). As outras ressalvas por matrícula são
`alteracao_salarial_no_intervalo` (outra alteração salarial entre Y e X) e
`rescisao_complementar_pendente`. Ressalva não recusa o lote; leve-a à
operadora antes do aceite.

## Desligados

Rescisão antes da vigência recusa a linha (`desligado_antes_da_vigencia`).
Desligado até o fim de X com abrangência `nao` também recusa
(`desligado_nao_abrangido_pelo_instrumento`); com `pendente`, a linha fica
pendente de decisão da DP (`abrangencia_de_desligados_pendente`). Com `sim`,
o efeito é gravado e a folha X mostra a ressalva
`diferenca_rescisao_complementar_pendente`.

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
  `diferenca_pago_divergente`, `diferenca_exige_particao_do_periodo`,
  `diferenca_revalorizacao_pendente`, `diferenca_reajustes_sobrepostos`,
  `diferenca_rra_exige_qualificacao` e `diferenca_retroativa_nao_positiva`;
  também `politica_diferenca_retroativa_ausente` e
  `instrumento_reajuste_divergente`. A diferença dessas pessoas não entra.
  Leve as pendências à DP; nunca as zere nem informe a diferença à mão em
  `dados_folha` (recusa `retroactive_difference_informed`).
- A verba 19 e a política `diferenca_retroativa` do mapa (INSS, FGTS e IRRF
  em `competencia_pagamento`) entram numa vigência nova do mapa a partir de
  X. Editar a vigência que cobre um mês já fechado muda o hash e deixa a
  diferença em `diferenca_mapa_origem_divergente`. A verba 19 fica fora das
  médias de férias e 13º.

## Pendente até a DP decidir

Estes pontos não têm convenção confirmada. Mostre a pendência, pergunte à DP
e não invente regra:

- vigência fora do dia 1: o mês de Y fica
  `diferenca_exige_particao_do_periodo` até a convenção da partição;
- RRA para competências de ano-calendário anterior a X
  (`diferenca_rra_exige_qualificacao`);
- rescisão complementar dos desligados abrangidos, e a abrangência quando o
  instrumento é omisso (`pendente`);
- regra para quem foi admitido depois de Y (proporcional ou integral) e para
  quem já está acima do piso: hoje é declarada por linha, com motivo fechado
  e ressalva;
- arredondamento do percentual: hoje é meio para cima em centavos sobre o
  salário anterior; falta confirmar a paridade com o Domínio.
