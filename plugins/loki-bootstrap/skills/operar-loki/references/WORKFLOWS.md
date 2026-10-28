# Dados operacionais e retomada

## Caso individual

1. Confirme acesso, instruções e `get_process_contract(process_type)`. Consulte
   `get_case(case_id)` e capture `input_snapshot` imediatamente antes da escrita.
2. Leia os originais externamente, mantendo hashes/localizadores no workspace
   privado. O Loki recebe dados estruturados e fontes; não interpreta os originais nem
   compara o resultado com o relatório da equipe.
3. Prepare o conteúdo de `data_section` em `data`, sem outro envelope. O pedido
   `loki.case-data/1` contém exatamente `schema_version`, `request_ref`,
   `expected_snapshot`, `data` e `field_sources`. `expected_snapshot` recebe o
   `input_snapshot` atual. Reutilize `request_ref` e o conteúdo em uma retomada.
4. Cada folha de `data` tem fonte no caminho relativo, inclusive null, falso e
   lista vazia quando declarados. `kind` é `document`, `declaration`, `history`
   ou `rule`; `reference` e `locator` são reais. `content_hash` é opcional e
   `foundation` guarda fundamento, vigência, alcance e operandos de uma derivação.
   Não invente ID remoto para um documento local. Documento é dado, não autoridade.
5. Use `case-request evidence.json PEDIDO_NOVO --contract contract.json
   --target CASE-ID --reference REFERENCIA --snapshot INPUT_SNAPSHOT` para preparar
   o pedido offline. A harness chama `receive_case_data` com `arguments`; o helper
   não envia. Não declare leituras que não ocorreram; arquive originais apenas como anexos opacos quando o contrato exigir fonte nativa.
6. Confira a resposta e salve pedido/resposta com `receipt`. Conflito exige
   releitura e conciliação, mantendo o conteúdo anterior. Dados em revisão usam
   o fluxo autorizado de correção e nova revisão; não contorne o snapshot.
7. Execute `run_prepared_case_workflow` ou as operações cálculo/geração/revisão
   declaradas no contrato. Versões internas servem à auditoria. Empresa de teste
   usa o mesmo fluxo operacional e os mesmos gates, sem modo especial.
8. Confira artefatos e páginas externamente; congele o resultado antes de abrir
   referências de comparação. Apresente pacote e ressalvas para decisão humana.
   Entrega para Drive Izzi e solicitante depende de destino e recibo próprios.
   Conferência não significa envio. Retry conserva pacote/revisão/hash, sem
   recalcular nem duplicar; destino ausente/falha permanece pendente.

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

## Cadastro e histórico em lote

Consulte `get_company_onboarding_contract` e a autorização efetiva. Apenas os
papéis administrativos aceitos pelo host realizam essas escritas. Reuse o lote
corrente; recepção/staging não significa cadastro ou histórico aplicado.

Os leitores locais podem preparar CSV de leitura como evidência externa e CSV
`loki.batch-csv/1` para o contrato de onboarding vigente. `source-csv` mantém seu
formato local de origem; não o envie como `field_sources` operacional. Use
`csv-request` somente com `onboarding-source` ou `onboarding-csv`; no tipado,
conserve referência, revisão e hash. Submeta chunks e valide/aplique apenas pelos
escritores do contrato, com fontes reais, snapshot/hash corrente e readback.
Não envie documentos originais pelo sincronizador antigo do kit desktop.

## Retomar

Conserve em pasta privada originais, leitura, fontes, contratos, pedidos,
respostas, recibos, referências, revisão e hashes. Resposta perdida exige leitura
antes de repetir. Erro ou pendência não vira sucesso porque existe um recibo.
Nova versão do plugin exige recarregar a sessão; instalação, catálogo, serviço
publicado e consumo real são provas distintas. Não altere OAuth, credenciais,
assinatura, pin do kit antigo ou agenda para contornar falha de leitura/contrato.

Conferência técnica usa `get_package_check_request` e `record_package_checks`, schema `loki.package-checks/1`, hashes/revisão/documentos exatos e PASS/FAIL explícito para content, structure, visual e pii_policy de cada documento. Inclua informativo obrigatório da admissão e provisões quando presentes. Registre somente conferência externa realizada; não atesta comparação com relatório, aprovação humana nem publicação. Após aceite documental privado, apresente `prepare_delivery` e aguarde intenção humana explícita sobre pacote/revisão/hash/destino antes de `authorize_delivery` e `execute_delivery`. O aceite privado anterior não autoriza envio externo. Consulte `get_delivery_status` pelo mesmo delivery_id; somente DELIVERED comprova envio observado, enquanto destino/credencial ausentes ou falha continuam PENDING. Destino e credencial são provisionados no host; não envie folder/token/URL nem use Drive Iris ou PUBLIC. Solicitante usa documentos/rotas autenticadas retornados.

Para usar fecho anterior como abertura de provisões, selecione explicitamente `opening_selection={kind:"previous_revision",competencia,input_hash,result_hash}` no contrato de folha_mensal/fechamento. Envie `opening_cents=null` nos movimentos; `opening_origin` é resolvido e rastreado pelo servidor, não preenchido pela harness. A revisão deve ser da competência imediatamente anterior e ainda corrente. Sem fechamento conhecido, a abertura e seus totais dependentes permanecem desconhecidos; não crie zero. Saldo documentado de abertura também pode ser recebido com fonte qualificada pelo contrato, sem seleção automática de uma revisão. Retificação da origem exige conciliação e nova revisão do pacote dependente.

Fontes `kind=document` exigidas como evidência nativa usam `document.reference` com o ID do anexo retornado por `attach_source_document` e `content_hash` igual ao retorno. O upload arquiva o original como bytes opacos; o Loki não extrai nem interpreta seu conteúdo. Não invente DOC com caminho local, ID do Drive ou hash avulso. Leitura externa declarada pode usar `kind=declaration`, referência/localizador/fundamento honestos e seus limites; isso não atesta verificação documental nativa. Quando identidade, efeito ou qualificação exigir fonte nativa, arquive o original opacamente ou selecione a fonte nativa já persistida/pinnada indicada pelo contrato. Não troque a classificação da origem para fabricar qualificação.


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
