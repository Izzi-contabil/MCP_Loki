# Dataprev mensal na folha

Este roteiro orienta a consulta de consignações de uma competência e sua
aplicação posterior à folha autorizada. Distribuir este guia ou preparar um
wheel não comprova publicação do backend, instalação no operador, acesso
ativado, homologação real ou consulta de dados reais.

## Descobrir e conferir o acesso

Consulte `get_process_contract("folha_mensal")`. Prossiga somente quando
`dataprev_monthly.schema_version` anunciar `loki.dataprev-monthly/1`, com
`tool=receive_case_data`, e `compatibility_transport` anunciar a mesma rota e
`dataprev_monthly.request_schema`. Use o schema servido. Um contrato ausente
mantém a consulta automática indisponível; não invente ferramenta ou transporte.
A importação estruturada por JSON ou CSV tipado continua pelo escritor mensal
existente, conforme seu contrato, sem representar consulta automática realizada.

A leitura exige `consultar`; reserva e aplicação exigem `operar_casos` no caso
autorizado. A consulta e sua referência pertencem ao próprio ator e caso;
automação usa identidade técnica própria e concessão vigente. O backend exige
worker escopado, população corrente e perfil empresarial de produção vigente.
Empresa, competência, vínculo, episódio e seleção de contratos vêm do cadastro
e do caso correntes. Não selecione por CPF isolado, CNPJ raiz, nome parecido ou
papel declarado livremente no request. Matrícula reutilizada exige o episódio
qualificado, incluindo admissão quando o contrato o requerer.

A [orientação pública da Dataprev](https://docs.dataprev.gov.br/docs/credito-trabalhador/orientacao-para-empregadores/obtencao-de-dados-de-consignacoes-via-api/)
descreve certificado do empregador ou de representante com procuração válida,
sem cadastro ou subscrição específicos. O transporte empresarial usa mTLS e
provisionamento externo de perfil, certificado, representação e concessões.
A harness não pede, lê ou envia chave privada, certificado, token ou caminho de
segredo. Não use credenciais de instituição financeira. Sem perfil ou concessão
válidos, informe a indisponibilidade e a dependência de provisionamento externo;
não declare acesso ativado por existir um guia, schema ou teste sintético.

## Reservar, consultar e aplicar

Use `receive_case_data(case_id, request)` na conexão HTTPS existente. O envelope
mensal é enviado diretamente em `request`, sem embrulhá-lo no `data` do intake
comum. O `case_id` é o caso autorizado, fora do envelope mensal. Copie
`employee_id` do cadastro do vínculo correto e `input_snapshot` de `get_case`.
Não invente snapshot nem acrescente campos de endpoint, perfil ou paginação.

Os exemplos JSON abaixo são sintéticos e masked, sem credenciais ou dados
pessoais. Substitua os identificadores e o snapshot pelos valores realmente
relidos no caso autorizado antes de operar. A referência deve ser estável,
única para a intenção de consulta desse ator e preservada durante a retomada.

Reserva (`enqueue`):

```json
{
  "schema_version": "loki.dataprev-monthly/1",
  "operation": "enqueue",
  "request_ref": "masked-monthly-001",
  "employee_id": "00000000-0000-4000-8000-000000000001",
  "input_snapshot": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
```

Releitura (`get`), inclusive após desconexão ou resposta perdida:

```json
{
  "schema_version": "loki.dataprev-monthly/1",
  "operation": "get",
  "request_ref": "masked-monthly-001"
}
```

`queued` é reserva; `running` indica execução em curso. Preserve `query_id`,
`request_ref`, corte, empresa, competência, estado e resultado retornados.
Consulte com a referência original antes de repetir qualquer comando com efeito incerto.
Não conclua que uma resposta perdida cancelou a consulta ou desfez a aplicação.

`complete` significa consulta e projeção completas; não significa aplicação à
folha. `incomplete` e `failed` são terminais sem promoção de parcelas parciais:
não confirma zero, fonte mensal nem ausência de consignado. Leia o motivo e
resolva a dependência correspondente. Prazo expirado, concessão perdida, seleção
pendente, limite de páginas e falha técnica não autorizam reaproveitar linhas
parciais. Havendo necessidade identificada de nova execução externa, use outra
referência; não crie referência nova apenas para contornar CAS ou conflito.
Uma reserva recusada deve ser distinguida de consulta existente pela releitura
e pelo código retornado, sem presumir efeito ou ausência de efeito.

A consulta exige paginação completa e coerência dos totais, sequência e
contratos. O limite de páginas pertence à administração: padrão 100, intervalo
1–1000. `provider_pagination_limit` requer avaliar a configuração e a necessidade
de outra consulta. O operador não envia `max_pages`. Antes de cada envio/retry,
o executor revalida vigência, escopo, seleção e prazo de execução. O recibo
terminal persistido prevalece sobre resposta tardia ou hash só em memória.
Hashes e manifesto registram integridade da evidência disponível, sem garantir
snapshot transacional oficial entre páginas; o contrato da Dataprev não fornece
token para essa garantia. Contagens estáveis não provam conteúdo imutável.

Somente após `complete`, confira o resultado, a seleção e o snapshot fixado na
reserva. Aplique pelo mesmo ator, caso e referência, com CAS; o backend revalida
o contexto atual. Mudança de dados, população ou seleção exige conciliação pelo
contrato, nunca substituir o snapshot arbitrariamente para forçar aplicação.

Aplicação (`apply`):

```json
{
  "schema_version": "loki.dataprev-monthly/1",
  "operation": "apply",
  "request_ref": "masked-monthly-001",
  "input_snapshot": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
```

O escritor complementa somente o campo mensal ausente
`credito_trabalhador_competencia`, conserva autoria e fontes e recusa sobreposição
com `dataprev_existing_monthly_source`. Não substitua confirmação/importação
anterior. Replay de aplicação devolve o recibo de aplicação; releia `get` e o
caso para conferir o recibo persistido, dados e snapshot resultantes. Registre
consulta concluída e aplicação confirmada separadamente. Prossiga ao cálculo e
à revisão somente conforme o contrato da folha; a consulta não comprova
desconto pago, pagamento, repasse, aceite do DP ou aprovação documental.

A consulta mensal não fornece saldo devedor rescisório nem garantias para
rescisão. Preserve `credito_trabalhador_rescisao` e seu contrato próprio;
parcela mensal não vira saldo devedor.
