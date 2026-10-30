# Atualizações MCP Loki — contrato 2.3.0

Candidata de30/10/2026: provider/wheel0.4.0, instruções2.3.0 e plugin2.3.0.
Texto versionado não atualiza serviço implantado nem a instalação do operador.
O backend incorpora o wheel; o plugin tem distribuição Git própria.

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
recomendado é2.3.0. Contrato2.3.0 é aditivo; cliente2.0.0 permanece compatível. Contrato1.x declarado é incompatível; cliente desconhecido
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

A candidata0.4.0 define entrega autenticada ao solicitante como padrão e Drive como opção futura explícita; contrato MCP2.3.0 é aditivo, mínimo de plugin2.0.0. Os wheels0.2.0,0.2.1 e0.2.2 já construídos permanecem imutáveis.

Compatibilidade da candidata0.4.0: fonte `loki-document-kit`0.2.0, com allowlist
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

Provider0.4.0, contrato/instruções/plugin2.3.0 preservam o mínimo2.0.0 e a
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
