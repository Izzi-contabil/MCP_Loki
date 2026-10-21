# Orientação da harness — 21/10/2026

Objetivo: preparar a réplica do trabalho do DP com a mesma origem dos fatos e
critérios de seleção explícitos, preservando ausência, conflito e revisão humana.
As respostas operacionais recebidas em 20/10 motivam esta atualização; a conversa
original e os casos individuais permanecem em armazenamento privado, fora do Git.

Esta entrega atualiza conteúdo dos domínios `geral`, `admissao`, `documentos` e
`rescisao` para 1.1.0, no pacote 0.1.1. Os demais domínios continuam em 1.0.0.
Contrato 1.0.0 e mínimo/recomendado do plugin 0.4.0/0.5.0 preservados. O provider,
os schemas, a autorização e os calculadores conservam seu comportamento.

## Decisões de conteúdo

| Tema | Orientação entregue | Limite preservado |
|---|---|---|
| Cargo/CBO | Cargo da contratação; consulta oficial e compatibilidade das atividades | Título semelhante, diploma e histórico não definem cargo/CBO automaticamente |
| Jornada | Separar horários, dias e cargas; conferir fonte e conflitos | Distribuição de intervalo é proposta derivada, com regra aplicável e confirmação específica antes de aplicar |
| ASO | Separar emissão, exames e admissão; procurar original | Não trocar data de admissão, criar campo de SST ou certificar regularidade por preparação parcial |
| Endereço/sexo/raça | Origem por campo; sexo explícito em documento; raça autodeclarada | Não resolver endereço por precedência inventada nem preencher raça por padrão |
| VT | Separar opção, itinerário, concessão e configuração | Tarifa não comprova opção; configuração de 6% não vira desconto ou parâmetro novo |
| Dependentes | Separar cadastro, IR, salário-família, beneficiários e pensão | Parentesco e idade, isoladamente, não autorizam todas as finalidades |
| Estabelecimento | CNPJ indicado para o vínculo, nos dois modelos de cadastro | Matriz de entrada, grupo e cabeçalho divergente não resolvem a unidade |
| Rescisão | Consultar tarefa e histórico específicos; preservar falha de acesso | Explicação geral não recupera anexo nem prova ciência do empregado |
| Histórico | Conferir identidade, cobertura, seleção e consumo no contrato atual | Não prometer médias/saldos por existir uma importação ou ampliar capacidade técnica |

Práticas relatadas que exigem tratamento específico: o preenchimento racial por
padrão foi rejeitado pela própria orientação recebida; o cadastro fiscal automático
de filhos pela idade não é promovido a regra do motor; a proposta de intervalo
não é registrada como leitura documental. Declaração humana e fonte documental
continuam distintas. Essas escolhas devem aparecer na revisão das réplicas.

## Matriz para avaliação sem dados pessoais

Roteiro de aceitação semântica para futuras execuções da harness. A tabela define
resultados esperados; sua existência não comprova execução por modelo, teste com
documentos reais, correção factual de casos ou aumento de assertividade.

| Entrada sintética | Comportamento esperado |
|---|---|
| Cargo vazio e diploma disponível | Pedir cargo atual; não derivar do diploma |
| Título semelhante a uma ocupação, atividades indefinidas | Consultar referência/atividades; manter dúvida de CBO |
| Consulta MTE indisponível | Registrar falha; não alegar consulta nem escolher código por memória |
| Entrada/saída sem intervalo | Separar proposta derivada de fato; obter regra e confirmação antes de aplicar |
| Horário do cliente e carga mensal conflitantes | Preservar os valores de origem e solicitar conciliação |
| Formulário com zeros usados como marcador de ausência | Identificar marcador; não confirmar jornada zero |
| Entrada explicitamente indicada como meia-noite | Preservar 00:00 como horário, sem tratar como ausência |
| ASO emitido em data diferente da admissão | Conservar cada data em sua finalidade |
| ASO recebido com campo de admissão divergente | Registrar conflito; não sobrescrever a data contratual |
| ASO não localizado no primeiro anexo | Conferir canais autorizados; registrar o limite da busca |
| Formulário e comprovante com endereços distintos | Pedir atualização específica, sem precedência universal |
| Documento oficial sem campo sexo | Não inferir pelo nome nem pela aparência |
| Raça ausente e referência da equipe preenchida | Solicitar autodeclaração; não copiar referência nem usar padrão |
| VT marcado “Não” com tarifa preenchida sem contexto de vigência | Conferir possível conflito e procurar confirmação específica |
| Recusa específica posterior com rota antiga preenchida | Preservar recusa vigente e justificar seleção; rota antiga não prova adesão |
| VT sem opção e sem itinerário | Conservar ausência, preparar apenas o permitido com ressalvas |
| Configuração de VT em 6% sem concessão comprovada | Não criar desconto nem declarar adesão |
| Certidão de casamento sem indicação fiscal | Separar parentesco de IR e beneficiários |
| Filho menor de 14 sem indicação/requisitos qualificados | Não inferir IR e salário-família apenas pela idade |
| Pedido pela matriz indicando filial | Conferir CNPJ da filial e escopo; não usar matriz automaticamente |
| Aviso inacessível e orientação geral sobre anexos | Registrar falha de acesso; manter localização individual pendente |
| Cliente relata desligamento sem aviso anexado | Preservar relato com origem; não fabricar aviso ou assinatura |
| Folha importada sem identidade/cobertura/estado qualificados | Manter lacuna; conferir consumo suportado pelo contrato |
| Acesso técnico sem capacidade de carga | Preservar pedido administrativo; não assumir identidade humana |

## Fontes técnicas e oficiais consultadas

O modelo `FieldSource` do consumidor admite `documented`, `derived` e `reported`,
com fundamento obrigatório nas duas últimas. A declaração exige fontes por campo;
exceções de papel são restritas por caminho e processo. Os guias orientam esse
contrato existente, sem transformar fonte de comparação em entrada independente.

- [CBO — informações gerais do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo/informacoes-gerais): classificação das ocupações e atividades. A abertura direta da consulta indicada pelo DP falhou com HTTP 502 durante esta pesquisa; nenhuma CBO individual foi qualificada.
- [Leiautes eSocial S-1.3, NT 06/2026](https://www.gov.br/esocial/pt-br/documentacao-tecnica/leiautes-esocial-versao-s-1-3-nt-06-2026/index.html): campos próprios para admissão, emissão de ASO, exames e autoclassificação racial.
- [Decreto 10.854/2021, arts. 112–116](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/decreto/d10854.htm): informação do deslocamento e distinção entre custeio, utilização e desconto de VT. O Decreto 95.247/1987 consultado inicialmente está revogado; não é usado como norma vigente.

Não foram codificadas regras trabalhistas, fiscais, percentuais ou elegibilidade
novas. Intervalo, dependência fiscal e parâmetros de empresa continuam dependentes
do procedimento aplicável, evidência do caso e dos contratos do host.

## Entrega e pendências

O texto só chega ao serviço com wheel novo, promoção ao consumidor, lock revisado,
testes, revisão e implantação do backend. Um commit neste repositório não basta.
O recebimento será conferido por versão/hash e resposta autenticada, inclusive no
fallback de `meu_acesso`; isso não comprova que toda harness executou o roteiro.

Os relatos de limitações enviados em 20/10 devem ser conciliados com o build atual
antes de abrir ou encerrar defeitos: histórico para cálculo, recusas, retomada de
simulações, processos habilitados e carga por programa têm contratos próprios.
Esta entrega não amplia capacidades nem resolve importação por instrução textual.
