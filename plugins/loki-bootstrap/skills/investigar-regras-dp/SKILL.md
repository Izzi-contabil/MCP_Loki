---
name: investigar-regras-dp
description: Use quando uma tarefa do Loki tiver fórmula, base, divisor, percentual, incidência ou histórico incompleto, divergência recorrente em holerites, ou precisar retomar uma regra investigada.
---

# Investigar regras e destravar tarefas do DP

Resolva a causa reutilizável durante a operação. Norma/ACT/CCT aplicável e
histórico suficiente podem qualificar uma regra sem export da configuração do
ERP. Pagamento observado também pode estar errado. Diferencie regra devida,
prática histórica e fato ocorrido antes de preencher a lacuna.

Use o acesso e os contratos atuais de [operar-loki](../operar-loki/SKILL.md).
Leia o [registro de qualificação](references/QUALIFICACAO.md) ao abrir ou retomar
uma investigação. Ele organiza evidências privadas, não cria campos no MCP.

## Decidir e avançar

| O que impede a tarefa | Próxima ação |
|---|---|
| Fato/competência sem fonte | Consultar cadastro/histórico e acervo autorizado, inclusive empregador anterior em transferência; registrar o alcance da busca. |
| Regra ou parâmetro derivável | Cruzar normas e holerites; explicitar incógnitas e hipóteses; testar observações que distingam alternativas. |
| Fonte conflitante ou regra refutada | Reter somente os resultados dependentes e investigar; preservar conflitos e decisões existentes. |
| Dado já gravado, cálculo não o usa | Conferir revisão, corte, seleção/pin e trace/recibo do executor antes de reenviar. |
| Contrato/motor não expressa a regra | Reproduzir o limite com entradas sintéticas e encaminhar correção de produto. |

1. **Enquadrar.** Concilie empresa, vínculo, categoria, território, competência
   e vigência. Consulte fontes primárias atuais e históricas pertinentes, ACT/CCT
   e aditivos, contrato e política empresarial comprovada. Código/rótulo de
   rubrica não define sua natureza nem a regra. Registre cláusula/página/edição,
   expressão, unidades, base, divisor, taxa, reflexos, arredondamento e exceções.
2. **Inferir.** Separe parâmetros desconhecidos de ocorrências desconhecidas.
   Use salários, quantidades e bases documentados como operandos; pagamentos
   são alvos de calibração. Compare candidatos em meses/pessoas com variação
   discriminante: reajuste, proporcionalidade, horas, afastamento ou transferência.
   Coincidência no centavo não identifica hipóteses equivalentes; procure a
   observação que as separa. Uma norma não comprova horas, faltas ou opção individual.
3. **Validar.** Registre documentos usados na inferência e congele a hipótese
   antes de abrir os reservados. Teste competências/pessoas e condições dentro
   do alcance proposto. Referência já vista é calibração; registre esse limite e
   busque controle ainda não usado. Havendo divergência, investigue entrada,
   regra, produto e referência, sem ajustar fatores ao pago. Sem evidência que
   discrimine, avance nas partes independentes e descreva a incógnita exata.
4. **Persistir e consumir.** Com evidência suficiente, autorização e schema
   expressável, prepare fatos/parâmetros pelos escritores vigentes e fontes de
   [WORKFLOWS.md](../operar-loki/references/WORKFLOWS.md). Use `get_process_contract` e `receive_case_data` para dados do caso,
   com `kind=rule` e `foundation` na fonte quando houver derivação; não apresente
   inferência como leitura documental. Confira preview,
   validação, escopo/vigência e revisão/hash; aplique, releia, selecione e observe
   o consumo real. Resposta perdida exige consultar estado antes de repetir.
5. **Retomar e encerrar.** Reexecute a tarefa afetada na versão corrente e
   confira artefatos/resultados independentes. Atualize a mesma investigação com
   fontes, configuração, testes e pendências; reutilize somente dentro do alcance.
   Contraprova nova exige suspender o uso da hipótese afetada, identificar seus
   consumidores e revalidar dependências; preserve o histórico e conflitos retidos.

## Corrigir o sistema enquanto opera

Fatos e configurações qualificados podem ser corrigidos pelas ações autorizadas
do MCP. Se faltarem schema/operador ou houver defeito reproduzido, prepare o
comportamento esperado, reprodução sintética, versão e tarefas afetadas. Use
[registrar-problema-loki](../registrar-problema-loki/SKILL.md) para o suporte
quando o envio estiver autorizado; mantenha o ID e confira o recibo. Sem esse
envio, preserve o diagnóstico para encaminhamento autorizado.

Se esta sessão também tiver checkout e autorização de desenvolvimento, siga
as instruções do projeto, implemente e teste a correção, revise e publique pelos
gates vigentes; depois confira o build servido e retome a tarefa. Caso contrário,
entregue a reprodução pronta e continue nas partes independentes. Relato enviado
não significa defeito corrigido. Não editar banco, container ou pins como atalho.

## Erros a evitar

- Pedir export por padrão: primeiro usar fontes e normas suficientes.
- Completar mês pelo total da equipe: é hipótese dependente da referência,
  não fato independente nem validação desse total.
- Repetir regra global por coincidência: limitar aplicação ao alcance validado.
- Reabrir conflito retido só porque outra parcela avançou: manter a retenção.
- Encerrar pelo anexo/relato: exigir releitura, consumo e resultado da retomada.

Instalar esta skill não amplia acesso nem autoriza alterar outro sistema,
agendamento, aprovação humana, pagamento ou transmissão.

Toda operação usa o conector HTTPS `https://loki.tominho.com/mcp`, com identidade, capacidades e escopo próprios da pessoa ou do executor. A harness lê, extrai, interpreta e prepara; envia parâmetros estruturados por JSON direto ou CSV tipado do contrato vigente; a proveniência detalhada é opcional. Originais permanecem na harness. Não restaure transporte operacional SSH/stdio nem empreste credencial humana à automação; o plugin não implementa transporte, autenticação ou renovação.

Se optar por preservar proveniência detalhada de um original sem enviá-lo, consulte `get_harness_source_contract()` no catálogo HTTPS. Quando oferecido, prepare `loki.harness-source/1` com `request_ref`, `reference` externa real, `content_hash` SHA256 declarado do original, `source_role=CLIENT_INPUT|HISTORICAL_SOURCE|OFFICIAL_REFERENCE`, `locator` e `foundation`; envie por `register_harness_source(case_id, request)` e releia por `get_harness_source(case_id, source_id)`. O recibo retorna `EXTSRC-...`, `kind=harness`, `source_kind=harness_manifest`, `content_hash`, `manifest_hash`, `manifest`, `original_archived=false` e `verification=authenticated_harness_declaration`. O Loki não verifica os bytes originais: registra a declaração autenticada da harness. Não anuncie download de original a partir de EXTSRC nem equivalência com documento arquivado. A fonte de cada campo usa `kind=harness`, `reference` igual ao ID EXTSRC retornado e o mesmo `content_hash`; não invente IDs ou altere hashes.

Fontes `kind=document` conservam o significado de documento já arquivado no Loki; `document.reference` seleciona uma fonte já registrada quando o contrato assim exigir. Caminho local, ID do Drive e hash isolado não são ID de fonte registrada. `kind=declaration` descreve somente uma declaração real com referência, localizador, fundamento e limites honestos. Não reclassifique documento como declaração para inventar uma qualificação, nem declare EXTSRC como DOC. A declaração informal autorizada do próprio request é válida quando a operação não exigir evidência específica. Se o consumidor ainda exigir anexação nova do original ou recusar o tipo harness, isso é lacuna contratual: preserve os dados preparados e peça adequação explícita da evidência estruturada pelo HTTPS, sem fabricar DOC nem enviar o original. Contrato indisponível e fonte insuficiente são pendências distintas.

`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. `kind=inference` e `kind=context` podem descrever inferência ou contexto sem hash e sem `foundation` obrigatório; preserve a justificativa quando disponível. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.


## Identificar rubricas nas perguntas ao DP

Antes de pedir validação de regra, base, incidência, classificação ou tratamento,
apresente cada rubrica como **nome legível da fonte (código exato da fonte)**.
Nome+código devem corresponder no mesmo namespace; rubrica ERP, verba TRCT e
alvo Loki não são equivalentes. Use contexto, catálogo, configuração ou histórico
atuais e autorizados, inclusive declaração humana real já disponível; preserve
referência e alcance consultáveis. Não exija DOC, EXTSRC ou hash por campo
universalmente.

Inclua empresa/grupo, processo e competência/vigência quando necessários para
desambiguar; vínculo individual somente quando a pergunta depender dele. Código
igual em outra empresa ou vigência não fornece nome global. Preserve o código de
exibição e os zeros à esquerda existentes na fonte; não acrescente zeros por
adivinhação nem altere a normalização interna de cálculo ou deduplicação.

Reutilize identificação e respostas já disponíveis. Se faltar nome, houver
conflito ou fonte retirada, faça consulta focal autorizada e conserve a pendência;
só a validação da regra dependente aguarda identificação. Não invente nome de
slug, exemplo de schema, semelhança numérica ou outro escopo. Continue nas partes
independentes; pergunte somente identificação ou alcance residual ainda não
respondido, dentro do ciclo vigente, sem nova menção ou repetição automática.

Uma dúvida útil por vez, com contexto mínimo. Não retire nomes nem ressalvas
indispensáveis para caber no limite de palavras; se o conjunto não couber,
encaminhe ao humano com o conteúdo completo, sem abrir novo ciclo automático.
Resposta do DP é fonte atribuída no alcance expresso; não vira parecer normativo,
autoridade humana da automação, mudança de dados/incidências, publicação ou
aceite operacional automático. Fala de terceiro e orientação prévia de IA não
ganham autoridade humana.

## Aproveitar o esclarecimento do DP

Separe a resposta por assunto e reutilize o histórico antes de perguntar.
Identificação existente não é pedida outra vez; pergunta citada não é resposta.
“Depende do cliente” encerra a busca de regra universal: preserve o alcance, a
vigência e a decisão residual. Prática relatada não é parecer normativo nem aceite
de operação. Encaminhe dados/procedimento para preparação da Ana, regra delimitada
como proposta de configuração e possível falha como triagem técnica, sem executar
alterações. No Slack, uma pergunta útil ou próximo passo claro, palavras comuns
e alvo60palavras; análise completa fica no Loki. Observe o limite conjunto de
três perguntas e o contato/ciclo realmente convidado no suporte nativo.

## Representação e respostas já disponíveis

Antes de investigar novamente uma regra, confira a resposta já persistida do
contato convidado e o estado da análise seguinte. Falha `agent_schema` não
transforma informação respondida em pergunta nova; o reprocessamento tem
contrato e autoridade próprios em `meu_acesso`.

No consumidor rescisório que oferecer `representacao`, distinga
`episodio_integral` de `faixa_pagador`. Intervalo já separado por responsável
não sofre outra retirada dos primeiros15dias. Essa representação não prova
concessão, espécie ou continuidade clínica. `retorno_episodio` é fato efetivo
separado do fim da faixa; sua ausência limita apenas o efeito dependente
conforme o contrato. Não adaptar automaticamente fontes históricas de outro
formato nem promover inferência contextual a confirmação.
