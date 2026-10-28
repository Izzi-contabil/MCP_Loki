# MCP Loki — contrato operacional 2.0.0

O pacote `mcp-loki-updates` **0.2.2** entrega instruções **2.0.2** ao backend.
A entrega padrão é autenticada ao solicitante; Drive Izzi permanece opção futura
explícita, sem configuração ou ativação nesta entrega.

O plugin nativo `loki-orientacoes@loki-equipe` **2.0.2** contém bootstrap, leitores
externos e guias de operação. A distribuição não é um servidor independente.
OAuth, autorização, cálculos, banco, documentos e decisões pertencem ao Loki.

O Loki recebe dados estruturados, valida, calcula, gera documentos, registra e
entrega. Leitura de originais e comparação são externas. O operador consulta
`get_process_contract`, captura `get_case.input_snapshot` e envia `receive_case_data`
com dados, fontes, referência idempotente e snapshot esperado. Depois segue cálculo,
geração e revisão do contrato. Versões internas preservam auditoria; a empresa de
teste usa o mesmo fluxo e gates da operação comum.

Esta é uma mudança incompatível: ferramentas antigas de extração, comparação e
execução especial foram retiradas. Clientes que declaram contrato/plugin1.x
precisam migrar. Cliente sem versão permanece desconhecido; bootstrap de identidade
não restaura ferramentas retiradas. O catálogo do aplicativo e a instalação no
operador exigem verificação própria. Esta árvore candidata não comprova deploy.

- [Contrato, migração e promoção](docs/MCP_UPDATES.md).
- [Skill operacional](plugins/loki-bootstrap/skills/operar-loki/SKILL.md) e
  [dados/fontes e retomada](plugins/loki-bootstrap/skills/operar-loki/references/WORKFLOWS.md).
- [Instalação e atualização](docs/DAILY_OPERATOR_UPDATES.md),
  [Codex Linux](docs/CODEX_LINUX_SETUP.md) e [ativação da rotina](docs/ANA_ROUTINE_ACTIVATION.md).
- [Leitores externos e limites](docs/LOCAL_READERS.md).

Para desenvolvimento use a `.venv` própria existente, Python3.11 e o lock vigente.
Valide testes apropriados, ruff e mypy antes de construir `uv build --wheel`.
Um wheel tem versão imutável. Promoção usa `scripts/promote.py` com destino explícito,
validação e proveniência honesta de HEAD/tree/dirty; não implanta nem muda OAuth.
Não substitua bytes sob a mesma versão. Lock, wheel, consumidor e publicação exigem
validação separada. Dados pessoais, fontes privadas e credenciais ficam fora do Git.

Os documentos de releases anteriores em `docs/` são históricos; não definem o
contrato operacional atual nem demonstram instalação, consumo ou aceite individual.

Compatibilidade da candidata0.2.2: fonte `loki-document-kit`0.2.0, com allowlist
operacional explícita e comandos para dados+fontes/conferência técnica. O kit0.1.0
usa escritores aposentados e precisa de migração separada. Não sobrescrever
artefatos, locks, pins ou assinaturas antigos. Esta candidata não comprova
instalação nem troca o executor da Ana. Build/promoção do kit e do backend
continuam sujeitos aos gates de implantação.
