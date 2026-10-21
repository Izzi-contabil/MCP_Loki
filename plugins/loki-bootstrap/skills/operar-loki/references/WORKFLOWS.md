# Contratos e retomada pela conexão existente

## Evidência local e CSV de leitura

A harness prepara evidence.json a partir do que realmente leu. Exemplo
estrutural sintético (substituir hash e localizadores pelos observados):

```json
{
  "data": {"dados_rescisao": {"valor_cents": 0}},
  "field_sources": {
    "dados_rescisao.valor_cents": {
      "source_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "locator": "page:1/linha:4",
      "basis": "documented"
    }
  },
  "missing_fields": ["dados_rescisao.outro_campo"],
  "ambiguous_fields": []
}
```

O exemplo não é schema de rescisão; use os campos reais do contrato vigente.
Cada folha de data exige origem exata, incluindo null/false/lista vazia quando
declarados. Ausente não vira zero. `derived` exige fundamento da derivação;
`reported` identifica informação reportada. Não atribuir automaticamente o mesmo
basis a toda leitura: essa classificação afeta autoridade/reuso no backend.

`source-csv` gera `loki.harness-reading/1`, com campo, estado, valor JSON,
hash/localizador do original local e fundamento. O CSV é uma **declaração da
harness**. Seu hash final é outro hash. Preserve os dois no workspace privado.
Para referenciar um campo remoto, abra o CSV com csv.DictReader(delimiter=';')
e use a linha real (`reader.line_num`) junto ao field_path; não estime a linha
pelo nome/ordem de um objeto. Não copie um campo original para chave extra de um
envelope MCP strict. Armazene complementos no CSV/local-provenance autorizado.

## Caso individual: somente CSV enviado

1. Consulte get_case, get_document_processing_contract(process_type) e
   get_document_processing_status(case_id), além do acesso/instruções atuais.
   Obtenha schema da seção correta e envelope de data correspondente.
2. Leia e confira originais localmente; gere reading.csv. Confirme hash do original
   novamente com `hash ARQUIVO --expected-sha256 HASH` antes de concluir a leitura.
3. Prepare csv-request destino case. Invoque anexar_documento_conteudo (ou a tool
   equivalente attach_source_document presente no catálogo) com os argumentos
   calculados: case_id, filename.csv, content_base64 e doc_role="outro".
   O helper não escolhe um papel que feche avisos documentais de outro tipo.
4. Salve resposta integral e confirme ID/hash do CSV. Reconsulte o estado: anexar
   fonte altera o snapshot. Se o caso for legado, a migração local é explícita,
   conforme contrato, com expected_snapshot corrente; não migre automaticamente
   para forçar compatibilidade de caso fora de preparação.
5. Monte submit_document_extraction(declaration) usando o snapshot novo,
   documents=[{document_id: ID_CSV, content_hash: HASH_CSV, role: CLIENT_INPUT}],
   execution verdadeiro da harness e origem por cada folha de data. Use o envelope
   correto (dados_admissao/dados_rescisao/dados_folha etc. do contrato), sem prefixo
   data. nos paths. Os localizadores remotos apontam ao CSV. Não invente ID do PDF.
   Referência oficial exige trilha e papel próprios do contrato, separados dos
   insumos; um CSV de insumos não vira fonte oficial reutilizada silenciosamente.
6. Obtenha get_document_verification_request(case_id, extraction_id=...); confira
   os bytes exatos do CSV e registre somente source_checks observados por ID.
   Isso confere CSV, não atesta que o servidor leu o PDF nem que houve duas leituras
   independentes. Se faltar evidência exigida, preserve a pendência.
7. Após validação, aplique pelo escritor existente apply_document_extraction com
   overwrite=False; reconsulte estado e siga next_actions. Correção/sobrescrita
   conserva a autorização, contrato, revisão e trilha próprios.
8. Execute o workflow autorizado, obtenha artefatos/recibos pelo MCP e grave bytes
   localmente conferindo hashes. Releia/renderize PDFs gerados com os leitores e
   a visão da harness, envie conferência observada, prepare revisão e apresente
   resultado ao operador. Nenhum helper local registra aceite humano.

## Onboarding: staging, parâmetros e aplicação separados

O conector OAuth restringe as ferramentas de onboarding a administradores
autorizados (owner/master no backend atual). Consulte capacidade/role real; ver
get_company_onboarding_contract público não prova que uma escrita será permitida.
Não altere contas nem use outra identidade para contornar recusa.

1. Consulte get_company_onboarding_contract, crie/reuse o lote no escopo autorizado.
2. Use source-csv e destino onboarding-source para CSV de leitura simples; ou
   render-csv com records e contrato batch_csv e destino onboarding-csv. O formato
   tipado é `loki.batch-csv/1`; pode começar por kind="reading", cujo declaration
   contém os fatos lidos e sua proveniência local. Isso evita referência circular
   a um CSV que ainda não tem hash/ID remoto.
3. Envie pela tool que o request indicar e salve o recibo. No tipado, percorra
   todas as páginas de get_company_onboarding_csv_status, preservando referência,
   revisão e hash. Staging não submete/aplica chunks ou executa registros task.
4. Construa submit_company_onboarding_chunk por parâmetros a partir da leitura,
   com SourceRef apontando ao ID/hash do CSV real no mesmo lote e à linha/célula
   que documenta o fato. Não reutilize aliases local: como IDs remotos. Originais
   continuam locais e não receberam prova independente do servidor.
5. Complete fragmentos e revisões, consulte validate_company_onboarding e
   aplique somente com validation_hash corrente pelos escritores autorizados.
   Confira get_company_onboarding_status/readback. Preserve lacunas e conflitos.
   Histórico, cálculo e primeira folha mantêm a qualificação/seleção próprias.

Não executar batch_sync/sync do kit antigo: esse fluxo arquiva todos os PDFs
antes do CSV e contraria o canal de envio solicitado para este plugin.

## Retomada e versão

No workspace privado mantenha originais, inventário/leitura, evidence/records,
contratos consultados, parâmetros, pedido exato, resposta integral, recibo e
ID/hash/revisão remotos. Retome esses arquivos, confirme acesso e estado atual;
não reconstrua de memória uma declaração antiga. Se resposta for BLOCKED/erro,
registrar o recibo não a transforma em sucesso. Resposta perdida exige consulta
antes de nova escrita; nova revisão só quando conteúdo mudou de fato.

Atualização nativa troca código/lock/skills. Reabra a sessão para carregar a versão
nova e rode doctor em outra pasta. Continue o workspace anterior com contratos
atuais; se formato ou snapshot mudou, preserve o antigo e prepare nova revisão.
Não remova OAuth/MCP para corrigir problema de Git ou leitor. Não copie cofre
Windows para Mac/Linux. Não toque em assinatura/pins do kit legado.
