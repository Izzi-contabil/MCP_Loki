# eSocial: modo da empresa e parâmetros temporais

Use o conector HTTPS existente `https://loki.tominho.com/mcp`, a identidade e o
escopo de `meu_acesso`/`get_operator_context`. Consulte instruções `geral` e
`alteracao_cadastral`; esta versão preserva a allowlist de domínios. O contrato
fiscal é `get_company_esocial_contract()`, versão `loki.company-esocial/1`.
Leia seus schemas e limites reais antes de preparar argumentos. Ferramenta ausente
é lacuna de distribuição/contrato; instalação, catálogo e execução observada são
provas separadas. Toda operação administrativa usa HTTPS; não encaminhe ao painel
nem crie transporte operacional SSH/stdio.

## Consultar e propor o modo

1. Confira a empresa por UUID e CNPJ no acesso autorizado. Consulte
   `get_company_esocial_state(company_id)`. Sem decisão registrada, a resposta
   mostra `mode=homologacao`, `tp_amb=2`, `revision=0`, `persisted=false` e
   `company_mode_not_configured`. Essa leitura conservadora não cria uma decisão,
   não transmite e não autoriza qualquer evento.
2. As opções são `homologacao` com `tp_amb=2` (Produção Restrita) e `operacao`
   com `tp_amb=1` (produção oficial). Não confunda o ambiente fiscal externo com
   empresa de teste ou execução de testes automatizados: a empresa de teste usa
   os mesmos contratos e gates operacionais. O destino fiscal é explícito.
3. Um administrador humano provisionado, tipo pessoa, obtém
   `preview_company_esocial_mode(company_id, proposal, expected_revision)`.
   A proposta contém `mode`, `event_types` e `cutover_on`. Para Operação,
   `event_types` não pode estar vazio e `cutover_on` deve estar informado.
   Use exatamente a revisão atual. A prévia não é escrita nem transmissão.
4. Apresente empresa, destino, escopo, corte, pendências e `preview_hash` ao humano.
   Com intenção específica, chame `apply_company_esocial_mode(company_id,
   proposal, decision)`, onde `decision` contém `expected_revision`,
   `preview_hash`, `reference` estável e `human_message` efetiva. A identidade vem
   do HTTPS, não de argumento ou documento. A intenção é declarada pela harness
   (`human_intent_declared_by_harness`), sem autenticação independente do texto.
   Automação não recebe autoridade humana por usar lote ou empresa de teste.
5. Preserve recibo, revisão, ator, hashes e referência; releia
   `get_company_esocial_state`. Replay do mesmo pedido conserva a referência e
   conteúdo; mudança de prévia, revisão, identidade ou conteúdo exige conciliação
   e nova prévia. Referência já usada com conteúdo diferente é conflito.

## Prontidão e limite de envio

Nesta implementação, `production_activation_supported=false` e
`transmission_ready=false`. A prévia Operação retorna `PENDING`; aplicar esse
destino recusa `esocial_activation_pending`, sem persistir ativação. A configuração
Homologação pode retornar recibo persistido, mas mantém `fiscal_events_sent=0`.
Faltam componentes operacionais verificados:

- `fiscal_dispatcher_not_configured`: executor e fila fiscal persistente;
- `signing_provider_not_configured`: provedor de assinatura/certificado;
- `company_representation_not_verified`: representação/procuração da empresa;
- `homologation_receipt_not_verified`: recibo de homologação verificado.

Uma flag, nome de certificado, declaração de procuração ou documento aprovado não
supera essas pendências. Não envie chaves, tokens ou credenciais no payload.
Provisionamento de assinatura, representação e envio não tem contrato operacional
implementado nesta entrega. Preserve o preparo e registre a lacuna; não invente
ferramentas de envio, fila ou coleta de recibos e não recorra ao painel/SQL/SSH.

Gerar ou validar S-1005 local pela biblioteca de XML/XSD não comprova transmissão,
assinatura válida, autorização de representação, aceite fiscal ou prontidão do
executor. Não há ferramenta HTTPS de emissão/transmissão S-1005 nesta entrega.
Importar histórico não cria eventos de saída; mudar modo não redireciona filas
anteriores nem retransmite histórico. Aprovação documental não autoriza eventos
fiscais, fechamento, reabertura, retificação ou exclusão.

## Perfis empresariais por estabelecimento e vigência

Consulte `get_company_parameter_state(company_id, effective_on)` com UUID exato
e data efetiva; não use o CNPJ da matriz para preencher filial. A resposta
`loki.company-parameters-state/1` seleciona `company_parameters` pelo
`establishment_cnpj` exato e intervalo fechado `valid_from`/`valid_until`.
Não há seleção automática de perfil anterior fora da vigência, default normativo
nem herança de outra empresa/filial. Perfil ausente ou lacuna de vigência mantém
`PENDING`; não complete zero. Um perfil selecionado pode conservar valores nulos
e pendências. `SELECTED` não certifica todos os parâmetros nem os consumidores.

Os valores opcionais são `cnae_preponderante`, `rat_bps`, `fap_10000`,
`classificacao_tributaria`, `fpas` e `codigo_terceiros`. O RAT usa pontos-base
inteiros (`100`, `200` ou `300`); o FAP usa inteiro na escala 10000 (`10000`
representa 1,0000). Preserve zeros à esquerda de códigos e taxas exatas; não
use float. Campo desconhecido permanece ausente/nulo conforme schema, sem
transformar ausência em isenção ou alíquota zero.

`basis=informado|inferido|confirmado` preserva a qualificação declarada.
`field_sources` é opcional e parcial: sem documento, hash ou fonte por campo,
a declaração autorizada recebe ator e registro da operação. Inferência não vira
confirmação independente. Metadados detalhados fornecidos permanecem associados
ao campo correto; não crie DOC, EXTSRC ou fundamento artificial. Provas específicas
continuam exigíveis apenas no ato que efetivamente as requerer.

A escrita usa os contratos empresariais existentes. Consulte `get_client_config`
e `get_client_config_history`; prepare alteração no caminho
`empresas[CODIGO_DOMINIO].company_parameters` sem inventar o código. Valide por
`validate_client_config` e aplique por `apply_client_config` com o mesmo
`expected_hash` do CAS, motivo, alterações e confirmações específicas exigidas.
O campo é uma coleção atômica: preserve perfis históricos e demais campos, sem
sobrepor vigências nem trocar CNPJ. Fontes opcionais podem ser informadas no
perfil e em `proveniencia` (`loki.company-config-provenance/1`); respeite o schema
de cada camada. O principal com `configurar_cliente` e os gates administrativos
vigentes continuam necessários. Não escreva parâmetros empresariais em caso de
empregado ou chame o writer de modo como substituto do cadastro.

Confira `APLICADO`, recibo e cadastro/histórico relidos. Depois consulte novamente
`get_company_parameter_state` para cada estabelecimento/data. Preserve
`profile_id`, `profile_hash` e o pin de `client_config` (`version`, `doc_hash`,
`slice_hash`) da seleção. Origem registra ator, data e base sem certificar bytes
originais. `financial_readiness_verified=false` e `transmission_verified=false`
continuam explícitos: persistência e seleção não comprovam consumo financeiro,
paridade de cálculo ou envio. Quando o contrato financeiro aceitar `selection`,
use a referência corrente e confira o resultado do consumidor; mudança de pin ou
perfil exige releitura/conciliação. Não afirme cobertura de processo não testado.

## Preparação local sem envio

O helper existente valida JSON contra o schema obtido por HTTPS, sem realizar
autorização, CAS, seleção temporal ou transmissão. Salve a resposta completa em
área privada da harness e prepare um perfil por vez:

```text
uv run --no-project --locked --python 3.11 --script CAMINHO/loki_local.py parameters perfil.json SAIDA_NOVA --schema contrato-esocial.json --schema-pointer /company_parameters_schema
```

A saída `parameters.json` conserva os dados e retorna `validated_not_sent`.
A validação local de schema não substitui os validadores do backend nem atesta
RAT legal, CNPJ válido, vigência não sobreposta ou prontidão fiscal. A harness
monta a alteração empresarial, usa os escritores HTTPS e relê o registro.
Originais permanecem na harness; parâmetros e proveniência opcional seguem ao
Loki. Não há solicitação artificial de PDF para confirmar esse cadastro.

`loki_local.py --version` informa somente a versão local declarada do helper.
Mantenha script/lock da distribuição juntos; não altere dependências ou pins do
kit legado. Código construído, plugin instalado, skill carregada, catálogo
descoberto e execução observada precisam de evidências próprias.
