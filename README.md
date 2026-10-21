# MCP Loki — instruções e compatibilidade

Este repositório mantém o pacote `mcp-loki-updates`, as instruções versionadas por domínio e um bootstrap curto para clientes Loki. O backend incorpora o wheel e entrega as instruções pelas ferramentas MCP autorizadas. Uma alteração neste repositório só alcança o serviço depois da promoção, revisão e implantação do backend.

O pacote não é um servidor MCP independente. Identidade Google/OAuth, permissões, banco, documentos, cálculos e decisões continuam no Project Loki. O conteúdo deste repositório não concede acesso nem representa aceite humano.

A candidata usa pacote `0.1.2` e instruções de admissão `1.2.0`. Geral,
documentos e rescisão permanecem em `1.1.0`; os demais domínios, em `1.0.0`.
O [guia operacional](docs/OPERATIONAL_GUIDANCE_20261021.md) registra a entrega
anterior e o [ajuste de período salarial](docs/ADMISSION_PERIOD_20261021.md)
registra a leitura do campo e seus limites. Publicação e entrega autenticada
exigem recibos próprios.

| Versão inicial | Valor |
|---|---|
| Pacote Python | `0.1.0` |
| Instruções | `1.0.0` |
| Primeiro contrato MCP formalizado | `1.0.0` |
| Plugin mínimo / recomendado | `0.4.0` / `0.5.0` |

`0.5.0` é uma recomendação do contrato; isso não declara uma instalação observada ou um pacote ChatGPT publicado. O plugin desktop existente `0.4.0` continua compatível. Cliente sem versão declarada recebe compatibilidade desconhecida, sem ser classificado como antigo.

## Uso pelo chat

O [bootstrap](plugins/loki-bootstrap/SKILL.md) orienta o cliente a identificar-se por `meu_acesso` ou `get_operator_context` e consultar `loki_verificar_versao` e `loki_obter_instrucoes` antes do fluxo pertinente, quando essas ferramentas estiverem disponíveis. Ele evita copiar regras de negócio para cada cliente.

As respostas das duas ferramentas antigas recebem `runtime_instructions` de forma aditiva na integração do backend. Isso oferece um caminho para um cliente `0.4.0` que já consulta identidade receber orientação atualizada, sem trocar o ZIP. O modelo pode deixar de consultar uma ferramenta; o servidor continua responsável por autorização e validação. Instruções não garantem invocação ou execução.

Não há manifest de distribuição ChatGPT neste repositório: essa fonte não foi encontrada na investigação. `plugins/loki-bootstrap/` contém somente `SKILL.md` e README. Consulte [MCP_UPDATES.md](docs/MCP_UPDATES.md) para refresh manual de ferramentas e diferenças entre ChatGPT e os kits desktop.

## Desenvolvimento e promoção local

Requer Python 3.11+ e `uv`.

```powershell
uv sync --locked --all-extras --no-editable
uv run --no-sync pytest
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync mypy src scripts
uv build --wheel
uv run --no-sync python scripts/promote.py --wheel .\dist\mcp_loki_updates-0.1.2-py3-none-any.whl --loki-path "CAMINHO_DO_CHECKOUT_LOKI"
```

No Windows com Python 3.11 e locale cp1252, um checkout em caminho acentuado pode falhar ao ler o `.pth` de uma instalação editable. `--no-editable` e `--no-sync` evitam esse caminho; depois de editar o pacote, sincronize novamente antes de validar sua cópia instalada. Os testes também exercitam o fonte e o smoke deve instalar o wheel fora do checkout.

O último comando valida ZIP, identidade, bytes contra o fonte e dados com o provider confiável; copia wheel e provenance para `vendor/` do checkout explicitamente informado. Não executa código do wheel, não altera autenticação, não atualiza o lock nem faz deploy. Sem commit inicial, provenance registra `head`/`tree` nulos e `dirty=true`.

No Loki, a integração deve fixar esse wheel local por `tool.uv.sources`, regenerar `uv.lock`, revisar e testar o conjunto. Isso dispensa registry. Um build novo exige versão nova; não substitua bytes diferentes sob o mesmo nome de wheel. O [guia de atualizações](docs/MCP_UPDATES.md) cobre publicação e rollback; o [registro de implementação](docs/IMPLEMENTATION.md) delimita o escopo autorizado.

CI valida pacote, testes, lint, tipos e importação do wheel instalado em ambiente separado e oferece o wheel como artefato do workflow. Upload desse artefato não é implantação nem release pública.

O [relatório de entrega local](docs/DELIVERY.md) registra os arquivos, validações,
compatibilidade observada e pendências de lançamento e aceite das quatro contas.

A [preparação no Coolify Trabalho](docs/COOLIFY_PREPARATION.md) registra a
configuração aplicada no projeto Izzi, a CI publicada e o que falta antes do
lançamento autorizado.

A [homologação técnica local](docs/HOMOLOGATION.md) registra o candidato do PR
consumidor, os testes Linux e os limites do ensaio isolado. A CI remota do backend
ficou pendente por orientação do usuário; isso não equivale a um check aprovado.

A [publicação autorizada em produção](docs/PRODUCTION_RELEASE.md), em 20/10/2026,
registra o build implantado, o health e as instruções recebidas pela conta
autenticada. Login no outro dispositivo e aceite das quatro instalações são
verificações individuais.

O [handoff para o servidor pessoal](docs/HANDOFF_PERSONAL_SERVER.md) reúne as
referências publicadas, os resultados e limites dos testes e a pendência de
catálogo observada no piloto. Use esse checkpoint para retomar o trabalho sem
reaplicar a integração já implantada.
