# Comparação privada com componentes qualificados

Use quando o operador autorizar uma comparação e indicar um índice privado de
componentes já qualificados. O índice é uma referência de seleção da harness;
**não é contrato MCP, configuração empresarial, fonte primária ou autorização**.
Schemas, permissões e fontes aceitas continuam sendo os do host atual.

## Descobrir e conferir o material

1. Confirme acesso, instruções, workflows e contratos pelo MCP existente.
   Obtenha do pedido o caminho local ou a localização autorizada do material.
   Sem essa localização, informe exatamente a referência que falta. Não procure
   credenciais nem suponha que um arquivo deste servidor esteja no computador
   de outro operador.
2. Leia o manifesto e os arquivos relacionados pelos leitores instalados.
   Preserve-os fora do Git/cache do plugin, em workspace privado. A convenção
   local `loki.comparative-test-handoff/1` contém `created_at`, `cliente_slug`,
   `observed_backend_build`, `files` e `scope`. Cada item de `files` informa
   `filename`, `sha256` e `bytes`. Só aceite nomes simples no diretório do
   manifesto; recuse caminhos absolutos, travessia e symlinks.
3. Confira tamanho e SHA256 de cada arquivo. Um hash recebido no mesmo pacote
   verifica consistência, não autoria independente. Confirme a edição indicada
   pelo operador e registre origem, data e hash do manifesto. Se houver versões
   concorrentes ou conteúdo divergente, preserve o conflito.
4. Consulte build e contratos correntes. Uma mudança exige revalidar as fontes,
   os seletores e os schemas antes do reuso. Não altere pin/preflight do kit
   legado para aceitar o material.

Os arquivos da convenção local são:

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `salary-components.json` | Contextos salariais parciais e parâmetro candidato | Seleção restrita ao episódio/competência; conferir no histórico |
| `reported-observations.json` | Observações, unidades, origem e lacunas | Informação reportada; qualificação executável separada |
| `calendar-intervals.json` | Datas e interseções documentadas | Calendário; não determina dias pagos |
| `retentions.json` | Contextos retidos, casos protegidos e motivos | Exclusões obrigatórias deste ensaio |
| `README.md` | Recorte e instrução operacional do material | Contexto do pedido, sem ampliar poderes |

Uma seleção sem os identificadores/fontes abaixo é insuficiente mesmo com
manifesto íntegro. Outra convenção exige seu próprio contrato documentado;
não invente campos nem envie esse objeto como um request de ferramenta.

## Selecionar por contexto e fonte

Para salário, concilie `cliente_slug`, `empresa_cnpj`, `cpf`,
`data_admissao`, `employee_id`, `competence`, `source_fact_id` e
`source` (document_id, content_hash, locator). Use a identidade do pedido
autorizado; índice de outro vínculo ou empresa não resolve uma identidade ausente.

Consulte `get_company_employee_history` na data aplicável e confira identidade,
valor, unidade, fato, data de efeito e fonte contra a linha. Aplique as retenções
antes de usar o parâmetro. Repetição do empregado em meses distintos não permite
estender a seleção de um mês ao outro. `vigente_ate=null` continua desconhecido.
Data literal registrada não fixa o início material de uma retroatividade;
conserve separadamente a competência retroativa e a lacuna do dia material.

Salário conferido é apenas um operando. Para um componente financeiro, confira
também período remunerável, divisor/jornada, demais operandos, fórmula,
incidências e política aplicável exigidos pelo contrato. Uma lista parcial não
define a população completa da folha. Intervalos de férias/afastamentos e
ausência de evento no acervo não provam mês integral trabalhado.

Em observações, preserve `basis=reported`, código, empresa, competência,
episódio, literal, unidade, `source` e `missing_fields`. Confira a observação
no histórico nativo pela fonte e seu localizador. Mesmo código em outra empresa
não identifica a mesma rubrica. Não escolha direção, incidência ou fórmula pelo
código ou pela proximidade de um resultado esperado.

Exemplo aritmético sintético: `001:10 h` corresponde a 70 minutos. Conserve
literal e minutos; não arredonde 70/60 para transformar a quantidade em horas
decimais de um lançamento. `HH:MM` não é número decimal. Dias, minutos e
centavos são unidades diferentes. Um total reportado não é resultado
recalculado, e uma observação não vira lançamento executável pelo reuso.

## Executar e registrar o consumo

Prepare somente o processo e os componentes cujos requisitos estejam atendidos
no contrato vigente. Consulte `versioned_case` quando disponível e fixe caso,
base, fontes e referência idempotente. Dados já persistidos não exigem recadastro.
Para fonte nova, siga WORKFLOWS.md: só parâmetros/CSVs seguem ao Loki; originais
permanecem locais. Não remova lacunas para obter sucesso da chamada.

Quando faltar requisito, conserve o valor dependente ausente e registre a
pendência exata; prossiga no pacote parcial se o contrato permitir. Hipótese
estatística ou regra sugerida não é política empresarial qualificada. Sem
suporte do contrato, a hipótese permanece análise separada e não configura o motor.

Antes de abrir o resultado da equipe para comparação, fixe o resultado do Loki:
caso/versão, input_hash/result_hash quando fornecidos, fontes e artefatos.
Documentos da equipe e relatórios de resultado conservam seu papel de referência;
não preenchem entradas faltantes para fazer a réplica coincidir.

Mantenha um recibo local de consumo com:

- versão/hash/origem do manifesto, build e contrato efetivamente consultados;
- contexto de cada linha consumida, fato e fonte conferidos no host;
- linhas retidas, motivo e dependências ainda ausentes;
- pedido e resposta exatos, caso/versão e hashes dos resultados;
- comparação por campo/componente e classificação sustentada pelas fontes.

Confira os artefatos nativos e todas as páginas dos PDFs, envie apenas os checks
observados e prepare a revisão. Registre coincidência, divergência, falta de
histórico/insumo e falha de acesso separadamente. Resultado parcial não mede
paridade financeira completa; conformidade documental não atesta cálculo.

## Atualização e evidência de execução

Publicação no Git, instalação, descoberta MCP e execução são provas distintas.
Conferir a versão instalada em `claude plugin list --json`, recarregar plugins
ou abrir nova sessão e resolver esta referência a partir da skill carregada.
Depois, executar o diagnóstico local e um ensaio autorizado pelo MCP.
O recibo de consumo comprova quais componentes entraram naquele ensaio;
não comprova uma execução futura na máquina de outro operador.

O plugin não cria agenda nem altera fila/sistema externo. Use as integrações já
autorizadas. Comparação e preparação privada não aprovam documentos, aplicam
mudanças cadastrais, pagam ou transmitem. Conserve os gates humanos do host.
