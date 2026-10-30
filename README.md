# MCP Loki — contrato operacional 2.2.0

O pacote `mcp-loki-updates` **0.3.1** entrega instruções **2.2.0** ao backend.
A entrega padrão é autenticada ao solicitante; Drive Izzi permanece opção futura
explícita, sem configuração ou ativação nesta entrega.

O plugin nativo `loki-orientacoes@loki-equipe` **2.2.0** contém bootstrap, leitores
externos e guias de operação. A distribuição não é um servidor independente.
OAuth, autorização, cálculos, banco, documentos e decisões pertencem ao Loki.

O Loki recebe dados estruturados, valida, calcula, gera documentos, registra e
entrega. Leitura de originais e comparação são externas. O operador consulta
`get_process_contract`, captura `get_case.input_snapshot` e envia `receive_case_data`
com dados, fontes opcionais, referência idempotente e snapshot esperado. Depois segue cálculo,
geração e revisão do contrato. Versões internas preservam auditoria; a empresa de
teste usa o mesmo fluxo e gates da operação comum.

A extensão2.2.0 é aditiva ao contrato2.0.0 e conserva o mínimo de plugin2.0.0.
A migração anterior de1.x foi incompatível: ferramentas antigas de extração, comparação e
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

Compatibilidade da candidata0.3.1: fonte `loki-document-kit`0.2.0, com allowlist
operacional explícita e comandos para dados+fontes/conferência técnica. O kit0.1.0
usa escritores aposentados e precisa de migração separada. Não sobrescrever
artefatos, locks, pins ou assinaturas antigos. Esta candidata não comprova
instalação nem troca o executor da Ana. A compatibilidade básica do kit0.2.0 limita-se às operações2.0 que ele declara;
não comprova suporte aos novos escritores2.1. Build/promoção de consumidor e
backend continuam sujeitos aos gates de implantação.


Esta candidata orienta100%HTTPS em `https://loki.tominho.com/mcp`, com identidade
própria por pessoa/executor. A harness lê, extrai, interpreta e prepara; envia
parâmetros JSON/CSV tipado; proveniência detalhada é opcional. Originais permanecem na harness.
O resultado contém documentos quando gerados ou recibo persistido/relido para
atos sem documento, sem PDF artificial. Caso único, lote operacional e ajustes
da empresa exigem os contratos realmente oferecidos pelo catálogo HTTPS.
Exigência de novo anexo nativo, endpoint ausente ou identidade do executor não
provisionada é lacuna explícita; não use transporte alternativo nem reclassifique
fonte. Veja [WORKFLOWS.md](plugins/loki-bootstrap/skills/operar-loki/references/WORKFLOWS.md)
para estados, retorno e retomada; esta árvore não comprova publicação ou adoção.


`field_sources` é opcional. Informação informal ou implícita autorizada pode ser enviada em `data` sem anexo, manifesto ou hash por campo. O Loki registra automaticamente ator, data/hora, request e origem declarada. Preserve a distinção entre informado, inferido e confirmado; inferência contextual deve conservar sua justificativa quando disponível, sem virar documento lido ou confirmação independente. Proveniência detalhada e EXTSRC são recursos opcionais: EXTSRC é opcional e não é pré-requisito universal. Não bloqueie cálculo ou registro inteiro pela ausência de fonte formal. Exija comprovante ou fundamento somente quando a operação específica o requerer e mantenha a pendência limitada ao resultado dependente.

## Extensão eSocial2.2.0

Provider0.3.1, contrato/instruções/plugin2.2.0 preservam o mínimo2.0.0 e a
compatibilidade declarada de2.0/2.1; cliente desconhecido continua desconhecido.
A allowlist e as permissões dos domínios permanecem: consulte `geral` e
`alteracao_cadastral` para as cinco ferramentas HTTPS de modo fiscal e parâmetros.
Veja o roteiro nativo [ESOCIAL.md](plugins/loki-bootstrap/skills/operar-loki/references/ESOCIAL.md). A configuração de homologação
pode persistir por intenção de administrador humano; não transmite. Operação
permanece PENDING/recusada sem fila/executor fiscal, assinatura, representação
e recibo de homologação verificados. S-1005 local não comprova transmissão.
Perfis por estabelecimento/data usam os escritores empresariais com CAS,
origem opcional e releitura; seleção não comprova consumo financeiro.

Esta distribuição não provisiona acesso fiscal, não emite eventos pelo catálogo
HTTPS e não instala o plugin no operador. Wheels anteriores, inclusive0.3.0,
permanecem imutáveis; promoção/publicação exigem revisão e gates do consumidor.
