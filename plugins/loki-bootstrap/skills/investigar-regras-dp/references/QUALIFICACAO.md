# Registro privado da investigação

Mantenha um registro por problema reutilizável, com identidade estável e revisões.
Antes de nova busca, leia o registro e as evidências atuais do Loki. Reutilize
conclusões válidas; evidência nova ou mudança de norma/build exige reavaliar o que
ela afeta. Arquivo do computador anterior não está automaticamente disponível em
outro executor. Persistência operacional usa os contratos nativos do Loki; uma
nota privada é memória auxiliar, não configuração consumida pelo cálculo.

## Conteúdo necessário

| Parte | Registrar |
|---|---|
| Problema | Referência estável, tarefa/caso, incógnita, efeito e próxima ação discriminante. |
| Alcance | Empresa/estabelecimento, vínculo, categoria, território, finalidade, competência, início/fim de vigência e exceções. |
| Fundamentos | Norma/ACT/CCT/aditivo ou política comprovada, edição/cláusula/página, vigência, fonte e motivo do enquadramento. |
| Evidências | Original/hash/localizador, valores e unidades; o que é extraído, derivado, ausente ou conflitante. |
| Hipóteses | Expressão, base, taxa, divisor, conversões, reflexos e arredondamento; alternativas e por que uma foi descartada ou ainda não é distinguível. |
| Testes | Documentos de calibração separados dos reservados; entradas, previsão congelada, resultado, diferenças e limites de cobertura. |
| Aplicação | Tool/contrato reais, revisão/hash, fontes nativas, preview/validação/aplicação, releitura e prova de seleção/consumo. |
| Retomada | Build/versão/corte, resultado da tarefa antes/depois, consumidores afetados, contraprovas, retenções e lacunas restantes. |

Use estados de investigação compreensíveis, como hipótese, qualificada para um
alcance, refutada e aguardando observação. São rótulos desta nota, não enums a
enviar ao servidor. Não invente campos/tools para caber neste quadro.
Se o contrato não guardar algum fundamento, conserve-o em evidência privada e
na fonte CSV aceita; isso não transforma a nota em regra executável.

## Exemplo sintético: verba percentual

Norma comprovadamente aplicável define adicional de 5% do salário contratual
vigente e seus reflexos. Quatro holerites usados na calibração têm salário
200000/200000/240000/240000 e adicional10000/10000/12000/12000, em centavos.
A hipótese é `adicional = arredondar(salario_contratual_cents × 5 / 100)`;
a política de arredondamento e as condições de proporcionalidade ainda precisam
ser qualificadas quando afetarem o caso. Dois meses não abertos são reservados
antes de ajustar a hipótese. Extraia seus operandos sem usar o adicional como
entrada, congele a previsão e só então confronte os pagamentos.

Se o controle sustentar a regra e as condições necessárias estiverem completas,
configure somente o alcance qualificado pelos contratos atuais, releia e confira
o consumo. A ausência do cadastro do ERP não bloqueia essa via. Um mês integral
não testa proporcionalidade; regra mensal não certifica reflexo rescisório.
Se o controle contrariar a hipótese, preserve a divergência e investigue antes
de promover a regra. Dois exemplos exatos não são taxa de assertividade geral.

Em quantidade horária, explicite horas decimais, HH:MM, minutos físicos ou horas
reduzidas. Teste a conversão uma única vez no ponto demonstrado. Se duas fórmulas
produzem o mesmo centavo, registre ambas e procure uma quantidade/base que as
separe, sem presumir jornada ou percentual do exemplo do fornecedor.

## Retomada eficiente

Registre uma ação concreta ao parar: fonte e período a consultar, variável que
separa candidatos, escrita autorizada pronta ou defeito que precisa de release.
Sem progresso possível nas fontes acessíveis, mantenha a parte dependente
pendente e peça somente o complemento específico; evite loops de buscas iguais.
Após uma correção compartilhada, retome consumidores pelo mesmo problema, mas
valide identidade, corte e fonte de cada tarefa. Preserve estados humanos e
conflitos prévios. Encerrar exige observar o bloqueio desaparecer no resultado
pertinente, não apenas confirmar que o relato ou a configuração foram gravados.
