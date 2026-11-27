# Atualizações MCP Loki — contrato 2.12.0

## Candidata 0.4.38 / contrato, instruções e plugin 2.12.0 — 27/11/2026

O contrato sobe de 2.11.0 para 2.12.0 porque há **ferramentas novas** e o schema de
`preparar_autorizacao` ganha o valor `confirmar_rescisao` no enum de capacidades:
**exige Refresh do conector e conversa nova** na conta da Ana, além de atualizar o
plugin (as skills mudaram). Base do Refresh: `confirm_termination` (#435) e
`preview_onboarding_vacation_balance_retirement` e `retire_onboarding_vacation_balance`
(#438) entram em `list_tools` e o snapshot `connector_tools_list_d863b1aa_masked.json`
foi atualizado na #438. Os demais itens chegam com o deploy do backend, sem Refresh
próprio (argumentos livres ou conteúdo de resposta). Instruções e plugin acompanham em
2.12.0; o provider sobe um patch (0.4.38). Mínimo 2.0.0 permanece. Wheel 0.4.37
permanece imutável.

**Endereço novo.** O Loki mudou de servidor em 27/11/2026: `https://loki.tominho.com/mcp`
passa a `https://loki.izzicontabil.com.br/mcp` (o antigo devolve 503). Trocado em todos os
domínios, nas skills e no README do plugin e nos documentos de configuração; o conector
cadastrado numa conta de pessoa precisa ser recadastrado no endereço novo. Ficam com o
endereço antigo, de propósito, só os parágrafos históricos de edições anteriores neste
arquivo e no `README.md` (registro datado).

Backend, conferido no código de `main` do Loki (`d0bcdd3d`): #432 (razão social), #433
(férias pela rotina), #434 (intermitente), #435 (`confirm_termination`, ADR-042,
migration 0068), #436 (prazo determinado), #437 (renumeração da migration, sem texto) e
#438 (retirada de saldo de férias, ADR-043).

- **Razão social do caso x cadastro (#432; `admissao`, `folha_mensal`, `rescisao`).**
  `loki.domain.company_name`: igual; só o tipo societário do fim diferente (aceito, com o
  aviso `razao_social_tipo_societario` e o evento `razao_social_normalizada_pelo_cadastro`);
  corte do PDF. Natureza jurídica diferente (LTDA x S.A. x EIRELI) recusa com
  `razao_social_natureza_juridica_divergente`; porte (ME, EPP) e tipo ausente só avisam.
  Conferência dupla CNPJ + `codigo_dominio` do caso; caso sem código vale só o CNPJ
  (provisório, constante `CASO_SEM_CODIGO_CONFIRMA_PELO_CNPJ`); código diferente tira a
  tolerância e, em cadastro não ancorado (`cases._ensure_empresa`), recusa a criação do
  caso. A geração (folha, rescisão, admissão) confere de novo contra o cadastro vigente
  (`_conferir_identidade`); não há teste dedicado a cadastro alterado entre o cálculo e a
  geração.
- **Férias pela rotina (#433; `ferias`, `geral`).** `CLIENT_INPUT_PROCESSES` passa a
  `admissao`, `rescisao` e `ferias`; a rotina dispensa `corrigir_dados` na preparação de
  férias; `aquisitivo_inicio`, `aquisitivo_fim`, `inicio` e `fim` imutáveis
  (`preparation_identity_changed`); programação preservada. Afastamento segue fora
  (`client_input_restart_scope_refused`). Os textos "férias e afastamento continuam com
  pessoa" passam a dizer só afastamento.
- **Intermitente (#434; `folha_mensal`).** `categoria_esocial` (`"111"`) em
  `dados_folha.funcionarios[*]`: `vinculo_intermitente_nao_suportado`, pendência agregada,
  memória só dentro do caso da competência. O Loki ainda não calcula intermitente.
- **`confirm_termination` (#435; `rescisao`, `aprovacoes`).** Capacidade
  `confirmar_rescisao`, caso em `aguardando_revisao`, `termination_confirmation_snapshot`,
  fonte anexada, recusa `confirmacao_desligamento_recusada` com `reason` fechado;
  compensação por `ajustar` ou cancelamento (que exige `confirmar_rescisao`). A descrição
  da ferramenta no catálogo diz "ou aprovado pelo chat", mas o código só aceita
  `aguardando_revisao`; o texto segue o código.
- **Prazo determinado (#436; `admissao`).** Seção `contrato_prazo_determinado`, oito
  recusas `prazo_determinado_*`, aviso `texto_contrato_prazo_determinado_nao_homologado`,
  retificação só do início (`admission_date_rectification_fixed_term_limit`) e
  `generate_documents` e `run_prepared_case_workflow` devolvendo a recusa tipada (`errors`
  com `path` e `type`, `next_action: receive_case_data`).
- **Retirada de saldo de férias (#438; `alteracao_cadastral`, `rescisao`).** Prévia e ato
  humano por `onboarding_id`; recibo sem migration; recusas
  `onboarding_vacation_balance_retirement_*`.
- **Consignado sem linha no mapa (`folha_mensal`).** `binding_for` em
  `payroll_worker_credit` devolve nulo sem linha de desconto com código do Domínio,
  sem `parametro_individual` e com INSS, FGTS e IRRF `sem_efeito`: a folha da pessoa
  fica parcial com `credito_trabalhador_mapeamento_pendente`.

Domínios: `geral` (aviso 2.12.0; avisos anteriores comprimidos por causa do limite de
65536 bytes), `admissao`, `ferias`, `folha_mensal`, `rescisao`, `alteracao_cadastral` e
`aprovacoes`. Plugin: WORKFLOWS (seção 2.12.0), CAPACIDADES_DP, operar-loki,
registrar-problema-loki, bootstrap e README. Wheel preparado não comprova publicação,
instalação ou uso.

## Candidata 0.4.37 / contrato, instruções e plugin 2.11.0 — 26/11/2026

Contrato aditivo, sem ferramenta nova e **sem Refresh do conector**: o hash do
`tools/list` não mudou. Base: as PRs #421, #422, #424, #425 e #426 declaram o hash de
`list_tools` idêntico; o snapshot `connector_tools_list_d863b1aa_masked.json` (nome,
`inputSchema`, `outputSchema`, descrição e `annotations` de cada ferramenta) só foi
criado na #425 e nenhuma PR posterior o alterou; e o diff de `d863b1aa` a `867efb14` em
`connector/` e `mcp_server/` não toca assinatura nem docstring de ferramenta (o
`REPLACEMENT_MAX_GRANTS = 500` de `preparar_autorizacao` mantém o `max_length` anterior).
O `request_schema` do comando `@connector` ganha a variante `prepare_authorization_removal`,
mas é conteúdo de resposta, não do catálogo. Basta a operadora atualizar o plugin (as
skills mudaram). Contrato, instruções e plugin sobem para 2.11.0; o provider sobe um patch
(0.4.37). Mínimo 2.0.0 permanece. Wheel 0.4.36 permanece imutável.

Backend, conferido no código de `main` do Loki (`867efb14`): #424 (`31d93dcf`), #426
(`d6facd51`), #421 (`78e3c2e7`) e #422 (`867efb14`). Sem texto para a operadora: #425
(`52959521`, só compacta o JSON das respostas) e #427 (`960eef5f`, coorte de preservação
do executor de publicação). 13º sem mudança de comportamento.

- **Acessos (#424, domínio `aprovacoes`).** `prepare_authorization_addition` aceita
  empresa que a conta já tem e acrescenta só os processos e capacidades que faltam, sem
  remover nada, até 100 empresas por chamada (inclusive para dar
  `atualizar_por_insumo_do_cliente` à rotina). Prévia em delta: `added_grants` (com
  `extends_existing_company`), `added_companies` e `extended_companies`. Recusas
  `authorization_addition_nothing_to_add` (a mensagem lista as empresas; repetir sem elas) e
  `authorization_addition_duplicate_company`. Operação `prepare_authorization_removal`
  (`removals[]`, até 100 empresas): prévia `removed_grants`, `removed_companies` e
  `reduced_companies`, aplicação por `aplicar_autorizacao`, recusas
  `authorization_removal_nothing_to_remove`, `authorization_removal_duplicate_company`,
  `concessao_exige_consultar` e `proprietario_protegido`. `preparar_autorizacao` (substituição
  completa) aceita no máximo 500 concessões; a conta guarda até 5000. A trava do grafo é
  global: `BUSY` repete a mesma chamada.
- **Rescisão (#426).** Catálogo `loki.termination-rubric-catalog/2` (tabelas por conteúdo
  e `groups[]` com ids, reconstrução pelo campo `reconstruction`); `get_dp_capabilities`
  só índice, com `contract_tool` e `contract_hash`.
- **Onboarding (#421, #422, domínio `alteracao_cadastral`).** `adoption_effects` e
  `released_closed_consumers` na linha `applied`; releitura por
  `get_employee_identifier_state` (`applied_receipts[].matricula_restoration`).
  `nome_do_vinculo_conflitante`, `dated_field_value_conflict` (`diagnostic.conflict`),
  avisos `existing_dated_conflict` e `aplicacao_sequencial_por_vinculo`,
  `snapshot_do_vinculo_desatualizado` e o mapa `refusals` de
  `get_company_onboarding_contract`.

Domínios: `aprovacoes`, `rescisao` e `alteracao_cadastral`; `geral` só com o aviso (menor
que antes, por causa do limite de 65536 bytes). Plugin: WORKFLOWS (seção 2.11.0),
operar-loki e registrar-problema-loki. Em `release.json`, `changes` guarda só a versão
corrente; o histórico das edições anteriores está nas seções abaixo. Wheel preparado não
comprova publicação, instalação ou uso.

## Candidata 0.4.36 / contrato, instruções e plugin 2.10.1 — 25/11/2026

Contrato aditivo, sem ferramenta nova e **sem Refresh do conector**: `create_case`
recebe o payload genérico e o marcador `payload.simulation` é lido pelo backend.
Basta a operadora atualizar o plugin (as skills mudaram). Contrato, instruções e
plugin sobem para 2.10.1; o provider sobe um patch (0.4.36). Mínimo 2.0.0
permanece. Wheel 0.4.35 permanece imutável.

Backend, conferido no código de `main` do Loki: #418 (`a6bfea66`, ADR-040,
migration 0067) e #419 (`8cc136a7`, par de preservação 0066→0067).
`docs/contracts/case-simulations.md`, `case_simulations.py` e `operational.py`
(`get_process_contract("rescisao").simulation`).

- Spec `loki.termination-simulation-create/2` (simulação de quem segue empregado,
  sem caso de origem): `get_company_employee_history` com `as_of` da data de
  desligamento hipotética (`history_hash`); `create_case` com o `CasePayload`
  completo e `payload.simulation` `{schema_version, source: {kind: employee,
  funcionario_id, expected_history_hash}, simulation_ref, field_sources}`;
  `field_sources` só de declaração (`locator = $.payload.<caminho>`), sem
  `documentos_origem`; `run_prepared_case_workflow`; `get_case_version` e
  artefatos. PDF e recibo saem como SIMULAÇÃO e dizem que o histórico não entrou
  no cálculo.
- Recusas: `simulation_history_changed`, `simulation_employment_not_active` e
  `simulation_source_not_supported`.
- Descarte só humano, por `cancel_case` (`expected_snapshot`, `human_message`); a
  rotina técnica não cancela; `simulation_cancelled` mantém a referência
  ocupada.
- Isolamento (`casos.simulation`): a simulação (v1, v2 e as de 18/11) não entra no
  13º, no fechamento nem na conciliação; não cria funcionário, evento de vínculo
  nem pin.
- A v1 (`source_case_id`) continua valendo. `requires_source_case: true` é o valor
  da v1; o valor por versão está em `requires_source_case_by_version`.

Domínios: `geral` (aviso 2.10.1 sem Refresh; aviso da 2.10.0 comprimido em
"Continua da 2.10.0" por causa do limite de 65536 bytes) e `rescisao` (roteiro,
recusas e descarte). Plugin: WORKFLOWS (seção 2.10.1), operar-loki e
registrar-problema-loki. Wheel preparado não comprova publicação, instalação ou
uso.

## Candidata 0.4.35 / contrato, instruções e plugin 2.10.0 — 25/11/2026

O contrato sobe de 2.9.9 para 2.10.0 porque o **schema de `preparar_autorizacao`
ganhou um valor no enum** (`atualizar_por_insumo_do_cliente`): **exige Refresh do
conector e conversa nova**, além da atualização do plugin. Depois disso, a Ana
concede a capacidade à rotina por `preparar_autorizacao`. Instruções e plugin
acompanham em 2.10.0; o provider sobe um patch (0.4.35). Mínimo 2.0.0 permanece.
Wheel 0.4.34 permanece imutável.

Backend: Project-loki #411 (ADR-039), #413 e #414, mescladas em `main` (`55e110c1`).
#413: regra legal `transcricao_cadastral_sem_efeito_no_13` no 13º (`scope`
`identificacao_cadastral` ou `alteracao_cargo_cbo`, três recusas
`historical_thirteenth_legal_rule_*`, até 1000 ids por avaliação). #414:
`formula.divisor_sob_calendario` (`"30"`/`"dias_do_mes"`) sob `folha_divisor_mes` e
`fator` 1 ou 2 em `salario_base_proporcional` (medição CX-D0D4F1EF); a orientação
"quantidade = 2 × dias" da 2.9.9 foi trocada pelo fator 2. A promoção ao Loki
segue o fluxo do backend.
A capacidade abre só `restart_case` em caso `aguardando_revisao`: admissão e
rescisão com `preparation.mode=replace_process_inputs` e `request_ref`
`sha256-<64 hex>`; folha mensal simples. Concedida só por
`preparar_autorizacao`/`aplicar_autorizacao` (`preparar_acesso_tecnico` recusa com
`capacidade_concedida_so_por_autorizacao`; pessoa, `capacidade_exclusiva_de_automacao`),
inclusive no modelo `@empresas-novas`. Não decide: aprovação, efeitos, entrega,
cancelamento, retificação de data, férias e afastamento seguem com pessoa.

Domínios: `geral` (aviso 2.10.0 com Refresh; aviso da 2.9.9 comprimido em
"Continua da 2.9.9" por causa do limite de 65536 bytes; a capacidade), `admissao`
e `rescisao` (roteiro e recusas) e `folha_mensal` (restart simples e enqueue pela
rotina). Plugin: WORKFLOWS (seção 2.10.0), CAPACIDADES_DP, operar-loki e
registrar-problema-loki. Wheel preparado não comprova publicação, instalação ou uso.

## Candidata 0.4.34 / contrato, instruções e plugin 2.9.9 — 24/11/2026

Contrato aditivo, sem ferramenta nova e **sem Refresh**. O contrato sobe de
2.9.8 para 2.9.9 pela regra "mudou interface → novo contrato" e pela prática
das edições 2.9.7 e 2.9.8: o schema de dados e as recusas do backend mudaram
desde a 2.9.8 (campos de horas e `folha_divisor_mes`, em `main`; campo `horas`
da política, recusa da 1ª parcela e `review_refusal` do comando de fila, nas
PRs abertas), sem passar pelo catálogo de ferramentas: `receive_case_data`,
`apply_client_config` e `validate_client_config` recebem JSON livre e o schema
vem dos contratos servidos. Instruções e plugin acompanham em 2.9.9 (as skills
mudaram: a operadora atualiza o plugin); o provider sobe um patch. Mínimo 2.0.0
permanece. A lista `compatible_tools` não muda. Wheel 0.4.33 permanece imutável.

Backend, conferido no código: #404 (média por quantidade das horas) e #405
(`folha_divisor_mes`) em `main` do Loki (`00cba4e9`). **#409 e #410 já estão mescladas; depende da PR aberta
#408** (cada texto diz "vale quando a resposta servida mostrar o sinal"):

- #409 (mesclada, `3b4d3b11`): recusa
  `historical_thirteenth_first_installment_already_paid` e as janelas
  `required_windows`/`missing_intervals` em `get_case` e no dossiê (hoje só na
  resposta imediata);
- #408 (aberta, `dbd7c765`; `next_action` `receive_case_data` com `guidance`; mudar para `valores` exige vigência nova; onboarding anuncia `hours_field`, `hours_policies` e `hours_values_refusal`): campo `horas` (`valores` |
  `quantidade_347`) em `empresas[].decimo_terceiro_medias` e recusa
  `decimo_horas_vedado_pela_norma_coletiva`;
- #410 (mesclada):
  `case_in_review_requires_restart` no `enqueue_case_workflow`.

Domínios:

- `decimo_terceiro`: o gap `thirteenth_payment_coverage_not_certified` é
  informativo e o cálculo não o lê; exige `thirteenth_payments` de 01/01 (ou
  admissão) até a `data_pagamento` e `leave_occurrences` até o corte; passo da
  cobertura adjacente; janelas só na resposta imediata; 1ª parcela com 13º já
  adiantado; horas (Súmula 347) só onde a norma coletiva é silente e política
  `horas: "valores"`; a seção "Médias" deixa de dizer que a média por
  quantidade não é calculada.
- `ferias`: a cobertura dela não é a do 13º.
- `folha_mensal`: recálculo em revisão por `restart_case` simples e novo
  enqueue; folha pelo mês civil (`folha_divisor_mes`); fórmulas do mapa e seus
  limites.
- `geral`: aviso "O que mudou nesta versão (2.9.9)" (atualizar o plugin, sem
  Refresh) e "Continua da 2.9.8" (Refresh só da ferramenta nominal
  `rectify_case_admission_date`).

Fora desta edição (plano do lote): o texto de descontos recorrentes e do
consignado em `credito_trabalhador_contratos` e `alteracao_cadastral.md`.

Plugin: WORKFLOWS (seção 2.9.9 e nota na cobertura), CAPACIDADES_DP, operar-loki
e registrar-problema-loki. A promoção ao Loki só ocorre depois da mesclagem das
PRs do backend; wheel preparado não comprova publicação, instalação ou uso.

## Candidata 0.4.33 / contrato, instruções e plugin 2.9.8 — 24/11/2026

Acompanha sete PRs do backend, todas em `main` do Loki (`2f866fdf`): #400
(alocação do consignado pela data do contrato e afastamento pago pela empresa,
`2f866fdf`), #402 (crédito ignora revisões substituídas por correção auditada,
`14a3f506`), #395
(aviso da norma coletiva e cumprimento parcial, `31e62b3c`), #396 (13º,
`4a9f84f2`), #397 (correções auditadas, `82f1497c`), #399 (saldo de salário na
rescisão, `6a14607d`) e #401 (arredondamento por empresa, `942ebaee`). A #398
(executor de publicação, `d60d07fe`) não muda texto da operadora. O texto
foi conferido contra o código mesclado, não contra os resumos das PRs. Cada
texto novo vale quando a resposta servida mostrar o sinal:

- #395: `aviso_norma_coletiva` e `aviso_cumprimento_parcial` no schema servido
  de `dados_rescisao`; versão do motor com `+aviso-declarado-v1`.
- #396: `empresas[].decimo_terceiro_medias` e
  `dados_decimo_terceiro.dezembro_anterior`; `thirteenth_rules.fact_assessment`
  e `thirteenth_rules.average_window` em `get_company_onboarding_contract`;
  motor `decimo-v5` com `dez_nov_12`.
- #397: `admission_date_rectification` em `get_process_contract("admissao")`
  (e a ferramenta `rectify_case_admission_date`); `replaces_fact_id` para
  `parametrizacao` e para o aquisitivo de `vacation_balance` no contrato de
  onboarding; `rule.admitted_on_base_date` por competência no contrato do
  reajuste.
- #399: `rescisao-v45` ou `rescisao-v46` no cálculo da rescisão.
- #400: `data_inicio_contrato` em `credito_trabalhador_contratos`;
  `afastamento_empregador` na rubrica do mapa; sufixos condicionais
  `-worker-credit-allocation-v1` e `-employer-leave-v1` no motor `folha-v33`.
- #402: sem sinal novo (a revisão do contrato deixa de ser travada pela correção
  auditada).
- #401: `policies.arredondamento_vale_transporte` e `accepted_formulas` em
  `payroll_map_policy_patch_transport`.

A mudança de interface é aditiva. Há uma ferramenta nova
(`rectify_case_admission_date`, #397: `build_server().list_tools()` ganha uma
ferramenta a mais) e a rota equivalente em `receive_case_data`
(`request.schema_version = loki.case-admission-date-rectification/1`, listada
em `compatibility_transport`). As demais mudanças de schema são de dados:
`dados_rescisao`, `dados_decimo_terceiro`, o cadastro da empresa, os fatos
`historico_operacional` e `parametrizacao`, e a política do mapa. Nenhuma delas
passa pelo catálogo de ferramentas: `receive_case_data`, `apply_client_config`,
`validate_client_config` e `submit_company_onboarding_chunk` recebem JSON livre
(`dict`) e o schema vem dos contratos servidos. Pela regra "mudou interface →
novo contrato", o contrato sobe de 2.9.7 para 2.9.8, um patch; instruções e
plugin acompanham em 2.9.8; provider sobe um patch. Mínimo 2.0.0 permanece. A
lista `compatible_tools` não muda.

**Refresh do conector.** É necessário só para a ferramenta nominal nova
`rectify_case_admission_date`. Os campos opcionais novos do contrato de crédito
e da rubrica do mapa (#400) entram por `dict` livre e não exigem Refresh: a #400
não toca `mcp_server` nem `connector`. Sem Refresh, a mesma retificação funciona por
`receive_case_data`. Os schemas de dados das #395, #396, #397 e #401 não
exigem Refresh. O aviso do domínio `geral` diz isso.

Conferido no código (divergências com os rascunhos, resolvidas pelo código):

- #395: `dias_base` vai de 31 a 90; a guarda `aviso_projecao_incoerente` só vale
  com norma ou com `empregador_dispensou_restante` (o aviso legal sem
  declaração fica fora dela). `empregado_faltou_sem_comunicacao` é a leitura
  adotada pela engenharia; a alternativa é decisão da DP.
- #396: `sem_efeito` tem como alvos `outro` e `afastamento` (não só `outro`);
  `afastamento_tipado` tem alvo `afastamento` sem data. A transferência não
  sai do estado: a qualificação é do consumidor do 13º. O texto da carga
  `dp_rule_pending` passa a tratar só a rescisão.
- #397: o contrato servido lista as capacidades `decidir_chat` e `corrigir_dados`
  para a retificação; a política da ferramenta (`principal.py`) só exige
  `corrigir_dados`. O texto cita as do contrato. Os estados gravados que
  recusam são `aguardando_revisao` e `rejeitado` (precisam de `restart_case`);
  o contrato descreve `allowed_states` como `aberto` e `em_preparacao`.
  `admission_date_rectification_case_cancelled` existe no código (próxima ação
  `create_case`) e fica fora do texto.
- #399: os dias efetivos valem com divisor 30 e com a convenção `calendario`;
  `regra_nao_medida:saldo_divisor_sem_convencao` continua para divisor que não
  é nenhuma das duas.
- #401: `requires_formula` guarda o texto da versão `/1`; as fórmulas aceitas
  estão em `accepted_formulas`. A partição não aceita política no membro
  (`particao_membro_arredondamento_use_arredondamento_total`).
- Salário-família (flag do cadastro do Domínio), DSR das faltas e percentual do
  VT pela escala são regras da DP informadas pelo solicitante; o código só
  recebe a quantidade de filhos (`salario_familia`) e a regra individual de VT
  (`vale_transporte_regra.percentual_basis_points`) declaradas por pessoa e não
  as deriva. O texto diz isso e não promete cálculo pelo Loki.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.8)" (atualizar o plugin; Refresh
  só da ferramenta nominal) e "Continua da 2.9.7"; seção do lote de políticas
  do mapa com os cinco métodos, `accepted_formulas`, VT e partição.
- `rescisao`: saldo de salário pelos dias efetivos e convenção `calendario`
  (sem o "até a DP responder"); seção "Aviso prévio: norma coletiva e
  cumprimento parcial (2.9.8)"; gozo antecipado sem "pergunte à Rafa".
- `decimo_terceiro`: seções "Janela da média por empresa (decimo-v5)" e "Fatos
  opacos do 13º qualificados pelo id"; "Médias" sem "dependem de confirmação da
  DP"; `dp_rule_pending` sem "leve à Rafa" para a transferência.
- `admissao`: "Data de admissão errada no caso" com a retificação antes da
  confirmação; cancelar e reabrir só para admissão reaberta, depois da
  confirmação (alteração com reenvio) ou sem o sinal.
- `alteracao_cadastral`: "Corrigir parâmetro já aplicado no onboarding".
- `ferias`: troca do aquisitivo de `vacation_balance`.
- `reajuste_salarial`: admitido no mês da data-base por competência.
- `alteracao_cadastral`: também "Alocação entre contratos (2.9.8)".
- `folha_mensal`: "Afastamento pago pela empresa: rubrica marcada no mapa" e "Regras da DP para declarar o cadastro e os descontos".

Tamanho (limite 65.536 bytes): `geral` 65.332, `ferias` 43.820,
`folha_mensal` 46.003, `rescisao` 43.084; os demais ficam abaixo.

Plugin espelha em WORKFLOWS (seção "2.9.8: rescisão, 13º, correções
auditadas e arredondamento", e notas nas seções antigas), CAPACIDADES_DP,
REAJUSTE_SALARIAL, operar-loki e registrar-problema-loki.

Wheel 0.4.32 permanece imutável; fonte e wheel 0.4.33 locais não comprovam
promoção, publicação, atualização do plugin instalado, Refresh do conector, uso
pela operadora ou aceite de DP.

## Candidata 0.4.32 / contrato, instruções e plugin 2.9.7 — 23/11/2026

Acompanha PRs do backend, todas em `main` do Loki. A #387 (worker de cálculo
sem concessão por empresa e teto de 5000 concessões) está publicada
(`5b8de2b3`). A #392 (pendências da diferença retroativa no dossiê,
`70709d1a`) e a #393 (pago declarado com várias `remuneracao_periodo`,
`cefea294`) foram mescladas; o texto foi conferido contra `cefea294`. A #391
(holerite do consignado, `0d2df471`) não muda texto: nenhum domínio cita o `OverflowDeCelula` da verba do Crédito
do Trabalhador, e a operadora não envia a descrição. Cada texto novo vale
quando a resposta servida mostrar o sinal:

- #387: não há sinal positivo; a recusa `worker_not_authorized` deixa de
  trazer `reason: "worker_company_grant_missing"`. Com o servidor anterior, a
  recusa com esse `reason` vai à engenharia: o servidor anterior recusa
  incluir a empresa no worker acima de 500 concessões, e o worker já está
  nesse teto.
- #392: `retroactive_actions` na issue `contexto_operacional_pendente` do
  dossiê; `diferenca_retroativa` em `MapaFolha` do `envelope_schema` de
  `get_client_config.payroll_map_patch_transport`.

A mudança de interface é aditiva e sem ferramenta nova: campos que saem da
recusa do worker (`required_grant`, `authorization_addition`,
`worker_account_id`, `worker_account_revision`), o teto de
`prepare_authorization_addition` (`access.Proposal`, 5000) e, na #392, campos
novos no dossiê (`retroactive_actions`, `retroactive_proof`,
`retroactive_detail`) e a política no schema servido do patch do mapa. As duas
PRs não tocam `src/loki/mcp_server`: as 96 ferramentas são as mesmas. Pela
regra "mudou interface → novo contrato", o contrato sobe de 2.9.6 para 2.9.7,
um patch; instruções e plugin acompanham em 2.9.7; provider sobe um patch.
Mínimo 2.0.0 permanece. A lista `compatible_tools` não muda.

Conferido no código:

- #387: o worker exige só identidade (conta `automacao` ativa, papel
  operator, igual a `CASE_JOB_WORKER_ID`); `worker_service_not_authorized`
  para cliente revogado, vencido ou conta diferente. O escopo de empresa e
  processo é o de quem enfileirou. `legacy_authorization.Proposal`
  (`preparar_autorizacao`) e `service_auth` seguem com 500 por pedido; o
  texto só cita 5000 para a conta e o `prepare_authorization_addition`.
- #392: `diferenca_funcionario_fora_da_folha` entra em `missing_fields`, mas
  não tem ação em `CODE_ACTIONS`; o texto dá a saída que já existia.
- Correção de lote aplicado: `instrument_id` é empresa, tipo e `reference`,
  então outra `reference` é outro instrumento e não cai em
  `reajuste_retroativo_ja_lancado_na_competencia`; a exclusão recusa linha
  `APPLIED` (`salary_adjustment_exclusion_invalid`) e a reabertura exige
  falha registrada (`salary_adjustment_reopen_invalid`). As regras de
  `quantidade` do pago declarado já valiam em `main`; a #392 só acrescenta o
  detalhe.
- #393 (`cefea294`): várias verbas
  `remuneracao_periodo` no mesmo mês do pago declarado são aceitas quando
  trazem a mesma quantidade e unidade (um só `periodo_remuneravel`); a regra
  `remuneracao_periodo_repetida` passa a
  `remuneracao_periodo_quantidades_divergentes`, com `codigo_origem` (a verba
  que diverge) e `codigo_periodo` (a que fixou o período). Códigos iguais
  depois de `normalizar_codigo` (`8` e `008`) são repetidos. O texto vale
  quando o `retroactive_detail` mostrar a regra nova; sem ela, uma por mês.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.7)" (só atualizar o plugin;
  sem Refresh) e "Continua da 2.9.6" (recálculo das folhas anteriores à
  `folha-v33` e revisão preparada de novo); os itens da 2.9.5, já publicada,
  saem do aviso. "Empresa nova e onboarding pela rotina" reescrita: worker
  sem concessão, recusas do worker à engenharia, rotina por empresa
  explícita, teto de 5000.
- `folha_mensal`: item 0 da fila durável reescrito; o dossiê remete às
  pendências da diferença.
- `reajuste_salarial`: `quantidade` pela fórmula do mapa da origem, "Corrigir
  o pago declarado de lote já aplicado", política ausente por `add` de
  vigência nova e "Pendências da diferença no dossiê da folha".

Tamanho (limite 65.536 bytes): `geral` 62.371, `folha_mensal` 42.403,
`reajuste_salarial` 34.808; os demais não mudam.

Plugin espelha em WORKFLOWS (seção "2.9.7: worker sem concessão por empresa e
pendências do reajuste no dossiê", com notas de substituição na 2.9.4 e 2.9.5),
REAJUSTE_SALARIAL, CAPACIDADES_DP, operar-loki e registrar-problema-loki.

Não exige Refresh do conector. Os textos chegam com o deploy do backend,
depois da promoção do wheel ao Loki. Wheel 0.4.31 permanece
imutável; fonte e wheel 0.4.32 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata 0.4.31 / contrato, instruções e plugin 2.9.6 — 22/11/2026

Acompanha três PRs do backend, no mesmo pacote do Loki que leva a 2.9.5
(mesclada e promovida, ainda não publicada). As três estão em `main` do Loki
(`1e74e642`): #382 (correções do operador no reinício) e #385 (`folha-v33`).
A #384 (férias pela CLT) foi mesclada (`1e74e642`, que completa o pacote de
código); o texto foi conferido contra esse `main`. A #383 só mexe em testes e
não entra. Cada texto novo vale quando a resposta servida mostrar o sinal do
tema, e a orientação anterior fica como caminho sem ele:

- #382: `corrections_carried` na resposta do `restart_case`;
- #385: o motor `folha-v33` no cálculo da folha;
- #384: `gozo_antecipado_source` no schema servido de `dados_ferias` (e
  `ferias_recibo` no schema do cadastro).

A mudança de interface é aditiva e sem ferramenta nova: campos novos na
resposta do reinício (`corrections_carried`, `corrections_not_carried`), na
memória do cálculo (`operator_corrections.carried`/`not_carried`), na revisão
(`estado_no_calculo_corrente`, `notas_informativas`, `regras_clt`), no
dossiê (`context_fields`), no contexto da folha (`payment_basis`), em
`dados_ferias.gozo_antecipado_source` e em `empresas[].ferias_recibo`, além
de códigos de recusa e pendência novos. As três PRs declaram
`build_server().list_tools()` idêntico (96 ferramentas). Pela regra "mudou
interface → novo contrato", o contrato sobe de 2.9.5 para 2.9.6, um patch;
instruções e plugin acompanham em 2.9.6; provider sobe um patch. Mínimo 2.0.0
permanece. A lista `compatible_tools` não muda.

Divergências entre os rascunhos das PRs e o código, resolvidas pelo código:

- #384: o rascunho cita `ferias_saldo_reservado_por_ferias_posteriores`, que
  não existe no código; a recusa do conjunto é
  `ferias_saldo_insuficiente_com_casos_irmaos`.
- #384: o rascunho diz que os casos irmãos contam "em qualquer ordem de
  cálculo". No código final (`1e74e642`), o aprovado ou publicado conta
  sempre, com os valores aprovados; o não aprovado só com cálculo corrente
  estrito (âncora na linha corrente, `ferias_calculo_reancorado` quando volta);
  quem já calculou não cai; aprovação e publicação conferem o conjunto. A
  âncora pelo início da preparação, da cabeça intermediária `95827af6`, não
  ficou.
- #384: o rascunho manda seguir `docs/Componentes_Ferias.md`, que é do
  repositório do Loki e não chega à harness; o exemplo vai resumido no
  domínio `ferias`. `component_consumption_incomplete` aponta o campo
  `componentes_medias`; a leitura de `pendencias` em `get_case` não foi
  confirmada e saiu do texto.
- #384: as recusas da CLT apontam `historical_state` com a próxima ação
  `get_case_historical_state`.
- #385: o código também recusa `confirmed_vacation_calculation_stale` (caso
  de férias sem cálculo corrente) e `loki_vacation_effect_reference_invalid`
  (sem `case_id` ou `result_hash`), que o rascunho não lista.
- #385: a declaração do Crédito do Trabalhador "com fonte da harness
  (`EXTSRC-…`) e contratos com versão confirmada" não foi confirmada no
  código e saiu; os códigos de rubrica do caso relatado também saíram (o
  texto fala em código do Domínio da rubrica).
- #385: a memória do VT fica em `fontes_insumos` da linha
  (`base_percentual`, `linhas_de_salario`, `salario_do_mes_cents`).
- #382: o rascunho não traz o estado `parcial`, a forma `{estado,
  caminhos}`, `reaplicacao: aguardando_calculo_corrente`, os motivos de
  `aposentada`, a regra do legado nem a revisão a preparar de novo; o texto
  inclui todos.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.6)", que leva também os itens
  da 2.9.5 (as duas chegam juntas): atualizar o plugin, recalcular as folhas
  não entregues com `folha-v33` e preparar de novo a revisão que recusar
  `pacote_mudou_desde_a_leitura`; sem Refresh. Sai "Continua da 2.9.4" (o
  recálculo da v33 cobre o da v32). As seções "eSocial por empresa" e
  "Preparação fiscal persistida" saem do `geral` (o mesmo texto já estava em
  `alteracao_cadastral`) e ficam como uma remissão.
- `folha_mensal`: "Motor folha-v33: recalcular as folhas não entregues" (VT
  e salário-família do admitido, férias do Loki e INSS do mês inteiro no
  contexto, dossiê, pensão do admitido, Crédito do Trabalhador) e "Correções
  calculadas atravessam o reinício da folha"; remissões nas seções da v32,
  que ficam como caminho sem o sinal.
- `ferias`: "Afastamento e fracionamento pela CLT, gozo antecipado e recibo
  por empresa (2.9.6)"; remissões no afastamento que não reduz férias, no
  gozo antecipado do histórico e na tabela de recusas.
- `afastamento`: CLT no aquisitivo e INSS do mês inteiro na folha.
- `rescisao`: recusa com caso de férias antecipadas do Loki.
- `alteracao_cadastral`: `empresas[CODIGO_DOMINIO].ferias_recibo`.

Tamanho (limite 65.536 bytes): `geral` 62.321, `folha_mensal` 43.021,
`ferias` 42.880; os demais abaixo de 39 KB.

Plugin espelha em WORKFLOWS (seção "2.9.6: correções no reinício, folha v33 e
férias pela CLT", com notas de substituição na 2.9.4 e 2.9.5),
CAPACIDADES_DP, operar-loki e registrar-problema-loki.

Não exige Refresh do conector: as 96 ferramentas são as mesmas. Os textos
chegam com o deploy do backend. Wheel 0.4.30 permanece imutável; fonte e
wheel 0.4.31 locais não comprovam promoção, publicação, atualização do plugin
instalado, uso pela operadora ou aceite de DP.

## Candidata 0.4.30 / contrato, instruções e plugin 2.9.5 — 21/11/2026

Acompanha quatro PRs do backend. Duas já estão em `main` do Loki: #376
(onboarding independente) e #379 (admissão). Duas estão aprovadas e ainda não
mescladas, e o texto foi conferido contra estas cabeças: #378 (férias,
`e6a9b851`) e #372 (matrícula do eSocial, migration 0066, `ff829a16`). O
backend pode chegar em partes, então cada texto novo vale só quando a resposta
servida mostrar o sinal do tema, e a orientação anterior fica como caminho
para o servidor que ainda não tem a parte:

- #376: `carga_historica` numa empresa real em `meu_acesso` da conta técnica
  (a concessão automática não tem sinal na resposta; a recusa
  `worker_company_grant_missing` continua com o mesmo recurso);
- #379: `supersedes_case_id` na resposta do `create_case`;
- #378: `historical_state.vacation_rules` em `get_company_onboarding_contract`
  e `data_calculo` no schema servido de `dados_ferias`;
- #372: o motivo `adocao_matricula_esocial` nas regras de
  `get_company_onboarding_contract`.

A mudança de interface é aditiva e sem ferramenta nova: campos novos dentro de
payloads existentes (`dados_ferias.data_calculo`,
`dados_ferias.abono_fora_do_prazo_source`, `leave.vacation_effect`,
`vacation_use.advance`, `supersedes_case_id`, `adoption_effects`), o motivo
`adocao_matricula_esocial` em `restoration_declaration.motivo` e códigos de
recusa e pendência novos. Pela regra "mudou interface → novo contrato" e pelo
precedente aditivo da 2.9.4, o contrato sobe de 2.9.4 para 2.9.5, um patch;
instruções e plugin acompanham em 2.9.5; provider sobe um patch. Mínimo 2.0.0
permanece. A lista `compatible_tools` não muda.

Divergências entre o rascunho das PRs e o código, resolvidas pelo código:

- #372: a recusa do valor já qualificado em outro namespace é
  `adocao_matricula_esocial_exige_codigo_dominio` (o rascunho e a
  documentação citam `_qualificado`). Valor sem recibo segue a restauração
  comum, não vai à engenharia.
- #372: `allow_identifier_restoration` não é argumento de
  `apply_company_onboarding`; o servidor o deriva de `corrigir_dados`.
- #378: as recusas da fonte do abono são
  `ferias_abono_fora_do_prazo_source_sem_uso` e
  `ferias_abono_fora_do_prazo_source_sem_fundamento`.
- #376: não há domínio `onboarding`. O roteiro da rotina fica no `geral`, o
  único domínio servido sem exigir processo.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.5)" (só atualizar o plugin,
  sem Refresh; a conta da rotina que receber `carga_historica` pode precisar
  de conversa nova para ver as ferramentas de onboarding; o recálculo da
  folha-v32 da 2.9.4 fica como "Continua da 2.9.4"); lembrete do Refresh da
  2.8.0 estendido à adoção, que usa os mesmos campos da restauração; a seção
  "Empresa nova: acesso do worker e da rotina" vira "Empresa nova e
  onboarding pela rotina" (concessão automática; os passos do
  `prepare_authorization_addition` passam ao item 0 da fila durável de
  `folha_mensal`, como recurso para `worker_company_grant_missing`; sai
  "Conta de automação não recebe `carga_historica`"; roteiro do onboarding
  pela rotina e o que continua com a pessoa); matrícula do eSocial no
  `create_case`; cancelamento libera a chave só na admissão sem rastro.
- `admissao`: "Razão social da empresa" e "Data de admissão errada no caso"
  com a reabertura, as recusas novas e o caminho do servidor anterior;
  recusas de matrícula eSocial no `create_case`.
- `ferias`: seção "Data do cálculo, afastamento sem redução, gozo antecipado
  e abono (historical-vacation-v2)", com o caso já calculado pela v1 que
  deixa de ser corrente sem o espelho nativo; o afastamento opaco e o gozo
  antes do fim do aquisitivo (texto e tabela) passam a apontar a saída nova.
- `afastamento`: `sem_reducao` por regra da operação e fato opaco só para
  férias.
- `rescisao`: `rescisao_ferias_gozo_antecipado_pendente_regra` e
  `termination_monthly_calculation_predates_registration_adoption`.
- `alteracao_cadastral`: "Adotar a matrícula do eSocial" (um lote por
  empresa, campos, recusas, `adoption_effects`); vale para todo vínculo
  carregado com código Domínio.
- `folha_mensal`: "Matrícula do eSocial na população da folha"
  (`matricula_coincide_com_codigo_auxiliar`, pares cruzados pela correção da
  população com `funcionario_id`); item 0 da fila com a concessão automática
  e os passos do recurso.

Tamanho: `geral` com 65.216 bytes do limite de 65.536; os demais abaixo de
39 KB.

Plugin espelha em WORKFLOWS (seção "2.9.5: onboarding pela rotina, admissão,
férias e matrícula do eSocial", com notas de substituição na 2.9.0, 2.9.1 e
2.9.4), CAPACIDADES_DP (seção 2.9.5 e o cancelamento), operar-loki e
registrar-problema-loki.

Não exige Refresh do conector: as 96 ferramentas são as mesmas (as quatro PRs
declaram `build_server().list_tools()` idêntico, e nenhuma muda schema de
ferramenta). Os textos chegam com o deploy do backend. Wheel 0.4.29 permanece
imutável; fonte e wheel 0.4.30 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata 0.4.29 / contrato, instruções e plugin 2.9.4 — 20/11/2026

Backend #374 (folha-v32, regra da DP de 19/11) e #375 (recusa do worker sem a
empresa). A #375 já está em `main` do Loki; a #374 sai junto com esta versão.
A mudança de interface é aditiva e sem ferramenta nova: na folha, os códigos
de pendência `salario_familia_mes_transferencia_pendente_regra`,
`salario_familia_salario_do_mes_nao_identificado`,
`salario_familia_adicional_mes_cheio_nao_identificado`,
`salario_familia_deducao_nao_classificada`,
`salario_familia_medias_ferias_nao_classificadas`,
`vale_transporte_mes_transferencia_pendente_regra` e
`vale_transporte_proporcao_concessao_admissao_ambigua`, com as próximas ações;
o caminho de correção `funcionarios.<matricula>.verbas.<rubrica de VT>.0.valor_cents`
para o VT ambíguo; `calculated: null` na memória de correção sobre valor
pendente; `salario_familia_mes_admissao_pendente_regra` deixa de ser emitida
(#374). Na fila, `worker_not_authorized` com
`reason: "worker_company_grant_missing"`, `required_grant`,
`worker_account_id`/`worker_account_revision` e `next_action` para o comando
aditivo `prepare_authorization_addition` (#375). Pela regra "mudou interface →
novo contrato" e pelo precedente aditivo da 2.9.3, o contrato sobe de 2.9.3
para 2.9.4, um patch; instruções e plugin acompanham em 2.9.4; provider sobe um
patch. Mínimo 2.0.0 permanece. A lista `compatible_tools` não muda.

**A troca de motor para `folha-v32` deixa desatualizadas todas as folhas
mensais não entregues**, inclusive as recalculadas na v31. As correções de
salário-família registradas na v31 continuam consumidas e prevalecem sobre a
cota nova: a harness confere declarado e calculado com a operadora.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.4)", com o recálculo da folha
  v32 e a conferência das correções da v31 em destaque, além de atualizar o
  plugin (sem Refresh); seção nova "Empresa nova: acesso do worker e da
  rotina" (passos com `listar_solicitacoes_acesso`,
  `prepare_authorization_addition` só com as empresas novas, `aplicar_autorizacao`
  e repetir o enqueue; `preparar_autorizacao` nunca para incluir empresa no
  worker).
- `folha_mensal`: "Motor folha-v32: recalcular as folhas não entregues" (com
  as correções da v31 que prevalecem); "Salário-família pela remuneração
  devida no mês (folha-v32)" (salário cheio, adicionais pelo mês cheio, fora
  faltas, 13º e terço; mês de admissão proporcional por `30 − dia + 1`, em
  confirmação com a DP; pendências novas e saída); "VT do admitido no mês
  (folha-v32)" (percentual uma vez sobre o salário proporcional; três casos da
  concessão; pendência ambígua com correção da linha do VT); a insalubridade
  da v31 fica em seção própria; saem os pontos "em consulta à DP" e o VT
  retido da v31; item 0 da fila durável para empresa nova sem o worker.

Plugin espelha em WORKFLOWS (seção "2.9.4: folha v32 (salário-família, VT do
admitido) e empresa nova no worker", com nota de substituição parcial na
2.9.3), CAPACIDADES_DP, operar-loki e registrar-problema-loki.

Não exige Refresh do conector: as 96 ferramentas são as mesmas. Os textos
chegam com o deploy do backend. Wheel 0.4.28 permanece imutável; fonte e wheel
0.4.29 locais não comprovam promoção, publicação, atualização do plugin
instalado, recálculo das folhas, uso pela operadora ou aceite de DP.

## Candidata 0.4.28 / contrato, instruções e plugin 2.9.3 — 19/11/2026

Backend #370 (folha-v31) e #368 (simulação com o estado histórico atual), já
mesclados em `main` do Loki depois da 2.9.2. A mudança de interface é aditiva e
sem ferramenta nova: o campo opcional `historical_state` (`selected` padrão |
`current`) no marcador de simulação, publicado em
`get_process_contract("rescisao").simulation.historical_state`, com
`historical_state_basis` (`loki.simulation-historical-state/1`), `notices`,
`pending_qualifications` e os subreasons novos
`historical_state_source_incompatible` e
`historical_settlement_bound_to_selection` (#368); na folha, três códigos de
pendência de salário-família no diagnóstico, a `next_action`
`qualificar_incidencia_inss_das_rubricas_do_mes` e o caminho de correção do
operador em `funcionarios.<matricula>.bases.salario_familia_cents` (#370).
Pela regra "mudou interface → novo contrato" e pelo precedente aditivo da
2.9.2, o contrato sobe de 2.9.2 para 2.9.3, um patch; instruções e plugin
acompanham o contrato em 2.9.3; provider sobe um patch. Mínimo 2.0.0
permanece e clientes 2.x anteriores continuam compatíveis. A lista
`compatible_tools` não muda.

**A troca de motor para `folha-v31` deixa desatualizadas todas as folhas
mensais não entregues** (abertas, em revisão e aprovadas não entregues): elas
precisam ser recalculadas, conferidas e aceitas de novo; as entregues não
mudam. O aviso do `geral` destaca isso.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.3)", com o recálculo da folha
  v31 em destaque como ação da operadora, além de atualizar o plugin (sem
  Refresh); substitui o da 2.9.2 e mantém o lembrete do Refresh da 2.8.0; o
  ponteiro da simulação cita a seção nova de `rescisao`. O `geral` fica com
  cerca de 61KB do limite de 64KB.
- `folha_mensal`: três seções novas no topo. "Motor folha-v31: recalcular as
  folhas não entregues" (abertas, em revisão e aprovadas não entregues; novo
  aceite; entregues não mudam; retificação para competência entregue).
  "Salário-família pelo limite da base do INSS (folha-v31)": limite contra a
  base do INSS do mês; pendências
  `salario_familia_mes_admissao_pendente_regra`,
  `salario_familia_remuneracao_zero_sem_declaracao` e
  `salario_familia_base_inss_zero_com_proventos` com as próximas ações
  servidas; saída por `submit_operator_correction` com
  `target: "calculation"` depois da decisão da DP; falta de filhos se resolve
  completando o cadastro; pontos em consulta à DP (1/3 de férias e faltas na
  base do limite, mês de admissão cheio ou parcial, transferência como
  entrada). "Insalubridade e VT no mês de admissão (folha-v31)": só a
  `rubrica_loki` no mapa, pagamento pelos dias no mês de admissão, VT do
  admitido no mês continua retido.
- `alteracao_cadastral`: exceção da insalubridade vigente desde a admissão na
  seção de adicionais.
- `rescisao`: seção nova "Simulação com o estado histórico atual" (#368):
  `payload.simulation.historical_state: "current"` com `simulation_ref` nova;
  nada muda no caso real; ressalvas, `historical_state_basis`,
  `history_consumed` e `pending_qualifications` com a ação "renovar seleção e
  qualificação no caso real"; subreasons novos; limite das fontes `CPH-*`
  (`source_document_missing`). Sai a orientação de que seleção desatualizada
  não tem caminho sem reiniciar o caso real.

Plugin espelha em WORKFLOWS (seção "2.9.3: folha v31 (salário-família e
insalubridade) e simulação com o estado atual", e o bullet de simulação da
2.9.0 aponta para ela), CAPACIDADES_DP, operar-loki e registrar-problema-loki
(o que é ou não defeito na 2.9.3).

Não exige Refresh do conector: as 96 ferramentas são as mesmas
(`build_server().list_tools()` em `main` do Loki, f35f5b1c). Os textos chegam
com o deploy do backend, na mesma conversa. A mudança nas skills exige
atualizar o plugin instalado, sem bloquear o uso. Wheel 0.4.27 permanece
imutável; fonte e wheel 0.4.28 locais não comprovam promoção, publicação,
atualização do plugin instalado, recálculo das folhas, uso pela operadora ou
aceite de DP.

## Candidata 0.4.27 / contrato, instruções e plugin 2.9.2 — 19/11/2026

Backend #365, #366 e #367, já mesclados em `main` do Loki depois da 2.9.1.
A mudança de interface é aditiva e sem ferramenta nova: o envelope
`loki.company-termination-map-policy-patch/1` no mesmo argumento `alteracoes`
de `validate_client_config` e `apply_client_config`, a chave de descoberta
`termination_map_policy_patch_transport` em `get_client_config`,
`termination_policy_preview` na prévia e a recusa
`termination_policy_patch_remove_incompatible` (#366); e, no 13º, a recusa
`historical_thirteenth_unqualified_documentary_facts` sai de `{"erro": ...}`
para `BLOCKED`/`code` com `blocking_facts` e `blocking_facts_total` (#367).
Pela regra "mudou interface → novo contrato" e pelo precedente aditivo da
2.9.1, o contrato sobe de 2.9.1 para 2.9.2, um patch; instruções e plugin
acompanham o contrato em 2.9.2; provider sobe um patch. Mínimo 2.0.0
permanece e clientes 2.x anteriores continuam compatíveis. A lista
`compatible_tools` não muda.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.2)" (só atualizar o plugin;
  sem Refresh), que substitui o da 2.9.1 e mantém o lembrete do Refresh da
  2.8.0. O `geral` fica com cerca de 60KB do limite de 64KB.
- `rescisao`: seção nova "Trocar só a política de arredondamento do mapa"
  (#366): várias empresas numa versão; a política declarada substitui a atual
  inteira, então ler antes a política de cada seleção em `get_client_config`
  e repetir `escopos`, `fonte` e as opções que continuam ligadas; seleções da
  mesma empresa recebem a mesma política; `termination_policy_preview`
  mostrado à operadora antes do apply; `parcelas_do_mes` não é exigido;
  `medias_por_bloco` continua desligada sem conferência da DP; sem a chave de
  descoberta, avisar que o servidor ainda não tem o patch. Ponteiros nas
  seções do patch de parcela e do método do Domínio.
- `decimo_terceiro`: seção nova "Fatos documentais não qualificados" (#367):
  `blocking_facts` com `origin`, `kind`, identificador, `effective_on`,
  `reason` e `path`; `outro` qualificado pelo reenvio da cobertura
  `thirteenth_payments` da mesma ficha, com `replaces_fact_id` e
  `qualifies_legacy_fact_ids`; aviso de que isso muda o `state_hash` do
  empregado e desatualiza as seleções dos outros casos abertos dele (não
  qualificar sem alinhar com a DP); a qualificação só vale em cortes a partir
  do fim da cobertura; `final_average` não qualifica fato do 13º (o uso em
  `medias_importadas` não muda); `no_typed_exit` e `dp_rule_pending` ficam
  pendentes e se registram.
- #365 (suporte no Slack) não pede instrução de domínio: só a nota no
  `registrar-problema-loki`.

Plugin espelha em WORKFLOWS (seção "2.9.2: política do mapa de rescisão e
fatos do 13º"), CAPACIDADES_DP, operar-loki e registrar-problema-loki (o que
é ou não defeito na 2.9.2 e a nota de que o bot do Slack só age quando
mencionado ou na thread do próprio pedido; o relato segue pelo assistente).

Não exige Refresh do conector: as 96 ferramentas são as mesmas. Os textos
chegam com o deploy do backend, na mesma conversa. A mudança nas skills exige
atualizar o plugin instalado, sem bloquear o uso. Wheel 0.4.26 permanece
imutável; fonte e wheel 0.4.27 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata 0.4.26 / contrato, instruções e plugin 2.9.1 — 18/11/2026

Backend #363 (b7c3d22f, já mesclado em `main` do Loki depois da 2.9.0):
regras da DP de 18/11/2026. A mudança de interface é só texto aditivo no
contrato `loki.salary-adjustment/1` (`rule.admitted_on_base_date` e
`declared_origins.transport_discount`), sem ferramenta nova, sem schema novo
e sem processo novo. Pela regra "mudou interface → novo contrato" e pelo
precedente aditivo da 2.7.1 (campo novo sem processo, transporte ou
ferramenta nova), o contrato sobe de 2.9.0 para 2.9.1, um patch; instruções e
plugin acompanham o contrato em 2.9.1; provider sobe um patch. Mínimo 2.0.0
permanece e clientes 2.x anteriores continuam compatíveis. A lista
`compatible_tools` não muda.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.1)" (só atualizar o plugin;
  sem Refresh), que substitui o da 2.9.0 e mantém o lembrete do Refresh da
  2.8.0; na seção "Matrícula no `create_case`", a matrícula do eSocial é o
  identificador oficial segundo a DP e, enquanto a forma de uso não for
  confirmada, nenhuma matrícula nova se grava por `identifier_only` sem falar
  com a engenharia. O `geral` fica com cerca de 60KB do limite de 64KB.
- `alteracao_cadastral`: a mesma regra da matrícula do eSocial antes das
  seções de restauração e troca de código Domínio.
- `reajuste_salarial` (e o guia REAJUSTE_SALARIAL.md): seção nova "Admitido
  no próprio dia da data-base" (`sem_reajuste` com
  `admitido_na_data_base_com_salario_novo`, `rule.admitted_on_base_date`,
  piso prevalece, `salario_novo_cents` maior diverge); sai a orientação antiga
  de deixar a linha pendente (`salario_anterior_divergente`); o VT não entra
  na diferença nem no pago declarado (`declared_origins.transport_discount`)
  e não impede `sem_outras_verbas_dependentes_do_salario`; o salário novo já
  registrado com vigência na data-base é o próprio reajuste e a diferença
  ainda não foi paga; fica pendente o admitido no mesmo mês, antes do dia da
  data-base.
- `ferias`: o gozo em que o fim do aquisitivo cai dentro do período passa a
  ser aceito no histórico do onboarding; só o que termina antes do fim do
  aquisitivo continua `historical_vacation_use_period_incompatible`. Lote
  recusado antes por esse código pode voltar `ready`: validar de novo e
  aplicar com o `validation_hash` novo (o antigo dá `snapshot_desatualizado`).
  O processo de férias segue a regra anterior.
- `afastamento`: um registro por atestado, com o retorno no dia seguinte ao
  fim; atestados encostados não são sobreposição; licença-maternidade não é
  falta e não reduz o aquisitivo.
- `rescisao`: a DP informou que o Domínio soma as médias das empresas do
  grupo, sem separar por empresa, em férias e no 13º; não ligar
  `medias_por_bloco` sem conferência com a DP.
- `decimo_terceiro`: a mesma regra de soma no 13º; a pendência com a DP sobre
  blocos no 13º sai.

Plugin espelha em WORKFLOWS (seção "2.9.1: regras da DP de 18/11/2026"),
CAPACIDADES_DP, REAJUSTE_SALARIAL, operar-loki e registrar-problema-loki.

Não exige Refresh do conector: as 96 ferramentas são as mesmas. Os textos
chegam com o deploy do backend, na mesma conversa. A mudança nas skills exige
atualizar o plugin instalado, sem bloquear o uso. Wheel 0.4.25 permanece
imutável; fonte e wheel 0.4.26 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata 0.4.25 / contrato, instruções e plugin 2.9.0 — 18/11/2026

Backend #358, #359 e #360, já mesclados em `main` do Loki depois da 2.8.0.
Há mudança de interface, toda aditiva e sem ferramenta nova: no reajuste,
`folha_bloqueante` na linha da prévia e os campos de documentação
`preview.blocking_payroll` e `decision.config_pending_reconciled`
(`loki.salary-adjustment/1`); na recusa, `subreason` fechado em
`operational_context_changed` (`loki.operation-refusal/1`) e
`version_refusal_subreasons` em `get_process_contract`;
`selection_matches_current_state` para pessoa em `get_case_historical_state`;
no mapa de rescisão, `metodo_ferias`, `terco`, `saldo` e `medias_por_bloco` em
`arredondamento_proporcionais`, com a recusa de cadastro
`rescisao_saldo_valor_dia_exige_trinta_fixo`; em `DadosRescisao`
(`medias_variaveis`) e `ImportedFinalAverage`, `horas_micros`, `valor_micros`,
`vantagens_micros` e `bloco`; `bloco` no formulário de fatos. Pela regra
"mudou interface → novo contrato", e por somar campos em vários schemas de
processo, o contrato sobe de 2.8.0 para 2.9.0; instruções e plugin acompanham
o minor; provider sobe um patch. Mínimo 2.0.0 permanece e clientes 2.x
anteriores continuam compatíveis. A lista `compatible_tools` não muda.

Por domínio:

- `geral`: aviso "O que mudou nesta versão (2.9.0)", separando o que exige
  ação da operadora (só atualizar o plugin) do que não exige nada, com o
  lembrete de que os três fluxos da 2.8.0 ainda exigem Refresh se ele não foi
  feito; ponteiro da simulação para `rescisao`. O `geral` fica com cerca de
  60KB do limite de 64KB.
- `reajuste_salarial` (e o guia REAJUSTE_SALARIAL.md): `folha_bloqueante`
  (#358) vale para a folha do Loki em X ou em qualquer competência posterior,
  e o histórico importado não conta; lançar na primeira competência depois da
  última folha do Loki em revisão ou fechada, com a DP confirmando o mês;
  `cliente_config_incompleta` fecha no apply, depois da decisão;
  `processo_nao_habilitado_no_cliente` não barra o apply, mas o certo é
  habilitar com a DP.
- `rescisao`: método do Domínio opt-in (#359), médias com micros e por bloco
  (#360) e simulação (#358): chaves nulas da origem, `foundation`, locator,
  `subreason`; comparar o `state_hash` de `get_case_historical_state` com o
  da seleção (ou `selection_matches_current_state`) antes de simular; sem
  reiniciar o caso real, não há caminho quando a seleção está desatualizada.
- `decimo_terceiro`: micros e blocos não valem no 13º (pendente com a DP).
- `admissao`: a data de admissão é identidade e não se troca; cancelar o caso
  com a mensagem do cliente e abrir outro, conferindo antes se o episódio
  antigo recebeu matrícula (se recebeu, registrar problema).

Plugin espelha em WORKFLOWS (seção "2.9.0"), CAPACIDADES_DP,
REAJUSTE_SALARIAL, operar-loki e registrar-problema-loki.

Não exige Refresh do conector: a revisão do backend confirmou que as 96
ferramentas têm o mesmo hash. Os textos chegam com o deploy do backend, na
mesma conversa. A mudança nas skills exige atualizar o plugin instalado, sem
bloquear o uso. Wheel 0.4.24 permanece imutável; fonte e wheel 0.4.25 locais
não comprovam promoção, publicação, atualização do plugin instalado, uso pela
operadora ou aceite de DP.

## Candidata 0.4.24 / contrato, instruções e plugin 2.8.0 — 18/11/2026

Onda 2 do Loki (backend #343 a #355, ainda em revisão quando esta fonte foi
preparada). Há mudança de interface: duas ferramentas novas
(`preview_onboarding_termination_revocation` e
`revoke_onboarding_termination`, também como operações do transporte
`@connector`, #350), o campo `revoga_com_rescisao_aberta` e campos novos de
prévia (`open_termination_cases`, `same_cpf_active_employee_ids`), e o schema
de `WorkerDeclaration.restoration_declaration` (#345, com `motivo` fechado
`troca_de_codigo_dominio` em #351). Pela regra "mudou interface → novo
contrato" e por haver ferramenta nova, como no precedente de processo novo da
2.7.0, o contrato sobe de 2.7.1 para 2.8.0; instruções e plugin acompanham o
minor; provider sobe um patch. Mínimo 2.0.0 permanece e clientes 2.x
anteriores continuam compatíveis. A lista `compatible_tools` da distribuição
não muda.

Por domínio:

- `geral`: aviso curto "O que mudou nesta versão (2.8.0)" para a operadora,
  com a regra operacional de atualização imperceptível e a separação entre o
  que exige Refresh e o que não exige nada; matrícula divergente aponta a
  restauração ou troca combinada com a operadora; fila com empresas em
  paralelo. O `geral` fica com cerca de 60KB do limite de 64KB.
- `folha_mensal`: paralelismo entre empresas, no máximo um job por empresa, e
  Dataprev esperando a fila (#347); janela de publicação (#352): nesta janela
  ainda é preciso esvaziar a fila, nas seguintes job nunca iniciado sobrevive
  à troca de build (`case_job_build_repinned`) e `job_build_changed` /
  `job_fingerprint_snapshot_changed` pedem reenfileirar; contexto do mês por
  pessoa e hashes dos lançamentos no dossiê (#343); efeitos da revogação e da
  troca de código na população.
- `decimo_terceiro`: `final_average` é a média mensal integral do Domínio e
  nunca vai proporcional aos avos; casos em `aguardando_revisao` com média
  importada seguem `ajustar` → `calculate_case` → geração → nova conferência;
  reinício com `replace_process_inputs` sem `corrigir_dados`;
  `historical_thirteenth_coverage_incomplete` com `missing_intervals` (#353).
- `ferias` e `afastamento`: cobertura completa que termina depois do corte
  limpa o gap até o corte (`historical-state-v2`); seleção v1 consumível não
  se refaz (#348). Substitui o texto da 2.7.1 que exigia terminar no corte.
- `rescisao`: patch de uma parcela do mapa de rescisão
  (`loki.company-termination-map-patch/1`, #344) e ponteiro da revogação.
- `reajuste_salarial` (e o guia REAJUSTE_SALARIAL.md): regras da DP de
  17/11/2026 (#346): abrangência `nao` por padrão com exclusão automática,
  salário-base para admitidos depois da data-base, sem reajuste proporcional,
  reajuste por competência e sem RRA, arredondamento igual ao Domínio; salário
  novo já registrado no cadastro (#349). As pendências respondidas saem.
- `alteracao_cadastral`: restauração auditada de matrícula (#345), troca de
  código Domínio com `message_reference` `CX-` obrigatória (#351) e revogação
  de desligamento gravado pelo onboarding (#350). `admissao`: ponteiro.
- #354 (executor de publicação) e #355 (memória do worker) não pedem
  instrução; o aviso de volta ao uso logo após a liberação entra na seção da
  janela.

Plugin espelha em WORKFLOWS (seções "Onda 2" e "Cadastro"), CAPACIDADES_DP,
REAJUSTE_SALARIAL, operar-loki e registrar-problema-loki.

Exigem Refresh do conector e conversa nova na conta da operadora: #345, #350 e
#351 (restauração de matrícula, revogação de desligamento e troca de código).
Até o Refresh, a revogação já funciona pelo transporte
`receive_case_data(case_id="@connector")`. Os demais itens não exigem nada:
chegam com o deploy do backend, na mesma conversa. A mudança nas skills exige
atualizar o plugin instalado, sem bloquear o uso. Wheel 0.4.23 permanece
imutável; fonte e wheel 0.4.24 locais não comprovam promoção, publicação,
Refresh, atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.23 / contrato, instruções e plugin2.7.1 —17/11/2026

Mudança de interface aditiva da Onda 1 (backend #337, #338, #340, #341 e
#342, ainda em revisão quando esta fonte foi preparada): códigos e campos
novos nas respostas, `admission: "one_pending_job_per_company"` no contrato
`durable_workflow` (mesmo `schema_version` `loki.case-workflow-command/1`) e
`minLength: 1` em `funcionario.matricula`. Pela regra "mudou interface → novo
contrato" e pelos precedentes de campo aditivo (2.6.4 e2.6.5), o contrato
sobe de2.7.0 para2.7.1, não para um minor: não há processo, transporte ou
ferramenta nova, como havia em2.7.0. Instruções e plugin acompanham o
contrato em2.7.1, como em2.7.0; provider sobe um patch. O `minLength` só
recusa matrícula vazia ou só com espaços, que nunca identificou vínculo; o
mínimo2.0.0 permanece e clientes2.x anteriores continuam compatíveis.

Domínio novo `folha_mensal` (permissão `consultar` no processo
`folha_mensal`; o provider passa a15 domínios): o `geral` já tinha cerca de
54KB do limite de64KB por arquivo, então a fila e o diagnóstico ficam num
domínio próprio, com ponteiros no `geral`. Fila: um job pendente por empresa,
`company_job_pending` (HTTP409, nada gravado) com `pending_job`, `next_action`
`get_case_workflow_job` ou `retry_enqueue_later` e `retry_after_seconds`;
enfileirar em série; não gravar em outro caso nem no cadastro da empresa
durante o job (`job_sources_changed`); 524 com o mesmo `request_ref`;
`BUSY`/429 com `retry_after_seconds`; retenção de até cerca de60 minutos.
Diagnóstico: dossiê em vez de `get_case_calculation` para `CALCF-`
(`calculation_kind_unsupported`), afastamento não qualificado como causa
primária (`qualificar_afastamento_na_origem`, `dependent_fields`,
`next_action_after_primary`, `leave_qualification` com origens), `EXTSRC` de
outro caso não serve, `salario_base_ausente` com `code_next_action`,
`population_count`/`population_hash` no restart e
`payroll_population_dependencies_busy` `retryable`; rescisão declarada no
onboarding na leitura da folha. `decimo_terceiro`: competência no dia1,
cancelar antes de recriar, envio por partes com `pending_rules`, 2ª parcela
por `historical_payments`, `medias_importadas`, dependentes de IRRF e recusas
`thirteenth_*` com campo e mês. `geral`: matrícula omitida por padrão,
`matricula_funcionario_divergente`/`_nao_qualificada`, `identifiers` e
matrícula vazia recusada, com ponteiros em `admissao` e
`alteracao_cadastral`. `ferias` e `afastamento`: códigos `historical_*` de
`declaracao_do_vinculo_invalida`, cobertura que só limpa o gap terminando no
corte ou antes, sem `leave` duplicado para afastamento antigo opaco, sem
alterar coberturas de casos com seleção feita e lote validado antes da
publicação revalidado. Plugin espelha em WORKFLOWS, CAPACIDADES_DP,
operar-loki e registrar-problema-loki. Insalubridade e salário-família
(backend #339) ficam para a Onda 2. Nenhuma proteção é removida.

Não há ferramenta nova nem mudança de argumento: `create_case` recebe
`payload` como objeto livre, e o `minLength` aparece só no schema servido por
`get_process_contract`. Por isso não há Refresh do conector; a mudança nas
skills exige atualizar o plugin instalado. Os textos valem somente quando a
resposta servida apresentar os campos. Wheel0.4.22 permanece imutável; fonte e
wheel0.4.23 locais não comprovam promoção, publicação, atualização do plugin
instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.22 / contrato, instruções e plugin2.7.0 —17/11/2026

Mudança de interface aditiva (backend #334, PR-C3 do feedback 71): processo
coletivo novo `reajuste_salarial` em `get_process_contract`
(`loki.salary-adjustment/1`) e três transportes novos em `receive_case_data`:
`loki.salary-adjustment-preview/1`, `loki.salary-adjustment-exclusion/1` e
`loki.salary-adjustment-reopen/1`. Pela regra "mudou interface → novo
contrato" e por ser processo novo (não só campo opcional, como em2.6.4 e
2.6.5), o contrato sobe de2.6.5 para2.7.0; instruções e plugin acompanham o
minor do contrato, como em2.5.0 e2.6.0; provider sobe um patch, como em todas
as promoções. Mínimo2.0.0 permanece e clientes2.x anteriores continuam
compatíveis.

Domínio novo `reajuste_salarial` (permissão `consultar` no processo
`reajuste_salarial`; o provider passa a14 domínios e a aceitar o processo no
allowlist): a harness lê e confere o instrumento e monta a população; o Loki
só valida a coerência interna e nunca confere a fonte. Passo a passo de
`create_case` à retomada pelo mesmo `request_ref` até `APPLIED`/`PARTIAL`;
recibo `PARTIAL` mostra o estado real; saídas por reabertura, exclusão e
retirada no caso filho; pago declarado com
`sem_outras_verbas_dependentes_do_salario`; motivos fechados para salário
fora da regra; blockers e ressalvas da folha X (`diferenca_*`,
`reajuste_coletivo_em_execucao`, `diferenca_rescisao_complementar_pendente`);
vigência fora do dia1, RRA, rescisão complementar e abrangência, admitidos
depois de Y e piso, e arredondamento pendentes de decisão da DP. A conta
precisa de `reajuste_salarial` e `alteracao_cadastral` na empresa. Ponteiros
em `geral` (folha X) e `alteracao_cadastral` (casos filhos). O geral já tem
cerca de54KB do limite de64KB por arquivo; por isso o roteiro fica num
domínio próprio. Plugin acrescenta o guia `REAJUSTE_SALARIAL.md` (mesmo texto
do domínio) e espelha em WORKFLOWS, CAPACIDADES_DP, operar-loki e
registrar-problema-loki. Nenhuma proteção é removida.

Não há ferramenta nova nem mudança de argumento: `process_type`, `payload` e
`request` continuam strings e objetos livres no schema das ferramentas, e
`loki_obter_instrucoes` recebe o domínio como string. Por isso o processo não
exige Refresh do conector; a mudança nas skills exige atualizar o plugin
instalado, e a conta da operadora precisa receber os dois escopos. Os textos
valem somente quando o contrato servido apresentar a interface. Wheel0.4.21
permanece imutável; fonte e wheel0.4.22 locais não comprovam promoção,
publicação, atualização do plugin instalado, uso pela operadora ou aceite de
DP.

## Candidata0.4.21 / instruções e plugin2.6.12, contrato2.6.5 —16/11/2026

Mudança de interface aditiva: `dados_ferias` ganha o campo opcional
`inicio_antes_de_feriado_source` (backend #332), sem ferramenta nova. Pela
regra "mudou interface → novo contrato" e pelo precedente2.6.4, o contrato
sobe de2.6.4 para2.6.5; mínimo2.0.0 permanece e clientes2.x anteriores
continuam compatíveis. Regra da DP (16/11/2026): a decisão é sempre do
cliente; o DP informa o passivo; se o cliente decidir, é feito. Domínio
`ferias`: `ferias_inicio_antes_de_feriado` deixa de recusar sempre e recusa
sem a decisão do cliente; `ferias_inicio_antes_de_feriado_source_sem_uso` e
`..._source_sem_fundamento` recusam fonte sem uso ou sem fundamento. A fonte é
a decisão do cliente (documento, manifesto de harness ou declaração com
`foundation`); o conteúdo da `foundation` (quem decidiu, onde, passivo
informado) é da harness e da operadora, e o Loki só exige `foundation` não
vazia, sem conferir a fonte; inferência e contexto são recusados. Início
antes de feriado e do repouso exige as duas fontes, e cada uma libera só a
sua regra. A exceção não muda valores, vira ressalva
`clt_134_3_vespera_feriado` em `ressalvas.declaracoes_dp` (`confirmed: false`,
`exige_aceite_humano: true`) e linha "Declaração do DP" no aviso e no recibo,
e só vale com aceite explícito das ressalvas. Feriados e decisão mudam numa
única `submit_operator_correction`. Recibos de componentes de férias e de
rescisão e consolidações de médias ficam obsoletos de novo, inclusive os
emitidos depois da2.6.11, com o mesmo caminho de recuperação; a descrição da
ressalva do repouso mudou, então revisões já preparadas com ela se preparam de
novo; aprovados e entregues não mudam. `rescisao` ajusta o ponteiro; plugin
espelha em WORKFLOWS, CAPACIDADES_DP, operar-loki e registrar-problema-loki.
Nenhuma proteção é removida.

O campo novo no schema pode exigir Refresh do conector e conversa nova na
conta da operadora; a mudança nas skills exige atualizar o plugin instalado.
Os textos valem somente quando a resposta servida e o schema apresentarem
esses códigos e o campo. Wheel0.4.20 permanece imutável; fonte e wheel0.4.21
locais não comprovam promoção, publicação, atualização do plugin instalado,
uso pela operadora ou aceite de DP.

## Candidata0.4.20 / instruções e plugin2.6.11, contrato2.6.4 —16/11/2026

Mudança de interface aditiva: `dados_ferias` ganha o campo opcional
`inicio_antes_de_repouso_source` (backend #328), sem ferramenta nova. Pela
regra "mudou interface → novo contrato" e pelos precedentes aditivos
(2.6.2, política opcional de FGTS mensal; 2.6.3, schema Dataprev), o contrato
sobe de2.6.3 para2.6.4; mínimo2.0.0 permanece e clientes2.x anteriores
continuam compatíveis. Domínio `ferias`: o código
`ferias_inicio_antes_de_repouso_ou_feriado` não é mais emitido;
`ferias_inicio_antes_de_feriado` sempre recusa (mude a data com o cliente);
`ferias_inicio_antes_de_repouso` recusa sem a declaração do DP;
`..._source_sem_uso` e `..._source_sem_fundamento` recusam a fonte sem uso ou
sem fundamento. A fonte é o pedido do cliente (documento, manifesto de harness
ou declaração com `foundation`); inferência e contexto são recusados. A
exceção não muda valores, aparece em `ressalvas.declaracoes_dp` e numa linha
"Declaração do DP" do aviso e do recibo, e só vale com aceite explícito das
ressalvas. Repouso e declaração mudam numa única `submit_operator_correction`.
Recibos de componentes de férias e de rescisão e consolidações de médias
anteriores ao deploy ficam obsoletos (`OBSOLETO`, `medias_rescisao_obsoletas`)
e se refazem por qualificação, consolidação e cálculo novos; aprovados e
entregues não mudam. `rescisao` ganha ponteiro; plugin espelha em WORKFLOWS,
CAPACIDADES_DP, operar-loki e registrar-problema-loki. Nenhuma proteção é
removida.

O campo novo no schema pode exigir Refresh do conector e conversa nova na
conta da operadora; a mudança nas skills exige atualizar o plugin instalado.
Os textos valem somente quando a resposta servida e o schema apresentarem
esses códigos e o campo. Wheel0.4.19 permanece imutável; fonte e wheel0.4.20
locais não comprovam promoção, publicação, atualização do plugin instalado,
uso pela operadora ou aceite de DP.

## Candidata0.4.19 / instruções e plugin2.6.10 —16/11/2026

Mudança de orientação, sem ferramenta ou argumento novo: contrato2.6.3 e
mínimo2.0.0 permanecem; só se acrescentam campos de resposta (backend #325).
Domínio `geral`: quando `get_case_workflow_job` termina `blocked` em
`calculate`, `diagnostic.errors` traz `field` (lançamento ou dado do
funcionário), `index` (posição em `dados_folha.funcionarios` do payload, base
zero) e `reason` fechado; índice de lançamento além dos enviados aponta efeito
operacional do Loki; `verba_nao_mapeada` traz `codigo` e pede mapeamento;
`dados_folha.valorizacao` sem `index` é recusa da competência, com motivo
específico quando houver. A matrícula nunca volta e o diagnóstico não autoriza
recomeçar o caso. Plugin espelha em WORKFLOWS, CAPACIDADES_DP, operar-loki e
registrar-problema-loki. Nenhuma proteção é removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.18 permanece
imutável; fonte e wheel0.4.19 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.18 / instruções e plugin2.6.9 —15/11/2026

Mudança de orientação, sem ferramenta ou argumento novo: contrato2.6.3 e
mínimo2.0.0 permanecem; só se acrescentam campos de resposta (backend #320).
Domínios `ferias` e `afastamento`: na preparação corrente,
`vacation_preparation_requires_complete_input` e
`leave_preparation_requires_complete_input` trazem `errors` por campo (código
de regra, `missing` ou `extra_forbidden`); a harness corrige o campo e reenvia
a seção completa, com a fonte nos campos `*_source`. `geral`: a recusa
`payroll_population_identity_changed` da prévia traz `errors` com
`population[*]`, `index` (posição na lista enviada, base zero) e motivo
fechado, e `next_action: preview_payroll_population_correction`; depois de
`restart_case`, `get_case` lista de novo `harness_sources` e anexos nativos,
que a harness reutiliza sem registrar de novo (ponteiro em `documentos`).
Plugin espelha em WORKFLOWS, CAPACIDADES_DP, operar-loki e
registrar-problema-loki. Nenhuma proteção é removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.17 permanece
imutável; fonte e wheel0.4.18 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.17 / instruções e plugin2.6.8 —14/11/2026

Mudança de orientação, sem ferramenta ou argumento novo: contrato2.6.3 e
mínimo2.0.0 permanecem. Domínios `ferias` e `afastamento`: a recusa de dados
traz em `errors` o campo exato (ex.: `dados_ferias.data_aviso`,
`leave.retorno`) e um código de regra (13 códigos `ferias_...` e 6
`afastamento_...`, backend #316). A harness corrige só o campo apontado,
conferindo com o original, e reenvia com novo `request_ref` e o snapshot atual;
reenvio sem correção, com ou sem `field_sources`, é recusado de novo; data que o
documento realmente traz vira dúvida com a DP, sem forçar valor. `geral` ganha
um ponteiro junto de `case_write_constraints`. Plugin espelha em WORKFLOWS,
CAPACIDADES_DP, operar-loki e registrar-problema-loki. Nenhuma proteção é
removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.16 permanece
imutável; fonte e wheel0.4.17 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.16 / instruções e plugin2.6.7 —14/11/2026

Mudança de orientação, sem ferramenta ou argumento novo: contrato2.6.3 e
mínimo2.0.0 permanecem. Domínios `geral`, `admissao` e `rescisao`: folha
protegida `equivalent` passa a ser provada pelo cálculo de onde saiu o pacote
dela (em revisão/aprovado), sem recompor a folha viva; corrige o texto2.6.6
que falava em cálculo vigente. `unknown` continua bloqueando,
`reconciliation_dependencies_busy` indica gravação em andamento na empresa e
pacote envelhecido segue barrado com `calculo_desatualizado`. `rescisao`: saldo
em mês comercial (`trinta_fixo`, `rescisao-v43`/`rescisao-v44`) calcula
fevereiro e dia31; cenários ainda `regra_nao_medida` aguardam a DP. `geral`:
conexão fechada com `/healthz` normal; lote
`loki.company-payroll-map-policy-patch/1` com `fgts_mensal` e
`arredondamento_monetario`; `case_write_constraints` com `field` e `reason`
fechados. `ferias`: segunda ocorrência em outra competência e `created: false`.
Plugin espelha em WORKFLOWS, CAPACIDADES_DP, operar-loki e
registrar-problema-loki. Nenhuma proteção é removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.15 permanece
imutável; fonte e wheel0.4.16 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.15 / instruções e plugin2.6.6 —14/11/2026

Mudança de orientação, sem ferramenta ou argumento novo: contrato2.6.3 e
mínimo2.0.0 permanecem. Domínios `geral`, `admissao` e `rescisao`: na
preservação de imports, folha mensal protegida classificada `equivalent` com
`employee_excluded_from_current_calculation` deixa de bloquear; `"unknown"`
continua em `import_preservation_protected_dependency`;
`import_preservation_consumer_changed` pede refazer a prévia e
`reconciliation_dependencies_busy`, tentar depois. `geral`: prévia de população
da folha aceita item só `{"matricula"}`, salvo matrícula que passou a outra
pessoa (`payroll_population_rebound_requires_identifier`); chaves de `field_sources` são
caminhos-folha (`field_source_coverage`); recusa de simulação traz `subreason`;
reinício em `aberto`/`em_preparacao` sem `preparation` recusa com
`restart_requires_preparation_for_state` (modo de
`get_process_contract.preparation.modes`). `rescisao`: motivos fechados dos
afastamentos. `ferias`: `related_case_ids` e `related_reason` em
`related_vacation_parameters_invalid`. Plugin espelha em WORKFLOWS,
CAPACIDADES_DP, operar-loki e registrar-problema-loki. Nenhuma proteção é
removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.14 permanece
imutável; fonte e wheel0.4.15 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.14 / instruções e plugin2.6.5 —13/11/2026

Correção de orientação após revisão independente, sem ferramenta ou argumento
novo: contrato2.6.3 e mínimo2.0.0 permanecem. No domínio `admissao`: o recibo
de `rectify_case_name` segue o `next_action` recebido
(`run_prepared_case_workflow` ou `restart_case`); a retificação vale só para
caixa, espaços e forma Unicode NFC; `unsupported_admission_event` de import
documental distingue `import_preservation` de
`import_preservation_blocked_by_pending_effects` (`next_action: null`);
dependente protegido fora do acesso da conta vem só com `case_id` e `access`;
o diagnóstico da ficha mostra `error_type: "OverflowDeBeneficiarios"`. No
domínio `geral` e nos roteiros do plugin: `next_action` vem somente em
`restart_case`; `cancel_case` recusado por efeitos nunca o traz e não tem
caminho pelo acesso da operadora. Nenhuma proteção é removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.13 permanece
imutável; fonte e wheel0.4.14 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.13 / instruções e plugin2.6.4 —13/11/2026

Mudança de orientação, sem ferramenta ou argumento novo: contrato2.6.3 e
mínimo2.0.0 permanecem. O domínio `admissao` orienta o campo Beneficiários da
Ficha de Registro no modelo `ficha_registro/6` (até 8 linhas, sem truncar), a
retificação de nome diferente só em caixa/espaços por
`preview_case_name_rectification`/`rectify_case_name` com cadastro inalterado,
e a leitura dos blockers de `preview_admission_reconciliation`. O domínio
`geral` e os roteiros do plugin descrevem `blocking_refs`/`next_action` nas
recusas de `restart_case`/`cancel_case`. Nenhuma proteção é removida.

Os textos valem somente quando a resposta servida apresentar esses campos; não
afirmam que o backend correspondente está publicado. Wheel0.4.12 permanece
imutável; fonte e wheel0.4.13 locais não comprovam promoção, publicação,
atualização do plugin instalado, uso pela operadora ou aceite de DP.

## Candidata0.4.12 / contrato, instruções e plugin2.6.3 —10/11/2026

A orientação mensal Dataprev usa `loki.dataprev-monthly/1` somente quando
anunciado por `get_process_contract("folha_mensal")`, pelo `receive_case_data`
existente. Reserva, releitura durável e aplicação separada com CAS preservam
ator, caso, população e episódio; fontes existentes não são sobrepostas.
O [guia público](../plugins/loki-bootstrap/skills/operar-loki/references/DATAPREV_MENSAL.md)
é distribuído também no domínio geral do wheel. Exemplos são sintéticos.

Consulta incompleta/falha não promove parciais ou confirma zero. Manifesto e
hashes não atestam snapshot transacional oficial. Perfil mTLS, representação
e concessões válidos dependem de provisionamento externo; consulta não é
pagamento, repasse ou aceiteDP. Importação tipada continua disponível.

Mínimo2.0.0 preservado. Wheel0.4.11 permanece imutável; fonte e wheel0.4.12
locais não comprovam promoção, backend publicado, instalação na Ana, acesso
ativado ou homologação real. Nenhuma ferramenta, credencial ou autoridade nova
é concedida por esta distribuição.

## Candidata0.4.11 / contrato, instruções e plugin2.6.2 —09/11/2026

Extensão aditiva orienta a preparação de férias pelo transporte existente, com
autorização de correção, âncoras preservadas e nova recepção completa. Expõe o
alcance contextual do saldo rescisório v42 e a política opcional de FGTS mensal
no mapa selecionado, com memória por empregado no consumidor folha-v29.

A representação de faixa por pagador do afastamento já existe: não aplicar nova
carência de15dias nem inferir essa representação de um caso sem declaração.
Mínimo2.0.0 e compatibilidade anterior preservados. Wheel anterior permanece
imutável; nova fonte, wheel/proveniência, integração e serviço publicado exigem
provas próprias. Não ativa configuração, corrige fatos, aprova documentos ou
transmite. Instalação do operador e adoção não são inferidas da publicação.

## Candidata0.4.10 / contrato, instruções e plugin2.6.1 —09/11/2026

A retomada autenticada de resposta corrente intake/procedure também admite
`preparation_internal_failure` quando anunciada pelo contrato do backend.
Proprietário ativo, revisão/job/build exatos, convite e fonte correntes, memória,
limites e replay permanecem obrigatórios. Não reinicia ciclo, não repete a
pergunta ao DP e não abre preparação de código por uma falha genérica.

Artefato auxiliar sanitizado e resposta operacional literal têm finalidades
diferentes; publicação, resultado dos jobs e atos de negócio exigem suas próprias
provas. O diagnóstico mensal conserva o corte histórico e detalhes desconhecidos
indisponíveis, sem cálculo ou correção automática. Wheel0.4.9 e evidências
anteriores permanecem imutáveis; mínimo2.0.0 e clientes anteriores preservados.

## Candidata0.4.9 / contrato, instruções e plugin2.6.0 —08/11/2026

Extensão aditiva para conciliar declaração adicionalONB com fato conservado,
com prévia, CAS e recibo separado de applied; reprocessar respostaDP corrente
após agent_schema no mesmo ciclo; e consultar causas mensais persistidas pelo
dossiê sem recálculo. A representação opt-in de afastamento rescisório separa
episódio integral de faixa por pagador, mantendo campos/hashes legados quando
novos campos estão ausentes. As ferramentas e transportes só são usados quando
anunciados nos contratos do backend.

Mínimo de plugin2.0.0 preservado; clientes2.0–2.5 continuam compatíveis conforme
versões declaradas, e instalação/desconhecimento do catálogo permanecem
desconhecidos até observação. Nenhum aceite factual/documental, concessão de
benefício, pagamento ou transmissão é inferido. A publicação exige validação e
revisão do consumidor, wheel/proveniência/lock novos e prova HTTP+worker.


## Candidata 0.4.8 / instruções e plugin 2.5.4 — 07/11/2026

Perguntas ao DP sobre rubricas exigem nome legível+código exato de fonte real no
mesmo namespace e alcance, preservando zeros à esquerda da fonte. A orientação
idêntica em geral/operar/registrar/investigar manda consultar fontes autorizadas
antes da pergunta residual, preservar conflito/ausência e liberar partes
independentes. Não exige DOC/EXTSRC/hash universal; veda rótulo inventado e pedido
de identificação já fornecida. Resposta do DP conserva atribuição e alcance, sem
conferir autoridade humana ou aplicar dados/incidências automaticamente.

Contrato 2.5.0 e mínimo 2.0.0 permanecem; não há mudança de interface. Os testes
conferem integridade, compatibilidade e coerência de distribuição; não comprovam
que um modelo seguiu a orientação. Wheel 0.4.7 continua imutável. Build, promoção,
serviço publicado, instalação do plugin e uso na Ana exigem provas distintas;
esta fonte não altera instalação, rotina, identidade, agenda ou pins legados.

## Candidata 0.4.7 / instruções 2.5.3 — 07/11/2026

A entrega aditiva orienta diagnóstico pelo escritor, consulta financeira exata,
faltas mensais do 13º e fontes de férias identificadas sem DOC/hash universal.
Contrato 2.5.0 e mínimo 2.0.0 permanecem. Wheel, catálogo servido, instalação e
consumo exigem conferências distintas; esta fonte não comprova publicação.
O wheel 0.4.6 e os registros anteriores permanecem imutáveis.


Candidata de06/11/2026: provider/wheel 0.4.6, instruções2.5.2 e plugin2.5.2.
Texto versionado não atualiza serviço implantado nem a instalação do operador.
O backend incorpora o wheel; o plugin tem distribuição Git própria.

## Recuperação e saldo2.5.2 — 06/11/2026

A edição0.4.6 orienta a nova preparação de afastamento somente quando anunciada
pelo contrato e o alcance salarial de mês civil30/divisor30 qualificado no motor.
Preserva identidade, efeitos, revisão e pendências restantes. Nenhum desses
textos publica código ou altera conta/dados/agenda da Ana. Contrato2.5.0 e
mínimo2.0.0 continuam; wheel0.4.5 e seu recibo original permanecem imutáveis.

## Recursos de DP2.5.1 — 06/11/2026

Provider/wheel0.4.5, instruções e plugin2.5.1; contrato2.5.0 e mínimo2.0.0
preservados. Mudança de orientação, sem novo escritor ou endpoint de backend.
O novo roteiro nativo
[CAPACIDADES_DP.md](../plugins/loki-bootstrap/skills/operar-loki/references/CAPACIDADES_DP.md)
e os domínios pertinentes cobrem:

- Prontidão cadastral/mensal, lacuna de prontidão por funcionário, histórico pelo
  lote sequencial existente e medição por casos completos/elegíveis.
- Jobs duráveis e consulta após resposta perdida; restart humano, preservação de
  imports e seleção/cancelamento tipados da PR240 somente quando o contrato servido
  anunciar cada rota. Preview não aplica e seleção nova exige dados financeiros novos.
- Saldo de abertura/médias de férias, correção de afastamentos, consignado,
  pensão por finalidade e adicionais individuais/políticas explícitas de cargo.
  A recusa de categoria e saldo de salário `regra_nao_medida` continuam como limitações.

Proveniência detalhada continua opcional, com fontes/declarações preservadas.
Sem download do acervo para smoke ou comparação de versão. O wheel0.4.4 e o
plugin2.5.0 anteriores permanecem imutáveis. Um build local não prova promoção
ao consumidor, deploy, instalação/uso no operador, integração Dataprev ou98%.
Não altera transporte, identidade, conta, parâmetros reais ou agenda da Ana.

## Extensão2.3.0 e migração anterior de1.x

O Loki recebe dados, valida, calcula, gera documentos, registra e entrega.
Leitura documental e comparação são externas. As ferramentas antigas de extração
e execução especial foram retiradas; snapshots e evidências históricos permanecem
auditáveis. A empresa de teste usa o fluxo e gates comuns, sem modo especial.
Versões internas servem à auditoria; o fluxo é cálculo, geração e revisão.

O novo caminho é `get_process_contract(process_type)` → `get_case(case_id)` →
`receive_case_data(case_id, request)` → `run_prepared_case_workflow` ou as operações
de cálculo, geração e revisão declaradas no contrato. Os contratos de cadastro e
histórico em lote continuam sendo específicos e sujeitos a autorização.

O request `loki.case-data/1` contém `schema_version`, `request_ref`,
`expected_snapshot`, `data` e `field_sources` opcional. O snapshot vem de
`get_case.input_snapshot`; `data` é o conteúdo da seção `data_section`, sem outro
envelope. Fontes opcionais por campo usam `kind=document|harness|declaration|inference|context|history|rule`, `reference`
e `locator`; `content_hash`/`foundation` preservam hash e fundamento quando aplicáveis.
Correção, concorrência, idempotência e gates humanos continuam no backend.

`meu_acesso` e `get_operator_context` conservam seus campos e acrescentam
`runtime_instructions`. Esse fallback entrega orientação; não restaura contratos
retirados. `loki_obter_instrucoes` mantém allowlist e autorização pelo host.
`loki_verificar_versao` compara apenas versões declaradas. Plugin mínimo permanece2.0.0;
Na candidata atual, o recomendado é 2.8.0 e o contrato 2.8.0 é aditivo;
cliente2.0.0 permanece compatível. Contrato1.x declarado é incompatível; cliente desconhecido
continua `compatible=null`, sem presumir instalação. `refresh_tools_required=null`
permanece desconhecido até conferir o catálogo no aplicativo.

Prepare o consumidor e a atualização do plugin juntos, preserve backups e
proveniência e faça o corte coordenado pelos gates/runbook do backend. Não inicie
um caminho antigo se o catálogo estiver desatualizado. Atualize/reconecte o catálogo
na interface somente quando necessário, preservando OAuth e identidade. Instalar,
carregar a skill, consultar instruções e executar são provas separadas.

## Atualizar e validar

1. Edite os domínios Markdown e metadados JSON em `src/mcp_loki_updates/data/domains`.
   Use somente operações implementadas no consumidor; não invente regra trabalhista.
2. Eleve versões de domínio/instruções/contrato conforme compatibilidade. A versão
   do pacote também muda ao mudar qualquer byte distribuído. Atualize
   `pyproject.toml`, `__init__.py`, `provider.py`, `scripts/promote.py` e `uv.lock`.
   Plugin, guias e scripts têm versão própria; dependências permanecem fixadas.
3. Recalcule SHA256 dos bytes UTF-8/LF de cada Markdown e JSON em `release.json`.
   Revalide integridade, allowlist, permissões, compatibilidade antiga recusada,
   cliente desconhecido, novo writer e proveniência antes do build.
4. Execute os testes apropriados, ruff/mypy e `uv build --wheel`. Verifique os bytes
   do wheel contra o fonte com `scripts/promote.py.validate_wheel`; só então gere
   proveniência. Árvore suja usa `dirty=true` e HEAD/tree da base, nunca release
   commitada fictícia. Não renomeie um wheel anterior nem sobrescreva bytes distintos
   sob a mesma versão.
5. Promoção ao checkout consumidor exige destino explícito, wheel e proveniência.
   O script copia esses artefatos; não modifica lock, OAuth, permissões ou deploy.
   O consumidor fixa wheel, revisa lock e valida integração. Build local não comprova
   publicação, descoberta MCP, rotina instalada nem aceite individual.

No servidor, siga `AGENTS.md` de cada repositório e use a `.venv` própria existente.
Não aponte testes destrutivos ao banco real. Não faça commit, push, merge ou deploy
por consequência de construir/validar o pacote; siga a autorização vigente.

## Entrega e rollback

A entrega padrão é ao solicitante autenticado: use `prepare_delivery(case_id, include_drive=False)` e preserve `version_id` quando houver. O plano usa `publication_scope=private_authenticated_requester`, `drive_requested=false` e `destination=null`. Execute `execute_delivery(case_id, delivery_id)` e consulte `get_delivery_status` com o mesmo delivery_id nas retomadas. O recibo traz `requester_documents` com `authenticated_path` e `mcp_resource`, e `drive_documents=[]`. Somente DELIVERED comprova a disponibilização autenticada observada; não comprova download, pagamento ou transmissão. Sem aceite documental privado corrente, permanece PENDING com `requester_delivery_approval_missing`; aprovação, revisão, fontes, bytes/hashes, PII e conferência técnica mantêm seus gates. Não chame `authorize_delivery` neste caminho: ele recusa `delivery_drive_not_requested`.

Não configure nem ative o Drive nesta entrega. Drive Izzi é opção futura: somente um pedido humano externo explícito permite `prepare_delivery(case_id, include_drive=True)`. Nesse caminho, apresente pacote/revisão/hash/destino e aguarde intenção humana própria antes de `authorize_delivery`, com `delivery_id`, `plan_hash`, `human_message`, `message_reference` e `authorize_external_delivery=true`; o aceite privado anterior não autoriza envio externo. Destino/credencial do host ausentes ou falha mantêm a entrega ao Drive PENDING. Não envie folder, conta, token ou URL no payload; não use Drive Iris nem PUBLIC. Estas instruções não provisionam acesso nem removem gates de publicação.

Retry não duplica entrega nem recalcula. Geração ou conferência não atesta entrega, aceite, pagamento ou transmissão.

Rollback restaura o conjunto backend+wheel+lock compatível e segue o runbook do
consumidor, incluindo conciliação de novas escritas. Não faça downgrade de banco,
altere pin/assinatura do kit legado ou troque identidade para contornar falha.
Os registros anteriores de publicação em `docs/` são históricos e preservados;
não comprovam o estado servido desta candidata nem atualização das instalações.

A candidata0.4.5 define entrega autenticada ao solicitante como padrão e Drive como opção futura explícita; contrato MCP2.5.0 é aditivo, mínimo de plugin2.0.0. Os wheels0.2.0,0.2.1 e0.2.2 já construídos permanecem imutáveis.

Compatibilidade da candidata0.4.5: fonte `loki-document-kit`0.2.0, com allowlist
operacional explícita e comandos para dados+fontes/conferência técnica. O kit0.1.0
usa escritores aposentados e precisa de migração separada. Não sobrescrever
artefatos, locks, pins ou assinaturas antigos. Esta candidata não comprova
instalação nem troca o executor da Ana. A compatibilidade básica do kit0.2.0 limita-se às operações2.0 que ele declara;
não comprova suporte aos novos escritores2.1. Build/promoção de consumidor e
backend continuam sujeitos aos gates de implantação.


Esta candidata orienta100%HTTPS em `https://loki.tominho.com/mcp`, com identidade
própria por pessoa/executor. A harness lê, extrai, interpreta e prepara; envia
parâmetros JSON/CSV tipado; proveniência detalhada é opcional. Originais permanecem na harness.
O resultado contém documentos quando gerados ou recibo persistido/relido para
atos sem documento, sem PDF artificial. Caso único, lote operacional e ajustes
da empresa exigem os contratos realmente oferecidos pelo catálogo HTTPS.
Exigência de novo anexo nativo, endpoint ausente ou identidade do executor não
provisionada é lacuna explícita; não use transporte alternativo nem reclassifique
fonte. Veja [WORKFLOWS.md](../plugins/loki-bootstrap/skills/operar-loki/references/WORKFLOWS.md)
para estados, retorno e retomada; esta árvore não comprova publicação ou adoção.


`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Extensão eSocial2.3.0

Provider0.4.5, contrato2.5.0 e instruções/plugin2.5.1 preservam o mínimo2.0.0 e a
compatibilidade declarada de2.0/2.1; cliente desconhecido continua desconhecido.
A allowlist e as permissões dos domínios permanecem: consulte `geral` e
`alteracao_cadastral` para as cinco ferramentas HTTPS de modo fiscal e parâmetros.
Veja o roteiro nativo [ESOCIAL.md](../plugins/loki-bootstrap/skills/operar-loki/references/ESOCIAL.md). A configuração de homologação
pode persistir por intenção de administrador humano; não transmite. Operação
permanece PENDING/recusada sem fila/executor fiscal, assinatura, representação
e recibo de homologação verificados. S-1005 local não comprova transmissão.
Perfis por estabelecimento/data usam os escritores empresariais com CAS,
origem opcional e releitura; seleção não comprova consumo financeiro.

Esta distribuição não provisiona acesso fiscal, não emite eventos pelo catálogo
HTTPS e não instala o plugin no operador. Wheels anteriores, inclusive0.3.0,
permanecem imutáveis; promoção/publicação exigem revisão e gates do consumidor.

## Correção da harness2.3.1 preservada

Provider0.4.5/instruções e plugin2.5.1 mantêm contratoMCP2.5.0 e mínimo2.0.0.
O helper offline `mcp-resource` salva bytes embutidos da resposta completa com
URI/SHA256/tamanho explícitos; os roteiros orientam seleção histórica tipada,
complemento somente de nome vazio pelo contrato e checks após leitura real.
Não há novo transporte, autofill de CTPS/CDI ou fórmula universal de avos.
Script e lock permanecem juntos; dependências não mudaram. Wheels0.4.1 e
anteriores continuam imutáveis. Esta candidata não comprova publicação,
instalação, carregamento ou execução real na Ana, nem muda agenda/credenciais.

## Comunicação2.5.0

Provider0.4.5/instruções e plugin2.5.1 orientam conclusão primeiro, pontos
essenciais e próxima ação, com alvo de60palavras no resumo. Ressalvas, evidências
e payloads completos permanecem; contrato2.5.0 e mínimo2.0.0 não mudam.
O Slack apresenta avisos compactos e a íntegra segue consultável pelo MCP.
Fonte, build, publicação, instalação no cliente e qualidade real são provas
separadas; esta alteração não atualiza a agenda ou a instalação da Ana.

## Refino e encaminhamento2.5.0

Pergunta curta na thread antes de hipótese; questão técnica exige resposta do
autor e consulta ao código, sem corrigir automaticamente. Procedimentos seguem
ao contato DP cadastrado (Rafa), uma vez. Estados internos e replay não geram
avisos repetidos. Triagem/correção e confirmações permanecem humanas e com gates.

Contrato2.5.0 acrescenta o comando HTTPS tipado `answer_problem` para resposta
de refino no chat autenticado do relator, com revisão/evento correntes, declaração
de apresentação e replay idempotente; não concede aprovação ou identidade Slack.


## Continuação com DP2.5.0

Resposta do contato DP convidado retoma somente o assunto solicitado. A memória
por assunto e os destinos propostos são consultáveis pelo suporteHTTPS; preparação
para Ana, configuração e desenvolvimento continuam sujeitos aos respectivos atos
autorizados. Novo ciclo exige proprietário humano, revisão/job correntes, assuntos
e motivo pelo contrato restart_problem_refinement. Uma pergunta/próximo passo por
mensagem, palavras comuns e alvo60palavras; sem progresso, nova menção ou repetição.
Esta versão não altera dados reais, sistema/agenda da Ana nem executa correções.
