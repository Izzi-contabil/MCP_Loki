# Validação do perfil Claude — 21/10/2026

O registro inicial abaixo antecede a integração da PR 4. A seção final registra
a integração e a configuração efetiva do Codex neste servidor; o aceite nas
máquinas da Ana e do Samuel permanece pendente.

Escopo confirmado pelo usuário: Ana/macOS, Samuel/Windows+Linux, ambos Claude
Code; Antônio/Codex+ChatGPT no servidor Linux. O plugin nativo é declarativo e
usa o MCP já conectado. O pacote provider permanece 0.1.3, sem mudança de conteúdo
ou wheel. Kit Windows assinado e seus gates são outro perfil.

Verificações executadas no Linux com Python3.11:

- `pytest -q`: **95 passaram, 3 ignorados** por ausência de PowerShell no host.
- Os mesmos três probes de cadastro do guia foram executados em PowerShell real
  no container Microsoft, sem rede: falha configure, falha run e controle válido
  passaram. Isso não é Task Scheduler Windows real.
- `ruff check .`, `ruff format --check .`, `mypy src scripts`: passaram.
- Claude Code oficial2.1.306, checksum conferido no manifest Anthropic, perfil
  isolado e sem login/modelo: validate do marketplace/plugin, instalação1.0.0,
  atualização Git para1.0.1, versão e bytes do cache conferidos, reversão manual
  para1.0.0 e configure/run/status do driver passaram. O Git redirecionou uma URL
  HTTPS sintética para um repositório local apenas nesse processo. Não houve
  autenticação GitHub de operador nem ensaio de rede privada real.
- O driver conservou o arquivo sintético de OAuth byte a byte. Isso não certifica
  o Keychain/Credential Manager real nem configura acesso para outra pessoa.

O teste diário verificou 09h59UTC/10hUTC (06h59/07h Brasília), idempotência,
repetição manual, falha sanitizada e lock concorrente. Os artefatos das três
plataformas foram analisados, com caminhos acentuados e espaços. Nenhum deles
foi registrado como agenda operacional neste servidor.

A revisão independente da nova superfície encontrou perfil herdado/relativo,
desativação Mac que não persistia ao login e cadastro após primeira falha. O
último foi reclassificado de Minor para Important pelo efeito no rollout.
Regressões observaram RED e GREEN: perfil padrão/herdado e customizado absoluto,
comandos reais do guia Bash com falhas configure/run, remoção do plist instalado
no Mac, e bloco PowerShell com run falho. Controles válidos de cadastro passaram.
O cadastro Windows usa o SID ASCII do usuário, evitando erro de codificação do
nome OEM/ANSI. O caso de nome acentuado falhou antes da correção e passou
depois; identidades malformadas são recusadas, com controle SID válido.
Nenhuma segunda revisão foi usada como substituto dos testes das correções.

Decisão de implementação: uma tentativa diária após07h, inclusive quando falha;
repetição no mesmo dia é manual. O plugin é distribuído pelo Git privado revisado,
sem assinatura de bundle ou rollback automático transacional. Uma orientação
pode ser restaurada por commit validado/CLI com agenda parada ou revert publicada
em versão nova. O executável do driver fica estável e requer reconfiguração para
mudar. Isso evita converter/coletar OAuth do Claude ou executar scripts novos a
cada pull. O custo é manter o ciclo do kit local separado e o aceite por máquina.

Prontidão operacional depende da integração desta PR na branch padrão, acesso
pessoal GitHub autorizado e aceite em cada máquina com disparo real da agenda.
Não houve merge, deploy, envio de convites ou alteração de OAuth/sistema da Ana.
A CI GitHub não iniciou por pagamento/limite da conta; verificações locais não
são anunciadas como CI hospedada verde.

## Integração e Codex no Linux

A PR 4 foi integrada, com autorização do usuário, em
`6da6dc5183461f8026977e007e5210fbf7d5ee81`, na branch padrão
`feature/dynamic-instructions`. Antes do merge, repetidos os 95 testes,
Ruff e mypy. Sem threads de revisão pendentes. A anotação do check
`119443507224` confirmou que o job não iniciou por cobrança/limite do GitHub.

O CLI real Codex 0.163.0 instalou o mesmo pacote compatível em container sem
rede ou credenciais. Uma URL HTTPS sintética redirecionada apenas dentro do
container para Git local exercitou atualização 1.0.0 → 1.0.1. O comando
`plugin marketplace upgrade loki-equipe` atualizou o manifesto no cache antes
de qualquer chamada a `plugin list` ou nova instalação. Outro incremento
1.0.1 → 1.0.2 manteve `enabled=false`. Repositório indisponível fez o comando
falhar com código 1. Não se usa `plugin add` no agendamento.

No servidor real, o marketplace foi adicionado por HTTPS ao GitHub privado,
e `loki-orientacoes@loki-equipe` 1.0.0 foi instalado e habilitado. A configuração
de servidores MCP e os hashes dos arquivos locais de autenticação permaneceram
iguais após a instalação. O conector autenticado já existente respondeu a
`meu_acesso`, `loki_verificar_versao` e `loki_obter_instrucoes(geral)`;
isso confirma o acesso do chat, sem exportar OAuth para processos Linux.

O bloco systemd de `CODEX_LINUX_SETUP.md` foi executado neste servidor.
`systemd-analyze --user verify` passou e o serviço executou uma consulta real
ao GitHub privado com `errors: []`, `Result=success` e `ExecMainStatus=0`.
O timer está habilitado/ativo; próximo disparo observado: **22/10/2026 às
10h UTC, 07h de Brasília**. O usuário já tinha `Linger=yes`. Não se afirma que
um disparo futuro às 07h ocorreu nem que esta conversa carregou a skill nova.

O complemento de documentação usa versão 1.0.1 do plugin, preservando o conteúdo
da skill, o provider 0.1.3, o contrato e o backend. As instruções do Codex e a
consulta diária dependem do seu gerenciador nativo; não foi criado launcher
desktop ou novo manifesto ChatGPT. No checkout desse complemento, os 95 testes,
Ruff e mypy passaram novamente. O aceite nas máquinas da equipe e a concessão
de leitura no GitHub continuam a cargo de cada pessoa e de Antônio.

Fontes: [comandos Claude](https://code.claude.com/docs/en/plugins/cli-reference),
[marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
[perfis](https://code.claude.com/docs/en/env-vars),
[launchd](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html),
[OpenAI Docs — plugins](https://developers.openai.com/plugins/build/plugins).
