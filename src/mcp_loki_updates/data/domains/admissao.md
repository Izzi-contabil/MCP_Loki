# Admissão

Consulte `list_workflows` e `get_dp_capabilities` para confirmar o estado atual de admissão e os gates aplicáveis. Trate fluxos partial/shadow como apoio à análise; não apresente admissão como concluída por existir um registro ou uma extração.

O host exige capacidade `consultar` e escopo do processo `admissao` antes de entregar estas instruções. Outras operações mantêm suas próprias verificações de autorização. Para documentos, consulte `get_document_processing_contract` e use somente canais autorizados; mantenha PII e evidências em seus repositórios privados de origem.

Separe dado extraído, dado ausente, divergência e decisão humana. Não preencha faltas com zero nem invente exigências legais, prazos ou validações. Obtenha a revisão humana indicada pelo runtime antes de avançar; aprovação técnica não concede aceite. Não publique ou transmita admissão a sistemas externos por inferência destas instruções.

## Seleção de fontes pela harness

As orientações abaixo organizam a leitura e a preparação nos contratos existentes. Não criam campos, regras de cálculo ou poderes no host. Consulte também o domínio `documentos`. Para cada campo, mantenha original, hash, página/campo e motivo da seleção; registre conflito e ausência antes de montar a declaração. A resposta geral do DP esclarece o procedimento, mas não prova qual documento, data ou orientação foi usado em um caso individual. Documento produzido pela equipe para comparação não substitui o insumo do cliente.

### Período salarial

Leia `contrato.periodo_salario` separadamente do valor do salário e da categoria do vínculo. Quando o pedido apresentar explicitamente a forma de remuneração, como `Categoria: Mensalista`, registre o valor integral `Mensalista` nesse campo, com original, hash e localizador da página/campo. Confira pelo conteúdo que a categoria descreve o período de remuneração; a palavra Categoria sozinha não identifica categoria do vínculo ou código eSocial. Preserve conflitos entre fontes, sem escolher automaticamente o documento mais recente.

Salário apresentado como montante, carga de 220 horas, valor compatível com piso ou rotina mensal de pagamento não confirma o período. Se a fonte não o disser ou a classificação for ambígua, preserve o branco e declare a ausência em `missing_fields` ou a ambiguidade no contrato vigente; não omita a lacuna nem adote Mensalista como padrão.

Depois da preparação ou de uma correção autorizada, confira que o campo Por da ficha imprime o mesmo valor integral. Um erro de overflow é falha técnica a investigar: conserve o fato e registre o erro; não remova, abrevie ou substitua o período para fazer a geração passar. Caso em revisão exige o fluxo de ajuste/correção correspondente e nova conferência; a orientação não reabre nem aprova o caso automaticamente.

### Cargo e CBO

Use o cargo da ficha admissional ou da confirmação específica do cliente para esta contratação. Cargo ausente exige confirmação; diploma, currículo e vínculo antigo não identificam o cargo atual. Preserve a nomenclatura informada pelo cliente.

Pesquise a ocupação na classificação oficial do MTE: https://consulta.trabalho.gov.br/empregador/cbo/procuracbo/. Confira atividades, descrição e compatibilidade; similaridade do título ou pertencimento à mesma família, isoladamente, não define o código. Registre a referência consultada, a data e a justificativa. Se a consulta não estiver acessível ou as atividades forem ambíguas, mantenha a CBO pendente e peça esclarecimento, sem alegar consulta realizada. Reutilização de CBO da empresa segue o contrato e a confirmação próprios do host.

### Jornada, intervalo e cargas

Leia separadamente entrada, saída, intervalo, dias da semana, escala e cargas semanal/mensal. Confira a consistência entre essas informações e as fontes. Campo vazio e zero usado como marcador de ausência não confirmam horário ou carga; `00:00` explicitamente informado como meia-noite pode ser horário válido e não deve ser apagado. Parâmetro da empresa só se aplica com fonte vigente e vínculo demonstrado ao empregado; divergência entre pedido, ficha, parâmetro e contrato exige registro e esclarecimento.

Quando o cliente informa entrada e saída, mas não o intervalo, o DP pode propor uma distribuição interna compatível com a jornada e a regra aplicável. Trate-a como proposta operacional derivada, nunca como horário lido ou praticado. Não adote um intervalo universal, não altere horário informado pelo cliente nem force cargas a coincidir. Antes de aplicar a proposta, confira a convenção/regra aplicável e obtenha confirmação humana específica; se não houver fundamento ou confirmação, deixe os horários desconhecidos pendentes. Se o contrato admitir `basis=derived`, declare os operandos e o fundamento em `derivation`, com localizador real dos insumos. Isso não dispensa os gates do host.

### Admissão e ASO

Separe data de admissão, data de emissão do ASO e datas dos exames. Use a solicitação/retificação do cliente para a admissão e o ASO para os respectivos dados de saúde. A expressão “data considerada no cadastro” do ASO não autoriza substituir a data contratual. Campo de admissão divergente dentro do ASO exige esclarecimento; exame posterior é uma ocorrência a informar, sem reescrever datas para ocultá-la.

Procure o ASO nos anexos e nos canais já autorizados antes de declarar que não foi enviado. Se disponível, leia tipo de exame, emissão, procedimentos/datas, médico, CRM/UF e resultado conforme o original. Não invente campos de SST no payload admissional: preserve o documento e relate o que o contrato não suporta. Se não houver ASO, registre a ausência sem fabricar lançamento; siga a possibilidade de pacote parcial indicada pelo runtime. Preparação documental não atesta cumprimento de SST, conclusão legal da admissão ou transmissão ao eSocial.

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
