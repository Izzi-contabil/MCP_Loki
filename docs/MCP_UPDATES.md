# Atualizações MCP Loki — contrato 2.0.0

Candidata de28/10/2026: provider/wheel0.2.1, instruções2.0.1 e plugin2.0.1.
Texto versionado não atualiza serviço implantado nem a instalação do operador.
O backend incorpora o wheel; o plugin tem distribuição Git própria.

## Migração incompatível

O Loki recebe dados, valida, calcula, gera documentos, registra e entrega.
Leitura documental e comparação são externas. As ferramentas antigas de extração
e execução especial foram retiradas; snapshots e evidências históricos permanecem
auditáveis. A empresa de teste usa o fluxo e gates comuns, sem modo especial.
Versões internas servem à auditoria; o fluxo é cálculo, geração e revisão.

O novo caminho é `get_process_contract(process_type)` → `get_case(case_id)` →
`receive_case_data(case_id, request)` → `run_prepared_case_workflow` ou as operações
de cálculo, geração e revisão declaradas no contrato. Os contratos de cadastro e
histórico em lote continuam sendo específicos e sujeitos a autorização.

O request `loki.case-data/1` contém `schema_version`, `request_ref`,
`expected_snapshot`, `data` e `field_sources`. O snapshot vem de
`get_case.input_snapshot`; `data` é o conteúdo da seção `data_section`, sem outro
envelope. Fontes por folha usam `kind=document|declaration|history|rule`, `reference`
e `locator`; `content_hash`/`foundation` preservam hash e fundamento quando aplicáveis.
Correção, concorrência, idempotência e gates humanos continuam no backend.

`meu_acesso` e `get_operator_context` conservam seus campos e acrescentam
`runtime_instructions`. Esse fallback entrega orientação; não restaura contratos
retirados. `loki_obter_instrucoes` mantém allowlist e autorização pelo host.
`loki_verificar_versao` compara apenas versões declaradas. Plugin mínimo permanece2.0.0;
recomendado é2.0.1. Contrato1.x declarado é incompatível; cliente desconhecido
continua `compatible=null`, sem presumir instalação. `refresh_tools_required=null`
permanece desconhecido até conferir o catálogo no aplicativo.

Prepare o consumidor e a atualização do plugin juntos, preserve backups e
proveniência e faça o corte coordenado pelos gates/runbook do backend. Não inicie
um caminho antigo se o catálogo estiver desatualizado. Atualize/reconecte o catálogo
na interface somente quando necessário, preservando OAuth e identidade. Instalar,
carregar a skill, consultar instruções e executar são provas separadas.

## Atualizar e validar

1. Edite os domínios Markdown e metadados JSON em `src/mcp_loki_updates/data/domains`.
   Use somente operações implementadas no consumidor; não invente regra trabalhista.
2. Eleve versões de domínio/instruções/contrato conforme compatibilidade. A versão
   do pacote também muda ao mudar qualquer byte distribuído. Atualize
   `pyproject.toml`, `__init__.py`, `provider.py`, `scripts/promote.py` e `uv.lock`.
   Plugin, guias e scripts têm versão própria; dependências permanecem fixadas.
3. Recalcule SHA256 dos bytes UTF-8/LF de cada Markdown e JSON em `release.json`.
   Revalide integridade, allowlist, permissões, compatibilidade antiga recusada,
   cliente desconhecido, novo writer e proveniência antes do build.
4. Execute os testes apropriados, ruff/mypy e `uv build --wheel`. Verifique os bytes
   do wheel contra o fonte com `scripts/promote.py.validate_wheel`; só então gere
   proveniência. Árvore suja usa `dirty=true` e HEAD/tree da base, nunca release
   commitada fictícia. Não renomeie um wheel anterior nem sobrescreva bytes distintos
   sob a mesma versão.
5. Promoção ao checkout consumidor exige destino explícito, wheel e proveniência.
   O script copia esses artefatos; não modifica lock, OAuth, permissões ou deploy.
   O consumidor fixa wheel, revisa lock e valida integração. Build local não comprova
   publicação, descoberta MCP, rotina instalada nem aceite individual.

No servidor, siga `AGENTS.md` de cada repositório e use a `.venv` própria existente.
Não aponte testes destrutivos ao banco real. Não faça commit, push, merge ou deploy
por consequência de construir/validar o pacote; siga a autorização vigente.

## Entrega e rollback

Drive Izzi e solicitante são destinos operacionais quando habilitados no host.
Destino, pacote/revisão/hash e recibo são necessários. Falha ou destino ausente
permanece pendente; retry não duplica entrega nem recalcula. Geração ou conferência
não atesta envio, aceite, pagamento ou transmissão.

Rollback restaura o conjunto backend+wheel+lock compatível e segue o runbook do
consumidor, incluindo conciliação de novas escritas. Não faça downgrade de banco,
altere pin/assinatura do kit legado ou troque identidade para contornar falha.
Os registros anteriores de publicação em `docs/` são históricos e preservados;
não comprovam o estado servido desta candidata nem atualização das instalações.

A candidata0.2.1 acrescenta os contratos de conferência técnica externa, abertura selecionada e autorização própria de entrega privada; contrato MCP permanece2.0.0. O wheel0.2.0 já construído permanece imutável.

Compatibilidade da candidata0.2.1: fonte `loki-document-kit`0.2.0, com allowlist
operacional explícita e comandos para dados+fontes/conferência técnica. O kit0.1.0
usa escritores aposentados e precisa de migração separada. Não sobrescrever
artefatos, locks, pins ou assinaturas antigos. Esta candidata não comprova
instalação nem troca o executor da Ana. Build/promoção do kit e do backend
continuam sujeitos aos gates de implantação.
