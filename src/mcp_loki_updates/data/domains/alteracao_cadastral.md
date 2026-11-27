# Alteração cadastral

## Reajuste retroativo vem do caso coletivo

Quando `get_process_contract("reajuste_salarial")` servir
`loki.salary-adjustment/1`, o reajuste com efeito retroativo (data-base
anterior à competência de lançamento) não entra por alteração cadastral
pública: o bloco `retroatividade` é recusado com
`retroactive_launch_not_available`. Ele entra pelo caso coletivo
`reajuste_salarial`, que cria um caso filho de alteração cadastral por
funcionário; o roteiro está no domínio `reajuste_salarial`. O prefixo
`reajuste:` do `occurrence_ref` é reservado aos casos filhos
(`reserved_occurrence_ref`). `apply_case_effects` direto num caso filho é
recusado (`salary_adjustment_child_requires_collective`); a retirada
(`withdraw:true`) no caso filho continua permitida e é a saída para uma
linha já aplicada. O lote exige esta conta com `alteracao_cadastral` na mesma
empresa, com `consultar`, `decidir_chat` e `corrigir_dados`
(`salary_adjustment_requires_employee_change_scope`).

## Matrícula registrada não muda pelo caso

`create_case` não troca a matrícula de um vínculo. Quando a resposta servida
apresentar, matrícula enviada diferente da operacional registrada é recusada
com `matricula_funcionario_divergente` (`campos: ["funcionario.matricula"]`,
sem repetir valores) e nada é gravado. Reenvie omitindo `funcionario.matricula`;
se o documento de origem mostra matrícula diferente da registrada, avise a
operadora. A correção de uma matrícula registrada errada não é alteração
cadastral nem nova criação de caso: depois de combinar com a operadora, ela
segue a restauração ou a troca auditada do código Domínio (seções abaixo);
quando a recusa disser que não
há caminho automático, registre o problema com `registrar_problema`. O roteiro
do `create_case` está no domínio `geral` ("Matrícula no `create_case`").

**Matrícula do eSocial.** A matrícula de cada vínculo no Loki é a do
eSocial; o código do Domínio (ou de outro sistema de folha) é identificador
auxiliar. Quando `get_company_onboarding_contract` citar o motivo
`adocao_matricula_esocial`, adote a matrícula eSocial pela seção "Adotar a
matrícula do eSocial", abaixo. Sem esse sinal no contrato, não grave matrícula
nova por worker `identifier_only` (restauração, troca de código Domínio ou
qualificação por onboarding comum, nas seções abaixo) sem falar antes com a
engenharia. Restauração e troca continuam no namespace `dominio`.

## Restaurar uma matrícula sobrescrita

Só depois de combinar com a operadora. Não restaure por iniciativa própria:
nenhuma matrícula corrigida por ela é revertida sem combinar antes. Para cada
vínculo, combine com ela o valor certo e a fonte, e guarde a mensagem dela: o
texto literal e a referência, por exemplo `CX-…`. Os campos novos do worker
exigem Refresh do conector e conversa nova.

1. Leia `get_company_employee_history` (com `process_type`) e anote
   `identifiers.matricula`. Esse é o valor atual literal.
2. Antes de restaurar, confira com a operadora os casos do vínculo: casos em
   revisão, aprovados ou publicados bloqueiam a restauração; casos de folha
   abertos com a matrícula atual vão precisar de reenvio (passo 6).
3. Crie um lote de onboarding da empresa e anexe o documento Domínio de onde
   sai o código, por exemplo o Extrato. Use `attach_onboarding_source` ou o
   envio autenticado.
4. Envie um worker com `existing_employee_id`, `identifier_only: true`,
   `reuse_registered_company: true`, `matricula: <código Domínio>`,
   `matricula_namespace: "dominio"`, `matricula_source` apontando para o
   documento anexado (`document_id`, `content_hash`, `locator`),
   `expected_current_matricula: <valor atual literal>` e
   `restoration_declaration: {human_message, message_reference, reason}`. Além
   de `human_message` (a mensagem literal da operadora), informe pelo menos
   `message_reference` ou `reason`.
5. Rode `validate_company_onboarding`, mostre a linha à operadora e rode
   `apply_company_onboarding` com o `validation_hash`. É preciso ter
   `corrigir_dados`. Recusas:
   - `matricula_esperada_divergente`: o valor mudou. Releia e confirme com a
     operadora.
   - `matricula_atual_qualificada_por_onboarding`: o valor atual tem recibo de
     onboarding com fonte (inclusive uma confirmação do mesmo valor). Não pode
     ser trocado pela restauração simples: se o Domínio trocou o código do
     mesmo contrato, use a troca de código abaixo; senão, `registrar_problema`.
   - `restauracao_matricula_valor_legado_use_reparo`: o valor atual é legado e
     reparável. Combine com a operadora e faça o reparo de namespace
     (`repair_employee_identifier_namespace`) com o `onboarding_id` e o
     `worker_ref` de `diagnostic.previous_origin`. Depois, qualifique o código
     Domínio por um onboarding comum (`identifier_only` sem
     `expected_current_matricula`).
   - `restauracao_matricula_legado_nao_reparavel` e
     `restauracao_matricula_vinculo_reparado`: não há caminho automático. Não
     tente de novo; use `registrar_problema` e leve à engenharia.
   - `restauracao_matricula_em_uso_na_empresa`: o código já pertence a outro
     vínculo. Não force; use `registrar_problema`.
   - `restauracao_matricula_exige_conciliacao_de_consumidores`: há caso do
     vínculo em revisão, aprovado ou publicado. Leve a lista
     `diagnostic.consumers` à operadora; nada foi alterado.
   - `restauracao_matricula_exige_fonte_documental`: anexe o documento.
   - `snapshot_desatualizado`: valide de novo.
   - `matricula_do_vinculo_conflitante`: faltou `expected_current_matricula`.
   - erro de validação `restauracao_de_matricula_exige_*`: falta a declaração
     ou ela está incompleta.
6. Depois de restaurar:
   - A folha passa a resolver pelo código Domínio. Um caso de folha aberto que
     traz a matrícula antiga no payload fica pendente
     (`vinculo_nao_identificado_na_competencia`) até você reenviar o payload
     com o código Domínio.
   - Refaça a seleção de histórico com `pin_company_employee_history`, porque
     os pins anteriores ficam `historico_desatualizado`.
   - Refazer a população pode mudar quem entra na folha e invalida a
     conferência feita antes. Combine com a operadora antes de refazer meses
     já conferidos.
   - Casos de vínculo único continuam ligados ao vínculo, mas a matrícula
     antiga no payload deles não é corrigida. Não crie casos novos com o
     código antigo: eles são recusados.

**Matrícula vinda do caso.** Quando o `create_case` preenche uma matrícula
vazia, a trilha do caso registra `vinculo_matricula_introduzida_pelo_caso`:
origem caso, sem fonte documental, com o valor guardado só como chave cifrada.
Esse valor pode ser substituído depois pelo código Domínio com o mesmo
procedimento. Continue omitindo `funcionario.matricula` no `create_case`
quando ela não vier do documento do caso.

## Troca de código Domínio do mesmo contrato

Quando usar: o Domínio passou a usar outro código de empregado para o mesmo
contrato (mesmo CPF e admissão, sem nova admissão no eSocial), e o Loki ainda
guarda o código antigo, qualificado por onboarding. Se o vínculo aparece
desligado por engano pelo cadastro, revogue o desligamento antes (seção
seguinte). Exige Refresh do conector e conversa nova, por causa do campo
`motivo`.

Provas: o Extrato (ou outro relatório do Domínio) **com o código novo**,
anexado ao lote. Não reanexe o documento que qualificou o código antigo. Também
é preciso a mensagem literal da operadora com a referência da Caixa (`CX-…`):
neste motivo, `message_reference` com prefixo `CX-` é obrigatória e `reason`
sozinho não basta.

Como enviar: worker `identifier_only` com `existing_employee_id`,
`matricula` = código novo, `matricula_namespace: "dominio"`,
`matricula_source` = o extrato novo anexado, `expected_current_matricula` =
código atual literal e
`restoration_declaration = {human_message, message_reference: "CX-…", motivo: "troca_de_codigo_dominio"}`.
Depois `validate_company_onboarding` e `apply_company_onboarding` (exige
`corrigir_dados`). Sem `motivo`, o worker segue a restauração da seção
anterior.

Recusas:

- `troca_de_codigo_dominio_exige_codigo_qualificado`: o código atual não veio
  de onboarding Domínio. Use a restauração sem motivo.
- `troca_de_codigo_dominio_fonte_do_codigo_anterior`: a fonte é o mesmo
  documento que qualificou o código atual. Anexe o extrato com o código novo.
- `troca_de_codigo_dominio_exige_message_reference_cx`: falta a referência
  `CX-…` da mensagem da operadora.
- `restauracao_matricula_exige_conciliacao_de_consumidores`: revise os casos
  listados antes. Se o diagnóstico trouxer
  `closed_consumers_without_closed_history`, a folha fechada não tem o
  histórico fechado do vínculo (aprovação antiga) e a troca não segue por
  este caminho: leve à engenharia.
- `restauracao_matricula_vinculo_reparado`: leve à engenharia.
- `matricula_esperada_divergente`: refaça a leitura do código atual.

Efeito: o código antigo fica como identificador histórico, sem uso
operacional. Voltar a um código antigo do mesmo vínculo é permitido e fica
registrado no recibo. Folhas abertas com o código antigo ficam pendentes:
reenvie a população com o código novo. Casos de vínculo único seguem pelo
`funcionario_id`. As seleções históricas do vínculo ficam desatualizadas e
precisam ser refeitas. Folhas aprovadas ou publicadas que só citam o código
antigo e já têm o histórico fechado do vínculo naquela competência não
impedem a troca e não são alteradas; esse histórico continua ligado ao
vínculo pelo `funcionario_id`, e o recibo da troca lista esses casos. Sem o
histórico fechado (aprovação antiga), a folha impede a troca. Os demais casos
aprovados ou publicados do vínculo, e qualquer folha em revisão com o código
antigo, impedem a troca até serem revisados.

## Adotar a matrícula do eSocial

Vale quando `get_company_onboarding_contract` citar o motivo
`adocao_matricula_esocial`; sem isso, o servidor ainda não tem a adoção. Vale
para todo vínculo carregado com código Domínio (`matricula_namespace:
"dominio"`). O deploy não muda nenhum caso: só a adoção muda. Usa o
onboarding de sempre, com os campos da restauração (Refresh da 2.8.0, se
ainda não feito). Exige pessoa com `corrigir_dados`: a automação com
`carga_historica` não adota: o apply dela é recusado inteiro com
`restauracao_matricula_exige_corrigir_dados`, sem aplicar nada.

Antes de adotar, para cada empresa:

1. Liste as folhas não finais (`listar_casos`). Folha em revisão bloqueia a
   adoção: combine com a operadora `restart_case` antes. Folha aberta que já
   cita um valor que vai virar a matrícula eSocial de outro vínculo faz a
   adoção recusar (`adocao_matricula_esocial_valor_citado_em_folha_aberta`,
   com os `case_id`): combine com ela se a folha será cancelada ou terá a
   população corrigida.
2. Obtenha a matrícula eSocial de cada vínculo no eSocial (S-2200 ou consulta
   de trabalhadores) e anexe o original ao lote (`attach_onboarding_source`
   ou o envio autenticado). Pode ser o mesmo relatório que traz o código
   Domínio. Nunca deduza a matrícula pelo formato ou pela igualdade com o
   código.

Adotar, com **um lote por empresa** (`reuse_registered_company: true`):

3. Para cada vínculo com código Domínio, um worker com `existing_employee_id`,
   CPF e admissão exatos; `identifier_only: true`; `matricula` = matrícula
   eSocial e `matricula_namespace: "esocial"`; `matricula_source` apontando o
   original anexado (`document_id`, `content_hash`, `locator`);
   `expected_current_matricula` = código Domínio atual, literal, lido em
   `get_company_employee_history`; e `restoration_declaration` com o
   `human_message` literal da operadora, `message_reference` `CX-…` e
   `motivo: "adocao_matricula_esocial"`. O valor eSocial pode ser igual ao
   código.
4. Vínculo ainda sem matrícula: só `matricula`, `matricula_namespace:
   "esocial"` e a fonte, sem CAS nem motivo.
5. `validate_company_onboarding` e mostre à operadora a prévia por vínculo:
   prontos, recusas com `reason`/`diagnostic` e o que cada aplicação vai
   deixar para refazer. Só depois do aceite dela, `apply_company_onboarding`
   com o `validation_hash`. O Loki deriva a permissão de restaurar da
   capacidade `corrigir_dados`; não há argumento para isso.

Recusas:

- `matricula_esocial_em_uso_no_empregador`: a mesma matrícula está em outro
  vínculo da mesma raiz de CNPJ (o mesmo CPF em outro estabelecimento da raiz
  conserva a matrícula). Confira a fonte com a operadora; não force.
- `adocao_matricula_esocial_exige_codigo_dominio`: o valor atual já está
  qualificado em outro namespace (inclusive o próprio eSocial). Leve à
  engenharia.
- `matricula_esocial_exige_adocao_auditada`: faltou o motivo ou o CAS sobre
  um código Domínio.
- `codigo_dominio_e_auxiliar_em_vinculo_esocial`: o vínculo já está no
  eSocial; o código Domínio não volta a ser operacional.
- `empresa_adotou_matricula_esocial`: código Domínio para vínculo sem
  matrícula em empresa que já tem vínculo no eSocial. Declare a matrícula
  eSocial.
- `restauracao_matricula_exige_conciliacao_de_consumidores`: caso em revisão
  ou folha fechada sem histórico fechado. Veja `diagnostic.consumers`.
- Erro de validação `adocao_matricula_esocial_exige_message_reference_cx` ou
  `adocao_matricula_esocial_exige_identifier_only_esocial`: falta a
  referência `CX-` ou o worker não é `identifier_only` com
  `matricula_namespace: "esocial"`.
- `matricula_esperada_divergente` e `snapshot_desatualizado`: como na
  restauração.

Depois de adotar, leia `adoption_effects` de cada recibo e mostre à operadora. Ele vem na
própria linha `applied` do `apply_company_onboarding` (e do `validate_company_onboarding`
quando a linha já está aplicada), junto de `released_closed_consumers`, inclusive na
repetição com `validation_hash` antigo. Para reler depois, use
`get_employee_identifier_state`, em `applied_receipts[].matricula_restoration`
(`matricula_restoration.adoption_effects`, `released_closed_consumers` e
`previous_identifier`, sem PII):

- `open_payrolls_citing_previous_code`: folhas abertas que citam o código
  antigo e ficam `matricula_coincide_com_codigo_auxiliar` até reenviar a
  população com as matrículas eSocial (domínio `folha_mensal`, "Matrícula do
  eSocial na população da folha");
- `stale_history_pins`: refaça o pin (`pin_company_employee_history`) com o
  `history_hash` novo;
- `transitional_collisions`: outro vínculo ainda usa o mesmo valor como
  código Domínio; adote-o também.

`released_closed_consumers` lista os casos fechados do vínculo, que não
bloqueiam. O código antigo fica em `identifiers` com `status: "auxiliar"`,
consultável e nunca operacional. Daqui em diante, população de folha, linha
de reajuste e caso individual usam a matrícula eSocial; caso novo com o
código Domínio recusa `matricula_funcionario_divergente`. Cliente novo
declara a matrícula eSocial desde o onboarding. Casos fechados continuam com
o código antigo impresso: não reabra nem recalcule por causa da adoção.

## Recusas de nome e de vigência no onboarding (2.11.0)

Valem quando `get_company_onboarding_contract` trouxer o mapa `refusals` (Project-loki
#422); ele descreve cada recusa e aviso com `meaning` e `next_action`. Os diagnósticos
não trazem nome, valor de campo nem outro dado pessoal.

- `nome_do_vinculo_conflitante` (`fields: ["workers[].nome"]`): o nome declarado difere
  do gravado no vínculo existente. Leia `identity.nome` em
  `get_company_employee_history` e declare o nome literal. Se for o cadastro que está
  errado, use `name_correction` (com `reuse_registered_company`, `expected_name` literal,
  mensagem e motivo humanos); só quem tem `corrigir_dados` corrige.
- `fato_historico_conflitante` com `dated_field_value_conflict`: um fato do próprio
  candidato declara, para o mesmo tipo, data de efeito e campo, valor diferente do já
  registrado. O diagnóstico traz `diagnostic.conflict` com `kind`, `effective_on`,
  `field`, `existing` e `incoming`, cada lado como `event{origem, seq}`,
  `onboarding_fact{fact_id}` ou `candidate`, sem os valores. Confira os valores na mesma
  vigência no histórico do vínculo e corrija a declaração, ou revogue ou substitua o
  fato anterior.
- Só recusa quando o conflito envolve fato do próprio candidato. Conflito antigo entre
  fato e evento já gravados, alheio ao candidato, vira o aviso `existing_dated_conflict`
  (em `rows[].warnings`, com o detalhe em `rows[].warning_details[].conflict`): o
  candidato continua `ready`, o `validation_hash` segue coerente e o aviso não altera o
  apply. É informativo; confira o histórico se o conflito importar ao DP.
- `aplicacao_sequencial_por_vinculo` (aviso, não bloqueia): mais de uma referência
  `ready` da mesma pessoa no mesmo validate. O apply grava uma por vez e as demais podem
  recusar com `snapshot_do_vinculo_desatualizado` (o vínculo mudou entre validate e
  apply). Junte os fatos de uma pessoa num único candidato; se já enviou separado, repita
  `validate_company_onboarding` e o apply com o `validation_hash` novo a cada referência.
  Um candidato por pessoa por chamada continua valendo.

## Revogar desligamento gravado pelo onboarding

Quando usar: o Loki mostra o vínculo desligado (`desligado_em`, fora da
população da folha) por uma rescisão que veio do cadastro de onboarding, e a
operadora confirma que o contrato segue ativo; por exemplo, o eSocial tem o
S-2200 e nenhum S-2299, e o Domínio só trocou o código do empregado. Não use
para desfazer rescisão calculada por caso: essa segue o cancelamento do caso.

Provas necessárias:

1. Anexe ao lote de onboarding (`attach_onboarding_source` ou
   `register_onboarding_harness_source`) o documento que mostra o vínculo
   ativo, por exemplo o extrato do eSocial sem S-2299. Declaração no chat não
   basta como fonte.
2. Mensagem literal da operadora pedindo a revogação, com a referência da
   mensagem (`CX-…`) ou o motivo.

Passos:

1. `get_company_employee_effect_state` para achar o `target_fact_id` (fato
   `rescisao`, `effect_state: active`).
2. `preview_onboarding_termination_revocation(onboarding_id, target={funcionario_id, target_fact_id, source})`.
   Mostre à operadora: data do desligamento, fonte, estado depois
   (`projected_state_after.desligado_em: null`) e `open_consumers`.
3. Com o aceite explícito,
   `revoke_onboarding_termination(onboarding_id, request={schema_version: "loki.company-onboarding-termination-revocation/1", intent: "revoke_onboarding_termination", request_ref, funcionario_id, target_fact_id, source, preview_id, expected_snapshot, human_message, message_reference ou reason})`.
4. As duas ferramentas são novas e aparecem só depois do Refresh do conector e
   de uma conversa nova. Antes disso, ou se não aparecerem no catálogo, use o
   transporte já servido
   `receive_case_data(case_id="@connector", request={schema_version: "loki.connector-command/1", operation: "preview_onboarding_termination_revocation" | "revoke_onboarding_termination", onboarding_id, target | request})`,
   com a mesma autoridade.

Se a prévia mostrar `open_termination_cases` (caso de rescisão ou aviso de
rescisão do próprio vínculo em aberto), confirme com a operadora que a
revogação vale mesmo assim e envie `revoga_com_rescisao_aberta: true`; sem
isso recusa com `onboarding_termination_revocation_open_termination_case`. A
confirmação fica no recibo. Se a prévia mostrar `same_cpf_active_employee_ids`,
a mesma pessoa tem outro vínculo ativo na empresa (provável cadastro duplicado
por troca de código). Mostre isso à operadora antes de seguir.

Recusas:

- `…requires_consumer_reconciliation`: há caso do vínculo, ou caso da empresa
  a partir do mês do desligamento, em revisão, aprovado ou publicado. O Loki
  não reabre caso fechado. Revise cada consumidor listado antes.
- `…snapshot_changed`: refaça a prévia.
- `…requires_documentary_source`: anexe a fonte ao mesmo lote.
- `onboarding_termination_revocation_effect_unresolved`: a rescisão do
  cadastro não tem evento (fundamento não qualificado ou campo faltando). Ela
  não tira a pessoa da folha, mas fica no histórico. Registre como problema.
- `onboarding_termination_fact_revoked`: uma rescisão verdadeira na mesma data
  da revogada não entra pelo onboarding; use o caso de rescisão. Não reenvie a
  rescisão revogada.

Efeito nas folhas abertas: nada é recalculado sozinho. Cada folha aberta da
empresa a partir do mês recebe na trilha `populacao_desatualizada_por_revogacao`.
Folhas abertas a partir do mês do desligamento passam a aceitar a pessoa na
população: refaça a preparação, incluindo a pessoa, e refaça as seleções
históricas (pins), que ficam desatualizadas. Casos de 13º, férias e rescisão
abertos deixam de ver o desligamento na próxima leitura do histórico. Folhas e
casos fechados não mudam. Depois da revogação, se o Domínio trocou o código do
empregado, faça a troca auditada do código (seção anterior).

## Retirar saldo de férias gravado pela carga histórica (2.12.0)

Vale quando o catálogo da conta mostrar
`preview_onboarding_vacation_balance_retirement` e
`retire_onboarding_vacation_balance` (backend #438, ADR-043). **Ferramentas
novas: exigem Refresh do conector e conversa nova**; antes disso use o transporte
`receive_case_data(case_id="@connector", request={schema_version:
"loki.connector-command/1", operation: "preview_onboarding_vacation_balance_retirement"
| "retire_onboarding_vacation_balance", onboarding_id, target | request})`, com a
mesma autoridade.

**Quando usar.** A carga histórica gravou um `vacation_balance` com período
aquisitivo que **não existe** (série errada na planilha). `replaces_fact_id` só
troca o período por outro; para só tirá-lo de vigor existe este ato humano
auditado, irmão da revogação de desligamento. Não serve para corrigir o
aquisitivo (use a troca explícita) nem para saldo que existe.

**Quem pode.** A prévia é leitura de pessoa provisionada com acesso ao lote. O ato
exige pessoa provisionada com `carga_historica`, `configurar_cliente`, `decidir_chat`
e `corrigir_dados` e `CHAT_DECISIONS_ENABLED`; rotina não faz.

**Passos.**

1. Anexe ao lote de onboarding a fonte que mostra a série correta (por exemplo a
   Programação de Férias do Domínio). Declaração nativa não basta.
2. `get_company_employee_history` e ache os `target_fact_ids` (`ONBFACT-…`, de 1
   a 20 saldos vigentes do **mesmo** vínculo, sem repetição).
3. `preview_onboarding_vacation_balance_retirement(onboarding_id,
   target={funcionario_id, target_fact_ids, source})`. Mostre à operadora os
   períodos retirados, os que restam (`periods_after`), os casos abertos que
   ficarão com a seleção histórica desatualizada (`open_consumers`), `snapshot`
   e `preview_id`. Não grava e não certifica a fonte.
4. Com o aceite explícito e a mensagem literal,
   `retire_onboarding_vacation_balance(onboarding_id, request={schema_version:
   "loki.company-onboarding-vacation-balance-retirement/1", intent:
   "retire_onboarding_vacation_balance", request_ref, funcionario_id,
   target_fact_ids, source, preview_id, expected_snapshot (o `snapshot` da
   prévia), human_message, message_reference ou reason})`. Replay exato devolve
   o recibo.

**Efeito.** Só um recibo em `company_onboarding_reconciliations`; o fato fica
arquivado e some do histórico, da projeção de períodos, da conferência de
sobreposição e de movimentos pendentes e do `state_hash`. Aparece em
`revoked_onboarding_facts` de `get_company_employee_history` e como
`revocation_receipt` em `get_company_employee_effect_state`. Nada é apagado nem
recalculado, e caso fechado não muda sozinho. O aquisitivo certo entra como fato
novo; reenviar o saldo retirado recusa (`onboarding_vacation_balance_fact_retired`)
e corrigir o retirado também (`onboarding_vacation_balance_target_retired`).

**O que bloqueia** (a prévia recusa sem gravar; prefixo
`onboarding_vacation_balance_retirement_`, salvo onde indicado):

- `target_incompatible` (fato fora do vínculo) e `target_not_vacation_balance`;
- `onboarding_vacation_balance_already_retired`, `target_replaced` e
  `target_is_correction` (retirar uma correção traria o corrigido de volta);
- `requires_documentary_source`: fonte ausente ou nativa;
- `period_has_vacation_use`: há gozo vigente no período; corrija o gozo antes;
- `period_schedule_pending`: há programação de férias vigente no período;
  cancele com `record_vacation_schedule`;
- `onboarding_vacation_balance_qualifies_legacy`: o saldo qualifica fato legado;
  qualifique o legado por outro saldo antes de retirar;
- `requires_consumer_reconciliation`: caso do vínculo, de qualquer tipo, ou caso
  da empresa com pin do histórico dele (folha mensal, 13º etc.) em
  `aguardando_revisao`, `aprovado` ou `publicado`; revise cada consumidor
  listado antes (os abertos entram em `open_consumers`, não bloqueiam);
- `snapshot_changed` na escrita: refaça a prévia;
- `onboarding_reconciliation_request_conflict`: mesmo `request_ref` com pedido
  ou pessoa diferentes.

**Regra operacional.** **Nunca declare na rescisão** um período de saldo que
não existe, retirado o saldo ou não: a retirada só tira o fato do histórico e da
projeção de períodos; o que a rescisão declara continua sendo da harness.

## Declaração adicional no onboarding

Use `get_company_onboarding_contract.additional_declaration_reconciliation`
quando publicado. `get_company_employee_effect_state` lê fatos/eventos e
compensações; `preview_company_onboarding_reconciliation` apresenta os seletores,
diferenças e snapshots. Após ato específico da pessoa habilitada,
`reconcile_company_onboarding` registra `reconciled_to_existing_fact`.
O recibo não comprova equivalência factual: preserva separadamente declarações,
fundamentos e efeito canônico. Não troca basis, não cria rescisão e não atualiza
fatos, eventos, pins ou casos. `reconciled_count` não é `applied_count`.
`CHAT_DECISIONS_ENABLED`, capacidades humanas, escopo, CAS e replay permanecem;
automação não ganha autoridade. Transporte alternativo somente no
`compatibility_transport` servido, com os mesmos gates do escritor.

## Corrigir parâmetro já aplicado no onboarding (2.9.8)

Vale quando `get_company_onboarding_contract` apresentar a regra de
`replaces_fact_id` para `parametrizacao` (a pensão com vigência ou valor
errados, por exemplo). Envie um novo fato `parametrizacao` com
`replaces_fact_id` do fato aplicado, pelo mesmo vínculo
(`existing_employee_id`), com os mesmos campos, a data certa, fonte própria e
sem `missing_fields`. O fato antigo continua arquivado e deixa de valer em todos
os cortes; o evento dele recebe `evento_revertido` e o substituto grava o seu.
Encerrar um parâmetro continua sendo um fato novo datado com o valor de fim
(por exemplo `pensao_alimenticia_regra: null` a partir do fim), sem
substituição. Casos abertos do vínculo ficam com a seleção histórica
desatualizada e releem o estado na próxima preparação.

Recusas `parameter_replacement_*`: `requires_dated_complete_fact` (falta data,
campo ou fonte), `target_outside_employee`, `target_not_parameter`,
`target_already_replaced` (corrija o substituto vigente),
`fields_incompatible` (campo diferente é outro fato), `no_change`,
`multiple_candidates` e `requires_consumer_reconciliation` (há caso em revisão,
aprovado ou publicado do vínculo desde a menor das duas vigências: o
diagnóstico lista os casos e o CAS de cada um; concilie antes, sem reiniciar
nem recalcular por conta própria). Caso protegido sem competência é datado
pelo fato do processo (desligamento, início do gozo, admissão); sem essa data a
recusa é `parameter_replacement_consumer_reference_date_unknown`, com o caso no
diagnóstico: leve à engenharia.

## Consignado: contrato, competência e rescisão

Consulte `get_company_onboarding_contract` e os parâmetros efetivamente
oferecidos. `credito_trabalhador_contratos` registra revisões de contrato,
número como string, instituição, vigência, parcela em centavos e
`rubrica_loki` explícita. Encerramento/cancelamento é outra revisão;
não altere revisões antigas nem presuma rubrica por código numérico global.

**Alocação entre contratos (2.9.8).** Vale quando o contrato servido de
onboarding mostrar `data_inicio_contrato` em `credito_trabalhador_contratos`.
Registre nesse campo o `dataInicioContrato` da Dataprev (o dia exato, diferente
de `inicio`, a competência do primeiro desconto) numa **nova revisão** de cada
contrato: revisão gravada não se altera. Uma data diferente da `dataInicioContrato` da
consulta Dataprev fica com `mapping_contract_mismatch`.

- Com **2 ou mais contratos confirmados no mês**, a soma respeita o teto de 35%
  e o Loki desconta do contrato mais antigo para o mais recente pela data de
  início (Portaria MTE 435/2025, art. 49-C). O que não couber vira saldo não
  descontado, na memória (`saldo_nao_descontado_cents`) e no holerite. Com 1
  contrato, nada muda.
- Acima do teto, o caso fica pendente sem a data
  (`credito_trabalhador_data_inicio_contrato_pendente`) ou com datas iguais
  (`credito_trabalhador_contratos_com_mesma_data_de_inicio`: leve à DP; o Loki
  não desempata). Dentro do teto a ordem não importa e a data não é exigida.
- `credito_trabalhador_desconto_fora_dos_contratos`: lançamento numa rubrica de
  crédito que algum contrato da empresa nomeia, sem contrato desta pessoa nela.
  Registre o contrato ou retire o lançamento. `credito_trabalhador_alocacao_pendente`
  deixa de ser emitido.
- A folha com alguém de 2 ou mais contratos confirmados ganha o sufixo
  `-worker-credit-allocation-v1` e precisa de `restart_case` e novo cálculo,
  mesmo se o valor não mudar.
- A correção auditada de `parametrizacao` (seção acima) não trava mais a
  revisão do contrato: o ato substituído deixa de contar nela.

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
e vigência parcial conservam pendência/necessidade de segmentação. Exceção
da folha `folha-v31`: insalubridade com `vigente_desde` igual à data de
admissão cobre o mês de entrada, paga pelos dias (domínio `folha_mensal`).

Elegibilidade difere de valoração: base, percentual, divisor, quantidade e
incidências dependem do mapa/regra qualificados; não invente fórmula universal.
Aplique cadastro somente por `validate_client_config`/`apply_client_config`
autorizados, com CAS e releitura. Parâmetros individuais seguem onboarding próprio.
Fonte informal atribuída pode ser aceita; confira consumo na memória por pessoa.


Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Quando o contrato atual oferecer o processo, prepare o conteúdo de `dados_alteracao_cadastral` e envie por `receive_case_data`. A proposta compara valores anteriores do perfil datado com valores novos fonteados, vigência e contexto capturado. Não declare anteriores apenas por relato nem substitua o hash esperado para contornar conflito de perfil.

O pacote factual contém recibo e artefatos JSON, sem PDF; `supports_apply=false` indica ausência de aplicação ao cadastro operacional. O recebimento dos dados prepara o caso; aplicação ao perfil exige a ação específica autorizada no contrato. Confira contexto, diferenças, fontes, hashes e pendências pelos checks do contrato e mecanismos de verificação/revisão da versão. Perfil alterado exige nova captura/versionamento.

Revisão e aprovação documental não aplicam salário, cargo, jornada ou outros dados ao cadastro. Qualquer efeito operacional exige fluxo e intenção humana específicos que o host efetivamente suporte. Preserve a proposta parcial se faltar fato, vigência ou fonte.

Para empresa e estabelecimentos, parâmetros e regras e demais dados vinculados, descubra os contratos e escritores HTTPS vigentes. Confira o CNPJ e o escopo da identidade autenticada, a revisão esperada, vigência, fontes, diferenças e histórico. Não use o caso de alteração do empregado como substituto de um contrato empresarial ausente nem atualize outra empresa do mesmo grupo. Preserve intenção/revisão exigidas, envie apenas parâmetros estruturados e obtenha recibo persistido; depois releia o objeto empresarial para conferir revisão e valores aplicados. Staging, proposta e recibo de recebimento não comprovam ajuste aplicado. Endpoint ou campo ausente é lacuna contratual explícita.

Toda operação usa o conector HTTPS `https://loki.izzicontabil.com.br/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

O cadastro empresarial usa os escritores existentes: consulte `get_client_config(cliente_slug)` e `get_client_config_history(cliente_slug)`, prepare `alteracoes` na harness e valide por `validate_client_config`. Use o `doc_hash` atual como `expected_hash`; vigência permanece nos campos tipados da regra, sem substituir cadastro vigente por rascunho. Aplique somente pelo `apply_client_config` autorizado, com `motivo`, mesmas alterações, hash e flags necessários; depois releia cadastro/histórico. `RASCUNHO` e `SEM_ALTERACAO` não comprovam aplicação; somente o resultado `APLICADO` com nova revisão/hash relidos sustenta essa afirmação.

`proveniencia` é opcional nos dois escritores. Quando utilizada, segue `loki.company-config-provenance/1` com `field_sources` por caminho alterado e `kind=declaration|inference|context|external_reference|rule`; referência, localizador, `content_hash` e `foundation` são opcionais, sem documento ou hash inventados. Fontes parciais recebem declaração do ator nos demais campos. Sem origem detalhada, o próprio request autorizado é declaração. O recibo/resumo retorna `receipt_hash`, `actor_id`, `input_hash`, `fields` e `assurance`, sem expor texto livre; preserve-o e confira os valores pelo readback autorizado. A resposta e a releitura preservam `field_basis` por caminho; inference/context usam `inferred`, sem promover informação recebida ou inferida a confirmed automaticamente.

Campo reservado ou gate que realmente exige evidência usa `confirmacao` específica. Primeiro valide com `expected_hash` do mesmo CAS e `reserved_paths`/`evidence_gate_paths` exatos; mostre a prévia ao humano e aplique com o mesmo objeto e `human_message` efetiva. Só pessoa provisionada com configurar_cliente e autoridade administrativa vigente realiza esse ato. A automação não recebe essa autoridade por usar lote ou empresa de teste. Não use confirmação genérica, outro CNPJ ou nova referência para contornar conflito; pendência específica não exige fonte formal universal.

## eSocial por empresa

Consulte `get_company_esocial_contract()` (`loki.company-esocial/1`) e
`get_company_esocial_state(company_id)` antes de propor modo. Os destinos são
`homologacao`/`tp_amb=2` e `operacao`/`tp_amb=1`. Sem decisão, o retorno
conservador de homologação tem `persisted=false` e revisão0; não transmite.
`preview_company_esocial_mode` exige administrador humano provisionado, empresa
explícita, proposta e `expected_revision`. Apresente escopo/corte/pendências e
`preview_hash`; somente a intenção humana específica autoriza chamar
`apply_company_esocial_mode` com proposta e decisão (`expected_revision`,
`preview_hash`, `reference`, `human_message`). Releia estado/recibo. Identidade
vem do HTTPS; automação e documento aprovado não concedem essa autoridade.

`production_activation_supported=false`: Operação fica PENDING e sua aplicação
recusa `esocial_activation_pending` enquanto faltarem executor/fila fiscal,
assinatura, representação/procuração e recibo de homologação verificados.
Homologação persistida mantém `fiscal_events_sent=0`; ausência de modo também
não transmite. Preparar XML/XSD S-1005 local não comprova transmissão nem
assinatura/aceite/prontidão. Esta entrega não oferece ferramenta HTTPS de
emissão, provisionamento ou envio fiscal. Importação histórica não cria saída;
mudança de modo não redireciona filas nem retransmite histórico. Não invente
ferramentas futuras, flag liberatória, DOC ou etapa de painel/SSH.

Consulte `get_company_parameter_state(company_id, effective_on)` para selecionar
parâmetros por estabelecimento e data. A orientação detalhada de cadastro e
consumo está em `alteracao_cadastral`; modo fiscal e perfil empresarial são
registros distintos e nenhum deles comprova transmissão.

Perfis `company_parameters` declaram `id`, `establishment_cnpj`, `valid_from` e
`valid_until`, sem sobreposição de vigência; `cnae_preponderante`,
`rat_bps` (100/200/300), `fap_10000` (escala10000), `classificacao_tributaria`,
`fpas` e `codigo_terceiros` são opcionais. Preserve códigos como texto e taxas
como inteiros; desconhecido permanece ausente/nulo, não complete zero. Selecione
o CNPJ exato e a data efetiva, sem herança de matriz/filial ou vigência expirada.
`basis=informado|inferido|confirmado` preserva qualificação declarada e
`field_sources` é opcional, parcial, sem documento/hash universal. Origem é
declaração autenticada da harness, não confirmação independente dos originais.

Escreva a coleção atômica pelo caminho
`empresas[CODIGO_DOMINIO].company_parameters` de `validate_client_config` e
`apply_client_config`, preservando perfis anteriores, `expected_hash` do CAS,
confirmações específicas e demais campos. Não invente código Domínio. Releia
cadastro/histórico e `get_company_parameter_state`; preserve `profile_id`,
`profile_hash` e pin `client_config` (`version`, `doc_hash`, `slice_hash`).
Perfil SELECTED pode conter pendências: `financial_readiness_verified=false`
e `transmission_verified=false` deixam explícito que declaração, persistência
e seleção não comprovam consumo financeiro nem transmissão. Use somente a
referência corrente quando o contrato consumidor a aceitar e confira seu resultado;
não afirme cobertura de processos sem prova própria.

Quando o schema do cadastro trouxer `empresas[].ferias_recibo`, a política do
recibo de férias da empresa (divisor do mês civil e arredondamento verba a
verba) segue o mesmo caminho, em `empresas[CODIGO_DOMINIO].ferias_recibo`, só
quando a operadora disser que a empresa usa essa regra. Campos, vigência e
efeitos no domínio `ferias` ("Divisor e arredondamento do recibo").


## Preparação fiscal persistida

Consulte `get_company_esocial_candidate_contract()` (`loki.company-esocial-candidate/1`).
`prepare_company_esocial_candidate` registra somente S-1005 por pedido explícito
com empresa/estabelecimento, inclusão ou alteração, vigência fiscal, perfil/pin,
revisão do modo e ambiente exatos. Siga o schema retornado; não deduza a operação
ou os antecedentes pelo cadastro local. O servidor fixa ID e XML sem assinatura;
`PREPARED_UNSIGNED` não é envio pronto. Consulte `get_company_esocial_candidate`
para recuperar o mesmo candidato e preservar seus bytes/hash, referência e revisão.
`cancel_company_esocial_candidate` usa CAS e motivo, preservando o histórico.

`transmission_ready=false`: esta etapa não oferece assinatura, envio, claim nem
provisionamento de autoridade fiscal. Importação histórica não cria candidatos;
mudança do modo não redireciona os anteriores. Não use a autoridade do worker de
suporte ou `operar_casos` como autorização fiscal. Assinatura, representação e
recibo oficial de homologação continuam pendentes; não ative Operação.

Em parâmetros empresariais, `valid_until` pode ser omitido ou null para
fim não informado; não invente data final. Preserve `valid_from`, CNPJ, fontes
opcionais e pendências, inclusive FAP ausente. Isso não confirma continuidade
normativa, encargo ou ausência de alterações. Sobreposições continuam recusadas.

Um relatório de movimentações pode qualificar CPF, matrícula, admissão e recibos
para conciliar o episódio com XMLs já disponíveis. Verifique os originais e as
retificações; o relatório não fornece o conteúdo completo do contrato ou da folha.
Use o XML para seus valores e preserve a proveniência de cada fato. Não peça
novamente S-2200 para provar a mesma identidade já conciliada por fontes suficientes.


Referências diferentes podem preparar drafts distintos. O contrato declara
`allowed_multiple_preparations=true` e `execution_deduplication_verified=false`;
idempotência do pedido não é deduplicação fiscal para uma futura execução.

## Categoria eSocial do vínculo no cadastro (2.13.0)

Vale quando `get_company_onboarding_contract` listar `categoria_esocial` em
`employee_parameters.data_schema` (texto de 3 dígitos, padrão `^[0-9]{3}$`, opcional) ou
`get_process_contract("alteracao_cadastral")` trouxer a mesma propriedade em
`dados_alteracao_cadastral.changes`. É parâmetro individual do vínculo e a fonte da
categoria para a folha e para os demais processos. Nenhuma ferramenta é nova e o
`tools/list` não mudou: não há Refresh do conector; o que mudou foi o contrato do
processo, que você lê pelo `get_process_contract`.

**Data de efeito: o início da pessoa naquela categoria** (em geral a admissão ou o
início do vínculo na categoria), **nunca a data do envio**. A folha, o 13º e a
rescisão leem a categoria vigente na competência do próprio processo: com a data de
hoje, os meses anteriores não a enxergam, a folha calcula a pessoa como empregada e o
13º ou a rescisão são criados. O campo da data é `effective_on` na alteração cadastral e no fato do onboarding
(`data_efeito` no perfil documental).

- **Caminho 1: alteração cadastral** (declarar ou corrigir a categoria de uma pessoa
  já cadastrada). O caso `alteracao_cadastral` aceita `categoria_esocial` em
  `dados_alteracao_cadastral.changes`, ao lado dos outros campos do perfil.
  1. `create_case` do processo `alteracao_cadastral` para o vínculo.
  2. `get_documentary_profile(case_id, funcionario_id, as_of)` com `as_of` igual à
     `effective_on`; guarde o `profile_hash`.
  3. `receive_case_data` com `dados_alteracao_cadastral = {effective_on, competencia,
     expected_profile_hash, changes: {"categoria_esocial": "723"}}`: `competencia` é o
     mês da `effective_on` (`AAAA-MM`), `expected_profile_hash` é o `profile_hash` do
     passo 2, e `request_ref` e `expected_snapshot` (o `input_snapshot` de `get_case`)
     seguem a regra de sempre. Valor sem 3 dígitos é recusado na recepção. A primeira
     declaração de um vínculo sem categoria vem com a pendência informativa
     `prior_value_missing` no recibo factual, porque não há valor anterior a comparar;
     não é defeito.
  4. Receber os dados não aplica nada. Só o efeito grava a categoria no vínculo:
     `apply_case_effects` com `request_ref`, `expected_snapshot` igual ao
     `correction_snapshot` de `get_case`, `human_message` e `message_reference` da
     operadora e `authorize_operational_effects: true`. Exige conta de pessoa com
     `decidir_chat` e `corrigir_dados` (a rotina não aplica); `identity_source` é
     opcional. Recusas: `effect_snapshot_changed` (releia o caso),
     `employee_profile_changed` (o perfil mudou desde o passo 2: refaça-o) e
     `employee_change_authority_required`. Releia o registro antes de afirmar aplicação.
  Corrigir (de `723` para `101`, por exemplo) é uma nova alteração cadastral, com
  `effective_on` no início da primeira competência a corrigir.
- **Caminho 2: fato `parametrizacao` do onboarding** (carga de vínculos). Como os outros
  parâmetros individuais (pensão, VT, adicionais), no lote de onboarding da empresa:
  1. `create_company_onboarding(cliente_slug, empresa_cnpj, reference)` (ou reutilize o
     lote da empresa).
  2. `submit_company_onboarding_chunk(onboarding_id, declaration)` com
     `schema_version: "loki.company-onboarding/1"`, `reuse_registered_company: true` e,
     em `workers`, um trabalhador que continua levando `reference`, `cpf`, `nome` e
     `data_admissao` (e `existing_employee_id` quando o vínculo já existe), com o fato
     `facts: [{reference, kind: "parametrizacao", effective_on, data:
     {"categoria_esocial": "723"}}]`; a fonte é opcional e, omitida, vira declaração
     nativa do pedido.
  3. `validate_company_onboarding(onboarding_id)` e, depois de mostrar a linha à
     operadora, `apply_company_onboarding(onboarding_id, validation_hash)`, com as
     capacidades de onboarding de sempre.
  Em caso `aberto` ou `em_preparacao`, também o perfil documental
  (`import_documentary_profile`, com `parametrizacao.categoria_esocial`, `data_efeito`
  (o mesmo início da pessoa na categoria), `competencia` igual ao mês de `data_efeito`,
  `field_sources` com a fonte do campo e `identity_source`, documentos anexados ao caso). Corrigir categoria
  já aplicada pelo onboarding segue a regra de `replaces_fact_id` acima.
- **Recomendação.** Declare a categoria no cadastro de todo sócio, estagiário e
  intermitente **antes** de rodar folha.
- **Efeito na folha** (detalhe em `folha_mensal`): folha sem o campo usa a do cadastro;
  folha e cadastro diferentes dão `categoria_esocial_divergente` e a pessoa não é
  calculada até alinhar; o cadastro vence a memória do caso. Categoria que não começa
  com `1` não é calculada (`categoria_esocial_nao_suportada`): o Loki ainda não calcula
  pró-labore nem bolsa de estágio.
- **Exigência de cadastro.** Para quem não é empregado o cadastro exige só os
  dependentes de IRRF; sindicato, escala, VT e salário-família não são cobrados.
  Empregado ou campo ausente: a exigência de sempre.
- **Outros processos.** Criar caso de 13º, férias, rescisão ou admissão, e simulação de
  rescisão, de quem tem categoria que não é de empregado é recusado com
  `categoria_sem_regime_clt` (seção própria em cada domínio).
