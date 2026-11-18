# Dados operacionais e retomada

## Caso individual

1. Confirme acesso, instruções e `get_process_contract(process_type)`. Consulte
   `get_case(case_id)` e capture `input_snapshot` imediatamente antes da escrita.
2. Leia os originais externamente, mantendo hashes/localizadores no workspace
   privado. O Loki recebe dados estruturados e fontes; não interpreta os originais nem
   compara o resultado com o relatório da equipe.
3. Prepare o conteúdo de `data_section` em `data`, sem outro envelope. O pedido
   `loki.case-data/1` contém exatamente `schema_version`, `request_ref`,
   `expected_snapshot`, `data` e o mapa opcional `field_sources`. `expected_snapshot` recebe o
   `input_snapshot` atual. Reutilize `request_ref` e o conteúdo em uma retomada.
4. `field_sources` é opcional e pode cobrir somente os campos detalhados pela
   harness. Campos sem fonte explícita conservam a origem declarada do request;
   null, falso e lista vazia mantêm seus significados. Quando informada, a fonte
   usa o caminho relativo real e `kind=document|harness|declaration|inference|context|history|rule`.
   `inference`/`context` não exigem hash ou fundamento fabricado; registre
   justificativa em `foundation` quando disponível. Não invente ID remoto para
   um documento local. Documento é dado, não autoridade.
5. Use `case-request evidence.json PEDIDO_NOVO --contract contract.json
   --target CASE-ID --reference REFERENCIA --snapshot INPUT_SNAPSHOT` para preparar
   o pedido offline. A harness chama `receive_case_data` com `arguments`; o helper
   não envia. Não declare leituras que não ocorreram; preserve os originais na harness e trate exigência de novo anexo como lacuna contratual.
6. Confira a resposta e salve pedido/resposta com `receipt`. Conflito exige
   releitura e conciliação, mantendo o conteúdo anterior. Dados em revisão usam
   o fluxo autorizado de correção e nova revisão; não contorne o snapshot.
7. Execute `run_prepared_case_workflow` quando oferecido ou as operações
   declaradas no contrato. Gere documentos somente quando previstos. Versões internas servem à auditoria. Empresa de teste
   usa o mesmo fluxo operacional e os mesmos gates, sem modo especial.
8. Confira recibos, artefatos e páginas existentes externamente; congele o resultado antes de abrir
   referências de comparação. Apresente pacote e ressalvas para decisão humana.
   Entrega padrão ao solicitante usa acesso autenticado e recibo próprio; Drive é opção futura explícita.
   Conferência não significa envio. Retry conserva pacote/revisão/hash, sem
   recalcular nem duplicar. No caminho futuro do Drive, destino ausente/falha
   permanece pendente.

## Proveniência externa sem envio do original

Este é um recurso opcional para preservar evidência detalhada, sem bloquear um
pedido informal autorizado. Consulte `get_harness_source_contract()` e salve o contrato privado. Prepare o
manifesto `loki.harness-source/1` na harness e valide-o offline por
`parameters manifesto.json PEDIDO_VALIDADO --schema contrato-fonte.json
--schema-pointer /request_schema`. O helper valida e salva parâmetros, sem enviar.
A harness chama `register_harness_source(case_id, request)` e relê
`get_harness_source(case_id, source_id)`. Confira `EXTSRC`, hashes, papel e manifesto;
`original_archived=false` declara que o original permaneceu na harness. Reutilize
o ID retornado com `kind=harness`, referência e hash correspondentes em
`field_sources`; preserve localizador e fundamento por campo.

No onboarding, use `register_onboarding_harness_source(onboarding_id, request)`
e `get_onboarding_harness_source(onboarding_id, source_id)` no escopo do próprio
onboarding_id. Não use um source_id de caso ou de outra empresa como substituto.
Alguns contratos históricos conservam o nome `document_id`; um ID EXTSRC continua
identificando manifesto da harness e não documento arquivado. Preserve o nome do
campo aceito, tipo e origem, sem inventar DOC. Manifesto autenticado não atesta
leitura independente nem verificação dos bytes originais pelo Loki.

Exemplo estrutural sintético, sem substituir o schema real do processo:

```json
{
  "data": {"campo_cents": 0},
  "field_sources": {
    "campo_cents": {
      "kind": "declaration",
      "reference": "declaracao-externa-sintetica",
      "locator": "pagina:1/campo:valor",
      "content_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  }
}
```

## Recomeçar ou descartar um caso

Para jobs duráveis, preservação de imports, correção explícita da população da
folha e cancelamento tipado, siga
[CAPACIDADES_DP.md](CAPACIDADES_DP.md). Use somente rotas anunciadas pelo
contrato servido; publicação da PR240 e disponibilidade na harness exigem
conferência própria. Uma falha de geração não autoriza reinício do caso.

Consulte `get_case` e capture `correction_snapshot` atual. Somente pessoa
autorizada com decidir_chat e intenção específica pode chamar
`restart_case(case_id, expected_snapshot, human_message)` ou
`cancel_case(case_id, expected_snapshot, human_message)` pelo HTTPS.
A automação apresenta caso, estado, pendências e ação proposta ao responsável;
não assume essa capacidade nem interpreta uma autorização geral de manutenção
como decisão sobre todos os casos antigos.

Confira elegibilidade antes da escrita. Caso com aprovação ou efeito exige a
conciliação indicada pelo contrato e pode recusar reinício/cancelamento. Ausência
de aprovação num resumo não prova ausência de efeito. Reinício de `local-v1`
para `structured-v1` exige recebimento de dados novos com origem declarada e conserva documentos, eventos,
decisões e revisões anteriores; não apaga trilha. Snapshot obsoleto pede releitura
e nova intenção quando exigida. Depois da ação humana, releia o caso para conferir
o estado efetivamente persistido.

## CSV operacional e retomada por item

CSV operacional é entrada tipada de parâmetros preparados pela harness.
Somente quando o catálogo HTTPS oferecer `get_operational_batch_contract()`,
consulte-o e confira seus escritores antes de preparar o envio. Se ausente,
registre lacuna de distribuição e use as operações individuais anunciadas;
não invente rota de lote ou dispatcher. Preserve
referência estável por lote e por item, empresa, processo, pessoa/episódio,
snapshot/revisão, dados e proveniência. Envie apenas o schema aceito, sem
originais, gabarito ou CSV de leitura usado como anexo genérico.

O executor de lote deve usar o mesmo domínio do caso único. Cadastros/históricos
CSV e seus DTOs não comprovam suporte ao lote de processos: staging não comprova execução.
Se o catálogo não oferecer o contrato operacional, registre lacuna explícita;
não anuncie ferramenta inexistente nem use onboarding como substituto.

No consumidor que oferecer esse contrato, `execute_operational_batch(request)`
recebe `schema_version=loki.operational-batch/1`, `request_ref` estável e
`csv_content` como texto UTF-8, sem upload/anexo. O CSV usa delimitador `;` e
colunas exatas `schema_version;record_ref;operation;arguments;depends_on`.
Cada linha declara `loki.operational-command/1`, operação da `allowed_operations`
corrente, `arguments` objeto JSON estrito e `depends_on` array JSON de referências
anteriores. Até100 linhas e8MiB, ou limite menor retornado pelo contrato.
Referências usam objeto `{"$ref":"record_ref.path.to.result"}`; conserve a
dependência correspondente e a ordem anterior, sem interpolar texto.

Prepare privadamente a lista de comandos com `record_ref`, `operation`,
`arguments` e `depends_on`. Execute `render-operational-csv comandos.json
CSV_NOVO --contract contrato-lote.json`; depois `operational-batch-request
CSV_NOVO/parameters.csv PEDIDO_NOVO --contract contrato-lote.json
--reference REFERENCIA_ESTAVEL`. Os helpers só validam/preparam. A harness envia
`arguments` de request.json pelo HTTPS e salva a resposta completa com `receipt`.
Dados informais sem fonte formal também são válidos no lote.

O lote é sequencial e não atômico; conserva as permissões, escopo e validações
de cada operação do caso único. O recibo retorna `batch_id`, status e `rows` com
`record_ref`, status `PENDING|STARTED|SUCCEEDED|FAILED|BLOCKED` e resultado ou código
de erro por linha. `SUCCEEDED` confirma a chamada; somente o resultado do domínio
permite afirmar `APPLIED`, cálculo ou registro. Consulte
`get_operational_batch(batch_id)` com o mesmo ator e escopo para reler o estado.

Na retomada, preserve request_ref e hash/conteúdo. O replay retorna resultados
prontos e pode retomar linhas PENDING. Se a resposta inicial se perder sem
batch_id, repita somente o mesmo pedido idempotente para recuperar o recibo;
com batch_id conhecido, consulte antes. Linha STARTED com resultado ambíguo não
é reexecutada automaticamente: concilie o caso/registro de origem antes de nova
ação. Não gere nova referência para contornar essa retenção.

Confira resultado e pendências por item, incluindo os inválidos, além do agregado.
Distinga recebido, pendente, preparado, calculado, registrado e aplicado. Uma
resposta perdida exige consulta pelo identificador/referência antes do retry;
conserve conteúdo e referências estáveis dos itens já enviados. Conflito de
snapshot ou conteúdo diferente pede conciliação, sem duplicar nem apagar o recibo
anterior. ACK de staging não é cálculo ou efeito confirmado.

## Registro sem documento

Quando `document_outputs=[]` ou o contrato declarar somente registro, devolva
recibo persistido com identificador do caso/registro, operação, status,
versão/revisão ou snapshot e pendências; depois releia o registro pelo HTTPS.
Confirmação de recebimento não comprova aplicação. Quando existir efeito próprio,
execute-o somente com a intenção humana e os gates exigidos e confira seu recibo.

Afastamento recebe fatos na seção `leave` do contrato atual. Para programação de
férias, consulte `get_vacation_schedule_contract()`; se oferecido, use
`record_vacation_schedule(case_id, request)` e releia por
`get_vacation_schedules(case_id)`. O schema `loki.vacation-schedule/1` usa `action`
`register|rectify|cancel`, `request_ref`, `expected_snapshot=correction_snapshot`,
`reference`, `data` com `aquisitivo_inicio`, `aquisitivo_fim`, `inicio`, `fim`,
`dias_abono` e fontes opcionais conforme o contrato. Retificação/cancelamento exigem pessoa
com CORRIGIR_DADOS, `human_message`/`message_reference` e
`supersedes_id`/`supersedes_input_hash`; o registro de planejamento com
OPERAR_CASOS não confirma gozo ou pagamento. Não improvise um escritor a partir
de um histórico de planejamento. Sem pacote, não chame
`get_package_check_request`, não invente PDF, inspeção visual ou aceite documental.
Se houver pacote factual existente, confira somente os checks factuais retornados
no seu contrato. Atos sem documento e documentos gerados seguem suas saídas próprias.

## Empresa e dados vinculados

Para empresa e estabelecimentos, parâmetros e regras, confira os contratos HTTPS
específicos, CNPJ, escopo, revisão esperada, vigência, fontes e histórico antes de
propor diferenças. Conserve a revisão humana e a intenção exigidas. Não atualize
outra empresa do grupo nem confunda ajuste do perfil do empregado com atualização
empresarial. Envie somente parâmetros estruturados, preserve recibo persistido e
releia o objeto para conferir os valores e a revisão aplicada. Proposta, staging e
recebimento permanecem distintos de aplicação confirmada. Contrato não oferecido
é lacuna explícita, sem nome de API presumido.

O cadastro empresarial usa os escritores existentes: consulte `get_client_config(cliente_slug)` e `get_client_config_history(cliente_slug)`, prepare `alteracoes` na harness e valide por `validate_client_config`. Use o `doc_hash` atual como `expected_hash`; vigência permanece nos campos tipados da regra, sem substituir cadastro vigente por rascunho. Aplique somente pelo `apply_client_config` autorizado, com `motivo`, mesmas alterações, hash e flags necessários; depois releia cadastro/histórico. `RASCUNHO` e `SEM_ALTERACAO` não comprovam aplicação; somente o resultado `APLICADO` com nova revisão/hash relidos sustenta essa afirmação.

`proveniencia` é opcional nos dois escritores. Quando utilizada, segue `loki.company-config-provenance/1` com `field_sources` por caminho alterado e `kind=declaration|inference|context|external_reference|rule`; referência, localizador, `content_hash` e `foundation` são opcionais, sem documento ou hash inventados. Fontes parciais recebem declaração do ator nos demais campos. Sem origem detalhada, o próprio request autorizado é declaração. O recibo/resumo retorna `receipt_hash`, `actor_id`, `input_hash`, `fields` e `assurance`, sem expor texto livre; preserve-o e confira os valores pelo readback autorizado. A resposta e a releitura preservam `field_basis` por caminho; inference/context usam `inferred`, sem promover informação recebida ou inferida a confirmed automaticamente.

Campo reservado ou gate que realmente exige evidência usa `confirmacao` específica. Primeiro valide com `expected_hash` do mesmo CAS e `reserved_paths`/`evidence_gate_paths` exatos; mostre a prévia ao humano e aplique com o mesmo objeto e `human_message` efetiva. Só pessoa provisionada com configurar_cliente e autoridade administrativa vigente realiza esse ato. A automação não recebe essa autoridade por usar lote ou empresa de teste. Não use confirmação genérica, outro CNPJ ou nova referência para contornar conflito; pendência específica não exige fonte formal universal.

## Cadastro e histórico em lote

Consulte `get_company_onboarding_contract` e a autorização efetiva. Apenas os
papéis administrativos aceitos pelo host realizam essas escritas. Reuse o lote
corrente; recepção/staging não significa cadastro ou histórico aplicado.

Os leitores locais podem preparar CSV de leitura como evidência externa e CSV
`loki.batch-csv/1` para o contrato de onboarding vigente. `source-csv` mantém seu
formato local de origem; não o envie como `field_sources` operacional. Use
`csv-request` somente com `onboarding-csv`; no tipado,
conserve referência, revisão e hash. Submeta chunks e valide/aplique apenas pelos
escritores do contrato, com fontes reais, snapshot/hash corrente e readback.
Não envie documentos originais pelo sincronizador antigo do kit desktop.
O helper2.3.0 reconhece o destino legado `onboarding-source` e recusa novas
preparações com `typed_parameters_required_instead_of_source_attachment`.
Migre a preparação para parâmetros tipados pelo contrato; leituras, pedidos e
checkpoints históricos permanecem privados e preservados. Não sobrescreva o kit
ou artefatos antigos nem repita upload para contornar a recusa.

## Retomar

Conserve em pasta privada originais, leitura, fontes, contratos, pedidos,
respostas, recibos, referências, revisão e hashes. Resposta perdida exige leitura
antes de repetir. Erro ou pendência não vira sucesso porque existe um recibo.
Nova versão do plugin exige recarregar a sessão; instalação, catálogo, serviço
publicado e consumo real são provas distintas. Não altere OAuth, credenciais,
assinatura, pin do kit antigo ou agenda para contornar falha de leitura/contrato.

Quando houver pacote, conferência técnica usa `get_package_check_request` e `record_package_checks`, schema `loki.package-checks/1`, hashes/revisão/documentos exatos e PASS/FAIL explícito nos checks retornados. Para PDFs, confira content, structure, visual e pii_policy de cada documento. Inclua informativo obrigatório da admissão e provisões quando presentes. Registre somente conferência externa realizada; não atesta comparação com relatório, aprovação humana nem publicação.

A entrega padrão é ao solicitante autenticado: use `prepare_delivery(case_id, include_drive=False)` e preserve `version_id` quando houver. O plano usa `publication_scope=private_authenticated_requester`, `drive_requested=false` e `destination=null`. Execute `execute_delivery(case_id, delivery_id)` e consulte `get_delivery_status` com o mesmo delivery_id nas retomadas. O recibo traz `requester_documents` com `authenticated_path` e `mcp_resource`, e `drive_documents=[]`. Somente DELIVERED comprova a disponibilização autenticada observada; não comprova download, pagamento ou transmissão. Sem aceite documental privado corrente, permanece PENDING com `requester_delivery_approval_missing`; aprovação, revisão, fontes, bytes/hashes, PII e conferência técnica mantêm seus gates. Não chame `authorize_delivery` neste caminho: ele recusa `delivery_drive_not_requested`.

Não configure nem ative o Drive nesta entrega. Drive Izzi é opção futura: somente um pedido humano externo explícito permite `prepare_delivery(case_id, include_drive=True)`. Nesse caminho, apresente pacote/revisão/hash/destino e aguarde intenção humana própria antes de `authorize_delivery`, com `delivery_id`, `plan_hash`, `human_message`, `message_reference` e `authorize_external_delivery=true`; o aceite privado anterior não autoriza envio externo. Destino/credencial do host ausentes ou falha mantêm a entrega ao Drive PENDING. Não envie folder, conta, token ou URL no payload; não use Drive Iris nem PUBLIC. Estas instruções não provisionam acesso nem removem gates de publicação.

Para usar fecho anterior como abertura de provisões, selecione explicitamente `opening_selection={kind:"previous_revision",competencia,input_hash,result_hash}` no contrato de folha_mensal/fechamento. Envie `opening_cents=null` nos movimentos; `opening_origin` é resolvido e rastreado pelo servidor, não preenchido pela harness. A revisão deve ser da competência imediatamente anterior e ainda corrente. Sem fechamento conhecido, a abertura e seus totais dependentes permanecem desconhecidos; não crie zero. Saldo documentado de abertura também pode ser recebido com fonte qualificada pelo contrato, sem seleção automática de uma revisão. Retificação da origem exige conciliação e nova revisão do pacote dependente.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.


Se a operação retornar `version_id`, preserve esse identificador em `get_package_check_request(case_id, version_id=...)`, dentro do request de `record_package_checks` e em `prepare_delivery(case_id, version_id=...)`. Siga `required_checks` retornados: PDFs usam content/structure/visual/pii_policy; recibos factuais sem PDF usam structure/timeline/sources/pii_policy. Não invente inspeção visual de PDF inexistente. Revisão, fontes, build, elegibilidade, ARTs e hashes são da mesma versão; correção/superação exige outro pacote e outro aceite. `execute_delivery`/`get_delivery_status` usam o delivery_id que já contém esse vínculo, sem escolher outra versão ou refazer cálculo.

Retificação de efeitos usa `apply_case_effects` com o par obrigatório
`supersedes_effect_id` + `supersedes_input_hash`; para retirar o efeito, envie
`withdraw:true` com esse par. Preserve o original e sua trilha. O servidor recusa
forks e não reativa o efeito substituído por replay. Se uma folha já aprovada
depende da origem retificada/retirada, faça a reconciliação exigida antes de
submeter sua nova revisão; aceite anterior não qualifica a origem alterada.

Na folha nova, `history_qualifications.payroll_context` segue
`loki.operational-payroll-context/1`: identifique alias, vigência, fontes e os
fatos qualificados exigidos, inclusive gozo confirmado e pagamento real.
Projeção, adiantamento ou efeito planejado não demonstram pagamento real.
Ausência de qualificação mantém pendência e valores dependentes desconhecidos,
sem completar zero. Consulte `get_process_contract` e os schemas atuais do
servidor antes de montar o pedido; esta orientação não substitui a validação.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## eSocial e parâmetros empresariais

Leia [ESOCIAL.md](ESOCIAL.md) para `get_company_esocial_contract`, `get_company_esocial_state`, `preview_company_esocial_mode`, `apply_company_esocial_mode` e `get_company_parameter_state`. A configuração de homologação pode ser persistida por administrador humano, mas não ativa fila, assinatura ou transmissão. O modo Operação continua PENDING/recusado enquanto a prontidão fiscal estiver ausente. Perfis `company_parameters` usam `validate_client_config`/`apply_client_config`, CAS e releitura por estabelecimento/data. A origem informal é aceita sem fonte formal universal; preservar informado/inferido/confirmado não comprova cálculo nem envio.

## Complemento de identidade ausente

`funcionario.nome` é identidade do caso, não um campo de `dados_rescisao` ou da
seção de cálculo. Consulte `get_process_contract` e `get_case` atuais. Somente se
o contrato oferecer `identity_completion_schema` e a rota autorizada, prepare o
request `loki.case-identity-completion/1` com `request_ref` estável,
`expected_snapshot=get_case.correction_snapshot`, `input_snapshot` corrente,
`expected_company_id`, `expected_employee_id`, `expected_admission_date` e `nome`
observado/declarado com origem honesta. Valide offline por `parameters` usando
`--schema contract.json --schema-pointer /identity_completion_schema`.

Use `complete_case_identity(case_id, request)` quando descoberto; se o contrato
anunciar `receive_case_data` como rota compatível para esse discriminador, envie
exatamente o mesmo request por essa rota, sem envelope `loki.case-data/1` e sem
misturar o nome à seção financeira. Rota ausente é lacuna de distribuição HTTPS;
não improvise escritor. Esse complemento só preenche nome antes vazio da mesma
empresa, pessoa e episódio. Nome já preenchido, divergência de identidade ou
snapshots antigos conservam recusa/pendência; não substitua nome nem cadastro.
Preserve recibo e replay idêntico, releia nome e ambos os snapshots antes de
retomar geração. A operação não cria decisão humana nem efeito financeiro.

## Destravar admissão: ficha, nome e recusas

Valem somente quando a resposta servida os apresentar; consulte o domínio
`admissao` em `loki_obter_instrucoes` para o roteiro completo.

- Ficha `ficha_registro/6`: Beneficiários quebra em até 8 linhas, só em
  espaços. Acima disso, ou palavra mais larga que a célula, a geração recusa
  com o campo identificado e nada é truncado (diagnóstico do dossiê:
  `error_type: "OverflowDeBeneficiarios"`): não abrevie nem invente; registre
  o impedimento. Ficha de modelo anterior pede nova geração.
  `empregado.beneficiarios` gravado só muda por nova preparação
  (`restart_case`, `preparation.mode=replace_process_inputs`) e reenvio completo.
- Nome diferente só em caixa, espaços ou forma Unicode NFC
  (`case_write_constraints` em
  `empregado.nome_completo` ou `identity_changed`):
  `preview_case_name_rectification` com `status: "READY"`,
  `basis: "case_only_equivalence"` e `registry_correction: null` → confirmação
  humana → `rectify_case_name` com a prévia corrente → recibo `RECTIFIED`,
  `registry_updated: false`; siga o `next_action` recebido
  (`run_prepared_case_workflow` ou `restart_case`), novo pacote e revisão.
  Acento, grafia, “case folding” (`ß` × `ss`) ou espaços sobrando no nome do
  cadastro exigem correção de cadastro pelo onboarding
  (`nominal_correction_requires_registry_correction`). Prévia anterior à
  atualização do serviço é refeita nos dois fundamentos.
- Recusa de `restart_case` ou blocker de `preview_admission_reconciliation`:
  siga somente o `next_action` recebido. `import_preservation` segue para
  `preview_import_preservation`;
  `import_preservation_blocked_by_pending_effects` vem com `next_action: null`
  (ex.: import documental com aprovação pendente). `cancel_case` recusado por
  efeitos nunca traz `next_action`: as prévias habilitam reinício, não
  cancelamento. Dependente de processo fora do acesso da conta vem só com
  `case_id` e `access: "not_authorized_for_process"`; não reutilize prévia
  bloqueada obtida por outra conta.
  Com `next_action: null` ou ausente, ou dependente protegido, pare, guarde a
  resposta e
  use [registrar-problema-loki](../../registrar-problema-loki/SKILL.md) com
  `case_id` e blockers, sem dado pessoal. Não contorne, cancele ou recrie.

## Recusas e prévias com motivo fechado

Valem somente quando a resposta servida os apresentar; o roteiro completo está
nos domínios `geral`, `admissao`, `rescisao` e `ferias`.

- `preview_import_preservation` (admissão/rescisão): folha mensal protegida
  com `classification: "equivalent"` e
  `reason: "employee_excluded_from_current_calculation"` deixa de bloquear:
  o cálculo de onde saiu o pacote da folha está ancorado e não inclui o
  funcionário (a prévia não recalcula a folha viva). `"unknown"` continua em
  `import_preservation_protected_dependency`. No restart,
  `import_preservation_consumer_changed` pede refazer a prévia;
  `reconciliation_dependencies_busy` (gravação em andamento na mesma empresa)
  pede tentar depois, sem forçar. Pacote envelhecido continua barrado na
  revisão (`calculo_desatualizado`).
- Folha: `preview_payroll_population_correction` aceita item só
  `{"matricula"}` e devolve `funcionario_id` em `population`; matrícula que
  passou a outra pessoa recusa com
  `payroll_population_rebound_requires_identifier` até o `funcionario_id` novo
  vir no item (confirme com o humano que é outra pessoa);
  `replace_payroll_population` exige `{funcionario_id, matricula}` copiados da
  prévia e o `preview_id`.
- Rescisão, afastamentos: `afastamento_representacao_mista` (`faixa_pagador`
  é tudo-ou-nada), `afastamento_concessao_incompativel`,
  `afastamento_pagadores_sobrepostos`, `afastamento_concessoes_sobrepostas`,
  `faixa_previdenciaria_exige_beneficio`,
  `beneficio_previdenciario_exige_pagador_inss`: corrija pelos dados reais,
  sem inventar benefício, concessão ou pagador.
- `field_sources`: chave é caminho-folha de `data` (`.` objeto, `[n]` lista,
  sem nome da seção, ex.: `periodos[0].inicio`); senão `field_source_coverage`.
- Simulação: `case_simulation_refused`/`simulation_request_invalid` traz
  `subreason`; reenvie `hypothesis_payload` completo com fontes
  `VersionFieldSource` em `$.payload.<caminho>`. `simulation_process_unsupported`
  não tem caminho.
- `restart_case` em `aberto`/`em_preparacao` sem `preparation`:
  `restart_requires_preparation_for_state` → `get_process_contract` e
  `preparation` (`loki.case-preparation/1`, `request_ref` e um dos modos de
  `get_process_contract.preparation.modes`); efeitos persistidos ainda podem
  exigir conciliação própria. Outros estados:
  `restart_requires_adjustable_state`.
- Férias: `related_vacation_parameters_invalid` traz `related_case_ids` (caso
  irmão do mesmo funcionário) e `related_reason` `incomplete`/`invalid`:
  complete ou corrija; duplicado só se cancela com decisão humana.

Sem caminho servido, pare, guarde a resposta e use
[registrar-problema-loki](../../registrar-problema-loki/SKILL.md), sem dado
pessoal. Não contorne, cancele ou recrie.

## Recusas de gravação, conector, saldo comercial e lote de mapas

Valem somente quando a resposta servida os apresentar; o roteiro completo está
nos domínios `geral`, `rescisao` e `ferias`.

- `case_write_constraints`: cada item de `errors` traz `field` e `reason`
  fechado (ex.: `campo_fora_do_schema`,
  `campo_ja_preenchido_exige_sobrescrever`, `dados_ferias_fora_do_schema`,
  `afastamentos_representacao_invalidos`,
  `vacation_preparation_requires_complete_input`,
  `caso_fora_de_estado_gravavel`). Corrija só o campo indicado; não reenvie o
  modelo inteiro às cegas. `reason` igual a `case_write_constraints` = motivo
  não classificado: registre como problema.
- "Connection closed"/timeout com `/healthz` normal: a falha pode estar antes
  do Loki. Espere alguns minutos, abra conversa nova ou faça Refresh do
  conector e avise pelo Caixa; não repita gravações sem `request_ref`.
- Rescisão em mês comercial (divisor 30, `trinta_fixo`): o Loki calcula os
  dias do saldo; não informe dias nem troque divisor. Fevereiro e dia 31
  calculam; admissão no mês com saída no dia 31 ou no último dia de
  fevereiro, INSS/licença-maternidade no mês da saída e divisor pelo
  calendário continuam `regra_nao_medida` até a DP responder. Cálculo novo
  (`rescisao-v43`/`rescisao-v44`) exige gerar o pacote de novo e nova revisão.
- Férias, segunda ocorrência: outra competência, com `competencia` = mês de
  início do gozo. `created: false` devolve o caso existente: não continue
  nele. Duas frações na mesma competência sem suporte; nunca cancele o
  primeiro caso para abrir o segundo.
- Lote `loki.company-payroll-map-policy-patch/1`: `fgts_mensal` e, quando
  `payroll_map_policy_patch_transport.policies.arredondamento_monetario.accepted`
  aparecer, `arredondamento_monetario` (`verbas`, `metodo`, `fonte`
  obrigatória), com seletores exatos de todos os mapas e `expected_hash`;
  prévia `VALIDO` → aplicar com `motivo`; uma única versão. O método é decisão
  humana/DP. Pode exigir Refresh do conector.

## Recusas de férias e afastamento com campo e código de regra

Valem somente quando a resposta servida os apresentar; o roteiro completo está
nos domínios `ferias` e `afastamento`. Quando o Loki recusar dados de férias
ou de afastamento, olhe a lista `errors`: cada item traz o campo exato (por exemplo
`dados_ferias.data_aviso` ou `leave.retorno`) e um código que diz qual regra não fechou. Corrija só o
campo apontado, conferindo com o documento original, e reenvie com um novo
`request_ref` e o snapshot atual do caso. Reenviar o mesmo dado sem corrigir,
com ou sem `field_sources`, vai ser recusado de novo. Se o documento realmente
traz essas datas, não force o valor: registre a dúvida com a DP antes de
reenviar.

- Férias: `ferias_aquisitivo_29_fevereiro_exige_qualificacao`,
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
  `ferias_medias_alternativas_exclusivas`, `ferias_media_repetida`,
  `ferias_media_competencias_invalidas`.
- Afastamento: `afastamento_inicio_antes_da_admissao`,
  `afastamento_inicio_diverge_do_primeiro_periodo`,
  `afastamento_periodos_descontinuos`, `afastamento_fonte_de_retorno_sem_data`,
  `afastamento_retorno_fora_da_vespera` (retorno = dia seguinte ao fim do
  último período), `afastamento_periodo_invertido`.

## Preparação corrente, população da folha e fontes após reinício

Valem somente quando a resposta servida os apresentar; o roteiro completo está
nos domínios `ferias`, `afastamento`, `geral` e `documentos`.

- Férias e afastamento numa preparação corrente:
  `vacation_preparation_requires_complete_input` e
  `leave_preparation_requires_complete_input` trazem `errors` por campo, por
  exemplo `{"field": "dados_ferias.data_aviso", "reason": "ferias_aviso_fora_do_prazo"}`.
  `reason` é código de regra, `missing` (campo obrigatório ausente) ou
  `extra_forbidden` (chave fora do schema, como `dados_ferias.*`). Corrija o
  campo apontado e reenvie a seção completa com novo `request_ref` e o
  snapshot atual. Fonte vai nos campos `*_source` do schema, nunca numa chave
  própria dentro de `dados_ferias` ou `leave`.
- Prévia da população da folha: `payroll_population_identity_changed` traz
  `next_action: "preview_payroll_population_correction"` e `errors` com
  `{"field": "population[*]", "index": N, "reason": ...}`; `index` é a posição
  do item na lista enviada, contando do zero. Motivos:
  `admissao_posterior_ao_mes`, `entrada_empresa_posterior_ao_mes`,
  `desligamento_anterior_ao_mes`, `matricula_sem_vinculo_operacional`,
  `matricula_ambigua_na_competencia`, `funcionario_id_diverge_da_matricula`,
  `vinculo_fora_da_competencia`. Remova ou corrija esses itens e peça a prévia
  de novo. `{"field": "population"}` sem `index` não aponta item: confira
  matrícula repetida ou vazia antes de repetir.
- Depois de `restart_case`, `get_case` lista de novo `harness_sources` e os
  anexos nativos em `documentos`. Reutilize os mesmos EXTSRC e anexos; não
  registre nem anexe de novo o mesmo original.

## Diagnóstico do job da folha bloqueado no cálculo

Vale somente quando a resposta servida o apresentar; o roteiro completo está no
domínio `geral`.

- `get_case_workflow_job` que termina `blocked` em `calculate` traz
  `diagnostic.errors` com `{"field": ..., "index": N, "reason": ...}`.
  `reason` é código fechado; `index`, quando houver, é a posição do
  funcionário em `dados_folha.funcionarios` do payload enviado, contando do
  zero.
- `field` aponta o lançamento (`dados_folha.funcionarios.N.lancamentos.M`,
  `.valor`, `.quantidade`, `.divisor_quantidade`,
  `.fatos_datados.K.alocacao`) ou o dado do funcionário (`.salario_base`,
  `.periodo_remuneravel`, `.parcelas_salariais`, `.matricula`).
- Índice de lançamento além dos enviados aponta um efeito operacional que o
  próprio Loki acrescentou: corrija o efeito ou o mapa, não o lançamento
  enviado.
- `verba_nao_mapeada` traz `codigo`, a rubrica do layout sem mapeamento: peça
  o mapeamento no mapa da empresa, sem mudar o lançamento.
- `{"field": "dados_folha.valorizacao"}` sem `index` é recusa da competência
  sem item apontável. `operational_pending_employee_out_of_scope` e
  `cadastro_pending_employee_out_of_scope`: contexto de matrícula fora do
  payload, confira a população. `tabela_legal_fora_da_competencia` e
  `fgts_mensal_...`: configuração.
- Grupos principais: bases negativas (`base_inss_negativa`,
  `base_fgts_negativa`, `base_irrf_negativa`); salário-base
  (`salario_base_ausente`, `salario_base_fora_da_competencia`); quantidades e
  fatos (`quantity_fact_required`, `monetary_fact_required`,
  `fato_datado_sem_alocacao`); parcelas e período
  (`salary_installments_period_mismatch`, `salary_periods_require_period_formula`);
  rubricas (`verba_nao_mapeada`, `rubrica_base_sem_valor`,
  `rubrica_dependencia_circular`); adicionais (`insalubridade_...`,
  `periculosidade_...`); vale-transporte (`vale_transporte_...`). O vocabulário completo é o
  conjunto servido no diagnóstico.
- O Loki nunca devolve a matrícula. O diagnóstico só aponta onde está a
  incoerência: não prova que o resto está certo e não autoriza recomeçar o
  caso. Corrija pelo fluxo normal com novo `request_ref` e o
  `expected_snapshot` atual.

## Férias antes do repouso semanal e recibos obsoletos

Valem somente quando a resposta servida e o schema os apresentarem; o roteiro
completo está no domínio `ferias` (e, para médias de rescisão, `rescisao`).

- `ferias_inicio_antes_de_repouso_ou_feriado` não é mais emitido.
  `ferias_inicio_antes_de_repouso` recusa sem a declaração do DP. A véspera
  de feriado tem regra e fonte próprias (veja "Férias antes de feriado:
  decisão do cliente"); a declaração do repouso não libera o feriado.
- Regra da DP da Izzi: aceita o início nos dois dias antes da folga semanal
  quando o cliente pede, porque a Izzi não acompanha a escala praticada.
- A declaração vai no campo opcional
  `dados_ferias.inicio_antes_de_repouso_source`. A fonte é o pedido do
  cliente: documento anexado, manifesto de harness ou declaração
  (`kind: "declaration"`, `reference`, `locator`) com `foundation` dizendo
  quem pediu e onde. Inferência e contexto são recusados
  (`ferias_inicio_antes_de_repouso_source_sem_fundamento`); declaração sem
  início na janela do repouso recusa com
  `ferias_inicio_antes_de_repouso_source_sem_uso`. Sem pedido real do
  cliente, não envie o campo.
- A exceção não muda valores: aparece em `ressalvas.declaracoes_dp` e numa
  linha "Declaração do DP" do aviso e do recibo, e só vale com o aceite
  explícito das ressalvas na revisão.
- Num caso existente, mudar o repouso e acrescentar a declaração é uma única
  correção: `submit_operator_correction` com as duas folhas juntas em
  `changes`. Corrigir só o repouso antes é recusado com
  `ferias_inicio_antes_de_repouso`.
- Depois do deploy, recibos de componentes de férias e de rescisão e
  consolidações de médias emitidos antes ficam obsoletos (`OBSOLETO` em
  `get_case`; `medias_rescisao_obsoletas` no recálculo da rescisão). Não é
  defeito e não pede reinício. Recuperação: nova qualificação, nova
  consolidação, novo cálculo, depois geração, conferência e revisão. Casos
  aprovados ou entregues não mudam.

## Férias antes de feriado: decisão do cliente

Valem somente quando a resposta servida e o schema os apresentarem; o roteiro
completo está no domínio `ferias`.

- Regra da DP da Izzi (16/11/2026): a decisão é sempre do cliente. O DP
  informa o passivo; se o cliente decidir, é feito.
  `ferias_inicio_antes_de_feriado` recusa sem a decisão do cliente: leve a
  data e o passivo ao cliente.
- A decisão vai no campo opcional
  `dados_ferias.inicio_antes_de_feriado_source`. A fonte é a decisão do
  cliente: documento anexado, manifesto de harness ou declaração
  (`kind: "declaration"`, `reference`, `locator`) com `foundation`. O
  conteúdo da `foundation` (quem decidiu, onde e que o passivo foi
  informado) é responsabilidade da harness e da operadora; o Loki só exige
  `foundation` não vazia e não confere a fonte. Inferência e contexto são
  recusados (`ferias_inicio_antes_de_feriado_source_sem_fundamento`); fonte
  sem início na janela do feriado recusa com
  `ferias_inicio_antes_de_feriado_source_sem_uso`. Sem decisão real do
  cliente, não envie o campo.
- Quando o início cai antes de feriado e antes do repouso, as duas fontes são
  exigidas; cada uma libera só a sua regra.
- A exceção não muda valores: aparece como ressalva
  `clt_134_3_vespera_feriado` em `ressalvas.declaracoes_dp`
  (`confirmed: false`, `exige_aceite_humano: true`), dizendo que a decisão foi
  do cliente, que o passivo foi informado e que a ressalva não afasta o
  passivo, e numa linha "Declaração do DP" do aviso e do recibo. Só vale com
  o aceite explícito das ressalvas na revisão.
- Num caso existente, mudar os feriados e acrescentar a decisão é uma única
  correção: `submit_operator_correction` com as folhas juntas em `changes`
  (`dados_ferias.feriados` e `dados_ferias.inicio_antes_de_feriado_source`).
  Corrigir só os feriados antes é recusado com
  `ferias_inicio_antes_de_feriado`.
- Depois do deploy, recibos de componentes de férias e de rescisão e
  consolidações de médias ficam obsoletos de novo, inclusive os emitidos
  depois da 2.6.11, com o mesmo caminho de recuperação. A descrição da
  ressalva do repouso mudou: revisões já preparadas com ela precisam ser
  preparadas de novo. Casos aprovados ou entregues não mudam.

## Reajuste coletivo com efeito retroativo

Valem somente quando `get_process_contract("reajuste_salarial")` servir
`loki.salary-adjustment/1`; o roteiro completo está em
[REAJUSTE_SALARIAL.md](REAJUSTE_SALARIAL.md) e no domínio `reajuste_salarial`.

- `create_case` (`case_type=reajuste_salarial`, `competencia` no dia 1 de X,
  `occurrence_ref` igual à referência do instrumento, sem funcionário) →
  `get_process_contract` → `receive_case_data` com o `instrumento` e as
  `linhas` em blocos de até 100 matrículas → `validate_case` → prévia
  `loki.salary-adjustment-preview/1` (paginada por `proximo_inicio`, com
  `resumo_total`) → conferência da operadora → `apply_case_effects` no caso
  coletivo com a decisão humana explícita → retomada pelo mesmo
  `request_ref` até `APPLIED` ou `PARTIAL`.
- `BLOCKED` antes da decisão: nenhum efeito gravado; corrija as linhas e
  refaça a prévia. `VALIDATING` e `IN_PROGRESS`: repita o mesmo pedido.
- `PARTIAL` mostra o estado real (`aplicadas`, `pendentes`,
  `effects_written`); nunca diga "nada foi gravado" se já houve efeito.
  Linha com falha registrada sai pela reabertura
  (`loki.salary-adjustment-reopen/1`) ou pela exclusão
  (`loki.salary-adjustment-exclusion/1`); linha já aplicada sai pela
  retirada no caso filho (`withdraw:true`).
- Na folha X: `reajuste_coletivo_em_execucao` enquanto o lote não fecha,
  pendências `diferenca_*` por matrícula e a ressalva
  `diferenca_rescisao_complementar_pendente`, decidida pela DP no aceite das
  ressalvas. Nunca zere uma pendência nem informe a diferença à mão.

## Fila da folha: um job pendente por empresa

Vale somente quando o contrato anunciar
`durable_workflow.admission: "one_pending_job_per_company"`; o roteiro completo
está no domínio `folha_mensal`.

- Outro caso da mesma empresa com job `queued` ou `running`:
  `enqueue_case_workflow` devolve `BLOCKED` `company_job_pending` (HTTP 409),
  nada gravado, com `pending_job: {case_id, job_id, request_ref}` e
  `retry: "after_pending_job_terminal"`. Cada identificador só vem quando a
  conta consegue usá-lo.
- Com `job_id` (`next_action: "get_case_workflow_job"`): consulte o job até
  `completed`, `blocked` ou `failed`. Sem ele (`next_action:
  "retry_enqueue_later"`, `retry_after_seconds: 60`): repita o mesmo enqueue,
  com a mesma referência, a cada `retry_after_seconds`; não troque de
  `request_ref` por causa de `job_not_found`.
- O job pendente pode reter a empresa por até cerca de 60 minutos se o worker
  cair; depois disso, avise a engenharia pelo Caixa em vez de insistir.
- Enfileire em série na mesma empresa. Folhas de empresas diferentes rodam
  ao mesmo tempo no worker, no máximo uma por empresa: enfileire uma de cada
  empresa sem esperar as outras. Consultas Dataprev mensais esperam a fila de
  folha esvaziar; acompanhe pelo recibo, sem reenviar. Releia `get_case` do
  caso recusado antes de repetir.
- Durante o job, não grave em outro caso da empresa nem no cadastro dela
  (`receive_case_data`, `update_case_payload`, `complement_payroll_items`,
  anexos): o job termina `BLOCKED` `job_sources_changed`. Leituras e gravações
  em casos de outras empresas são seguras.
- 524 ou timeout: consulte `get_case_workflow_job` com o mesmo `request_ref`;
  com `job_not_found`, repita o enqueue com o mesmo `request_ref` e o mesmo
  corpo. `BUSY`/429: respeite `retry_after_seconds` ou `Retry-After`.
  `company_job_pending` não é `BUSY`.

## Diagnóstico da folha no dossiê

Vale somente quando a resposta servida o apresentar; o roteiro completo está no
domínio `folha_mensal`.

- O diagnóstico está em `get_case_dossier`, `calculations[].diagnostics`. Um
  `CALCF-` em `get_case_calculation` recusa com `calculation_kind_unsupported`
  e `next_action: "get_case_dossier"`, sem dizer se o cálculo existe.
- Na issue `contexto_operacional_pendente`, `leave_qualification_incomplete` é
  a causa primária: `next_action: "qualificar_afastamento_na_origem"` vem
  sempre primeiro. `dependent_fields` não se trata agora (nem com
  `history_qualifications.payroll_context`); as causas próprias em
  `missing_fields` seguem `next_action_after_primary` depois de qualificar e
  recalcular. `missing_fields_complete: false`: há causa não reconhecida;
  trate depois, sem inferir.
- `leave_qualification.origins[*]` diz onde completar `leave.categoria`,
  `leave.policy_version` e `leave.periodos[N].responsabilidade`:
  `company_onboarding` (declaração `historico_operacional` do fato, com
  `category_code`, `policy_version` e `payment_periods`; valide, aplique e fixe
  de novo o histórico) ou `operational_effect` (nova preparação do caso de
  afastamento). `leave_qualification_not_recognized`: nada foi separado;
  registre o problema. Não infira categoria nem pagador.
- Um `EXTSRC` de outro caso não serve como fonte da folha.
- `salario_base_ausente`: siga `next_action`; `code_next_action:
  "qualify_payroll_salary"` é a alternativa do código.
- Restart com `replace_payroll_population`: o recibo traz `population_count` e
  `population_hash`; compare com o `population_hash` da prévia.
- `payroll_population_dependencies_busy` (`retryable: true`, `dependency`):
  nada gravado; releia `get_case` e repita o mesmo `request_ref` depois.
- Em `get_company_employee_history` com `process_type=folha_mensal`, rescisão
  declarada no onboarding vem em `unqualified_facts` (`kind: "rescisao"`,
  `effective_on`, `constraint_hash`). A ausência não prova vínculo ativo; com
  `desligamento_anterior_ao_mes`, leve a restrição à operadora.

## 13º por etapas: competência, envio por partes e 2ª parcela

Vale somente quando a resposta servida e o contrato o apresentarem; o roteiro
completo está no domínio `decimo_terceiro`.

- `create_case` exige `competencia` no dia 1 do mês do pagamento da parcela
  (`thirteenth_competence_required`). Competência diferente do mês de
  `data_pagamento` recusa com `thirteenth_competence_mismatch` e
  `next_action=cancel_case`: cancele o caso e só depois recrie. Sem
  `occurrence_ref` no 13º operacional.
- A segunda aceita dezembro com `variavel_cents: null` (média ÷ 11); o ajuste
  exige dezembro. A 1ª parcela dispensa dependentes de IRRF, salvo pensão
  `interdependente`.
- A seção pode ir por partes: regra que depende de `historical_payments`,
  `numero_ajuste`, `afastamento_source` ou `medias_importadas` ainda não
  enviados só é cobrada no cálculo. O recibo avisa em `pending_rules`; é só
  aviso e não volta no replay.
- 2ª parcela e ajuste: `casos_anteriores=[]` (sem
  `thirteenth_prior_cases_require_shadow`); envie a seção, leia os ids
  `ONBFACT-…` dos fatos `thirteenth_payment` em `get_case_historical_state` do
  próprio caso, envie `historical_payments`, aplique o estado e calcule.
- `medias_importadas` (média final do Domínio) exclui `variavel_cents` mensal.
- Recusas: no cálculo, `thirteenth_parameters_invalid` com `fields`, `errors` e
  `months`; no receive, `invalid_case_data` com `{field, reason, mes}`.
  `thirteenth_stage_duplicated` e `thirteenth_peer_section_invalid` trazem
  `related_case_ids`: veja o outro caso e cancele o rascunho que sobrou.

## Matrícula no `create_case`

Vale somente quando a resposta servida o apresentar; o roteiro completo está no
domínio `geral`.

- Caminho padrão: omitir `funcionario.matricula` (identidade é CPF + data de
  admissão). Nunca copie para o caso o valor lido no Loki;
  `identifiers.matricula` de `get_company_employee_history` serve para conferir
  o documento.
- `matricula_funcionario_divergente` ou `matricula_funcionario_nao_qualificada`
  (`campos: ["funcionario.matricula"]`): nada foi gravado. Reenvie omitindo a
  matrícula; se o documento divergir da registrada, avise a operadora. A
  correção combinada com ela segue a restauração ou a troca auditada do código
  Domínio (“Cadastro: matrícula, código Domínio e desligamento do onboarding”);
  sem caminho automático, use `registrar_problema`.
- Caso existente volta com `created: false`, sem comparar matrícula. Matrícula
  vazia ou só com espaços é recusada.

## Recusas de fatos históricos e cobertura até o corte

Vale somente quando a resposta servida o apresentar; a tabela completa está no
domínio `ferias`.

- `declaracao_do_vinculo_invalida`: `diagnostic.details[*]` traz `path` e
  `type` com o código da regra (`historical_vacation_period_inverted`,
  `historical_vacation_use_inverted`,
  `historical_vacation_use_period_incompatible`,
  `historical_vacation_use_days_incompatible`,
  `historical_leave_return_incompatible`,
  `historical_leave_payment_outside_leave`, `historical_leave_payment_overlap`,
  `historical_leave_payment_inverted`, `historical_coverage_inverted`).
  Corrija conforme a fonte. Gozo em que o fim do aquisitivo cai dentro do
  período é aceito (regra da DP de 18/11/2026); gozo que termina antes do fim
  do aquisitivo continua recusado: pergunte à Rafa.
- Lote validado antes da atualização pode recusar `snapshot_desatualizado`:
  valide de novo e aplique com o `validation_hash` novo, sem mudar os dados.
- `leave_history_coverage_not_certified` e
  `thirteenth_payment_coverage_not_certified`: a cobertura completa desde a
  admissão limpa o gap até o corte, termine ela no corte, antes (emendada) ou
  depois dele (estado `historical-state-v2`). Seleção v1 consumível não se
  refaz. Não altere coberturas de casos com seleção histórica feita.
- Afastamento antigo opaco: não grave `leave` duplicado; mantenha o gap
  pendente.

## Onda 2: folha, 13º, rescisão, reajuste e cadastro

Vale somente quando a resposta servida e o contrato o apresentarem; o roteiro
completo está em cada domínio de `loki_obter_instrucoes`.

**Não exige nada da operadora:**

- Folha (`folha_mensal`): empresas diferentes em paralelo, uma por empresa.
  Contexto do mês por pessoa no dossiê: `payroll_context` com `context_hash`
  (use só com `context_current=true`) e `lancamentos.items` com
  `lancamento_hash` copiados para `history_qualifications.payroll_context`;
  `payroll_effective_launch_codes_repeated` é problema a relatar.
- Janela de publicação: na que publica esta versão a fila de folha ainda
  precisa estar vazia; nas seguintes, job nunca iniciado é retomado no build
  novo (`case_job_build_repinned`). Depois da janela, `job_build_changed`,
  `job_snapshot_changed`, `job_sources_changed` ou
  `job_fingerprint_snapshot_changed` pedem reenfileirar com `request_ref` novo.
- 13º (`decimo_terceiro`): `final_average` é a média mensal integral do
  Domínio, nunca proporcional aos avos (o Loki aplica `média × avos ÷ 12`).
  Caso em `aguardando_revisao` com média importada: decisão `ajustar`, depois
  `calculate_case`, geração e nova conferência. Reinício com `restart_case` e
  `replace_process_inputs`, sem `corrigir_dados`.
  `historical_thirteenth_coverage_incomplete` traz `missing_intervals`.
- Rescisão (`rescisao`): `loki.company-termination-map-patch/1` com `add` ou
  `replace` de uma parcela, quando `get_client_config` trouxer
  `termination_map_patch_transport`.
- Reajuste (`reajuste_salarial`): desligados ficam fora por padrão
  (`excluidas_automaticamente`); admitido depois da data-base depende de
  `salario_base_anterior_cents`; `proporcional_admissao` recusa
  (`reajuste_proporcional_nao_praticado`); salário novo já registrado vira
  ressalva `salario_novo_ja_registrado_no_cadastro`.

**Exige Refresh do conector e conversa nova (`alteracao_cadastral`):**

- Restauração de matrícula: worker `identifier_only` com
  `expected_current_matricula` e `restoration_declaration`
  (`human_message` mais `message_reference` ou `reason`), só depois de
  combinar com a operadora.
- Troca de código Domínio: o mesmo worker com o extrato do código novo e
  `restoration_declaration` com `motivo: "troca_de_codigo_dominio"`; a
  `message_reference` `CX-…` é obrigatória
  (`troca_de_codigo_dominio_exige_message_reference_cx`).
- Revogação de desligamento do onboarding:
  `preview_onboarding_termination_revocation` e
  `revoke_onboarding_termination` (ou, antes do Refresh,
  `receive_case_data(case_id="@connector")`), com
  `revoga_com_rescisao_aberta` igual a `true` quando houver
  `open_termination_cases`.

## Cadastro: matrícula, código Domínio e desligamento do onboarding

Os roteiros completos (passos, provas e recusas) estão no domínio
`alteracao_cadastral`. Depois de qualquer um deles, folhas abertas com o
código antigo ficam `vinculo_nao_identificado_na_competencia` até reenviar a
população, e as seleções históricas do vínculo precisam ser refeitas.

## 2.9.0: reajuste, rescisão, simulação e admissão

Vale somente quando a resposta servida e o contrato o apresentarem; o roteiro
completo está em cada domínio de `loki_obter_instrucoes`. **Não exige Refresh
do conector**: as 96 ferramentas são as mesmas. A única ação da operadora é
atualizar o plugin instalado.

- Reajuste (`reajuste_salarial`): `folha_do_lancamento_em_revisao_ou_fechada`
  traz `folha_bloqueante` (`competencia`, `estado`). Vale para a folha do
  Loki em X ou em qualquer competência posterior; o histórico importado não
  conta. Diga qual folha é; as saídas são devolver a folha para ajuste ou
  lançar na primeira competência depois da última folha do Loki em revisão
  ou fechada, com a DP confirmando o mês (caso coletivo novo nessa
  competência). `cliente_config_incompleta` fecha no apply, depois da
  decisão; `processo_nao_habilitado_no_cliente` não barra o apply, mas o
  certo é habilitar o processo com a DP.
- Rescisão (`rescisao`): método do Domínio opt-in em
  `arredondamento_proporcionais` (`metodo_ferias: valor_dia_6_casas`,
  `terco: por_parcela`, `saldo: valor_dia_6_casas`, `medias_por_bloco`), só
  com medição citada em `fonte`; `saldo` exige `trinta_fixo`
  (`rescisao_saldo_valor_dia_exige_trinta_fixo`); cálculo com opção traz
  `+metodo-dominio-v1`. Médias com `horas_micros`, `valor_micros`,
  `vantagens_micros` (coerentes com os centavos) e `bloco` por empresa do
  grupo. O 13º não usa micros nem blocos.
- Simulação de rescisão: antes, compare o `state_hash` de
  `get_case_historical_state` com o da seleção (ou leia
  `selection_matches_current_state`); seleção desatualizada não tem caminho
  sem reiniciar o caso real. Copie as chaves de topo da origem, inclusive as
  nulas; `locator` `$.payload.<caminho>` na declaração; `foundation` com
  `derived`/`reported` ou `harness`; `operational_context_changed` traz
  `subreason` (`version_refusal_subreasons` no contrato).
- Admissão (`admissao`): a data de admissão é identidade e não se troca.
  Cancele o caso com a mensagem do cliente em `human_message` e abra outro;
  antes, confira se o episódio antigo recebeu matrícula e, se recebeu,
  registre o problema.

## 2.9.1: regras da DP de 18/11/2026

Vale somente quando a resposta servida e o contrato o apresentarem; o roteiro
completo está em cada domínio de `loki_obter_instrucoes`. **Não exige Refresh
do conector**: as 96 ferramentas são as mesmas. A única ação da operadora é
atualizar o plugin instalado.

- Reajuste (`reajuste_salarial`): admitido no próprio dia da data-base com o
  salário novo vai com `salario_anterior_esperado_cents` igual ao salário de
  admissão e sem `salario_novo_cents`; o Loki devolve `sem_reajuste`
  (`admitido_na_data_base_com_salario_novo`, `rule.admitted_on_base_date`),
  sem divergência, e o piso novo prevalece. Admitido no mesmo mês, antes do
  dia da data-base: não envie a linha; pergunte à Rafa. O VT não entra na
  diferença nem no pago declarado (`declared_origins.transport_discount`):
  não declare VT nas verbas, e ele não impede
  `sem_outras_verbas_dependentes_do_salario`. Salário novo já registrado com
  vigência na data-base é o próprio reajuste: envie a linha normalmente.
- Férias antigas no onboarding (`ferias`): gozo em que o fim do aquisitivo cai
  dentro do período, do primeiro ao último dia, passa a ser aceito. Lote
  recusado antes com `historical_vacation_use_period_incompatible` pode vir
  `ready` na próxima validação: valide de novo e aplique com o
  `validation_hash` novo; o hash antigo dá `snapshot_desatualizado`.
- Afastamento (`afastamento`): um registro por atestado, com `retorno` no dia
  seguinte ao fim; atestados encostados não são sobreposição.
  Licença-maternidade (`categoria: licenca_maternidade`) não é falta e não
  reduz o aquisitivo.
- Médias (`rescisao`, `decimo_terceiro`): o Domínio soma as médias das
  empresas do grupo, sem separar por empresa, em férias e no 13º. Não ligue
  `medias_por_bloco` sem conferência com a DP.
- Matrícula (`geral`, `alteracao_cadastral`): a matrícula do eSocial é o
  identificador oficial. Enquanto a forma de uso não for confirmada, não grave
  matrícula nova por `identifier_only` sem falar com a engenharia.

## Ler recursos binários retornados pelo MCP

`get_case_document(case_id, doc_id)` pode retornar os bytes no bloco
`content[type=resource].resource.blob` (base64), além dos metadados em
`structuredContent`. Preserve a resposta MCP completa em JSON privado; metadata
isolada não é download e uma URL não substitui o recurso embutido. Confira caso,
documento, URI exata `loki://cases/CASE-ID/documents/DOC-ID`, SHA256 e tamanho
contra o pacote/versão ou dossiê esperado, antes da leitura.

Pelo entrypoint local, execute offline:

```text
mcp-resource resposta-mcp.json SAIDA_PRIVADA_NOVA --expected-uri loki://cases/CASE-ID/documents/DOC-ID --expected-sha256 SHA256 --expected-size TAMANHO_EM_BYTES
read SAIDA_PRIVADA_NOVA/document.pdf LEITURA_PRIVADA_NOVA --expected-sha256 SHA256
```

O helper exige expectativas explícitas, decodifica base64 estrito, confere hash,
tamanho e metadados de caso/documento/MIME quando presentes e salva nome local
fixo e manifesto0700/0600 (ACL restrita no Windows). Não deriva caminhos do nome
remoto, não busca URLs, não usa rede/SDK/OAuth e não sobrescreve destino existente.
Erro, bytes ausentes, URI divergente e seleção ambígua não produzem artefato
válido; falha de gravação remove a saída nova. O limite de bytes é32MiB, com
respostaJSON de até64MiB. Outros MIME usam a extensão registrada no manifesto;
formato desconhecido conserva `.bin` e pendência de interpretação.

`saved_not_reviewed` comprova apenas bytes locais verificados. Depois use `read`
e inspecione todas as páginas/imagens efetivas pela harness. Com pacote
existente, obtenha `get_package_check_request` para a mesma `version_id` quando
houver; confira os recursos e somente então envie `record_package_checks` com
os mesmos hashes e `required_checks` efetivamente examinados. Não marque PASS
por disponibilidade/download, não copie checks antigos e preserve FAIL/pendência.
Sem pacote/documento previsto, releia o recibo factual; não invente PDF ou check
visual. Conferência técnica não é decisão humana, entrega ou pagamento.
