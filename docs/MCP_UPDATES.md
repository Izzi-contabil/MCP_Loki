# Atualizações MCP Loki

As instruções são dados versionados incorporados ao backend, consultados no momento do uso. Alterar Markdown neste repo não atualiza um serviço já implantado. O pacote não consulta Git, downloads remotos ou registry em produção.

## Superfícies e versões

O conector remoto OAuth/Streamable HTTP atende o ChatGPT com identidade Google e permissões persistidas. O kit desktop Claude Code/Codex tem executáveis, leitores locais, checkpoints, assinatura de bundle, runtime pessoal e preflight do build exato. São caminhos diferentes; esta mudança preserva a função dos scripts desktop.

| Componente | Versão inicial | Significado |
|---|---|---|
| `mcp-loki-updates` | `0.1.0` | Código Python incorporado ao host |
| Instruções gerais | `1.0.0` | Conteúdo inicial do provider |
| Contrato MCP | `1.0.0` | Primeira formalização de compatibilidade |
| Plugin mínimo | `0.4.0` | Cliente existente que conserva a interface antiga |
| Plugin recomendado | `0.5.0` | Bootstrap central recomendado; não é mínimo obrigatório |
| Backend | informado pelo host | Versão de aplicação e build real, ou origem desconhecida |

`versions_by_domain` identifica o conteúdo de cada domínio. `client_plugin_version` e `client_contract_version` são opcionais. Quando ausentes, `compatible` e `manual_update_required` são `null`: o servidor não conhece a versão instalada. A versão do pacote Python não identifica o cliente.

`mcp_contract_version` identifica o contrato de aplicação do Loki formalizado nesta entrega. O `protocolVersion` da inicialização MCP continua sendo negociado pelo SDK existente. As instalações anteriores não tinham uma versão observada desse contrato de aplicação.

O primeiro contrato formal não reclassifica clientes antigos como quebrados. Ferramentas novas são aditivas; o host conserva assinaturas existentes e acrescenta `runtime_instructions` a `meu_acesso` e ao `get_operator_context` HTTP. Quando essas consultas já fazem parte do cliente 0.4.0, a nova orientação pode chegar pela resposta sem ZIP novo. Isso depende de a consulta acontecer.

## O que exige implantação e ação do usuário

| Mudança | Deploy backend | ZIP desktop | Ação no ChatGPT |
|---|---|---|---|
| Texto/metadados de instruções, mesma API | Sim, com wheel revisado | Não para obter texto por tools antigas; kit conserva seu preflight | Nova consulta; não há garantia de invocação pelo modelo |
| Nova tool ou mudança de schema | Sim | Só se o código/helper local depender dela | Catálogo pode exigir refresh manual/reconexão; conferir no aplicativo |
| Campo aditivo em resposta antiga | Sim | Não por esse campo isolado | Consultar novamente a tool antiga |
| Correção no helper, leitor ou launcher desktop | Conforme dependência | Sim, pelo fluxo assinado existente | Sem efeito direto no conector remoto |
| Skill/bootstrap importado ou manifest da instalação | Conforme integração | Sim, se o pacote foi distribuído em ZIP | Atualização individual do pacote/skill; texto no servidor não reescreve a instalação |
| Contrato incompatível ou mínimo de cliente maior | Sim, com migração explícita | Conforme cliente afetado | Seguir instrução específica de atualização; preservar o caminho anterior enquanto suportado |
| Permissão, status ou revogação de conta | Operação administrativa própria | Não é mudança de código do kit | Novo login ou ajuste de acesso somente quando necessário e autorizado |

`refresh_tools_required` fica `null`, pois a consulta não comprova a sincronização do catálogo do aplicativo. `manual_update_required` descreve a comparação de versões declaradas; não comprova que o humano atualizou/reconectou a conexão. Não há promessa de instalação automática, atualização de catálogo ou de execução obrigatória das consultas pelo modelo.

## Contratos disponíveis

- `loki_obter_instrucoes(dominio, empresa_id=None)` devolve conteúdo e metadados autorizados; domínio é escolhido por allowlist, nunca tratado como caminho.
- `loki_verificar_versao(client_plugin_version=None, client_contract_version=None)` informa versões, diferenças conhecidas, ação e incerteza do cliente.
- `meu_acesso` e `get_operator_context` HTTP conservam dados antigos e acrescentam `runtime_instructions`, com orientação e versão para o acesso corrente.
- `get_document_processing_contract`, `get_company_onboarding_contract`, `list_workflows` e demais contratos do host continuam sendo consultados para schemas e validação do processo.

O host verifica empresa, processo e capacidades conforme os metadados `permissions` do domínio e filtra o conteúdo devolvido à conta. O provider pode carregar/consultar internamente o snapshot antes dessa verificação; ele não é a fronteira de autorização. Nenhuma instrução concede acesso e não há um domínio administrativo separado nesta implementação.

Conteúdo ausente/corrompido durante reload conserva o último snapshot válido e sinaliza degradação; o health do host retorna 503. Um snapshot inicial inválido aborta a inicialização da candidata, exigindo corrigir o artefato ou voltar ao build anterior. A disponibilidade da versão anterior durante essa falha depende do mecanismo de implantação e precisa ser observada no ambiente; esta entrega não comprova rolling deploy nem continuidade das tools antigas. Não inventar regras para uma escrita dependente da orientação indisponível.

## Atualizar um procedimento

1. Edite `src/mcp_loki_updates/data/domains/<dominio>.md`, usando somente comportamento comprovado no host. Não adicione regra trabalhista ou capacidade que o runtime não implementa. Os JSONs adjacentes declaram versão SemVer, data ISO, compatibilidade e permissões do domínio.
2. Incremente a versão desse domínio e `instructions_version`/`updated_at` em `data/release.json`; registre o efeito relevante na categoria correspondente de `changes`. Texto compatível não exige mudar `contract_version` nem a versão mínima do plugin. Mudança de requisito de acesso precisa de revisão e testes de autorização do host.
3. Salve os arquivos UTF-8 com LF, como exige `.gitattributes`. Recalcule SHA256 dos bytes dos dois arquivos por domínio no manifest. Exemplo executado na raiz, com Python 3.11+:

```python
from pathlib import Path
import hashlib
import json

data = Path("src/mcp_loki_updates/data")
path = data / "release.json"
release = json.loads(path.read_text(encoding="utf-8"))
for domain, hashes in release["domains"].items():
    for suffix, key in (("json", "metadata_sha256"), ("md", "content_sha256")):
        content = (data / "domains" / f"{domain}.{suffix}").read_bytes()
        assert b"\r\n" not in content, "Normalize LF antes de calcular o hash"
        hashes[key] = hashlib.sha256(content).hexdigest()
path.write_text(
    json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)
```

4. Cada wheel publicado tem identidade imutável. Para outra release, incremente a versão do pacote em `pyproject.toml`, `__version__` em `src/mcp_loki_updates/__init__.py`, `PROVIDER_VERSION` no provider e `VERSION` no promotor; ajuste o smoke CI que confere a versão, regenere `uv.lock` e siga o README. Não reutilize o nome de uma release já distribuída para bytes diferentes.
5. Confira `git status` e as diferenças; prepare no índice somente as fontes revisadas. O teste `test_instruction_snapshot_from_git_index_is_valid` carrega os bytes que o Git realmente entregará e detecta diferenças de hashes após normalização. Execute testes, lint, tipos e smoke antes da promoção. Não edite o índice para fazer um snapshot inválido parecer aceito.

## Adicionar domínio e evoluir ferramentas

Para um novo domínio, confirme primeiro o processo/capacidades no host. Acrescente o identificador à allowlist `DOMAINS`, JSON/Markdown e entrada de hashes do release; ajuste a validação de processos permitidos do provider quando necessário. Toda entrada continua declarativa. Teste consulta permitida, consulta sem permissão, empresa fora do escopo, bootstrap filtrado e erro de domínio inválido. Não basta acrescentar um arquivo solto. Promova nova versão do pacote e implante o host.

Uma tool nova exige registro explícito no conector e autorização individual da ação. Preserve nomes, parâmetros, defaults, campos e anotações dos consumidores existentes; a fixture `mcp_contract_64d8e02_masked.json` impede apagar essa evidência para aceitar uma quebra. Operações antigas continuam usando os próprios gates. Se a evolução exigir interface incompatível, mantenha uma adaptação da interface antiga durante a migração, documente o prazo e atualize o contrato/cliente de forma explícita. O provider atual aceita apenas major `1` do contrato; outro major exige também uma implementação compatível, nunca apenas alterar JSON.

Testes de contrato não demonstram que o ChatGPT descobriu uma tool nova. Para conexão direta, conferir Refresh individual e nova conversa; para skill/manifest importado, atualizar o pacote correspondente. Nenhuma atualização da instrução obriga invocação pela harness.

## Promoção revisável, sem deploy

1. Confira branch, `git status`, diferenças e versão. Preserve alterações de outras sessões. Uma promoção suja deve ficar identificada como preparação local.
2. Execute testes/lint/tipos e construa com `uv build --wheel`. Instale o wheel em ambiente isolado e confirme o provider e seus dados; o CI repete esse smoke fora do diretório fonte.
3. Depois do sync sem editable descrito no README, rode `uv run --no-sync python scripts/promote.py --wheel CAMINHO_DO_WHEEL --loki-path CAMINHO_DO_CHECKOUT_LOKI`. O script exige destino explícito, valida allowlist/ZIP, identidade, versão e RECORD, compara os membros do pacote com o fonte corrente e valida somente os dados extraídos com o provider confiável. Não importa nem executa código do wheel.
4. Revise `vendor/mcp_loki_updates-0.1.0-py3-none-any.whl` e o JSON `.provenance.json`. Ele registra SHA256, hashes por membro, HEAD/tree quando existentes e dirty explícito. HEAD/tree nulos significam repo ainda sem commit. Hash e proveniência local não equivalem a assinatura de release.
5. No Loki, fixe a dependência local em `tool.uv.sources` e nos extras `mcp-updates` e `dev`; regenere `uv.lock` com uv e revise lock, integração e regressões do host. O script não altera esses arquivos. Wheel e provenance existentes com bytes diferentes são recusados; suba a versão para outra release.
6. Prepare a revisão/PR conforme as regras dos dois repos. Commit, push, publicação remota e implantação dependem do escopo autorizado. A publicação posterior desta integração está registrada em [HOMOLOGATION.md](HOMOLOGATION.md); autorização de publicação de branch não autoriza merge ou deploy em produção.

O pipeline CI executa sync congelado, pytest, ruff, mypy, build e smoke do wheel instalado em venv separado. O artefato do workflow facilita revisão; não publica no registry e não implanta. Os scripts de assinatura e launchers desktop permanecem nos seus projetos de origem.

No servidor Loki, a instalação é `uv sync --frozen --no-dev --extra mcp-updates`. Nixpacks instala esse extra explicitamente; a CI do host usa `uv sync --frozen --extra dev --extra mcp-updates` e executa as etapas seguintes com `uv run --no-sync`. O extra `dev` também inclui o provider para preservar os comandos locais existentes. O host permanece editable, como exige sua resolução atual de catálogos. O pacote de instruções é o wheel autocontido.

O array de comandos do Nixpacks conserva `...` antes do sync adicional: isso mantém o bootstrap Python existente, que cria `/opt/venv` e instala uv. Substituir esse bootstrap por um `uv sync` isolado pressuporia um executável ainda não instalado. A [extensão de arrays](https://nixpacks.com/docs/configuration/file) é o mecanismo documentado para conservar os comandos do provider.

A dependência não entra na instalação base: o exportador do kit desktop assinado lê somente as dependências base e continua gerando requisitos com hashes sem referência ao wheel local. Sem conector habilitado, stdio e `/healthz` funcionam sem importar o provider. Com `CONNECTOR_ENABLED=true`, sua ausência ou snapshot inicial inválido impede iniciar a candidata.

O remoto [T0minh0/MCP_Loki](https://github.com/T0minh0/MCP_Loki) recebeu o commit inicial `c0af9ed`, na branch `feature/dynamic-instructions`; a CI desse commit passou. O PR consumidor #145 foi integrado e implantado em produção no build `c91c145`, após autorização explícita do usuário. O [registro da publicação](PRODUCTION_RELEASE.md) confirma o health e a resposta autenticada das instruções. A [homologação local](HOMOLOGATION.md) delimita os candidatos e os ensaios anteriores. A CI remota do consumidor permaneceu pendente por orientação do usuário; não foi declarada aprovada nem desabilitada. O deploy usa o Coolify/Nixpacks existente. Não foi criado webhook, pull automático ou pipeline público de deploy. A [preparação](COOLIFY_PREPARATION.md) registra os metadados configurados e o auto-deploy de `main`, que já estava ativo.

Na implantação com conector habilitado, conferir `/healthz`: `build`, `schema` e `dynamic_instructions` devem corresponder à release aprovada. Com OAuth individual, chamar `loki_verificar_versao` ou consultar a versão dentro de `runtime_instructions` em `meu_acesso`; comparar `backend_build`, versões e `release_sha256`. Build `desconhecido` permanece uma lacuna a resolver na configuração de release, nunca evidência de paridade. A nova inicialização valida o provider antes das migrations. Nenhuma migration ou alteração de OAuth foi adicionada por esta feature.

## Migração em seis fases

| Fase | Entrega verificável | Limite |
|---|---|---|
| 1. Inventário | SHA de origem, transporte e fontes de distribuição registrados | Histórico salvo não prova produção atual |
| 2. Conteúdo | Domínios, versões, hashes e testes do provider | Sem dados de cliente ou decisões |
| 3. Compatibilidade | Tools novas e respostas antigas aditivas | Nenhum campo antigo removido; unknown preservado |
| 4. Artefato | Wheel, smoke e provenance revisáveis no host | Sem registry, deploy ou edição de OAuth |
| 5. Implantação autorizada | Build e health observados depois do lançamento | Teste local não comprova implantação |
| 6. Aceite individual | Quatro contas verificadas, com evidências separadas | Não inferir aceite de uma conta a partir de outra |

## Checklist das quatro contas individuais

O código permite contas independentes; não exige um workspace ChatGPT compartilhado. A disponibilidade da conexão customizada, sua configuração e atualização do catálogo precisam ser conferidas em cada conta/plano real. Esta documentação não certifica suporte de produto sem ensaio.

O login Google é uma identidade separada da conta ChatGPT. No backend investigado, não-owner precisa de email verificado, claim corporativo `hd` e domínio configurado; Gmail pessoal fora desse domínio é recusado. Contas novas ficam pendentes até concessão administrativa. Não mudar essa regra como consequência de uma atualização de instruções.

| Evidência por conta | Conta 1 | Conta 2 | Conta 3 | Conta 4 |
|---|---|---|---|---|
| Conexão disponível e configurada no aplicativo | Pendente | Pendente | Pendente | Pendente |
| Login Google e identidade observados | Pendente | Pendente | Pendente | Pendente |
| Status/capacidades/empresas conferidos | Pendente | Pendente | Pendente | Pendente |
| `runtime_instructions` por tool antiga observado | Pendente | Pendente | Pendente | Pendente |
| Catálogo novo ou necessidade de refresh documentada | Pendente | Pendente | Pendente | Pendente |
| Domínio autorizado e recusa fora do escopo observados | Pendente | Pendente | Pendente | Pendente |
| Fluxo de ensaio autorizado e retomada observados | Pendente | Pendente | Pendente | Pendente |

Use referências de evidências privadas no ambiente apropriado, sem trazê-las para Git. Não registre aprovação de pacote documental, concessão de acesso ou aceite de instalação só porque o provider respondeu.

## Rollback

Antes da implantação autorizada, registre build backend, wheel/digest, lock e versão de instruções anteriores. O rollback restaura o **conjunto** revisado: build backend e wheel/lock correspondentes. Um wheel anterior não deve ser renomeado com a versão nova. Siga o runbook operacional do Loki; este repo não aciona infraestrutura.

Confira também a diferença entre o schema implantado e a base aprovada do consumidor. Esta feature não cria migration, mas a base `3ff2533` já inclui `0041`. O rollback do pacote não autoriza downgrade de banco nem garante que uma imagem anterior seja compatível com migrations intermediárias. A migration `0041` possui recusa de downgrade quando existem cálculos operacionais de férias; não contorne essa guarda.

Se a falha for apenas de novo conteúdo em um processo em execução, a retenção do último snapshot válido limita a falha; ela não substitui rollback de release ou restauração após reinício. O provedor sinaliza degradação. Não editar permissões, clientes OAuth, tokens ou bancos como forma de voltar instruções. Para kits desktop, preserve o pin/assinatura e o mecanismo de rollback já existente; não edite `expected_build` para vencer preflight.
