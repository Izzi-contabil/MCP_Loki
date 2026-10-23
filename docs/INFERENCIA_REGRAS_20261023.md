# Investigação de regras durante a operação — plugin 1.1.5

Quando faltar dado ou regra, ou surgir divergência recorrente, o fluxo normal
encaminha para `investigar-regras-dp`. A skill cruza normas/ACT/CCT, parâmetros e
holerites, registra hipóteses e procura observações que distingam alternativas.
Configuração do ERP é uma fonte possível, sem exigir export quando outras
fontes forem suficientes. Um pagamento histórico pode conter erro; uma norma
não comprova a ocorrência individual.

A skill separa calibração de controles reservados, limita a regra ao alcance e
vigência demonstrados e exige releitura, seleção, consumo e retomada da tarefa.
Um registro privado orienta a continuidade sem substituir persistência nativa.
Nova contraprova exige identificar consumidores e revalidar dependências,
preservando conflitos e decisões anteriores. Há exemplo exclusivamente sintético.

Dados/configurações suficientes seguem escritores autorizados do MCP. Limitação
do motor segue reprodução sintética e fluxo de desenvolvimento/testes/revisão/
publicação quando houver acesso e autorização. Não há edição direta de banco,
container ou pins; relato de suporte tem autorização e recibo próprios.

## Distribuição e ativação

- Plugin Git: 1.1.5, no mesmo marketplace e nome `loki-orientacoes@loki-equipe`.
- Skill: [investigar-regras-dp](../plugins/loki-bootstrap/skills/investigar-regras-dp/SKILL.md).
- Rotas: bootstrap, operar-loki e ROUTINES.md; chamada direta disponível no Claude
  como `/loki-orientacoes:investigar-regras-dp` e no Codex como `$investigar-regras-dp`.
- [Ativação na rotina existente](ANA_ROUTINE_ACTIVATION.md): versão instalada,
  recarga da sessão, roteiro salvo e execução observada são verificações distintas.
  Um executor legado não passa a usar a skill só porque ela foi publicada.

Provider0.1.6, instruções1.3.2, contrato1.0.0, scripts e locks preservados.
Não há promoção de wheel, deploy de backend, alteração do sistema da Ana, agenda,
OAuth ou credenciais nesta mudança. A instalação e execução no equipamento dela
não foram observadas. A skill não garante execução pelo modelo ou acerto financeiro.

## Validação realizada

Baseline do repositório:153 testes passaram. Após a mudança:154 testes passaram;
Ruff/lint/formatação, mypy e diff-check passaram. O teste de distribuição verifica
os arquivos incluídos, igualdade do bootstrap e rotas/links da nova skill.
Validador do SKILL.md passou. Doctor dos leitores com Python3.11 passou usando
somente documentos sintéticos. Wheel construído e instalado fora do fonte:
provider saudável/13domínios; SHA-256 igual ao wheel0.1.6 do consumidor, sem nova
identidade ou alteração de bytes. Nenhum wheel foi promovido.

Cinco avaliações independentes com os guias atuais e cinco com a nova skill
cobriram: fonte suficiente sem export; mês ausente/gabarito; hipóteses horárias
indistinguíveis; motor sem operador; contraprova após regra aplicada. Todas as
saídas foram lidas manualmente. Os controles atuais já tomaram decisões seguras;
a comparação não demonstra melhoria causal. A falha observada na conversa foi
a dependência excessiva da configuração do ERP como condição de avanço.
Esta entrega formaliza o método e sua descoberta/retomada, sem afirmar ganho de
assertividade. Revisão independente não encontrou achados acionáveis.

As avaliações foram textuais, sintéticas e sem MCP/rede/escritas de negócio.
Não houve teste financeiro real, validação de uma fórmula específica ou aferição
da meta98%. Provas de trabalho e respostas literais permanecem fora do Git.
