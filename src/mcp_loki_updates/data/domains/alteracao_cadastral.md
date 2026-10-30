# Alteração cadastral

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Quando o contrato atual oferecer o processo, prepare o conteúdo de `dados_alteracao_cadastral` e envie por `receive_case_data`. A proposta compara valores anteriores do perfil datado com valores novos fonteados, vigência e contexto capturado. Não declare anteriores apenas por relato nem substitua o hash esperado para contornar conflito de perfil.

O pacote factual contém recibo e artefatos JSON, sem PDF; `supports_apply=false` indica ausência de aplicação ao cadastro operacional. O recebimento dos dados prepara o caso; aplicação ao perfil exige a ação específica autorizada no contrato. Confira contexto, diferenças, fontes, hashes e pendências pelos checks do contrato e mecanismos de verificação/revisão da versão. Perfil alterado exige nova captura/versionamento.

Revisão e aprovação documental não aplicam salário, cargo, jornada ou outros dados ao cadastro. Qualquer efeito operacional exige fluxo e intenção humana específicos que o host efetivamente suporte. Preserve a proposta parcial se faltar fato, vigência ou fonte.

Para empresa e estabelecimentos, parâmetros e regras e demais dados vinculados, descubra os contratos e escritores HTTPS vigentes. Confira o CNPJ e o escopo da identidade autenticada, a revisão esperada, vigência, fontes, diferenças e histórico. Não use o caso de alteração do empregado como substituto de um contrato empresarial ausente nem atualize outra empresa do mesmo grupo. Preserve intenção/revisão exigidas, envie apenas parâmetros estruturados e obtenha recibo persistido; depois releia o objeto empresarial para conferir revisão e valores aplicados. Staging, proposta e recibo de recebimento não comprovam ajuste aplicado. Endpoint ou campo ausente é lacuna contratual explícita.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

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
`valid_until`, com intervalo fechado sem sobreposição; `cnae_preponderante`,
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
