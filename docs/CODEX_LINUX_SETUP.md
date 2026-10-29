# Codex — plugin Loki com atualização nativa


Contrato candidato2.1.0: plugin/instruções2.1.0 e provider0.3.0.
Consulte `get_process_contract` e envie `receive_case_data` com fontes opcionais, referência
estável e o `input_snapshot` atual de `get_case`. Leitura e comparação são externas;
a empresa de teste usa o mesmo fluxo e gates. Atualização, catálogo e execução
no operador exigem comprovação própria; preserve OAuth e a agenda existente.

O plugin `loki-orientacoes@loki-equipe` usa o MCP e o OAuth já conectados.
Este roteiro substitui o timer das 07h e deixa a atualização com o próprio
Codex. A versão1.1.0 inclui leitores locais, a skill `operar-loki` e preparação
de parâmetros/CSVs pela harness. O kit executável Windows antigo não é alterado.

## 1. Instalar uma vez

No terminal do mesmo usuário/perfil que executa o Codex, conferir `codex --version`.
O procedimento foi verificado no Codex 0.163.0. Git e GitHub CLI precisam estar
instalados, além de `uv` para os leitores, com leitura pessoal de `T0minh0/MCP_Loki`. Se necessário, executar
`gh auth login --hostname github.com --web --git-protocol https` e
`gh auth setup-git` antes da instalação.

```text
codex plugin marketplace add https://github.com/T0minh0/MCP_Loki.git --json
codex plugin add loki-orientacoes@loki-equipe --json
codex plugin list --marketplace loki-equipe --json
```

Conferir `installed: true` e `enabled: true`. Se já estiver instalado, manter
essa instalação. Preservar a conexão MCP existente e suas credenciais.

## 2. Usar o auto-update do Codex

Manter o marketplace registrado pelo Git e o plugin habilitado. A inicialização
dos plugins no Codex 0.163.0 dispara em segundo plano a consulta e atualização
dos marketplaces Git configurados e do cache dos plugins. Não há um botão
`Enable auto-update` equivalente ao Claude para acrescentar neste roteiro.

Abrir o aplicativo normalmente e iniciar uma conversa nova para carregar as
orientações. Se uma atualização acontecer com uma conversa já aberta, iniciar
outra conversa depois de concluída. Sem agendador externo, a atualização depende
do ciclo da harness; não há promessa de consulta às 07h ou com ela fechada.

Em conversa nova, selecionar a skill `loki-bootstrap` ou invocar `$loki-bootstrap`.
Pedir que consulte `meu_acesso` e as instruções `geral`. Conferir identidade e
capacidades; a instalação no disco não comprova recarga numa conversa antiga.

Para documentos e operação completa, selecionar `$operar-loki`. Pedir que rode
o diagnóstico local e depois leia os documentos indicados. A harness localiza
o script na skill instalada e o executa por uv com Python3.11 e lock; o lock
acompanha as atualizações Git.

Dados estruturados e fontes seguem para o Loki pela conexão já autenticada.
Originais, imagens e estado ficam em workspace privado fora do cache do plugin.
Python/dependências são preparados pelo uv sem importar cofre Windows ou copiar
tokens. Ver [formatos e diagnóstico](LOCAL_READERS.md).

## 3. Conferir ou atualizar imediatamente

Se precisar conferir uma publicação sem esperar o próximo ciclo nativo:

```text
codex plugin marketplace upgrade loki-equipe --json
codex plugin list --marketplace loki-equipe --json
```

Conferir `errors: []`, a versão instalada e `enabled: true`, depois abrir nova
conversa. Esses comandos são uma ação manual de diagnóstico, sem cron, systemd,
automação do chat ou script periódico. Falha de acesso GitHub deve ser resolvida
na credencial pessoal do Git; ela é separada do OAuth do Loki.

Quem seguiu o roteiro anterior deve [remover a agenda externa](REMOVE_EXTERNAL_SCHEDULERS.md#codex-no-linux).
O ChatGPT continua usando a conexão MCP existente no aplicativo; instalar o
plugin local não instala outro plugin na conta ChatGPT.

Quem já tinha1.0.2 deve conferir2.1.0 ou superior avaliada e as duas skills após upgrade.
Reabrir a conversa para usar o pacote completo. Não reinstalar MCP/OAuth.

Na versão1.1.7, `$registrar-problema-loki` orienta relatos sanitizados, backlog
Slack e propostas de correção, com autorização de suporte.
Confira a skill instalada e a ação `registrar_problema` no catálogo da conexão
existente. Se faltar a ação, atualize as ferramentas pelo aplicativo e confira
novamente; o upgrade Git só atualiza o plugin local. Um teste autorizado usa
conteúdo sintético e resumo TESTE. Guarde `report_id` e `problem_id` quando
retornado; entrega confirmada exige `sent` e `message_id` no recibo. A fila
retoma pendências no servidor; acompanhe o problema sem reenvio. Leia a skill
para incerteza, decisão exclusiva do proprietário OAuth, publicação e confirmação
humana da solução. O backend conserva recibos Discord com suporte novo desligado.

Referências: [OpenAI Docs — marketplaces](https://developers.openai.com/plugins/build/plugins),
[inicialização nativa no Codex 0.163.0](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core-plugins/src/manager.rs#L2823).

Na versão1.1.5, `$investigar-regras-dp` integra a operação de fórmulas,
parâmetros e históricos incompletos. Bootstrap e operar-loki também encaminham
para essa skill. Confira versão instalada e carregue uma conversa nova;
publicação/instalação não comprovam execução da rotina de outro operador.

Na1.1.7, ao concluir execução com falha inesperada, a IA carrega a skill de
suporte e registra quando já houver autorização no escopo. Pendência prevista
não é defeito automático; falha de suporte não gera recursão. O leitor retorna
support_handoff, sem enviar dados. [Escopo e limites](SUPPORT_COLLABORATION_20261027.md).


A operação usa100%HTTPS em `https://loki.tominho.com/mcp`, com originais e
preparação na harness, parâmetros JSON/CSV tipado e retorno por documentos ou
recibo persistido quando não houver documento. Atualização Git não comprova
publicação, identidade própria da automação ou execução observada; siga
[ativação coordenada](ANA_ROUTINE_ACTIVATION.md), preservando a agenda existente.


`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
