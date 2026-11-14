# Atualizações MCP Loki — contrato 2.6.3

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
Na candidata atual, o recomendado é2.6.1 e o contrato2.6.1 é aditivo;
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
