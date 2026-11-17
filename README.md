# MCP Loki — contrato operacional 2.7.1
Candidata **provider0.4.23 / contrato, instruções e plugin2.7.1**,17/11/2026 (Onda 1,
backend #337, #338, #340, #341 e #342): contrato aditivo, sem ferramenta nova.
Domínio novo `folha_mensal` com a fila durável de um job pendente por empresa
(`company_job_pending`, enfileirar em série, sem gravar em outro caso da
empresa durante o job) e o diagnóstico da folha no dossiê (afastamento não
qualificado como causa primária, `leave_qualification`, `population_hash`);
13º por etapas no `decimo_terceiro`; matrícula omitida por padrão no
`create_case` (`matricula_funcionario_divergente`) no `geral`; códigos
`historical_*`, cobertura até o corte e lote revalidado em `ferias` e
`afastamento`. Vale quando a resposta servida apresentar os campos; wheel
preparado não comprova publicação do backend, instalação ou uso.

Edição anterior **provider0.4.22 / contrato, instruções e plugin2.7.0**,17/11/2026: processo
coletivo `reajuste_salarial` (feedback 71, backend #334) servido por
`get_process_contract` (`loki.salary-adjustment/1`), com prévia, exclusão e
reabertura como transportes de `receive_case_data`
(`loki.salary-adjustment-preview/1`, `-exclusion/1`, `-reopen/1`). Sem
ferramenta nova; o domínio novo `reajuste_salarial` e o guia
[REAJUSTE_SALARIAL.md](plugins/loki-bootstrap/skills/operar-loki/references/REAJUSTE_SALARIAL.md)
orientam a leitura do instrumento pela harness, a prévia, a decisão humana do
lote, a retomada até `APPLIED`/`PARTIAL`, as saídas, o pago declarado e as
pendências da folha X que ficam com a DP. Vale quando o contrato servido
apresentar a interface; wheel preparado não comprova publicação do backend,
instalação ou uso.

Edição anterior **provider0.4.21 / instruções e plugin2.6.12**,16/11/2026; contrato2.6.5
aditivo (campo opcional `dados_ferias.inicio_antes_de_feriado_source`, backend
#332): véspera de feriado recusa sem a decisão do cliente, tomada depois de o
DP informar o passivo (`ferias_inicio_antes_de_feriado`); com a decisão como
fonte, vira ressalva `clt_134_3_vespera_feriado` em `ressalvas.declaracoes_dp`
para aceite humano; início antes de feriado e do repouso exige as duas fontes;
recibos de componentes e consolidações de médias ficam obsoletos de novo,
inclusive os emitidos depois da 2.6.11. Vale quando a resposta servida e o
schema apresentarem o campo; wheel preparado não comprova publicação do
backend, instalação ou uso.

Edição anterior **provider0.4.20 / instruções e plugin2.6.11**,16/11/2026; contrato2.6.4
aditivo (campo opcional `dados_ferias.inicio_antes_de_repouso_source`, backend
#328): véspera de feriado sempre recusa (`ferias_inicio_antes_de_feriado`);
véspera do repouso semanal recusa sem a declaração do DP com o pedido do
cliente como fonte (`ferias_inicio_antes_de_repouso`), que vira ressalva
`ressalvas.declaracoes_dp` para aceite humano; recibos de componentes e
consolidações de médias anteriores ficam obsoletos e se refazem pelo fluxo
normal. Vale quando a resposta servida e o schema apresentarem o campo; wheel
preparado não comprova publicação do backend, instalação ou uso.

Edição anterior **provider0.4.19 / instruções e plugin2.6.10**,16/11/2026; contrato2.6.3
inalterado: job da folha bloqueado em `calculate` traz `diagnostic.errors` com
`field`, `index` (funcionário em `dados_folha.funcionarios`, base zero) e
`reason` fechado; `verba_nao_mapeada` traz `codigo` da rubrica. Vale quando a
resposta servida apresentar os campos; wheel preparado não comprova publicação
do backend, instalação ou uso.

Edição anterior **provider0.4.18 / instruções e plugin2.6.9**,15/11/2026; contrato2.6.3
inalterado: na preparação corrente, recusas de férias e de afastamento trazem
`errors` por campo (código de regra, `missing` ou `extra_forbidden`); a recusa
da prévia de população da folha traz `index` (base zero) e motivo fechado por
item; depois de `restart_case`, fontes da harness e anexos seguem em `get_case`
para reuso. Vale quando a resposta servida apresentar os campos; wheel
preparado não comprova publicação do backend, instalação ou uso.

Edição anterior **provider0.4.17 / instruções e plugin2.6.8**,14/11/2026; contrato2.6.3
inalterado: recusas de dados de férias e de afastamento trazem em `errors` o
campo exato e um código de regra (`ferias_...`, `afastamento_...`); a harness
corrige só o campo apontado e reenvia com novo `request_ref`. Vale quando a
resposta servida apresentar os campos; wheel preparado não comprova publicação
do backend, instalação ou uso.

Edição anterior **provider0.4.16 / instruções e plugin2.6.7**,14/11/2026; contrato2.6.3
inalterado: preservação de imports pelo cálculo de onde saiu o pacote da folha,
saldo da rescisão em mês comercial, conexão fechada com `/healthz` normal,
segunda ocorrência de férias, lote de políticas de mapa com arredondamento e
`case_write_constraints` com `field`/`reason`. Vale quando a resposta servida
apresentar os campos; wheel preparado não comprova publicação do backend,
instalação ou uso.

Edição anterior **provider0.4.15 / instruções e plugin2.6.6**,14/11/2026; contrato2.6.3
inalterado: recusas e prévias com motivo fechado — consumidor equivalente na
preservação de imports, prévia de população só por matrícula, afastamentos da
rescisão, chaves de `field_sources`, `subreason` da simulação, reinício sem
`preparation` e férias relacionadas. Vale quando a resposta servida apresentar
os campos; wheel preparado não comprova publicação do backend, instalação ou uso.

Edição anterior **provider0.4.14 / instruções e plugin2.6.5**,13/11/2026; contrato2.6.3
inalterado: correções do destrave de admissão após revisão — `next_action` do
recibo de retificação de nome, alcance só caixa/espaços/NFC, import documental
bloqueado por efeitos pendentes, dependente fora do acesso da conta e
cancelamento recusado por efeitos sem `next_action`. Vale quando a resposta
servida apresentar os campos; wheel preparado não comprova publicação do
backend, instalação ou uso.

Edição anterior **provider0.4.13 / instruções e plugin2.6.4**,13/11/2026; contrato2.6.3
inalterado: destrave de admissão — Beneficiários da ficha em várias linhas sem
truncar, retificação de nome diferente só em caixa/espaços e motivo das recusas
de reinício/conciliação. Vale quando a resposta servida apresentar os campos;
wheel preparado não comprova publicação do backend, instalação ou uso.

Edição anterior **provider0.4.12 / contrato, instruções e plugin2.6.3**,10/11/2026:
consulta mensal Dataprev pelo contrato servido, referência durável e aplicação
separada com CAS. O [guia público](plugins/loki-bootstrap/skills/operar-loki/references/DATAPREV_MENSAL.md)
conserva importação tipada e limites de autoridade/completude. Wheel preparado
não comprova publicação do backend, instalação ou acesso real.

Edição anterior **provider0.4.11 / contrato, instruções e plugin2.6.2**,09/11/2026:
orienta substituição delimitada de insumos de férias, saldo contextual no mês31
e política contextual de FGTS mensal. Recursos dependem dos contratos servidos
e da publicação do consumidor; configuração real e aceiteDP permanecem próprios.

Edição anterior **provider0.4.10 / contrato, instruções e plugin2.6.1**,09/11/2026: retomada autenticada de resposta corrente intake/procedure também após falha interna, preservando limites, memória e CAS. O consumidor e a publicação precisam de validação própria; não altera a rotina da Ana.

Edição anterior **provider0.4.9 / contrato, instruções e plugin2.6.0**,08/11/2026: conciliação aditivaONB, reaproveitamento de respostaDP após falha de schema, diagnóstico mensal persistido e representação explícita de afastamento no consumidor rescisório. O conteúdo depende da publicação do backend e dos contratos servidos; não comprova instalação ou aceite na rotina daAna.

O pacote `mcp-loki-updates` **0.4.23** entrega instruções **2.7.1** ao backend.
A entrega padrão é autenticada ao solicitante; Drive Izzi permanece opção futura
explícita, sem configuração ou ativação nesta entrega.

O plugin nativo `loki-orientacoes@loki-equipe` **2.7.1** contém bootstrap, leitores
externos e guias de operação. A distribuição não é um servidor independente.
OAuth, autorização, cálculos, banco, documentos e decisões pertencem ao Loki.

A orientação introduzida na edição2.5.4 continua: perguntas ao DP com nome+código reais e escopo da fonte,
preservando zeros, conflitos e partes independentes. As três skills pertinentes
e o domínio geral entregam o mesmo contrato; isso não comprova uso pelo modelo.

A edição2.5.2 acrescenta o roteiro de
[recursos de DP](plugins/loki-bootstrap/skills/operar-loki/references/CAPACIDADES_DP.md):
descoberta da prontidão mensal, histórico pelo lote existente, jobs duráveis,
nova preparação e parâmetros recentes. A seleção da folha da PR240 só se aplica
quando o contrato servido oferecer a rota. A edição orienta a nova preparação
de afastamento e o alcance salarial qualificado de mês civil30/divisor30 quando
o backend os oferecer; o pacote de instruções não publica essas capacidades.
O contrato atual é2.7.1, aditivo; o mínimo2.0.0 permanece. Acurácia exige coorte e medição reais;
esta candidata local não atualiza conta, instalação ou agenda da Ana.

O Loki recebe dados estruturados, valida, calcula, gera documentos, registra e
entrega. Leitura de originais e comparação são externas. O operador consulta
`get_process_contract`, captura `get_case.input_snapshot` e envia `receive_case_data`
com dados, fontes opcionais, referência idempotente e snapshot esperado. Depois segue cálculo,
geração e revisão do contrato. Versões internas preservam auditoria; a empresa de
teste usa o mesmo fluxo e gates da operação comum.

A extensão2.3.0 é aditiva ao contrato2.0.0 e conserva o mínimo de plugin2.0.0.
A migração anterior de1.x foi incompatível: ferramentas antigas de extração, comparação e
execução especial foram retiradas. Clientes que declaram contrato/plugin1.x
precisam migrar. Cliente sem versão permanece desconhecido; bootstrap de identidade
não restaura ferramentas retiradas. O catálogo do aplicativo e a instalação no
operador exigem verificação própria. Esta árvore candidata não comprova deploy.

- [Contrato, migração e promoção](docs/MCP_UPDATES.md).
- [Skill operacional](plugins/loki-bootstrap/skills/operar-loki/SKILL.md) e
  [dados/fontes e retomada](plugins/loki-bootstrap/skills/operar-loki/references/WORKFLOWS.md).
- [Instalação e atualização](docs/DAILY_OPERATOR_UPDATES.md),
  [Codex Linux](docs/CODEX_LINUX_SETUP.md) e [ativação da rotina](docs/ANA_ROUTINE_ACTIVATION.md).
- [Leitores externos e limites](docs/LOCAL_READERS.md).

Para desenvolvimento use a `.venv` própria existente, Python3.11 e o lock vigente.
Valide testes apropriados, ruff e mypy antes de construir `uv build --wheel`.
Um wheel tem versão imutável. Promoção usa `scripts/promote.py` com destino explícito,
validação e proveniência honesta de HEAD/tree/dirty; não implanta nem muda OAuth.
Não substitua bytes sob a mesma versão. Lock, wheel, consumidor e publicação exigem
validação separada. Dados pessoais, fontes privadas e credenciais ficam fora do Git.

Os documentos de releases anteriores em `docs/` são históricos; não definem o
contrato operacional atual nem demonstram instalação, consumo ou aceite individual.

Compatibilidade da candidata0.4.6: fonte `loki-document-kit`0.2.0, com allowlist
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
fonte. Veja [WORKFLOWS.md](plugins/loki-bootstrap/skills/operar-loki/references/WORKFLOWS.md)
para estados, retorno e retomada; esta árvore não comprova publicação ou adoção.


`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Extensão eSocial2.3.0

Provider0.4.6, contrato2.5.0 e instruções/plugin2.5.2 preservam o mínimo2.0.0 e a
compatibilidade declarada de2.0/2.1; cliente desconhecido continua desconhecido.
A allowlist e as permissões dos domínios permanecem: consulte `geral` e
`alteracao_cadastral` para as cinco ferramentas HTTPS de modo fiscal e parâmetros.
Veja o roteiro nativo [ESOCIAL.md](plugins/loki-bootstrap/skills/operar-loki/references/ESOCIAL.md). A configuração de homologação
pode persistir por intenção de administrador humano; não transmite. Operação
permanece PENDING/recusada sem fila/executor fiscal, assinatura, representação
e recibo de homologação verificados. S-1005 local não comprova transmissão.
Perfis por estabelecimento/data usam os escritores empresariais com CAS,
origem opcional e releitura; seleção não comprova consumo financeiro.

Esta distribuição não provisiona acesso fiscal, não emite eventos pelo catálogo
HTTPS e não instala o plugin no operador. Wheels anteriores, inclusive0.3.0,
permanecem imutáveis; promoção/publicação exigem revisão e gates do consumidor.

## Correção da harness2.3.1 preservada

Provider0.4.6/instruções e plugin2.5.2 mantêm contratoMCP2.5.0 e mínimo2.0.0.
O helper offline `mcp-resource` salva bytes embutidos da resposta completa com
URI/SHA256/tamanho explícitos; os roteiros orientam seleção histórica tipada,
complemento somente de nome vazio pelo contrato e checks após leitura real.
Não há novo transporte, autofill de CTPS/CDI ou fórmula universal de avos.
Script e lock permanecem juntos; dependências não mudaram. Wheels0.4.1 e
anteriores continuam imutáveis. Esta candidata não comprova publicação,
instalação, carregamento ou execução real na Ana, nem muda agenda/credenciais.

## Comunicação2.5.0

Provider0.4.6/instruções e plugin2.5.2 orientam conclusão primeiro, pontos
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
