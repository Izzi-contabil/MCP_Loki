# Afastamento

## Responsabilidade já dividida no consumidor rescisório

Confira o schema de `get_process_contract("rescisao")` antes de preparar seus
afastamentos. `representacao=episodio_integral` conserva o episódio e a partição
legada; `representacao=faixa_pagador` identifica intervalo já separado por
responsável e evita uma segunda retirada dos primeiros15dias.
O opt-in não presume concessão, espécie, mesma doença ou continuidade de faixas
adjacentes. Não transforme `HistoricalLeave.payment_periods` automaticamente
em episódio clínico nem altere datas para fechar avos.

Use `retorno_episodio` somente para retorno efetivo informado no alcance do
contrato. Fim da faixa de um pagador não comprova retorno ao trabalho. Se o
retorno necessário ao reinício de férias não for conhecido, conserve essa
dependência; não retenha automaticamente os componentes independentes.
O fato documental e o consumo por rescisão/13º/férias têm finalidades distintas.

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


Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Não invente diagnóstico, motivo, duração, enquadramento, legislação ou prazo. Preserve dados ausentes, fontes e divergências sem converter ausência em zero. Submeta decisões aos responsáveis e cumpra os gates humanos declarados no runtime. Não publique ou transmita alterações por conclusão automática de leitura ou extração.

Consulte `get_process_contract` para o schema da seção `leave` e envie seu conteúdo em `data` por `receive_case_data`, sem outro envelope. A harness lê o atestado; o Loki recebe somente fatos e proveniência. Quando `document_outputs=[]`, devolva o recibo persistido com caso, versão/revisão, status e pendências e releia o registro. Não exija PDF, inspeção visual ou aceite de documento inexistente; checks factuais de um pacote existente seguem o contrato.

Respeite identidade, vigência e fontes. Recebimento de dados ou pacote factual não comprova aplicação ao vínculo. Quando o contrato exigir efeito, `apply_case_effects` usa sua intenção humana e os gates próprios; preserve ID, revisão e status do efeito e releia o registro antes de afirmar aplicação. Atestado preparado, recebido, registrado e efeito aplicado são estados distintos. Não transmita evento nem tome decisão humana pela automação.

Toda operação usa o conector HTTPS `https://loki.izzicontabil.com.br/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Recusa com campo e código de regra

O campo e o código valem somente quando a resposta servida os apresentar.
Quando o Loki recusar dados de afastamento, olhe a lista `errors`: cada item
traz o campo exato (por exemplo `leave.retorno`) e um código que diz qual regra
não fechou. Corrija só o campo apontado, conferindo com o documento original, e
reenvie com um novo `request_ref` e o snapshot atual do caso. Reenviar o mesmo
dado sem corrigir, com ou sem `field_sources`, vai ser recusado de novo. Se o
documento realmente traz essas datas, não force o valor: registre a dúvida com
a DP antes de reenviar.

Códigos de afastamento:

- `afastamento_inicio_antes_da_admissao`: início antes da admissão.
- `afastamento_inicio_diverge_do_primeiro_periodo`: início diferente do
  primeiro período.
- `afastamento_periodos_descontinuos`: períodos com lacuna ou sobreposição.
- `afastamento_fonte_de_retorno_sem_data`: fonte de retorno sem data de
  retorno.
- `afastamento_retorno_fora_da_vespera`: o retorno deve ser o dia seguinte ao
  fim do último período.
- `afastamento_periodo_invertido`: período com fim antes do início.

## Preparação corrente: recusa por campo

O campo e o motivo valem somente quando a resposta servida os apresentar.
Numa preparação corrente (por exemplo, depois de `restart_case`),
`receive_case_data` recusa `leave` incompleto ou fora do modelo com
`leave_preparation_requires_complete_input`, e `errors` traz um item por campo:
`{"field": "leave.retorno", "reason": "afastamento_retorno_fora_da_vespera"}`.
`[*]` indica um item da lista (ex.: `leave.periodos[*].fim`); a mesma regra
pode apontar mais de um campo. `reason` é um código `afastamento_...` da lista
acima, `missing` (campo obrigatório ausente) ou `extra_forbidden` (chave fora
do schema, sem o nome da chave). Corrija o campo apontado conferindo com o
original e reenvie a seção `leave` completa, com novo `request_ref` e o
snapshot atual. A fonte de um campo vai no campo `*_source` do schema (ex.:
`retorno_source`, `identity_source`), nunca numa chave própria dentro de
`leave`: essa chave volta como `extra_forbidden`.

## Atestados consecutivos e licença-maternidade

Regras da DP (18/11/2026):

- Lance cada documento como um registro próprio, respeitando o período de
  cada um: dois atestados de 5 dias são dois afastamentos, cada um com
  `inicio`, `retorno` (dia seguinte ao fim) e a fonte do seu atestado. Não
  junte atestados num afastamento só e não estenda um registro para cobrir o
  seguinte. Atestados encostados (o retorno de um é o início do outro) não são
  sobreposição.
- Licença-maternidade não é falta e não reduz o aquisitivo de férias: use
  `categoria: licenca_maternidade` e não lance os dias como falta.
- No histórico de onboarding usado pelas férias, quando
  `get_company_onboarding_contract` trouxer `historical_state.vacation_rules`:
  o `leave` de atestado ou licença-maternidade no aquisitivo leva
  `vacation_effect: {"kind": "sem_reducao", "source": {"kind":
  "operation_rule", "rule": "atestado_e_licenca_maternidade_nao_sao_falta",
  "message_reference": "CX-AB5EE178", "category": "atestado" |
  "licenca_maternidade"}}`. O atestado exige `return_on`. Atestado com período
  pago pelo INSS é benefício e exige a decisão do DP (`dp_decision`), como
  qualquer outra categoria. O roteiro completo e os códigos estão no domínio
  `ferias` ("Data do cálculo, afastamento sem redução, gozo antecipado e
  abono").
- Quando o schema servido de `dados_ferias` tiver `gozo_antecipado_source`,
  o Loki aplica a CLT (arts. 131 e 133) ao `leave` do aquisitivo sem
  `vacation_effect`: basta `category_code` e `payment_periods` com
  `responsibility` (`empregador`, `inss` ou `sem_remuneracao`) em todos os
  dias. Lance também os afastamentos contíguos anteriores ao aquisitivo. Um
  afastamento do INSS o mês inteiro, já qualificado e iniciado antes da
  competência, qualifica sozinho o mês da folha (`folha-v33`). Roteiro e
  códigos no domínio `ferias` ("Afastamento e fracionamento pela CLT").

## Afastamento no histórico e no diagnóstico da folha

Os códigos valem somente quando a resposta servida os apresentar. Fatos
históricos de afastamento do onboarding recusados em
`declaracao_do_vinculo_invalida` trazem `type` com o código da regra
(`historical_leave_return_incompatible`, `historical_leave_payment_outside_leave`,
`historical_leave_payment_overlap`, `historical_leave_payment_inverted`); a
tabela completa e a regra de cobertura até o corte
(`leave_history_coverage_not_certified`), inclusive a cobertura que termina
depois do corte (`historical-state-v2`), estão no domínio `ferias`. Corrija
conforme a fonte; nunca ajuste a data só para passar.

Afastamento antigo opaco (`unqualified_documentary_facts`,
`operational_semantics_missing` ou `leave_observations_not_classified`): não
grave um `leave` novo para o mesmo afastamento, porque duplicaria a ocorrência;
mantenha o gap pendente e informe a operadora. A exceção é o cálculo de férias
com `vacation_rules`: quando a recusa trouxer `blocking_facts` com
`kind: afastamento`, o `leave` confirmado que começa na data do fato e o cita
em `qualifies_legacy_fact_ids`, com `vacation_effect`, qualifica o fato só
para férias (domínio `ferias`). O 13º e o estado não mudam.

Quando o dossiê da folha apontar `leave_qualification.origins[*]` com
`origin: "operational_effect"` e o `case_id` deste caso, complete categoria,
`policy_version` e a responsabilidade de cada período pela nova preparação
acima, quando o contrato oferecer; o roteiro está no domínio `folha_mensal`.
Não infira categoria nem pagador.
