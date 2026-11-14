# Recursos de DP: descobrir, preparar e conferir

Leia antes de preparar folha com muitas pessoas, retomar caso ou qualificar
férias, afastamento, consignado, pensão e adicionais. Este roteiro descreve
recursos condicionados ao contrato servido, sem corrigir defeitos de cálculo.

## Descobrir prontidão e medir acurácia

Consulte `meu_acesso`, `get_dp_capabilities`, `list_workflows` e
`get_process_contract` no serviço autenticado. Fonte no Git, plugin instalado,
catálogo do aplicativo e contrato servido são observações separadas. Uma rota
nova só pode ser usada quando anunciada pelo contrato servido; instrução local
não comprova publicação, acesso ou instalação no executor.

Para folha, consulte `get_client_readiness` com `process_type=folha_mensal`,
`empresa_cnpj` e `competencia` exatos. `pronto` é cadastral;
`folha_avaliada`, `pronto_folha` e `mapa_folha` mostram a avaliação mensal,
com hash/grupo/origem. Sem contexto mensal, `pronto_folha=null` e
`mapa_folha_nao_avaliado` conservam a lacuna. Essa leitura não mede acurácia
nem comprova completude ou prontidão por funcionário.

O contrato atual não oferece endpoint bulk específico de prontidão por pessoa.
Quando o catálogo/contrato não oferecer esse recurso, registre a lacuna sem
inventar nomes ou concluir que uma tabela da harness seja estado do Loki.
Consulte população/identidade no caso, histórico e pendências por pessoa.
Uma tabela de cobertura é diagnóstico da harness, com data e fontes explícitas.

Para histórico em lote, somente quando o catálogo HTTPS oferecer
`get_operational_batch_contract`, consulte esse contrato e confira as operações
permitidas. Sem essa ferramenta no catálogo, registre pendência de distribuição
e use consultas e seleções individuais anunciadas e autorizadas. Não invente
alias, dispatcher ou rota de lote em `receive_case_data`.
O lote existente, quando disponível, pode encadear leituras
`get_case_historical_state` e seleções `apply_historical_state` por caso,
com o `state_hash` retornado, identidade/episódio e corte conferidos.
Isso continua sendo execução sequencial por item, sem endpoint bulk novo.
Use dependências/referências de resultado somente no formato do contrato;
releia recibos e consumo por calculador. `SUCCEEDED` da linha não comprova
consumo financeiro; `STARTED` ambíguo exige conciliação antes de repetir.

A meta de98% usa casos completos corretos / casos elegíveis, com coorte,
finalidade, período e elegibilidade definidos antes da rodada. Falha, parcial
e abstenção não são acerto; não exclua casos após conhecer o resultado.
Sem referência ou completude necessárias, declare percentual não aferido.
Registre também comparáveis, coincidências por campo, bloqueios e motivos,
sem substituir o indicador principal. Prontidão, testes de software e seleção
de histórico não comprovam acurácia geral. Separe defeito reproduzido,
parâmetro/dado pendente, regra ainda não medida e diferença de recepção da harness.

## Retomada, nova preparação e seleção da folha

Na folha, siga `preferred_execution` e `durable_workflow` do contrato.
Quando `available=true`, use os jobs duráveis
`enqueue_case_workflow`/`get_case_workflow_job`, inclusive pela rota declarada
`receive_case_data` com `loki.case-workflow-command/1`.
Preserve `request_ref` e `job_id`; resposta perdida exige consulta do mesmo
job, não outro cálculo. `exception_type`, `phase` e `reference` são diagnóstico
técnico, sem provar correção dos dados ou autorizar restart.

Recomeçar exige pessoa autorizada, intenção específica e
`expected_snapshot=get_case.correction_snapshot`. Siga `preparation` do
contrato; `loki.case-preparation-transport/1` em `receive_case_data` só é rota
quando anunciada. `replace_process_inputs` abre nova preparação e exige novos
dados financeiros; documentos, decisões e eventos anteriores permanecem.
Preservar imports de admissão/rescisão exige a prévia `preview_import_preservation`
e o plano/hash/dependências correntes em `preserve_imports`; não escolha eventos
de memória. Aprovação ou efeito pode exigir conciliação prévia.
Folha mensal protegida (`aguardando_revisao`, `aprovado`, `publicado`) deixa de
bloquear a preservação só com `consumer_impact.protected_consumers[]` em
`classification: "equivalent"` e
`reason: "employee_excluded_from_current_calculation"` (contrato declara
`protected_consumer_equivalence_proofs`). `"unknown"` continua bloqueando com
`import_preservation_protected_dependency`. No restart,
`import_preservation_consumer_changed` pede refazer a prévia;
`reconciliation_dependencies_busy` pede tentar depois, sem forçar.

Quando o serviço informar o motivo, a recusa de `restart_case`/`cancel_case`
por efeitos conserva `restart_requires_effect_reconciliation` ou
`case_lifecycle_action_refused` e traz `blocking_refs` (`ref` e `kind` entre
`vinculo_event`, `documentary_approval`, `chat_review` e `operational_effect`;
eventos também `origin` e `event_type`), `blocking_ref_count` (lista limitada
a 50). `next_action` vem somente em `restart_case`:
`preview_import_preservation` quando todos os refs são imports documentais, só
em admissão e rescisão; `preview_admission_reconciliation` nos demais casos de
admissão; ausente nos outros processos. As duas prévias habilitam nova
preparação (reinício), não cancelamento: `cancel_case` recusado por efeitos
nunca traz `next_action` e não tem caminho pelo acesso da operadora. Nele,
`blocking_refs` e `blocking_ref_count` só vêm quando o estado permitiria
cancelar sem os efeitos (`aberto`, `em_preparacao`, `aguardando_revisao`,
`rejeitado`); fora deles `case_lifecycle_action_refused` vem sem esses campos
e a recusa é de estado. Nenhuma proteção mudou. Siga somente o `next_action`
recebido; sem ele, pare, guarde a resposta e relate pelo fluxo de problema com
`case_id` e refs, sem dado pessoal. Não contorne, não cancele nem recrie o
caso. Blockers da prévia de conciliação, Beneficiários da ficha e nome
diferente só em caixa/espaços estão no domínio `admissao`.

`restart_case` em `aberto`/`em_preparacao` sem `preparation` recusa com
`restart_requires_preparation_for_state` (`next_action: "get_process_contract"`):
envie `preparation` com `schema_version: "loki.case-preparation/1"`,
`request_ref` e, em `mode`, um dos modos de
`get_process_contract.preparation.modes`; efeitos persistidos ainda podem
exigir conciliação própria. Nos demais estados, `restart_requires_adjustable_state` não tem
reinício por esse caminho.

Correção da população da folha depende de
`preparation.population_correction` no contrato servido. Quando oferecido,
prepare a lista final completa de `funcionario_id`+`matricula`, consulte
`preview_payroll_population_correction` ou a rota anunciada
`loki.payroll-population-preview/1` e apresente diferenças ao humano.
A prévia aceita item só `{"matricula"}` e devolve `funcionario_id` em
`population`. Matrícula que passou a apontar para outra pessoa recusa o item
só com `{"matricula"}` (`payroll_population_rebound_requires_identifier`) até o
`funcionario_id` novo vir no item; confirme antes com o humano que é outra
pessoa. A aplicação exige `{funcionario_id, matricula}` copiados da prévia e o
`preview_id`.
A aplicação usa `loki.case-preparation/1`, `mode=replace_payroll_population`,
`preview_id`, `reason`, `request_ref` e `reset_financial_inputs=true`,
no restart autorizado ou seu transporte tipado anunciado. Não é complemento
incremental: exige repor dados/qualificações financeiras e nova revisão.
Prévia não aplica; seleção antiga, valores e aceite não migram por presunção.
Sem esse bloco/rota, preserve a pendência; plugin novo não publica a PR240.

Cancelamento usa `cancellation` do contrato. Quando anunciado,
`loki.case-cancellation/1` pode seguir em `receive_case_data`, com
`expected_snapshot=correction_snapshot` e `human_message` específico.
Releia estado e trilha; cancelamento não exclui registros nem libera a chave
natural para criar outro caso. Automação não recebe autoridade humana.

Para publicação, smoke ou comparação de versões, não baixar o acervo nem
rebaixar todos os documentos. Confira fatos, eventos, decisões e metadados/hashes
pelo conector; integridade dos bytes usa provas do servidor/storage/backup.
Baixe somente o documento necessário à demanda expressa. Metadados não são
bytes lidos; checks de um pacote documental exigem a conferência correspondente.

## Histórico, saldo de abertura e médias de férias

Consulte `get_case_historical_state` no episódio e corte do caso e selecione
por `apply_historical_state` somente após conferir identidade, cobertura e
`state_hash`. `saldo_source` admite a referência histórica tipada anunciada
pelo schema, com `fact_ref` e `fact_hash`; não substitua por ID ou saldo inventado.
Confira período aquisitivo, corte da abertura anterior ao gozo,
`fragments_complete`, dias consumidos, abono e movimentos entre abertura e gozo.
Histórico selecionado não comprova saldo qualificado nem pagamento.

As alternativas `medias`, `componentes_medias`, `medias_importadas` e
`medias_nao_aplicaveis_source` são exclusivas conforme o schema.
Média final importada usa seleção explícita por finalidade, período de uso,
fato e hash; não é média recalculada de qualquer folha disponível.
Não troque ausência de histórico por zero ou “não se aplica”.
Siga o schema atual para programação, calendário, incidências e fontes próprias.

Releia resultado e proveniência para demonstrar consumo real; seleção e
contrato disponível são provas distintas. Não mova datas ou saldos para
forçar aceitação de uma origem incompatível.

## Nova preparação de afastamento

Consulte `get_process_contract("afastamento")`. Quando o contrato anunciar
`preparation.supported=true`, a pessoa autorizada pode usar
`replace_process_inputs` pelo transporte `loki.case-preparation-transport/1`
em `receive_case_data`, com `correction_snapshot`, mensagem humana e referência
idempotente. Exige `operar_casos`, `decidir_chat` e `corrigir_dados`; automação não recebe
essas capacidades humanas. Siga o schema anunciado, sem inventar parâmetros.

A nova preparação conserva caso, empresa, funcionário, CPF/CNPJ, admissão e
referência da ocorrência; arquiva os fatos anteriores e exige nova recepção
completa de categoria, início, períodos e retorno coerentes. Releia o recibo,
os fatos recebidos e a nova revisão. Não reenvie o payload antigo sem conferir
suas âncoras e os parâmetros corretos. Histórico e decisões permanecem.

Aprovação ou efeito aplicado impedem essa recuperação até a conciliação própria;
não use restart para reescrever um episódio efetivo. O corretor genérico
`submit_operator_correction` mantém
a recusa `correcao nao pode alterar identidade ou escopo do caso` para
`leave.categoria`. Essa recusa não impede a nova preparação quando o contrato
a oferecer. Sem o suporte anunciado, conserve a pendência do caminho e sua
reprodução; o plugin não publica a capacidade nem altera a conta do operador.

## Consignado: contrato, competência e rescisão

Para a consulta automática mensal, siga
[DATAPREV_MENSAL.md](DATAPREV_MENSAL.md), somente quando o contrato servido
anunciar `loki.dataprev-monthly/1`. Consulta completa exige aplicação separada;
retomada usa a referência durável original antes de repetir comandos.

Consulte `get_company_onboarding_contract` e os parâmetros efetivamente
oferecidos. `credito_trabalhador_contratos` registra revisões de contrato,
número como string, instituição, vigência, parcela em centavos e
`rubrica_loki` explícita. Encerramento/cancelamento é outra revisão;
não altere revisões antigas nem presuma rubrica por código numérico global.

Na folha, `credito_trabalhador_competencia` identifica os contratos/versões
confirmados no mês e as qualificações exigidas pelo schema. Declaração atribuída
pode ser aceita, sem documento/hash universal. Cronograma não comprova desconto
pago ou repasse; confira memória, limites, operandos e pendências.

Na rescisão, `credito_trabalhador_rescisao` é snapshot próprio da consulta,
com data do desligamento/consulta, identidade, completude, contratos, saldos e
garantias informados. Parcela mensal não vira saldo devedor.
Consulta automática Dataprev exige acesso corporativo e contrato técnico próprio;
importação estruturada disponível não comprova integração automática ativa.
Sem dados/qualificação específicos, preserve o resultado dependente pendente.

## Pensão por finalidade

Analise o ofício/decisão na harness antes de preparar
`pensao_alimenticia_regra`, pelo contrato de onboarding/parâmetros autorizado.
Originais permanecem na harness; a regra extraída conserva referência, vigência
e autoria, sem anexação ou hash por campo universal.
Quando oferecido, `loki.pension-rule/2` define aplicações explícitas para
`folha_mensal`, `ferias`, `decimo_terceiro` e `rescisao`, com situação,
rubrica, percentual, base, deduções, tratamento do IRRF e critério temporal.
Não estenda regra mensal a outra finalidade nem conclua “não beneficiário”
a partir de ausência. Política desconhecida retém parcelas dependentes.

No décimo terceiro, confira `apuracao` (`parcela` ou
`acumulada_com_compensacao`), `etapas` e retenção anterior efetivamente qualificada;
retenção omitida não é zero. Nas férias e na folha, confira a proveniência
da retenção já calculada para evitar consumo duplicado. Persistência do parâmetro
não demonstra consumo: releia a seleção e a memória do cálculo correspondente.

## Adicionais por pessoa e cargo

Consulte o contrato de parâmetros e o cadastro empresarial vigente.
`insalubridade_regra` e `periculosidade_regra` são escolhas individuais
explícitas, com `recebe`, vigência, rubrica e operandos do schema; ausência não
é `recebe=false`. Regra individual qualificada prevalece sobre política por cargo.

`additional_policies` só atribui por cargo quando houver política explícita
com CNPJ, estabelecimento, cargos, período e população de admissões.
`inherit_future_hires` exige escolha e corte de admissão explícitos;
o nome do cargo isolado não cria direito. Sobreposição, cargo/unidade desconhecidos
e vigência parcial conservam pendência/necessidade de segmentação.

Elegibilidade difere de valoração: base, percentual, divisor, quantidade e
incidências dependem do mapa/regra qualificados; não invente fórmula universal.
Aplique cadastro somente por `validate_client_config`/`apply_client_config`
autorizados, com CAS e releitura. Parâmetros individuais seguem onboarding próprio.
Fonte informal atribuída pode ser aceita; confira consumo na memória por pessoa.

## Saldo de salário na rescisão

Quando o calculador servido oferecer o alcance qualificado, admissão e
rescisão no mesmo mês civil de 30 dias, com divisor 30 e sem afastamento
sobreposto, usam o intervalo contratual inclusivo das datas
reais de admissão e desligamento. É uma inferência técnica documentada das
fontes aplicáveis e da semântica temporal, não medição histórica nem regra
universal de calendário. A harness informa fatos; os dias e centavos são derivados
pelo motor, sem entrada livre para coincidir com a referência.

O consumidor `rescisao-v42` estende o alcance ao mesmo mês civil de 31 dias,
com divisor 30, desligamento até o dia 30 e sem afastamento sobreposto. A versão
nova é selecionada somente nesse predicado. Mês30 e contratos anteriores
permanecem no alcance próprio; fevereiro, desligamento no dia31 e outros
divisores não são habilitados por essa extensão. Releia dias, seleção e memória;
`regra_nao_medida:saldo_admissao_no_mes` continua um diagnóstico possível fora
do alcance qualificado. Não adapte a data ou o divisor para coincidir com o comparador.

`regra_nao_medida:saldo_admissao_no_mes` pode continuar pendente fora desse alcance; fevereiro,
dia31, divisores e afastamentos seguem suas guardas próprias. Atualização de
instruções não corrige o calculador publicado nem certifica o caso completo.
Confira versão do motor, dias, memória e bases; não reutilize memorial parcial
antigo ou aceite anterior como resultado da regra nova. Parcelas independentes
permanecem disponíveis conforme o contrato, sem preencher ausência com zero.

## Substituição de insumos e pins de férias

Quando `get_process_contract("ferias")` anunciar `preparation.supported=true`,
use a preparação `replace_process_inputs` no restart existente ou pelo transporte
`loki.case-preparation-transport/1` anunciado em `receive_case_data`. A pessoa
precisa das capacidades do contrato, inclusive `corrigir_dados`; o replay também
revalida a autorização. Transcreva a intenção específica e use o
`correction_snapshot` corrente. Aprovação ou efeito aplicado exigem a conciliação
própria antes do reinício.

Pessoa, empresa, vínculo, competência, aquisitivo e gozo conhecidos permanecem
âncoras. Depois da fronteira, releia `get_case.input_snapshot` e envie a seção
`dados_ferias` completa com nova referência: alternativas de médias, pins de saldo
e datas/flags precisam ser reapresentados conforme o schema. A seleção nova
continua sujeita a vigência, identidade, cobertura e integridade. O corretor
pontual conserva seu alcance; documentos e decisões anteriores permanecem.

`related_vacation_parameters_invalid` pede `get_case` do contexto relacionado
para diagnóstico, sem inventar flags ou ignorar histórico parcial. A orientação
não autoriza corrigir fatos ou reaplicar casos automaticamente. Segunda ocorrência
em outra competência usa o caminho existente; suporte na mesma competência não
é inferido desta substituição. Publicação e reteste real exigem provas próprias.



## Política contextual do FGTS mensal

Quando o consumidor oferecer `folha-v29`, o mapa selecionado pode declarar
`fgts_mensal` com `policy_version=loki.fgts-mensal/1`, método, fonte e
`escopo=trabalhador_competencia_mensal_8pct`. Confira empresa, competência e
vigência do mapa efetivamente selecionado. Política ausente conserva o cálculo
legado; política ausente não comprova configuração ou validação do critério.
A memória `calculo_fgts` por empregado distingue método, fonte, pin, base,
valor da fórmula e valor final; uma base pendente não vira zero.

Confronte a memória com persistência, materialização, documentos e soma dos
encargos individuais. Apuração sobre base agrupada e FGTS rescisório têm
contratos próprios. Disponibilidade da política não autoriza alterar configuração
real, corrigir valores, aprovar casos ou transmitir. Uma diferença relatada de
centavo só é conferida com os operandos e a referência daquele cálculo.
