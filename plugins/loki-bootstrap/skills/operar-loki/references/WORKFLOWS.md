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

CSV operacional é entrada tipada de parâmetros preparados pela harness. Consulte
`get_operational_batch_contract()` e seus escritores antes de preparar o envio. Preserve
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
