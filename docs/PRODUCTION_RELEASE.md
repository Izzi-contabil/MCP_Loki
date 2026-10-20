# Publicação em produção — 20/10/2026

Após autorização explícita do usuário, o PR #145 do Project Loki foi integrado
pelo fluxo normal do GitHub, sem bypass de proteção. O webhook existente da
`main` iniciou a publicação na aplicação Project Loki, projeto Izzi, instância
Trabalho do Coolify. O deploy terminou às 20:23:05 UTC.

| Verificação | Resultado |
|---|---|
| Build publicado | `c91c145985c2d2bd092486ff01a75ad97fb092ad` |
| Árvore Git | `53a1e30ebffc6a07f2194243fd3f65dcd3451b01`, igual à combinação validada com `main` |
| Build anterior preservado para rollback | `f08206ae60f295dce0654343463818978c59758a` |
| Coolify | Deploy concluído |
| Health público | `status=ok`, schema `0041`, calculador `rescisao-v22` |
| Provider / instruções / contrato | `0.1.0` / `1.0.0` / `1.0.0` |
| Snapshot | Disponível, status `ok` |
| Manifest SHA256 | `ff39a63c78b609cd4001906a17e76149c4401e3d00952b1bf98f93b3e65dc730` |
| Metadados OAuth | Origem correta, PKCE S256 e sem registro dinâmico de clientes |
| Inicialização MCP anônima | HTTP 401, desafio do recurso presente |
| Configuração de ambiente | Digest dos valores de produção e preview igual ao anterior |
| Banco | Mesmo schema; esta feature não acrescenta migration |

O backup diário mais recente do banco estava registrado como `success` antes da
publicação. Não foi executado restore ou downgrade. O healthcheck nativo do
Coolify continua desabilitado; a conferência acima foi externa.

Uma tentativa de smoke com o User-Agent padrão do Python recebeu HTTP 403.
O ensaio com identificação de navegador alcançou o desafio OAuth HTTP 401.
Não houve mudança de proxy, autorização ou credenciais para realizar o ensaio.

## Acesso autenticado observado

A conta autenticada nesta conversa já estava `active`, com papel `owner` e
revision `1`. A consulta `meu_acesso` após o deploy confirmou a mesma conta,
o build publicado e `runtime_instructions` para os oito domínios autorizados.
Não foi necessário alterar permissões, reaprovar a conta ou revogar sessões.
Identidade e resposta integral não foram copiadas para este repositório público.

O login Google em outro dispositivo será realizado pelo usuário. Isso continua
pendente, assim como o aceite individual das outras instalações ChatGPT e o
refresh do catálogo quando necessário. O ensaio autenticado pela ferramenta
antiga não comprova descoberta das ferramentas novas. Compatibilidade do cliente
permanece desconhecida quando ele não declara suas versões.

Não foram executadas operações em empregados, casos ou documentos de RH durante
essa publicação. A CI remota do backend permaneceu pendente por orientação do
usuário; não foi declarada aprovada. Os testes locais e seus limites estão em
[HOMOLOGATION.md](HOMOLOGATION.md).

As evidências sanitizadas e os identificadores de infraestrutura ficam em
`var/mcp-updates/production-preflight-20261020.json`,
`production-release-20261020.json` e
`production-account-verification-20261020.json` no worktree consumidor, fora do Git.
O [rollback](MCP_UPDATES.md#rollback) conserva o conjunto backend/wheel/lock e não
exige alterar OAuth ou dados para esta mudança sem migration.
