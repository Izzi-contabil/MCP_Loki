> Registro histórico de 20/10/2026, preservado de notas locais durante a limpeza
> de 21/10/2026. Builds, versões, contagens e telas descritos abaixo pertencem
> àquele registro e não certificam o estado atual. Para instalar e atualizar
> hoje, usar os roteiros de [Claude Code](DAILY_OPERATOR_UPDATES.md) e
> [Codex](CODEX_LINUX_SETUP.md). O repositório agora usa a branch padrão `main`.

# Descoberta de ferramentas e migração das contas — ChatGPT e Codex

Procedimento de leitura e atualização do catálogo, conferido na documentação
oficial em 20/10/2026. A integração do PR #145 já foi publicada; este procedimento
não requer repeti-la. O [handoff](HANDOFF_PERSONAL_SERVER.md) registra a release
inicial e os limites dos testes anteriores.

O escopo confirmado pelo usuário inclui **ChatGPT e Codex**. O resultado válido
em cada produto conta como entrega própria. Registrar por conta e produto:
sucesso no Codex não exige repetir o mesmo ensaio naquele produto e não preenche
o resultado do ChatGPT. Ambos usam a autorização do backend; esta migração trata
da descoberta e do uso das ferramentas, preservando as permissões vigentes.

## Identificar a instalação antes de agir

Abrir **Loki → Gerenciar** na conta piloto e registrar os rótulos realmente
visíveis. Nome, autor, versão da listagem e descrições de ferramentas não bastam
para determinar a origem. O conector disponível no Codex também não comprova
qual configuração foi usada na conta ChatGPT.

| Evidência da configuração | Procedimento aplicável |
|---|---|
| MCP personalizado direto, com URL, OAuth, estado de desenvolvimento e Refresh tools | Atualizar os metadados pela conexão existente; conferir catálogo e testar em nova conversa |
| Plugin publicado, identificado no portal do desenvolvedor | Inspecionar o servidor em MCPs e a disponibilidade das ferramentas; usar a varredura do portal quando aplicável |
| Pacote/skill importado, com fonte de distribuição identificada | Conferir a fonte existente e sua versão antes de preparar qualquer atualização individual |
| Só nome, versão ou lista de ferramentas | Origem ainda desconhecida; obter os detalhes de Gerenciar antes de escolher o caminho |

Não criar um manifest para substituir uma fonte desconhecida. O bootstrap deste
repositório não é um instalador ChatGPT. Os manifests do kit desktop do backend
não identificam automaticamente a instalação remota do ChatGPT.

## Atualizar pelo mecanismo confirmado

Para **MCP direto**, abrir a conexão existente e selecionar **Refresh** ou
**Refresh tools**, conforme o rótulo efetivamente observado. Verificar os
metadados anunciados e iniciar nova conversa. O passo de implantação do servidor
já foi cumprido pela release entregue; a ausência de uma ferramenta no catálogo,
isoladamente, não justifica outro deploy.
Fonte: [Connect and test — Refresh metadata](https://developers.openai.com/plugins/deploy/connect-chatgpt#refresh-metadata).

Para **plugin publicado**, abrir o plugin existente no portal, selecionar
**MCPs → servidor conectado → Issues → Rescan**, quando esse controle estiver
disponível, e aguardar o resultado. Conferir individualmente as ferramentas
novas, **Live definition**, **Held update** e os achados. Uma ferramenta nova
pode permanecer indisponível enquanto sua definição não for aprovada. Atualizar
metadados/skills do pacote tem fluxo próprio de versão, revisão e publicação;
mudanças de ferramentas hospedadas não exigem por si só outro ZIP.
Fonte: [Submit and publish — MCP updates](https://developers.openai.com/plugins/deploy/submission#update-to-your-mcp-server).

Esses mecanismos dependem da instalação real e do acesso à interface. Os tools
de gerenciamento disponíveis nesta retomada não expõem Refresh/Rescan. Busca de
plugins sem resultado não prova que o Loki instalado deixou de existir.
Preservar a conexão funcional. Não desinstalar, desconectar ou reconectar como
experimento. Não alterar permissões ou habilitar ferramentas se a interface
exigir uma concessão adicional; registrar a exigência para autorização própria.

## Aceite do piloto em cada produto, somente por leitura

No **Codex**, usar uma conversa nova com o Loki disponível e executar o pedido
abaixo. Registrar o produto e a conta autenticada. Uma conexão já validada pode
ser registrada como sucesso no Codex, sem repetir chamadas somente porque falta
testar o ChatGPT.

No **ChatGPT**, abrir [ChatGPT no navegador](https://chatgpt.com/),
entrar na conta piloto, selecionar **Work**, iniciar uma conversa nova e escolher
Loki pelo `@`. Esse percurso consta no
[quickstart oficial](https://developers.openai.com/plugins/quickstart#test-the-plugin).
Se usar **Try now**, conferir em qual produto a conversa foi aberta. Um teste
realizado no Codex deve ser registrado como Codex e não conclui o piloto ChatGPT.

Usar o mesmo pedido de leitura nos dois produtos:

> Use o Loki somente para leituras. Consulte meu_acesso e confira identidade,
> estado e escopo sem reproduzir dados pessoais. Se estiverem disponíveis no
> catálogo, chame loki_verificar_versao sem inventar versões do cliente e
> loki_obter_instrucoes para geral e, se autorizado, rescisao. Informe quais
> ferramentas realmente foram chamadas, build, versão e hash das instruções.
> Se alguma ferramenta estiver ausente, registre a ausência e confira o conteúdo
> correspondente em runtime_instructions de meu_acesso. Não crie casos nem faça
> operações de RH, decisões, cálculos, documentos ou mudanças de acesso.

Não passar versões do pacote Python ou da listagem como se fossem a versão
declarada pelo cliente deste contrato. Sem declaração comprovada, compatibilidade
e necessidade de atualização podem continuar `null`.

Registrar separadamente: ferramenta visível; invocação real; resultado; erro ou
recusa; caminho de fallback; build; versões e hash. Comparar com o estado atual
da produção, sem rebaixar uma release posterior. Receber o texto pelo fallback
prova esse caminho; não conclui a descoberta das duas ferramentas novas.

## Quatro contas, quatro registros com resultados por produto

Manter um arquivo privado por conta, sem identidades ou evidências operacionais
neste repositório. Cada arquivo distingue **Codex** e **ChatGPT**, com resultado,
origem da evidência e vínculo da conta autenticada. Identificar a conta antes
de associar a ela um teste. Depois do piloto de cada produto, repetir nas outras
contas que o utilizarem, individualmente, conservando seus escopos. O teste já
validado em um produto pode prosseguir para as demais contas desse produto.

Cada registro deve distinguir identidade/escopo autenticados, tipo e fonte da
instalação, atualização efetivamente executada, conversa nova, catálogo, chamadas
e resultados. Não preencher lacunas com o resultado de outra conta. Não presumir
sincronização automática entre produtos/contas ou login observado a partir de
relato do usuário. Um resultado ainda sem vínculo de identidade fica registrado
como sucesso da conexão testada, sem preencher outras contas.

Recusas de autorização são verificadas com os testes sintéticos do backend;
não consultar empresas reais fora do escopo nem criar casos para esse ensaio.
Uma recusa legítima não autoriza ampliar permissões. Declarar descoberta e
migração concluídas somente para a conta que produziu suas próprias evidências.

## Incremento de sugestões e feedbacks

O [PR #140](https://github.com/T0minh0/Project-loki/pull/140) acrescenta
`registrar_problema` ao conector HTTPS, para erros e pedidos de ajuste. Conferir
o estado publicado no PR e no build informado pelo servidor antes de atualizar
o catálogo. O aceite das consultas de instruções já obtido permanece registrado;
a descoberta dessa ação é uma evidência adicional por conta e produto.

No MCP direto, usar **Refresh tools** na conexão existente e conferir a ação
entre as ferramentas de escrita. O catálogo combinado testado tem 94 ferramentas
(41 de leitura e 53 demais); a contagem sozinha não comprova que o nome apareceu.
No Codex, conferir o catálogo efetivamente exposto à conversa e seguir a fonte
real da instalação. Não presumir que atualizar um produto atualiza o outro.

Conferir o nome e o schema sem chamar a ação. `registrar_problema` pode enviar
uma mensagem ao suporte; um teste de entrega exige autorização para esse envio,
relato sanitizado e confirmação do recibo. Não usar dados de RH, documentos,
credenciais ou logs brutos como conteúdo de teste. Registrar separadamente
descoberta, invocação e entrega confirmada, pendente ou incerta.

A skill `registrar-problema-loki` acompanha o plugin desktop IZZI Loki 0.5.0.
Esse pacote, o app MCP do ChatGPT, o provider Python e as instruções versionadas
têm ciclos distintos. A distribuição assinada do kit mantém seus controles
administrativos e pins; o refresh do catálogo não os substitui.
