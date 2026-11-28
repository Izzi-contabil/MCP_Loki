# Rescisão

## Episódio de afastamento e faixa de responsabilidade

No schema servido, `representacao=episodio_integral` conserva a interpretação
legada do episódio, incluindo a partição inicial do empregador quando aplicável.
`representacao=faixa_pagador` é opt-in para intervalo já dividido por responsável;
não desconta novamente os primeiros15dias da faixa declarada como INSS.
Essa indicação não presume concessão, espécie, continuidade clínica ou vínculo
entre intervalos vizinhos. Coleção mista, sobreposição ou responsabilidade
conflitante precisam ser conciliadas pelos dados reais e pelo contrato.

`retorno_episodio` informa o retorno efetivo quando a faixa não encerra o episódio.
Não deduza esse fato do último dia do pagador. Sem retorno necessário conhecido,
somente o efeito dependente permanece pendente. Ausência dos campos novos
preserva o formato e a interpretação legados; entrada, versão, seleção e memória
do cálculo precisam comprovar consumo antes de afirmar destrave financeiro.

Quando o serviço informar o motivo, a recusa da coleção de afastamentos traz
`reason` fechado: `afastamento_representacao_mista` (`faixa_pagador` é
tudo-ou-nada na coleção), `afastamento_concessao_incompativel`,
`afastamento_pagadores_sobrepostos`, `afastamento_concessoes_sobrepostas`,
`faixa_previdenciaria_exige_beneficio` ou
`beneficio_previdenciario_exige_pagador_inss`. Corrija a coleção pelos dados
reais; não troque a representação nem invente benefício, concessão ou pagador
para vencer a recusa. Sem o dado, preserve a pendência do efeito dependente.

Preservação de imports da rescisão segue `preview_import_preservation`: folha
mensal protegida classificada `equivalent` com
`employee_excluded_from_current_calculation` (o cálculo de onde saiu o pacote
da folha está ancorado e não inclui o funcionário) deixa de bloquear; a prévia
não recalcula a folha viva. `"unknown"` continua em
`import_preservation_protected_dependency`; `reconciliation_dependencies_busy`
pede tentar depois; pacote envelhecido continua barrado na revisão
(`calculo_desatualizado`). Detalhes em
“Retomada, nova preparação e seleção da folha” do domínio `geral`.

## Faltas mensais e elegibilidade do 13º

Consulte `get_process_contract` antes de preparar `faltas_decimo_terceiro`.
Quando o schema oferecer `loki.thirteenth-absences/1`, informe janela, corte,
competências, completude e ocorrências com a natureza e os dias realmente
conhecidos. Uma declaração atribuída ao pedido pode bastar; fontes por campo
são opcionais. Ausência de competência ou cobertura não significa zero faltas.
Preserve faltas justificadas, partição patronal/INSS e conflitos entre fontes;
não some novamente a mesma ocorrência do pedido e do histórico.

Confira `elegibilidade_decimo_terceiro` no resultado, quando persistida, e
confronte avos informados e derivados. Não altere o inteiro para vencer uma
recusa. Dados que já determinam a elegibilidade podem sustentar a parcela sem
redigitação; uma competência indeterminada retém somente os dependentes.
O 13º sobre aviso tem escopo próprio. Memórias e políticas de centavos devem
ser conferidas por cálculo e versão, sem aplicar retroativamente o cadastro.

Pensão/IR interdependentes só usam o regime explicitamente oferecido no schema,
qualificado por ato, base, dedutibilidade, percentual, processo e vigência.
Não use um regime pós-impostos como aproximação; incerteza do ato ou do imposto
permanece limitada aos resultados dependentes e não vira autorização de pagamento.

## Consignado: contrato, competência e rescisão

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


Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources` opcional, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga as operações declaradas no contrato; use `run_prepared_case_workflow` quando oferecido. Gere e revise documentos somente quando previstos; `document_outputs=[]` permite retorno por recibo persistido, sem PDF artificial. Releia o registro pelo contrato vigente antes de afirmar aplicação. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Registre valores ausentes como pendências, nunca como zero; mantenha divergências e origens para revisão. Não derive legislação, verbas, datas ou prazos a partir deste guia. As regras válidas e os gates de decisão devem vir do contrato operacional e das fontes aprovadas. O responsável humano deve cumprir os gates antes de qualquer efeito externo; não transmita nem publique resultados automaticamente.

## Pedido, aviso e anexos

Procure os originais e o histórico na tarefa correspondente ao fluxo de aviso trabalhado, indenizado ou pedido de demissão, usando somente acesso e canais já autorizados. O aviso pode ter sido emitido pela contabilidade ou pelo cliente; uma carta de demissão pode ser documento distinto. Registre origem, datas, localizador e eventual orientação posterior. Não deduza modalidade ou datas pela simples ausência do arquivo.

Anexo que não abriu é falha de acesso, não prova de inexistência. Preserve a falha e peça o original ou sua localização no canal autorizado, sem repetir pedido já pendente e sem buscar senhas ou contornar permissões. A explicação geral do fluxo não localiza automaticamente um anexo de um caso específico.

Se o cliente tiver comunicado o desligamento sem encaminhar documento, registre os fatos efetivamente informados e a orientação específica com sua origem. Só avance no que o contrato permitir, com pendências e revisão; não fabrique aviso, assinatura, carta ou ciência do empregado para completar o processo. Comunicação relatada não substitui aceite humano nem prova documental ausente.

## Histórico e médias

Consulte o contrato e os estados históricos correntes antes de afirmar que folha importada sustenta o cálculo. Cadastro importado, matrícula presente, histórico carregado, identidade qualificada, estado selecionado e consumo pelo calculador são etapas distintas. Não prometa que fatos antigos viram automaticamente médias, faltas aquisitivas ou saldo de FGTS. Qualifique empregado/vínculo, competência, rubricas, bases e fontes e preserve lacunas de cobertura; “não se aplica” só é válido se sustentado pelo caso e aceito pelo contrato, nunca como substituto de verba dependente de dado ausente.

Recusa de acesso técnico à carga histórica não autoriza conceder capacidades humanas, usar identidade de pessoa por automação ou criar canal de envio alternativo. Preserve o pedido para a operação administrativa correspondente; estas instruções não habilitam processos ou importadores.

Com raiz mínima válida, ausência de operandos não deve ser completada com zero nem impedir por orientação da harness as parcelas independentes admitidas pelo contrato. Dependentes desconhecidos mantêm IRRF e totais dependentes desconhecidos; saldo FGTS ausente pode reter a guia correspondente. Dado contraditório conserva conflito e não equivale a mera ausência. Não prometa cálculo integral nem documento condicionado sem os insumos próprios.

Consulte `get_case_historical_state` e selecione somente o estado tipado aceito por `apply_historical_state` no caso e corte correntes. A seleção e as qualificações de `receive_case_data` não são a fixação legada de um histórico opaco. Confira recibo de carga, releitura, identidade, cobertura, seleção, hash/operandos e consumo efetivo nos resultados de rescisão e folha. Episódio errado, competência/corte errado, fonte adulterada, revisão superada ou cobertura insuficiente impedem a seleção correspondente; preserve as parcelas independentes disponíveis sem contaminar seu cálculo. Não declare consumo apenas porque o histórico existe.

Toda operação usa o conector HTTPS `https://loki.izzicontabil.com.br/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Gozo antecipado e matrícula do eSocial na rescisão

Valem quando a resposta servida os apresentar.

- `rescisao_ferias_gozo_antecipado_pendente_regra`: o vínculo tem gozo
  antecipado (`vacation_use.advance`, confirmado ou programado) no aquisitivo
  em curso. A regra das proporcionais nesse caso ainda não foi definida pela
  DP, e o Loki recusa em vez de pagar as proporcionais cheias, com ou sem
  histórico selecionado. É esperado: não remova o `advance`, não mude datas
  nem contorne. Avise a operadora; a regra já está decidida (o gozo
  antecipado abate o direito proporcional, sem desconto no TRCT), mas o motor da
  rescisão ainda não a aplica. O gozo antecipado está no domínio `ferias`.
  Quando o schema servido de `dados_ferias` tiver `gozo_antecipado_source`, a
  regra já está definida (dias antecipados abatidos do direito), mas ainda não
  está no motor da rescisão. A mesma recusa vale quando houver, no aquisitivo
  em curso no desligamento, um caso de férias do Loki não cancelado com
  `gozo_antecipado_source` e algum cálculo, em qualquer estado. Leve à
  operadora.
- `termination_monthly_calculation_predates_registration_adoption`: a folha
  mensal referenciada foi calculada antes da adoção da matrícula do eSocial
  que mudou um identificador da população dela. Recalcule essa folha depois
  da adoção e repita a rescisão (domínio `folha_mensal`, "Matrícula do eSocial
  na população da folha").

## Complemento de identidade ausente

`funcionario.nome` é identidade do caso, não um campo de `dados_rescisao` ou da
seção de cálculo. Consulte `get_process_contract` e `get_case` atuais. Somente se
o contrato oferecer `identity_completion_schema` e a rota autorizada, prepare o
request `loki.case-identity-completion/1` com `request_ref` estável,
`expected_snapshot=get_case.correction_snapshot`, `input_snapshot` corrente,
`expected_company_id`, `expected_employee_id`, `expected_admission_date` e `nome`
observado/declarado com origem honesta. Valide offline por `parameters` usando
`--schema contract.json --schema-pointer /identity_completion_schema`.

Use `complete_case_identity(case_id, request)` quando descoberto; se o contrato
anunciar `receive_case_data` como rota compatível para esse discriminador, envie
exatamente o mesmo request por essa rota, sem envelope `loki.case-data/1` e sem
misturar o nome à seção financeira. Rota ausente é lacuna de distribuição HTTPS;
não improvise escritor. Esse complemento só preenche nome antes vazio da mesma
empresa, pessoa e episódio. Nome já preenchido, divergência de identidade ou
snapshots antigos conservam recusa/pendência; não substitua nome nem cadastro.
Preserve recibo e replay idêntico, releia nome e ambos os snapshots antes de
retomar geração. A operação não cria decisão humana nem efeito financeiro.

Na automação, o caminho concreto é `get_case_historical_state(case_id)` →
conferir identidade, corte, cobertura e `state_hash` →
`apply_historical_state(case_id, expected_state_hash)` → reler recibo/estado →
conferir consumo no cálculo. Pin legado pode exigir pessoa; não troque identidade
para contornar a recusa. Seleção não comprova pagamento ou ocorrência aplicada.
Não use meses tocados como avos devidos nem copie avos do TRCT comparado para
completar a entrada. Dados ausentes mantêm parcelas dependentes pendentes;
este guia não oferece fórmula universal de avos.

## Saldo de salário na rescisão

Quando o calculador servido oferecer o alcance qualificado, admissão e
rescisão no mesmo mês civil de 30 dias, com divisor 30 e sem afastamento
sobreposto, usam o intervalo contratual inclusivo das datas
reais de admissão e desligamento. É uma inferência técnica documentada das
fontes aplicáveis e da semântica temporal, não medição histórica nem regra
universal de calendário. A harness informa fatos; os dias e centavos são derivados
pelo motor, sem entrada livre para coincidir com a referência.

O consumidor `rescisao-v42` estende o alcance ao mesmo mês civil de 31 dias,
com divisor 30, desligamento até o dia 30 e sem afastamento sobreposto. Mês30
e contratos anteriores permanecem no alcance próprio. Releia dias, seleção e
memória. Não adapte a data ou o divisor para coincidir com o comparador.

Mês comercial (divisor 30, `trinta_fixo`), quando a resposta servida o
apresentar (`rescisao-v43`/`rescisao-v44`): os dias do saldo são calculados
pelo Loki; não informe dias nem troque o divisor. Desligamento em fevereiro ou
no dia 31 agora calcula; mês inteiro trabalhado conta 30 dias; admissão no mesmo
mês conta os dias corridos desde a admissão, incluindo atestado pago pela
empresa. Dias efetivos e convenção do calendário (regra da DP de 18/11/2026), quando
a resposta servida apresentar `rescisao-v45` (ou `rescisao-v46` com
`faixa_pagador`): com divisor 30, admissão no mês (depois do dia 1) com saída
no dia 31 ou no último dia de fevereiro paga os dias efetivos, sem completar o
mês comercial (10/07 a 31/07 = 22 dias; 10/02 a 28/02 = 19). Com
`convencoes.dias_do_mes: calendario` (da empresa ou, na falta, do cliente), o
saldo divide pelos dias do mês civil, inclusive em fevereiro e na admissão no
mês. A convenção vale só para o saldo da rescisão: folha mensal e férias não a
leem. Continua `regra_nao_medida:saldo_afastamento_no_mes` o afastamento por
INSS ou licença-maternidade no mês da saída, e
`regra_nao_medida:saldo_divisor_sem_convencao` o divisor que não é 30 fixo nem
os dias do mês. Nesses casos não altere datas nem divisor. Sem o sinal
(servidor anterior), admissão no mês com saída no dia 31 ou no fim de
fevereiro e o divisor pelo calendário seguem como
`regra_nao_medida:saldo_admissao_no_mes`, `saldo_fevereiro` ou
`saldo_dia_31_trinta_fixo`: a regra já é da DP e só falta a publicação, então
avise a operadora em vez de perguntar à DP. Cálculo novo
exige gerar o pacote de novo e uma nova
revisão; versões congeladas antigas desses cenários passam a exigir nova versão.
Atualização de instruções não corrige o calculador publicado nem certifica o
caso completo.
Confira versão do motor, dias, memória e bases; não reutilize memorial parcial
antigo ou aceite anterior como resultado da regra nova. Parcelas independentes
permanecem disponíveis conforme o contrato, sem preencher ausência com zero.

## Aviso prévio: norma coletiva e cumprimento parcial (2.9.8)

Valem quando o schema servido de `dados_rescisao` (`get_process_contract`)
apresentar `aviso_norma_coletiva` e `aviso_cumprimento_parcial`. Sem
declaração nada muda. Com qualquer uma, a versão do motor ganha o sufixo
`+aviso-declarado-v1` (por exemplo `rescisao-v40+aviso-declarado-v1`). A
harness confere a norma e a comunicação nos originais; o Loki só valida a
coerência dos parâmetros e não guarda norma de cliente.

- `aviso_norma_coletiva` `{dias_base, soma_lei_12506, fonte}`: só na dispensa
  sem justa causa, com aviso trabalhado ou indenizado. `dias_base` vai de 31 a
  90; com `soma_lei_12506: true` o total é a base mais 3 dias por ano completo
  (teto 90; 45 com 3 anos = 54), e com `false` são os dias fixos da norma, nunca
  abaixo do aviso legal. `fonte` cita a norma e a cláusula; idade, tempo de
  casa e vigência da elegibilidade são da harness.
- O aviso trabalhado cumpre 30 dias e o excedente sai indenizado (45 dias com
  0 anos indenizam 15). A projeção e os avos de 13º e férias do aviso
  (`avos_decimo_terceiro_aviso`, `avos_ferias_aviso`) contam pelo total.
- `data_projecao_aviso` tem de ser `data_desligamento` mais os dias indenizados
  (indenizado: o total; trabalhado: total menos 30; interrompido: total menos
  os dias cumpridos). Se não bater, a recusa é `aviso_projecao_incoerente`, com
  o campo e os dias esperados. A guarda vale com norma ou com
  `empregador_dispensou_restante`; o aviso legal sem declaração fica fora.
- `aviso_cumprimento_parcial` `{ramo, fonte}`, para o aviso trabalhado não
  cumprido até o fim (dias cumpridos = dias corridos entre `data_aviso` e
  `data_desligamento`; 30 é o aviso inteiro). `ramo`:
  - `empregador_dispensou_restante` (dispensa sem justa causa, desligamento
    antes dos 30 dias): os dias que faltavam do aviso total saem indenizados;
    exige `data_projecao_aviso` e admite avos do aviso.
  - `empregado_comunicou_desistencia` (pedido de demissão, antes dos 30 dias):
    desconto de (30 menos os dias cumpridos) × salário/30, só sobre o salário.
  - `empregado_faltou_sem_comunicacao` (pedido de demissão, desligamento no fim
    do aviso): o bloco do aviso não desconta; os dias não trabalhados entram
    como faltas na declaração do mês (`faltas_do_mes_operacionais` ou a 8792
    das parcelas, com ao menos um dia). É a leitura adotada pela engenharia; se
    a DP pedir outra contagem, registre o problema.
- Sem documento que mostre o ramo, não escolha um: o aviso curto fica pendente
  em `regra_nao_medida:aviso_trabalhado_nao_cumprido`. Quando o empregado pediu
  a dispensa do cumprimento e comprovou novo emprego (Súmula 276 do TST), o
  caso não usa o ramo `empregador_dispensou_restante` e também fica pendente.
- Recusas de contexto: ramo em motivo ou modalidade que não é o dele, ramo que
  encurta o cumprimento com 30 dias cumpridos, e ramo sem comunicação com
  desligamento antes do fim do aviso ou sem falta declarada no mês.
- Cálculo novo exige gerar o pacote de novo e nova revisão; casos já gravados
  não mudam.

## Médias de rescisão obsoletas depois do deploy

Quando a resposta servida apresentar, os recibos de componentes de rescisão e
as consolidações de médias emitidos antes de cada mudança da regra de férias
ficam obsoletos, inclusive os emitidos depois da mudança anterior (2.6.11):
`get_case` mostra `OBSOLETO` e o recálculo da rescisão com consolidação recusa
com `medias_rescisao_obsoletas`. Não é defeito e não pede reinício: faça nova
qualificação dos componentes, nova consolidação das médias e novo cálculo,
depois geração, conferência e revisão. Casos aprovados ou entregues não mudam.
O roteiro está no domínio `ferias`.

## Acrescentar ou trocar uma parcela no mapa de rescisão da empresa

Use quando a empresa já tem uma seleção de `rescisao_rubricas` com `mapa`
embutido e só uma ou poucas parcelas de `mapa.parcelas_do_mes` precisam entrar
ou mudar. Não reenvie o mapa inteiro nem use caminho indexado
(`rescisao_rubricas[0]...`), que volta `forma_incompativel`.
Este patch só aceita `operations` e não altera a política de arredondamento;
para ela, veja "Trocar só a política de arredondamento do mapa".

1. Chame `get_client_config(cliente_slug)` e confira que a resposta tem
   `termination_map_patch_transport`. Se a chave faltar, o servidor ainda não
   oferece o patch: use a escrita da seleção inteira. Anote `doc_hash` e, em
   `documento.empresas[<código>].rescisao_rubricas`, o `group` e o
   `vigente_desde` exatos da seleção que cobre a data de desligamento. Copie
   os dois da configuração, sem aproximar.
2. Monte `alteracoes`:
   ```json
   {
     "schema_version": "loki.company-termination-map-patch/1",
     "company_code": "{{CODIGO_EMPRESA}}",
     "selector": {"group": "{{GRUPO}}", "vigente_desde": "{{AAAA-MM-01}}"},
     "operations": [
       {"action": "add", "parcela": {
         "codigo": "{{CODIGO_RUBRICA}}", "rotulo": "{{ROTULO_DA_FICHA}}",
         "natureza": "provento|desconto", "disposicao": "por_tributo",
         "incidencias": {
           "inss": {"efeito": "adicionar|reduzir|sem_efeito", "fonte": "{{FONTE}}"},
           "fgts": {"efeito": "...", "fonte": "{{FONTE}}"},
           "irrf": {"efeito": "...", "fonte": "{{FONTE}}"}
         }}}
     ],
     "confirmacao": {"expected_hash": "{{CONFIG.doc_hash}}"},
     "proveniencia": {"field_sources": {"empresas[{{CODIGO_EMPRESA}}].rescisao_rubricas": {"kind": "declaration", "reference": "{{REFERENCIA}}", "locator": "{{LOCALIZADOR}}"}}}
   }
   ```
   `add` só aceita código que ainda não está no mapa, e a parcela entra no fim
   da lista. `replace` só aceita código presente e troca a parcela inteira:
   mande todos os campos dela, não só o que mudou. Um código aparece uma vez
   só por declaração. Os campos da parcela seguem o mesmo schema do mapa
   (`inline_map_schema` em `termination_rubric_catalog`). A incidência de cada
   tributo vem da ficha ou do DP com a fonte. Não presuma incidência.
3. Chame `validate_client_config` com `cliente_slug`, `expected_hash` igual ao
   mesmo `doc_hash`, `sobrescrever: true` e `alteracoes`. Espere `VALIDO` com
   `caminhos_alterados: ["empresas[<código>].rescisao_rubricas"]`. Se vier
   `parametro_de_gate_com_evidencia`, acrescente
   `confirmacao.evidence_gate_paths` com esse caminho e a `human_message` da
   operadora no apply.
4. Chame `apply_client_config` com os mesmos argumentos mais `motivo`. Releia a
   versão e o `doc_hash`.
5. Recusas (`cliente_config_invalida`, campo `erros`):
   - `termination_patch_selector_missing`: grupo ou início não conferem.
     Releia a configuração.
   - `termination_patch_embedded_map_required`: a seleção só nomeia um grupo
     do catálogo. Grave antes uma seleção com `mapa` (o catálogo aceita
     `herda` mais as parcelas).
   - `termination_patch_parcel_exists`: use `replace`.
     `termination_patch_parcel_missing`: use `add`.
   - `rescisao_parcela_duplicada` em `operations`: o mesmo código foi
     declarado duas vezes.
   - `cliente_config_versao_desatualizada`: outra escrita chegou antes.
     Releia e refaça a prévia.
6. Efeito nos casos: os casos da empresa recebem `cliente_config_alterada`,
   como em qualquer mudança de mapa. A rescisão cujo desligamento cai na
   vigência alterada perde o cálculo corrente. Recalcule pelo fluxo normal:
   sem a parcela nova, o resultado é o mesmo. Casos em outras vigências não
   mudam.

## Método do Domínio na rescisão (opt-in por empresa e vigência)

Quando o contrato servido apresentar, a política
`arredondamento_proporcionais` do mapa de rubricas da empresa aceita opções
que reproduzem o método do Domínio. Quem não declara nada não muda nada.
Declare só quando a operadora tiver medido o método contra TRCTs do Domínio
daquela empresa, e cite a medição em `fonte`. A política fica em
`empresas[<codigo_dominio>].rescisao_rubricas[].mapa.arredondamento_proporcionais`,
gravada com a expectativa de versão do cadastro (para trocar só a política,
use o patch da seção seguinte):

```json
"arredondamento_proporcionais": {
  "tipo": "por_componentes",
  "arredondamento": "half_up",
  "escopos": ["ferias_proporcionais_indenizadas", "ferias_vencidas_indenizadas",
              "ferias_em_dobro_indenizadas", "ferias_aviso_indenizado"],
  "metodo_ferias": "valor_dia_6_casas",
  "terco": "por_parcela",
  "saldo": "valor_dia_6_casas",
  "medias_por_bloco": true,
  "fonte": "Medição da operadora: N de N TRCTs do Domínio conferidos (referência)"
}
```

- Cada opção é independente: omita a que não foi medida.
  `metodo_ferias: valor_dia_6_casas` calcula as férias por componente pelo
  valor-dia com seis casas e exige ao menos um escopo de férias.
  `terco: por_parcela` arredonda o terço de cada rubrica e soma, e exige os
  quatro escopos de férias. `medias_por_bloco: true` exige escopo de férias
  (seção seguinte) e não se liga sem conferência com a DP. O aviso indenizado fica fora: não foi medido.
- As férias por componente exigem `medias_variaveis[].componentes` nas médias
  de férias; sem isso o bloco fica pendente, como antes.
- `saldo: valor_dia_6_casas` exige a convenção
  `convencoes.dias_do_mes: trinta_fixo` da empresa (ou do cliente, se a
  empresa não declarar). Sem ela, `validate_client_config` e
  `apply_client_config` recusam com
  `rescisao_saldo_valor_dia_exige_trinta_fixo` em
  `empresas[<codigo>].rescisao_rubricas`. Não troque a convenção para
  contornar: ela é regra da DP; pergunte à Rafa. Se um caso ainda chegar com
  divisor diferente de 30, o Loki retém o saldo com
  `saldo_valor_dia_exige_mes_comercial`: não altere `dias_no_mes` do caso e
  relate o problema.
- Cálculo com opção traz `calculator_version` com `+metodo-dominio-v1`.
  Casos já calculados não mudam; trocar a política invalida o cálculo
  corrente, que precisa ser recalculado, gerado e conferido de novo.
- O Loki não confere a fonte; a conferência do pacote contra o Domínio
  continua sendo da harness e da operadora.

## Trocar só a política de arredondamento do mapa

Quando `get_client_config` anunciar `termination_map_policy_patch_transport`,
ligue, desligue ou troque as opções de `arredondamento_proporcionais` (seção
anterior) sem reenviar `rescisao_rubricas` inteira. Uma chamada leva várias
empresas e grava uma única versão do cadastro. Se a chave não for anunciada,
avise a operadora que o servidor ainda não tem o patch. Não tente o caminho
indexado (`rescisao_rubricas[0]...`), que volta `forma_incompativel`.

1. Em `get_client_config`, anote o `doc_hash` e, de cada empresa, o `group` e
   o `vigente_desde` exatos das seleções que vão receber a política. Leia
   também a `mapa.arredondamento_proporcionais` atual de cada uma delas. **A
   política declarada substitui a atual inteira:** repita nela os `escopos`,
   a `fonte` e as opções que devem continuar ligadas. Opção omitida fica
   desligada. Todas as seleções indicadas de uma empresa recebem a mesma
   política; para manter políticas diferentes, faça uma chamada por política.
2. Monte `alteracoes`, com uma entrada por empresa em `companies`:
   ```json
   {
     "schema_version": "loki.company-termination-map-policy-patch/1",
     "companies": [
       {
         "company_code": "{{CODIGO_EMPRESA}}",
         "selectors": [{"group": "{{GRUPO}}", "vigente_desde": "{{INICIO_ISO}}"}],
         "policy": {"arredondamento_proporcionais": {
           "escopos": ["ferias_proporcionais_indenizadas", "ferias_vencidas_indenizadas",
                       "ferias_em_dobro_indenizadas", "ferias_aviso_indenizado"],
           "fonte": "{{FONTE}}",
           "metodo_ferias": "valor_dia_6_casas",
           "terco": "por_parcela",
           "saldo": "valor_dia_6_casas"
         }}
       }
     ],
     "confirmacao": {"expected_hash": "{{CONFIG.doc_hash}}"}
   }
   ```
   `fonte` é obrigatória. As regras são as da seção anterior: `terco:
   por_parcela` exige os quatro escopos de férias, e `saldo:
   valor_dia_6_casas` exige `dias_do_mes: trinta_fixo` na empresa (senão vem
   `rescisao_saldo_valor_dia_exige_trinta_fixo` no caminho dela). Não mande
   `medias_por_bloco`: ela continua desligada sem conferência com a DP. O
   patch não pede `parcelas_do_mes`: parcelas, caixas e tributos do mapa não
   são reenviados nem alterados.
3. Chame `validate_client_config` com `cliente_slug`, `expected_hash` igual ao
   `doc_hash`, `sobrescrever: true` e `alteracoes`. Proveniência e gate usam o
   caminho `empresas[<código>].rescisao_rubricas` de cada empresa. A prévia
   devolve `termination_policy_preview`, uma linha por empresa e seleção.
   **Mostre à operadora, antes do apply:**
   - opções ligadas, desligadas e alteradas (`opcoes_ligadas`,
     `opcoes_desligadas`, `opcoes_alteradas`);
   - escopos adicionados e removidos (`escopos_adicionados`,
     `escopos_removidos`);
   - se a fonte muda (`fonte_trocada`);
   - se seleções com políticas diferentes serão unificadas
     (`politicas_distintas_unificadas`).

   Se algo que seria desligado ou removido não era a intenção dela, refaça a
   declaração.
4. Só com a prévia `VALIDO` e o aceite dela, aplique a mesma proposta em
   `apply_client_config`, com `motivo`. Se houver gate de evidência, declare
   em `confirmacao.evidence_gate_paths` os caminhos
   `empresas[<código>].rescisao_rubricas` devolvidos e a `human_message`
   aceita pela operadora. `remover` não combina com o patch
   (`termination_policy_patch_remove_incompatible`).
5. Recusas: qualquer recusa recusa o pedido inteiro, sem gravar. Nas recusas
   de seleção (`termination_patch_selector_missing`,
   `termination_patch_embedded_map_required`,
   `termination_patch_company_not_unique`) e de `trinta_fixo`, o caminho
   indica a empresa. Erro de formato da política volta como
   `companies[*].policy.arredondamento_proporcionais` (`value_error`): confira
   a política de cada empresa e refaça a prévia.
6. Efeito nos casos: só os casos abertos cuja fatia mudou (cliente mais a
   empresa do caso) recebem `cliente_config_alterada`, um por versão. A
   rescisão cujo desligamento cai na vigência alterada perde o cálculo
   corrente; recalcule pelo fluxo normal. As outras vigências mantêm o
   cálculo.

## Médias com seis casas e por bloco de empresa

Quando o contrato servido apresentar:

- **Seis casas.** Se o original do Domínio mostra a média da categoria com
  mais casas que centavos, declare em `medias_variaveis[].componentes` os
  centavos (como hoje) e também `horas_micros`, `valor_micros` e
  `vantagens_micros`, em milionésimos de real (R$ 30,125003 → `30125003`).
  Cada micros precisa arredondar para os centavos declarados; senão o Loki
  recusa com `componentes_media_micros_incoerente` e o nome do campo
  (`ctx.campo`). Corrija a transcrição; não ajuste os centavos. Médias
  importadas (`ImportedFinalAverage`) aceitam os mesmos campos na declaração
  estruturada (recusa `imported_average_micros_incoerente`); a carga por CSV
  ainda não tem colunas de micros. Os micros só têm efeito com
  `metodo_ferias: valor_dia_6_casas`, e só nas férias.
- **Por bloco.** Quando a média de férias vier apurada por empresa do grupo
  (blocos separados no Domínio), declare uma entrada por bloco com `bloco`
  igual à referência da empresa (por exemplo, o código Domínio dela) e a
  mesma `origem` e `escopo`. O formulário de fatos de `medias_variaveis`
  passa a trazer o campo `bloco`. Para o Loki ratear e arredondar cada bloco
  separadamente, a política precisa de `medias_por_bloco: true`, com `fonte`
  citando a medição; sem a opção, os blocos somam como uma média só. O 13º
  não usa blocos nem micros.
- **Regra da DP (18/11/2026): o Domínio soma as médias.** A DP informou que o
  Domínio soma as médias de todas as empresas do grupo, sem separar por
  empresa, em férias e no 13º. Não ligue `medias_por_bloco` sem conferência
  com a DP: o padrão é enviar uma média por `origem` e `escopo`, com a soma
  das empresas, sem `bloco`. A opção continua disponível só se a DP pedir uma
  exceção.

## Simulação de rescisão

Antes de simular, confira o estado histórico da origem: compare o
`state_hash` de `get_case_historical_state` com o da seleção do caso, ou leia
`selection_matches_current_state` (agora também para pessoa). Se vier
`false`, a seleção do caso real está desatualizada e a simulação padrão será
recusada (`historical_state_stale`). O caminho sem mexer no caso real é a
simulação com o estado histórico atual (seção seguinte). Reiniciar o caso
real é decisão da operadora, nunca um passo para viabilizar a simulação.

- Copie para a hipótese todas as chaves de topo da origem (`get_case`),
  inclusive as que vierem `null`: `origem`, `origem_ref`,
  `shadow_scenario_id`, `occurrence_ref` e `shadow_termination`. Omitir uma
  chave dá `identity_changed`; o Loki não trata chave ausente como nula.
- Em `field_sources`: com `kind=declaration`, o `locator` é
  `$.payload.<caminho da folha>` (por exemplo
  `$.payload.dados_rescisao.salario_base_cents`). Com basis `derived` ou
  `reported`, ou com kind `harness`, preencha `foundation`.
- Recusa `operational_context_changed` traz `subreason` (lista fechada em
  `get_process_contract(...).version_refusal_subreasons`):
  `historical_state_stale` (os fatos mudaram depois da seleção),
  `historical_state_pin_missing` ou `historical_state_window_pin_missing` (o
  pin do histórico sumiu) e `canonical_anchor_changed` (parta de uma captura
  nova). Nos três primeiros, no caso real, o caminho é reselecionar o estado
  na origem com `apply_historical_state`. Com `historical_state_stale`,
  quando isso não é possível (caso já calculado ou em `aguardando_revisao`),
  simule com o estado atual (seção seguinte). Sem
  `subreason`, a recusa vem de outra origem (deduções, frescor de férias e
  13º): leia o `reason` e relate se não houver caminho.

## Simulação com o estado histórico atual

Use quando a simulação voltou `operational_context_changed` /
`historical_state_stale` e o caso real não pode ser reiniciado (por exemplo,
está em `aguardando_revisao`). Antes, consulte `get_case_historical_state` do
caso real para ver o estado atual que será usado. Repita o `create_case` da
simulação com `payload.simulation.historical_state: "current"` e uma
`simulation_ref` **nova**: a mesma referência com outra base é recusada com
`simulation_intent_conflict`. Sem o campo (ou com `selected`), nada muda: a
simulação usa a seleção do caso real, como antes. O opt-in só vale em
simulação; num caso real é recusado com `parameters_invalid`.

- **O que muda e o que não muda.** A simulação usa o estado atual só para si.
  Não renova a seleção do caso real nem grava nada nele (seleção, pin,
  evento, versão ou snapshot); o caso real continua recusando
  `historical_state_stale` até a seleção ser renovada lá. A simulação
  continua sem efeito e não aprovável. Fontes `ONBSRC-*` de um upload novo do
  histórico entram nesta simulação sem pin no caso real.
- **Limite:** fontes `CPH-*` de folha fechada nova ainda não entram. Um fato
  de folha fechada que o caso real nunca pinou recusa com
  `source_document_missing`; não há contorno pela simulação.
- **`historical_state_basis`** (em `simulation` de `get_case`, das listas, do
  dossiê e em `get_case_version`): o `state_hash` usado, o
  `selected_state_hash` do caso real, `differs_from_selection`,
  `history_consumed` e as fontes congeladas. A simulação já nascida não muda
  se o histórico mudar depois.
- **Ressalvas** (`notices`, todas as páginas do PDF e o recibo). Repasse-as à
  operadora sempre que mostrar números da simulação: eles não valem para o
  caso real até a seleção ser renovada lá.
  - "ESTADO HISTÓRICO ATUAL, DIFERENTE DO SELECIONADO NO CASO REAL" ou "IGUAL
    AO SELECIONADO NO CASO REAL".
  - "HISTÓRICO NÃO CONSUMIDO NO CÁLCULO DESTA SIMULAÇÃO"
    (`history_consumed: false`): o caso não tem qualificação que use o
    histórico; os números são os de uma simulação sem o opt-in.
  - "QUALIFICAÇÕES DO HISTÓRICO PERTENCEM À SELEÇÃO ANTERIOR: OPERANDOS
    QUALIFICADOS PENDENTES".
- **Qualificações do caso real pertencem à seleção anterior** (faltas do
  aquisitivo, médias qualificadas ou importadas, prazo de experiência, saldo
  de FGTS e avos e faltas do 13º). Com o estado atual esses operandos ficam
  pendentes e a simulação sai `completed_partial`;
  `simulation.pending_qualifications` traz
  `historical_qualification_context_incompatible` com a ação "renovar seleção
  e qualificação no caso real". Não é erro dos dados nem defeito: para
  simular com essas qualificações no estado atual, é preciso renovar a
  seleção e qualificar de novo no caso real, decisão da operadora ou da DP.
  Fatos que não dependem de qualificação (dependentes de IRRF, por exemplo)
  entram.
- **Recusas** (`operational_context_changed`, `subreason` fechado):
  - `historical_state_not_selected`: o caso real nunca teve seleção; o
    opt-in substitui uma seleção, não a cria.
  - `historical_state_pin_missing` ou `historical_state_window_pin_missing`:
    o histórico atual não sustenta um pin (hash ou fatos incompletos).
  - `historical_state_source_incompatible` (novo): uma fonte do histórico
    está ausente, alterada ou ilegível; confira o cadastro histórico e a
    fonte.
  - `historical_settlement_bound_to_selection` (novo; antes chegava como
    `simulation_operation_failed`): a liquidação foi qualificada na seleção
    anterior; renove a seleção e a qualificação no caso real.
- `simulation_source_changed`: o histórico mudou durante a criação; repita
  com outra `simulation_ref`.

## Simulação de quem segue empregado, sem caso de origem (2.10.1)

Vale quando `get_process_contract("rescisao").simulation.versions` trouxer
`loki.termination-simulation-create/2`. Sem o sinal, a única porta é a v1 das
seções acima. A v1 continua valendo (`source_case_id`): o booleano
`requires_source_case: true` é o da v1 e o valor por versão está em
`requires_source_case_by_version`. Só `create_case` recebe o marcador; não há
ferramenta nova nem Refresh.

1. `get_company_employee_history` com `as_of` igual à data de desligamento
   hipotética; guarde o `history_hash`.
2. `create_case` com o `CasePayload` completo de rescisão, `preparation_only`
   padrão, e `payload.simulation = {schema_version:
   "loki.termination-simulation-create/2", source: {kind: "employee",
   funcionario_id, expected_history_hash}, simulation_ref, field_sources}`. O
   `expected_history_hash` é o `history_hash` do passo 1.
3. `field_sources` só aceita **declaração**: um item por folha do payload, com
   `kind=declaration` e `locator = $.payload.<caminho da folha>`. Não mande
   `documentos_origem`; fonte documental ou `harness` exige caso e é recusada
   (`field_source_invalid`).
4. `run_prepared_case_workflow` no id da simulação.
5. `get_case_version` e os artefatos (`get_case_version_artifact`).
6. O PDF e o recibo saem como SIMULAÇÃO e dizem que o histórico não entrou no
   cálculo (`BASE HISTÓRICA: ESTADO ATUAL DO VÍNCULO NO CORTE SIMULADO` e
   `HISTÓRICO NÃO CONSUMIDO NO CÁLCULO DESTA SIMULAÇÃO`). Informe isso à
   operadora ao mostrar os números.

Recusas:

- `simulation_history_changed`: o histórico mudou; releia
  `get_company_employee_history` e repita com o hash novo.
- `simulation_employment_not_active`: o vínculo já tem rescisão ou saída
  efetiva; não há o que simular por este caminho.
- `simulation_source_not_supported`: vínculo inexistente, de outra empresa ou
  sem escopo `consultar` e `operar_casos` de rescisão; mesma recusa para os três.

**Descarte.** Só a pessoa descarta, com `cancel_case` (decisão humana, com
`expected_snapshot` e `human_message`). A rotina técnica não cancela. A
`simulation_ref` fica ocupada: repetir a criação devolve `simulation_cancelled`
e `run_prepared_case_workflow` devolve `BLOCKED/simulation_cancelled`. Para uma
nova hipótese, use outra `simulation_ref`.

**O que a simulação não faz.** Não é aprovada, entregue nem publicada, e não
cria funcionário, evento de vínculo ou pin. Toda simulação (v1, v2 e as
anteriores, inclusive as de 18/11) fica isolada: não entra no 13º, no
fechamento do mês nem na conciliação. A resposta traz `source_employee_id` e
`source_history_hash` no lugar de `source_case_id` e `source_snapshot`.

## Desligamento gravado pelo onboarding

Rescisão vinda do cadastro de onboarding que não aconteceu (o contrato segue
ativo) se desfaz pela revogação auditada, no domínio `alteracao_cadastral`
("Revogar desligamento gravado pelo onboarding"). Não use esse caminho para
desfazer rescisão calculada por caso: essa segue o cancelamento do caso. Se
houver caso de rescisão ou aviso de rescisão do próprio vínculo em aberto, a
revogação só segue com a confirmação da operadora
(`revoga_com_rescisao_aberta: true`). Uma rescisão verdadeira na mesma data da
revogada não entra pelo onboarding (`onboarding_termination_fact_revoked`):
use o caso de rescisão.


## Confirmar o desligamento efetivo: `confirm_termination` (2.12.0)

Vale quando o catálogo da conta mostrar `confirm_termination` (backend #435,
ADR-042). **Ferramenta nova: exige Refresh do conector e conversa nova**; sem
ela, pare e avise a Ana. A aprovação pelo chat (`registrar_decisao_chat`) é só
documental e **não grava o vínculo**: sem esta confirmação a folha e o 13º
seguem considerando a pessoa. Quando a aprovação é pelo chat, só esta ferramenta grava o
desligamento (a aprovação fora do chat continua gravando o vínculo).

**Quem pode.** Só pessoa provisionada com `confirmar_rescisao`, concedida pela
Ana por empresa e processo `rescisao` (`preparar_autorizacao`/`aplicar_autorizacao`).
Rotina e conta técnica não a recebem; `confirmar_admissao` não a substitui.

**Quando.** Rescisão conferida pela operadora, com o fato do desligamento
comprovado por anexo do caso (recibo do S-2299 ou TRCT, conferido por você).
O caso tem de estar em `aguardando_revisao` (depois de `prepare_case_review`):
**confirme antes de aprovar**. Caso aprovado pelo chat recusa
`estado_nao_confirmavel`, e em preparação também.

**Como.** `get_case` e copie `termination_confirmation_snapshot`. Chame
`confirm_termination` com `declaration`: `case_id`, `funcionario_id`,
`empresa_cnpj`, `cpf`, `data_desligamento` (igual à do caso e não futura),
`expected_snapshot` (o snapshot acima), `reference` (idempotência),
`termination_occurred: true`, `human_message` (transcrição literal da mensagem
da operadora) e `source` (`document_id`, `content_hash` e `locator` do anexo; o
Loki confere que o anexo existe e é íntegro, não o conteúdo). O efeito é um
evento `rescisao` com `data_efeito = data_desligamento` e origem
`confirmacao_desligamento`: a folha da competência seguinte deixa de considerar
a pessoa, e o mês do desligamento ainda a conta. **Não atesta envio ao eSocial,
não aprova pacote e não publica.** Repetir a mesma `reference` e declaração
devolve o registro original (`created: false`). Desligamento já declarado pelo
onboarding na mesma data é reconhecido sem evento novo (`already_present: true`).

**Recusas** vêm com `status: BLOCKED`, o código `confirmacao_desligamento_recusada`
e um `reason` fechado, entre eles: `exige_pessoa_provisionada`,
`estado_nao_confirmavel`, `caso_cancelado_ou_rejeitado`,
`caso_sem_data_desligamento`, `data_desligamento_divergente_do_caso`,
`identidade_incompativel`, `desligamento_futuro`,
`desligamento_anterior_a_admissao`, `snapshot_desatualizado` (releia o
`get_case`), `fonte_invalida`, `fonte_integra_indisponivel`,
`referencia_conflitante`, `referencia_sem_efeito_vigente` (o fato foi
compensado: use outra `reference`), `desligamento_ja_confirmado`,
`desligamento_ja_registrado` (aprovação legada anterior),
`desligamento_divergente_no_historico` (onboarding em outra data: corrigir é
`revoke_onboarding_termination`) e `exige_rescisao_operacional` (simulação não
confirma). A mesma `reference` com declaração diferente é `referencia_conflitante`.

**Desfazer e compensar.** Uma confirmação errada se desfaz pelo caso: voltar o
caso à preparação (`registrar_decisao_chat` com `ajustar`) ou cancelá-lo grava
`evento_revertido` uma só vez e o vínculo volta a valer. Corrija a data no
caso, leve de novo à revisão e confirme com **outra** `reference`. **Cancelar um
caso com confirmação vigente exige `confirmar_rescisao`**. Pelo conector HTTPS, sem
ela o cancelamento volta `{status: BLOCKED, code: lifecycle_authorization_revoked}`
(a autorização barra antes do serviço, que diria `case_lifecycle_action_refused` com
`cancelamento_exige_confirmar_rescisao`): nesse contexto significa "falta a concessão
`confirmar_rescisao`"; peça a concessão à Ana e não repita;
reiniciar o caso com a confirmação vigente continua recusado
(`restart_requires_effect_reconciliation`). Depois da compensação o reinício não
é mais bloqueado por ela.

Descrição da ferramenta no catálogo diz "ou aprovado pelo chat": vale o
comportamento acima, só `aguardando_revisao`.

## Razão social e saldo de férias inexistente na rescisão (2.12.0)

- A razão social do caso é conferida de novo contra o cadastro vigente na geração: natureza
  jurídica diferente recusa com `razao_social_natureza_juridica_divergente`;
  só o tipo societário diferente gera o aviso `razao_social_tipo_societario`.
  Regras em `admissao` ("Razão social da empresa").
- Saldo de férias que a carga histórica gravou com aquisitivo que não existe é
  retirado por `retire_onboarding_vacation_balance` (`alteracao_cadastral`).
  **Nunca declare esses períodos na rescisão**, retirado o saldo ou não.

## Insumo novo do cliente com o caso em revisão (rotina, 2.10.0)

Vale quando `meu_acesso` mostrar `atualizar_por_insumo_do_cliente` na empresa e
em `rescisao` (a Ana concede por `preparar_autorizacao`; sem ela, pare e avise
a Ana). O gatilho é um insumo novo do cliente com o caso em
`aguardando_revisao`. A capacidade não decide: aprovação, efeitos, entrega e
cancelamento seguem com pessoa.

1. `get_case` e copie o `correction_snapshot`.
2. `restart_case` com `expected_snapshot=correction_snapshot`,
   `preparation.mode=replace_process_inputs` (sem `preserve_imports`),
   `preparation.request_ref = sha256-<impressão do insumo>` (`sha256-` e 64
   hex minúsculos, calculada por você sobre o insumo novo) e `human_message`
   com os campos que mudam e o motivo.
3. `receive_case_data` com os dados completos e siga o fluxo normal; o pacote
   novo exige nova revisão e novo aceite humanos.

Pare e avise a Ana, sem insistir, se vier
`restart_requires_effect_reconciliation`,
`client_input_restart_requires_review_state`,
`client_input_restart_scope_refused`, `client_input_request_ref_invalid`,
`client_input_restart_grant_origin_unrecorded`, `capacidade_nao_concedida` ou
`caso_inexistente_ou_nao_autorizado`. Não repita em laço: o replay com o mesmo
`request_ref` é idempotente. A data de admissão (vínculo) não muda por esse
caminho: retificação de data e cancelamento ficam com a pessoa.

## Catálogo de rubricas v2 e `get_dp_capabilities` como índice (2.11.0)

Vale quando o catálogo servido trouxer `schema_version` igual a
`loki.termination-rubric-catalog/2` (Project-loki #426). Sem Refresh: nenhuma ferramenta
nem schema mudou; só o conteúdo das respostas encolheu. O catálogo vem em
`termination_rubric_catalog` de `get_process_contract("rescisao")` e de
`get_company_onboarding_contract`.

- **Tabelas por conteúdo.** `parcel_table`, `mapping_table`, `tax_mapping_table` e
  `caixa_table` guardam cada parcela, mapeamento, mapeamento de tributo e caixa uma
  vez, com id por conteúdo: `p`, `m`, `t` ou `c` mais os 12 primeiros hex do sha256 do JSON
  canônico da entrada. Ids iguais denotam conteúdo idêntico em todos os grupos.
- **Grupos.** Cada item de `groups[]` traz `group`, `herda`, `parcel_ids`, `mapping_ids`,
  `tax_mapping_ids`, `caixa_ids`, `resolved_other` e `resolved_map_hash`, além do
  `selection_example`. Não procure a parcela dentro do grupo: ele só aponta ids.
- **Reconstrução.** Leia o campo `reconstruction` do próprio catálogo. Em resumo: o mapa
  resolvido de um grupo é o `resolved_other` mais, em `parcelas_do_mes`, `mappings`,
  `tax_mappings` e `caixas_fora_do_modelo`, a lista, na mesma ordem, de `tabela[id]` para
  cada id de `parcel_ids`, `mapping_ids`, `tax_mapping_ids` e `caixa_ids`. O
  `resolved_map_hash` é o sha256 do JSON canônico (chaves ordenadas) desse mapa.
  `catalog_hash` e `resolved_map_hash` cobrem o mapa resolvido completo, iguais aos da v1.
- **Uso.** Para conferir a incidência de uma rubrica, reconstrua o grupo da empresa e da
  data de desligamento e leia a parcela ali. O envelope de `validate_client_config` e
  `apply_client_config` (`add`, `replace`, `selector`, `inline_map_schema`,
  `inline_extension_schema`) não mudou.
- **`get_dp_capabilities` é só índice.** Cada linha com `standalone_available` traz
  `contract_tool` (`get_process_contract`) e `contract_hash`; o contrato inteiro do
  processo vem de `get_process_contract(<processo>)`. Guarde o `contract_hash` do contrato
  que você leu: quando ele mudar em `get_dp_capabilities`, releia o contrato antes de
  montar o envio. Não espere schema, seções nem catálogo dentro de `get_dp_capabilities`.

## Categoria eSocial que não é de empregado no cadastro (2.13.0)

Vale quando a recusa abaixo aparecer. Quem tem, no cadastro do vínculo,
`categoria_esocial` que não começa com `1` (723 sócio com pró-labore, 901
estagiário) não passa por rescisão no Loki: `create_case` recusa antes de gravar, com
`codigo` `categoria_sem_regime_clt` (`mode` `HUMAN_DECISION`; `proxima_acao`: conduzir
o processo fora do Loki ou, se a categoria cadastrada estiver errada, corrigi-la por
alteração cadastral, com a data de efeito do início da pessoa naquela categoria
(domínio `alteracao_cadastral`), e recriar o caso). O caso não é criado. A simulação de rescisão recusa pela mesma regra, com `code` `case_simulation_refused` e `reason` `categoria_sem_regime_clt`, lendo a competência do caso de origem ou, na simulação sem caso de origem, a do desligamento hipotético. Limites: vale só na
criação (categoria cadastrada depois de o caso existir não o derruba, e o reenvio de
caso já existente não a relê); `vinculo_nao_clt_*`, de `contrato.dados.categoria_vinculo`,
vem antes. A categoria é lida na competência do próprio processo: a do caso; senão
a data de desligamento de `dados_rescisao`, se vier no pedido de criação; sem nada disso, o mês corrente
(America/Sao_Paulo). Sem vínculo conhecido (mesma empresa, CPF e admissão), sem
categoria declarada ou com erro de leitura, o caso segue. Detalhe e declaração da
categoria: `folha_mensal` e `alteracao_cadastral`.

## Reinício em lote autorizado por correção (rotina, 2.14.0)

Vale quando a proprietária repassar `authorization_id` (`rst-` e 32 hex) e o
`expected_snapshot` de cada caso, após uma correção `CL-N`. A rotina (`consultar` e
`operar_casos` em `rescisao`; `atualizar_por_insumo_do_cliente` nem é exigida nem basta)
reinicia **uma vez cada caso listado**, em `aguardando_revisao`, de forma simples, com o
payload preservado (sem `replace_process_inputs`): `receive_case_data(case_id,
request={schema_version: "loki.case-restart-authorized/1", authorization_id, case_id,
expected_snapshot, human_message})`, com `case_id` igual ao argumento, `expected_snapshot`
igual ao repassado e `human_message` que nomeia o `CL-N`. O recibo traz
`requires_case_data`: `true` em caso legado (reenvie os dados pelo `receive_case_data`
comum) e `false` em `structured-v1`. Depois, siga o fluxo normal
(`run_prepared_case_workflow`); o pacote novo exige nova revisão e novo aceite humanos.
Repetir o mesmo pedido devolve o recibo com `replayed: true`: releia `get_case`; em
`em_preparacao`, o reinício desta autorização valeu e o fluxo normal segue; se o caso já
voltou à revisão, não há segundo reinício: pare e avise a proprietária (autorização nova;
o item consumido não bloqueia). Entre a autorização e a execução, `prepare_case_review` pela primeira vez, `record_package_checks` e decisão registrada no caso gravam evento e invalidam o item: a execução devolve `case_snapshot_changed`; pare e avise a proprietária, sem mandar o snapshot atual (dá `correction_restart_snapshot_mismatch`). Ler caso, dossiê e documentos não invalida.
Não rode a rotina de correção durante uma janela de publicação do executor anterior: o
reinício muda o censo de eventos e a publicação recusa.

**Recusa** (`BLOCKED` com `code`; nada é consumido e o item segue aberto; não repita em
laço). Corrija sozinha só `correction_restart_snapshot_mismatch` (reenvie o snapshot do
recibo da concessão, não o atual do caso; se vier `replayed: true`, é o caso acima) e `correction_restart_message_requires_code` (a
mensagem nomeia o `CL-N`); nos limites diários (`correction_restart_authorization_daily_limit`
e `correction_restart_account_daily_limit`), espere o dia seguinte; `BUSY`
(`authorization_change_busy`): repita a mesma chamada. Em qualquer outro `code`
(`correction_restart_*`, `case_snapshot_changed`, `restart_requires_effect_reconciliation`,
`case_simulation_refused`, `lifecycle_authorization_revoked`) ou no erro de ferramenta
`caso_inexistente_ou_nao_autorizado` (sem escopo no caso), pare e avise a proprietária,
pela Caixa, com o código: a autorização aberta bloqueia uma nova do mesmo caso, e ela decide
entre revogar e autorizar de novo ou deixar o caso fora (o item fica aberto até vencer).
