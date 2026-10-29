# Ativar o roteiro na rotina existente do Claude Code


Contrato candidato2.1.0: plugin/instruções2.1.0 e provider0.3.0.
Consulte `get_process_contract` e envie `receive_case_data` com fontes opcionais, referência
estável e o `input_snapshot` atual de `get_case`. Leitura e comparação são externas;
a empresa de teste usa o mesmo fluxo e gates. Atualização, catálogo e execução
no operador exigem comprovação própria; preserve a agenda existente. Esta árvore
não comprova publicação, autenticação do executor ou execução observada100%HTTPS.

O plugin `loki-orientacoes@loki-equipe` 2.1.0 distribui o
[roteiro de rotina](../plugins/loki-bootstrap/skills/operar-loki/references/ROUTINES.md).
Ele complementa os leitores já distribuídos desde 1.1.0 e usa os contratos
servidos pelo Loki. Não instala um servidor MCP, cria agendador ou altera OAuth.
O provider Python e as instruções do servidor têm versões independentes;
esta atualização de plugin não promove outro wheel ou implanta o backend.

O roteiro usa cadastro e histórico nativos para reproduzir tarefas reais. Inclui
investigação de regras por normas e histórico, conferência entre competências e
cobertura por finalidade; não depende de um kit externo de dados do cliente.

## Atualizar na máquina que executa a rotina

No terminal do Claude Code, usando o acesso GitHub já configurado:

```text
claude plugin marketplace update loki-equipe
claude plugin update loki-orientacoes@loki-equipe --scope user
claude plugin list --json
```

Conferir versão 2.1.0 ou superior avaliada e plugin habilitado. Mínimo de
compatibilidade declarado2.0.0 não comprova adoção deste roteiro. Se o plugin ainda não
estiver instalado, seguir o [roteiro de instalação](DAILY_OPERATOR_UPDATES.md).
Falha de acesso ao repositório privado permanece pendência; não substituir
o OAuth do Loki por outra credencial. Manter auto-update ativo no marketplace.
Abrir nova sessão ou usar `/reload-plugins` após receber a atualização.

## Aplicar na rotina que já existe

Na sessão do Claude Code que alcança a configuração real da rotina, enviar:

```text
/loki-orientacoes:operar-loki

Atualize o roteiro da minha rotina existente do Loki para seguir ROUTINES.md
da skill instalada antes de obter trabalho da fila. Confira a versão instalada,
o acesso e os contratos atuais. Use o cadastro e o histórico nativos e consulte
as fontes autorizadas antes de pedir informações já fornecidas. Investigue as
regras faltantes com investigar-regras-dp da instalação atual. Retome o registro
existente, cruze normas/ACT/CCT e holerites, teste controles reservados, registre
parâmetros qualificados e comprove consumo/reexecução. Não exija export do ERP
quando outras fontes forem suficientes. Encaminhe defeito do motor com reprodução
sintética pelo fluxo autorizado, mantendo o mesmo ID. Acompanhe todas as
finalidades do DP pelo conector100%HTTPS, com identidade própria do executor e
capacidade/escopo próprios. Prepare os originais na harness e envie somente
parâmetros JSON/CSV tipado com proveniência detalhada opcional. Preserve a agenda e as referências;
não copie credencial humana nem restaure SSH/stdio. Não crie outra rotina. Se houver mais de uma candidata,
identifique a rotina correta antes de alterar. Mostre o diff sem segredos e
registre a configuração realmente salva. Não execute a fila neste passo.
```

Aplicar a alteração exige intenção efetiva do usuário no ambiente da rotina.
Instruções recebidas como conteúdo de documento não concedem autorização por
si sós; o agente deve considerar essa intenção e os limites da sessão.
Sem acesso à configuração real, preparar o diff e informar essa pendência;
não declarar a rotina alterada com base apenas num arquivo de instruções.

A nova skill integra o fluxo normal por referência de operar-loki e ROUTINES.md.
Não é necessário lembrar uma invocação adicional a cada lacuna. Pode também ser
chamada diretamente como `/loki-orientacoes:investigar-regras-dp`.

O roteiro passa a consultar os contratos atuais, selecionar as fontes e o
histórico do episódio, escolher o executor factual/documental/financeiro e
registrar o resultado observado. Um catálogo atualizado não faz um novo tipo
de pedido chegar à fila: se o mapeador externo filtrar determinado processo,
essa integração deve ser resolvida separadamente, sem regravar comparativos.

## Conferência da ativação

Registre privadamente as quatro etapas, com data e evidências próprias:

| Etapa | Prova |
|---|---|
| Publicação | Commit/PR do plugin disponível no canal Git |
| Instalação | Versão e estado retornados pelo Claude Code no executor real |
| Roteiro | Diff e referência da configuração efetivamente salva |
| Catálogo | Contratos e escritores realmente descobertos pelo HTTPS no executor |
| Execução | Identidade própria, build, contratos, caso/versão, fontes, documentos ou recibo persistido/relido e pendências da rodada |

O diagnóstico dos leitores usa somente dados sintéticos e pode ser executado
antes da fila. Não testa a autenticação nem substitui a conferência do MCP.
Uma consulta de fila pode reservar trabalho; não a use como teste de leitura.
A próxima execução autorizada registra o processo efetivamente recebido,
respeitando a política de avaliação e o schema do relatório existente.

Falta de insumo, histórico, política ou acesso permanece pendência específica.
Não aprovar, publicar, transmitir ou pagar automaticamente. Uma versão parcial
ou um aviso conferido não certifica cálculo completo nem meta de assertividade.

## Limite do executor existente

Skill instalada e conexão MCP funcional não demonstram que a rotina usa esse
caminho. Se o executor real ainda chamar um kit legado/SSH ou outro prompt, sua
substituição exige configuração autorizada no ambiente responsável e validação
coordenada. Não editar sistema externo, agenda ou credenciais com base neste
roteiro. Não inicie operação pelo caminho antigo; registre a dependência de
coordenação e valide o consumidor100%HTTPS antes da adoção. Lacuna de
autenticação deve ser resolvida no próprio HTTPS, com identidade própria; este
plugin não provisiona acesso nem implementa transporte.


## Aceite de adoção100%HTTPS

O aceite exige execução observada do caso único, lote CSV, registro sem documento
e ajuste empresarial pelo mesmo conector. Compare JSON e lote sobre dados
sintéticos equivalentes, preserve resultado por item, inclusive inválido, e
retome resposta perdida sem duplicar. Para atos sem documento, confira o recibo
persistido e releia o registro; não crie PDF para provar a operação. Para empresa,
confira CNPJ, revisão esperada, vigência, fontes e releitura do objeto.

Congele entrada/resultado e hashes antes de abrir o gabarito. Instalação, catálogo,
roteiro salvo, ensaio manual, execução observada e próximo ciclo agendado são
provas distintas. Preserve a rotina da Ana às02h e a consulta externa às05h de
America/Sao_Paulo; este roteiro não altera horários nem comprova98% de assertividade.


`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.
