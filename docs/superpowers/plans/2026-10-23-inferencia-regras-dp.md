# Investigação de regras como operação padrão

## Escopo autorizado

O usuário pediu formalizar o método já discutido na conversa e distribuí-lo no
plugin MCP_Loki para o operador suprir lacunas e corrigir causas reutilizáveis.
Escolha de implementação: skill `investigar-regras-dp`, descoberta pelos guias
existentes, com registro de qualificação em referência própria. Acrescentar texto
somente à rotina existente diluiria o método; duplicá-lo no provider exigiria
release independente do backend. Nesta etapa, plugin Git 1.1.5; provider 0.1.6,
instruções 1.3.2, contrato, leitores e locks preservados. Não alterar sistema da
Ana, agenda, credenciais ou dados de clientes. Instalação e execução no ambiente
real dela exigem evidências próprias.

## Plano e validação

- [x] Conferir instruções, HEAD/status e criar worktree isolado.
- [x] Executar baseline do repositório: 153 testes passaram.
- [x] Registrar cinco amostras de controle com guias atuais e o comportamento
  observado na conversa que motivou a mudança; não inventar falha dos controles.
- [x] Criar skill concisa, nome/frontmatter válidos, descoberta por sintomas,
  expressão/unidades/escopo, exemplo sintético e referência de qualificação.
- [x] Integrar bootstrap duplicado, operar-loki e ROUTINES sem duplicar método.
- [x] Versionar plugin e documentar ativação, sem alterar provider/wheel.
- [x] Conferir cinco aplicações independentes com a skill e ler todas as saídas;
  incluir fonte suficiente sem export, ambiguidade, gabarito, motor e refutação.
- [x] Revisar rotas, links relativos, pacote, lint/tipos, leitores e wheel isolado.
- [x] Fazer revisão independente da mudança e corrigir achados reproduzidos.
- [ ] Commit, PR e distribuição Git conforme autorização vigente e gates.
- [ ] Conferir cache nativo local e separar publicação, instalação, carregamento
  e execução. Atualizar continuidade com limites e passo do executor da Ana.

## Critérios da entrega

A skill permite avançar com evidência suficiente e configuração expressável;
indica a observação que distingue candidatos quando não há identificação única;
não reconstrói um fato usando o gabarito para certificar esse mesmo gabarito;
registra versão/consumo/replay e invalidação quando houver nova contraprova.
Defeito de produto segue reprodução sintética e fluxo de desenvolvimento/teste/
publicação autorizado. Instruções não concedem capacidades ou novo transporte.
Não há teste financeiro real nem medição de assertividade nesta entrega.
