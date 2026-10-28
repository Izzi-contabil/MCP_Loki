# Admissão

Consulte `meu_acesso` (ou `get_operator_context`), `list_workflows`, `get_dp_capabilities` e `get_process_contract` para o processo autorizado. Obtenha o schema e a seção atuais; envie o conteúdo da seção em `data` por `receive_case_data`, com `field_sources`, `request_ref` estável e `expected_snapshot` igual ao `input_snapshot` corrente de `get_case`. Dinheiro usa centavos inteiros; ausências, conflitos e totais dependentes permanecem pendentes.

Leitura de originais e comparação são externas ao Loki. Após receber os dados, siga cálculo, geração e revisão pelo `run_prepared_case_workflow` ou pelas operações declaradas no contrato. Versões internas preservam auditoria. A empresa de teste usa o mesmo fluxo e os mesmos gates. Disponibilidade de uma ferramenta não comprova cálculo validado, aprovação, envio, pagamento ou transmissão.

Separe dado extraído, dado ausente, divergência e decisão humana. Não preencha faltas com zero nem invente exigências legais, prazos ou validações. Obtenha a revisão humana indicada pelo runtime antes de avançar; aprovação técnica não concede aceite. Não publique ou transmita admissão a sistemas externos por inferência destas instruções.

## Seleção de fontes pela harness

As orientações abaixo organizam a leitura e a preparação nos contratos existentes. Não criam campos, regras de cálculo ou poderes no host. Consulte também o domínio `documentos`. Para cada campo, mantenha original, hash, página/campo e motivo da seleção; registre conflito e ausência antes de montar a declaração. A resposta geral do DP esclarece o procedimento, mas não prova qual documento, data ou orientação foi usado em um caso individual. Documento produzido pela equipe para comparação não substitui o insumo do cliente.

### Período salarial

Leia `contrato.periodo_salario` separadamente do valor do salário e da categoria do vínculo. Quando o pedido apresentar explicitamente a forma de remuneração, como `Categoria: Mensalista`, registre o valor integral `Mensalista` nesse campo, com original, hash e localizador da página/campo. Confira pelo conteúdo que a categoria descreve o período de remuneração; a palavra Categoria sozinha não identifica categoria do vínculo ou código eSocial. Preserve conflitos entre fontes, sem escolher automaticamente o documento mais recente.

Salário apresentado como montante, carga de 220 horas, valor compatível com piso ou rotina mensal de pagamento não confirma o período. Se a fonte não o disser ou a classificação for ambígua, preserve o branco e declare a ausência como pendência ou ambiguidade no contrato vigente; não omita a lacuna nem adote Mensalista como padrão.

Depois da preparação ou de uma correção autorizada, confira que o campo Por da ficha imprime o mesmo valor integral. Um erro de overflow é falha técnica a investigar: conserve o fato e registre o erro; não remova, abrevie ou substitua o período para fazer a geração passar. Caso em revisão exige o fluxo de ajuste/correção correspondente e nova conferência; a orientação não reabre nem aprova o caso automaticamente.

### Opção pelo FGTS

Leia `dados_admissao.contrato.fgts_opcao_em` separadamente da data de admissão. Para empregado CLT comum com admissão posterior a 04/10/1988, a orientação do Manual SEFIP 8.4 da CAIXA, edição de outubro/2022 conferida, itens 4.11 e 4.12, nota 1, é registrar a opção com a mesma data da admissão. Aplique esse fundamento somente depois de qualificar nos insumos o regime, a categoria, o empregador, o episódio atual do vínculo e sua data de admissão. O `case_type` de admissão e a presença de uma data, isoladamente, não comprovam essas condições. Um vínculo anterior na CTPS não qualifica a contratação atual. O relatório da equipe serve para comparação, nunca como fonte desses fatos ou da regra.

Fonte primária efetivamente conferida: [Manual SEFIP 8.4 — outubro/2022, itens 4.11 e 4.12, nota 1, página 52 do PDF/impressa 50](https://www.gov.br/receitafederalsimples/pt-br/assuntos/orientacao-tributaria/declaracoes-e-demonstrativos/gfip-sefip-guia-do-fgts-e-informacoes-a-previdencia-social-1/manuais-e-formularios/manual_sefip_8_4_17102022.pdf). A [edição maio/2026 da CAIXA](https://www.caixa.gov.br/Downloads/fgts-manuais-e-cartilhas-operacionais/Manual_SEFIP_8_4_05_2026.pdf) é complemento localizado/indexado com a mesma orientação nesses itens; seu acesso integral ficou bloqueado nesta verificação de 22/10/2026. Não declare leitura integral dessa edição. Registre a edição, a consulta e a vigência aplicável ao episódio/competência; não apresente maio/2026 como início universal da regra nem a consulta atual como qualificação histórica de qualquer caso. Confira ainda os limites do [eSocial S-1.3, NT 07/2026, REGRA_EVETRAB_VALIDA_OPCAO_FGTS](https://www.gov.br/esocial/pt-br/documentacao-tecnica/leiautes-esocial-versao-s-1-3-nt-07-2026/regras.html). Essa validação do eSocial, sozinha, não determina igualdade para toda categoria ou data.

Quando o campo estiver ausente e os insumos comprovarem o regime CLT comum e episódio atual, a categoria, o empregador e a admissão posterior a 04/10/1988 dentro do alcance acima, prepare a opção igual à admissão como derivação normativa fonteada. Em `field_sources` para esse caminho, use `kind=rule` e descreva em `foundation` a norma/edição/item, vigência e alcance, o regime/categoria e os operandos: admissão, empregador e episódio qualificados, com referências aos insumos, hash e localizador de cada fundamento. Use uma `reference` real, `locator` e `content_hash` quando disponíveis na fonte; não invente fontes ou campos no payload. A norma fundamenta a relação entre as datas; os insumos comprovam a admissão e o vínculo a que ela se aplica. Uma data assim calculada não foi extraída: não marque como documento lido. Confira o contrato corrente antes de enviar a declaração e preserve as qualificações na trilha privada.

Para admissão anterior ou igual a 04/10/1988, doméstico (categoria 104), diretor não empregado com FGTS (categoria 721), categoria incerta, transferência, reintegração, vínculo anterior sem episódio atual qualificado ou conflitos de admissão/opção, mantenha pendência e verifique a regra específica e as fontes pertinentes. Não aplique igualdade universal nesses cenários. Se houver opção declarada, não sobrescreva esse valor por derivação; preserve o fato e registre eventual conflito para esclarecimento. Falta de qualificação mantém o campo ausente ou o conflito como pendência no contrato vigente, sem preencher para coincidir com a equipe.

Caso em revisão exige preservar o snapshot, o pacote existente e os gates do host. Use o fluxo autorizado de ajuste/correção, submeta à revisão humana exigida e confira novamente o campo Opção em da ficha e o recibo da nova versão. Esta orientação não aplica alterações a casos, não reabre revisão, não aprova documentos e não autoriza transmissão ou aceite automático.

### Cargo e CBO

Use o cargo da ficha admissional ou da confirmação específica do cliente para esta contratação. Cargo ausente exige confirmação; diploma, currículo e vínculo antigo não identificam o cargo atual. Preserve a nomenclatura informada pelo cliente.

Pesquise a ocupação na classificação oficial do MTE: https://consulta.trabalho.gov.br/empregador/cbo/procuracbo/. Confira atividades, descrição e compatibilidade; similaridade do título ou pertencimento à mesma família, isoladamente, não define o código. Registre a referência consultada, a data e a justificativa. Se a consulta não estiver acessível ou as atividades forem ambíguas, mantenha a CBO pendente e peça esclarecimento, sem alegar consulta realizada. Reutilização de CBO da empresa segue o contrato e a confirmação próprios do host.

### Jornada, intervalo e cargas

Leia separadamente entrada, saída, intervalo, dias da semana, escala e cargas semanal/mensal. Confira a consistência entre essas informações e as fontes. Campo vazio e zero usado como marcador de ausência não confirmam horário ou carga; `00:00` explicitamente informado como meia-noite pode ser horário válido e não deve ser apagado. Parâmetro da empresa só se aplica com fonte vigente e vínculo demonstrado ao empregado; divergência entre pedido, ficha, parâmetro e contrato exige registro e esclarecimento.

Quando o cliente informa entrada e saída, mas não o intervalo, o DP pode propor uma distribuição interna compatível com a jornada e a regra aplicável. Trate-a como proposta operacional derivada, nunca como horário lido ou praticado. Não adote um intervalo universal, não altere horário informado pelo cliente nem force cargas a coincidir. Antes de aplicar a proposta, confira a convenção/regra aplicável e obtenha confirmação humana específica; se não houver fundamento ou confirmação, deixe os horários desconhecidos pendentes. Declare `kind=rule`, os operandos e o fundamento em `foundation`, com localizador real dos insumos. Isso não dispensa os gates do host.

### Admissão e ASO

Separe data de admissão, data de emissão do ASO e datas dos exames. Use a solicitação/retificação do cliente para a admissão e o ASO para os respectivos dados de saúde. A expressão “data considerada no cadastro” do ASO não autoriza substituir a data contratual. Campo de admissão divergente dentro do ASO exige esclarecimento; exame posterior é uma ocorrência a informar, sem reescrever datas para ocultá-la.

Procure o ASO nos anexos e nos canais já autorizados antes de declarar que não foi enviado. Se disponível, leia tipo de exame, emissão, procedimentos/datas, médico, CRM/UF e resultado conforme o original. Não invente campos de SST no payload admissional: preserve o documento e relate o que o contrato não suporta. Se não houver ASO, registre a ausência sem fabricar lançamento; siga a possibilidade de pacote parcial indicada pelo runtime. Preparação documental não atesta cumprimento de SST, conclusão legal da admissão ou transmissão ao eSocial.

### Documentos de identificação e significado dos campos

Confira a modalidade e o rótulo da data na CTPS. A data de emissão ou de extração de uma CTPS digital não comprova, por si, a data de expedição da carteira física e não deve preencher automaticamente `empregado.data_expedicao_ctps`. Preserve a emissão digital como fato separado quando o contrato não tiver destino correspondente; uma equivalência exige fundamento explícito no contrato e na fonte. Não derive número, série ou UF da CTPS a partir do CPF, de outro documento ou do endereço.

O título “Certificado de Dispensa de Incorporação” identifica um tipo documental; não comprova a categoria de reservista. Transcreva o número identificador no caminho aceito e preencha `empregado.documento_militar_categoria` somente com categoria explicitamente informada e qualificada. Não use o título do certificado nem “CDI” como categoria padrão.

No órgão emissor do RG, confira a sigla e a UF atribuídas ao próprio emissor. Pode usar uma sigla também impressa no original, com o literal extenso e o localizador preservados como fundamento da normalização. Sem sigla ou UF explícitas, conserve o que foi informado e a lacuna correspondente; não invente abreviação ou UF para fazer o texto caber. Falha de espaço é problema a diagnosticar no documento, sem truncar ou trocar o fato.

### Endereço, sexo e raça/cor

Endereço vem do comprovante ou formulário admissional e de atualização específica do cliente. Preserve a divergência; a resposta geral não estabelece precedência universal entre comprovante e formulário. Cadastro anterior só é fonte atual com qualificação correspondente.

Para sexo, priorize a informação explícita no documento oficial enviado diante de formulário divergente, registrando ambas as fontes e o critério. Documento sem esse campo não o comprova. Nunca infira sexo pelo nome ou aparência.

Raça/cor exige autodeclaração do trabalhador, inclusive quando registrada na ficha encaminhada pelo cliente. Não use “parda” como padrão, não infira pela aparência e não copie o relatório da equipe para preencher a lacuna. Sem autodeclaração, peça confirmação e mantenha pendência. Campo obrigatório no destino não autoriza inventar seu valor.

### Vale-transporte

Separe opção pelo benefício, linhas, tarifas, quantidade, concessão e configuração de cálculo. Opção “Não” acompanhada de tarifa/itinerário pede conferência de vigência e finalidade: pode haver conflito, rota antiga ou recusa específica posterior. Preserve as fontes e o motivo da seleção; se não houver resolução sustentada, peça confirmação. Não troque a opção para fazer a declaração passar nem fabrique declaração de próprio punho. Represente no payload apenas os fatos vigentes aceitos pelo contrato, conservando os demais como evidência e justificativa; não remova dados silenciosamente.

Use somente linhas, tarifas e quantidades efetivamente informadas. Valor monetário no campo de linha é preenchimento suspeito, não nome de linha. Ausência de opção não significa “Não”; ausência de tarifa não significa zero. Conforme o contrato, prepare termo com campos desconhecidos em branco e pendências no recibo separado, sem apresentar essa preparação como admissão concluída. Recusa explícita deve ser respeitada; a seleção dos documentos segue o contrato corrente, sem promessa de que o host omita automaticamente o termo.

O percentual de 6% relatado pelo DP é configuração, não prova de opção, concessão ou autorização de desconto. Não converta esse relato em desconto de folha, marque uso do benefício ou crie parâmetro que o contrato não expõe. Desconto depende da concessão e das regras aplicáveis, com os gates próprios do processo.

### Dependentes e beneficiários

Separe vínculo familiar/cadastro, indicação para IR, salário-família, beneficiários e pensão alimentícia. Certidões e identificação podem comprovar o parentesco, mas não são, sozinhas, declaração de dependência fiscal ou indicação de beneficiário. “Possui dependentes” genérico não preenche automaticamente as seções de IR e salário-família.

O relato de cadastro automático de filhos menores de 14 anos é prática informada pelo DP, não regra a aplicar apenas pela idade. Qualifique separadamente a indicação e os requisitos de cada finalidade pelo procedimento aprovado e pelo contrato. Pensão depende da documentação específica. Sem documentos ou indicação suficiente, mantenha as finalidades pendentes; não declare que não existem dependentes nem bloqueie por conta própria toda preparação documental. Siga os requisitos mínimos e as ressalvas do runtime.

### Estabelecimento do vínculo

Use o CNPJ indicado pelo cliente para a contratação, com referência ao portal, ficha ou orientação específica. Em cadastro com códigos separados por estabelecimento, confira o CNPJ da unidade selecionada; em cadastro centralizado na matriz, confira a filial indicada. Não confunda empresa pela qual o pedido entrou com estabelecimento do vínculo, nem considere pertencer ao mesmo grupo como equivalência de CNPJ.

Cabeçalhos de contrato, ficha e extrato divergentes exigem conciliação e registro da orientação/retificação. Não escolha automaticamente matriz, primeiro cadastro ou CNPJ mais frequente. Se a unidade correta estiver fora do escopo autenticado ou não cadastrada, preserve a pendência e solicite a providência autorizada; não redirecione o caso para outra empresa.

Fontes `kind=document` exigidas como evidência nativa usam `document.reference` com o ID do anexo retornado por `attach_source_document` e `content_hash` igual ao retorno. O upload arquiva o original como bytes opacos; o Loki não extrai nem interpreta seu conteúdo. Não invente DOC com caminho local, ID do Drive ou hash avulso. Leitura externa declarada pode usar `kind=declaration`, referência/localizador/fundamento honestos e seus limites; isso não atesta verificação documental nativa. Quando identidade, efeito ou qualificação exigir fonte nativa, arquive o original opacamente ou selecione a fonte nativa já persistida/pinnada indicada pelo contrato. Não troque a classificação da origem para fabricar qualificação.
