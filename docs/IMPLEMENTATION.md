# Implementação local — 19/10/2026

O usuário autorizou a criação de `MCP_Loki` separado e a preparação local da integração, com bootstrap estável, instruções dinâmicas e compatibilidade com quatro contas ChatGPT individuais. O trabalho atual prepara fontes e artefatos revisáveis, sem commit, push, deploy ou alteração de contas.

## Desenho investigado

A raiz `Project_loki` estava em `0742bfcb`, branch de rescisão de 22/09. A referência local `origin/main` estava em `64d8e02` de 19/10. A integração usa worktree isolado `mcp-dynamic-updates-20261019` a partir desse SHA, preservando os outros worktrees e suas alterações.

Nesse ponto, `src/loki/connector/server.py` contém o conector OAuth/Streamable HTTP usado pelo ChatGPT; suas instruções eram uma string estática. `connector/operations.py` exporta explicitamente ferramentas dos serviços existentes e aplica escopo por conta. `connector/oauth.py` usa clientes pré-cadastrados, PKCE e tokens opacos. `connector/access.py` mantém contas e concessões; login não-owner exige identidade Google corporativa com domínio e claim `hd` configurados.

O plugin desktop encontrado era `izzi-loki` 0.4.0, com skill longa e runtime preso a build. O cache administrativo local indicava build `64d8e02` e transporte SSH stdio; os scripts também suportam HTTPS com bridge local e cofre Windows. `scripts/operator_release.py` constrói bundle assinado dos objetos Git e `plugins/izzi-loki/scripts/prepare.py` prepara runtime pessoal. O empacotamento pessoal de dois operadores encontrado fora do repo era anterior, de 17/10. A investigação não encontrou fonte de manifest/pacote ChatGPT. Não copiar estado privado nem inferir instalação dos operadores desses registros administrativos.

## Entregas e fases

1. **Inventário:** identificar origem atual, transporte remoto, kits locais e limites de atualização; registrar sem dados privados.
2. **Pacote:** provider local versionado com conteúdo por domínio, hashes, carregamento atômico e último snapshot válido. Instruções `1.0.0`; primeiro contrato formal `1.0.0`; pacote `0.1.0`.
3. **Integração aditiva:** duas ferramentas novas e `runtime_instructions` nas respostas antigas de identidade. A conta e o escopo vêm do host; o pacote não contém autorização.
4. **Bootstrap e promoção:** guia mínimo central e wheel local com provenance; pin em `vendor/` e lock do backend. Não reescrever assinatura ou launchers desktop.
5. **Verificação e revisão:** testar isolamento, fallback, falhas do provider, versões desconhecidas e wheel instalado fora do fonte. Preparar diferenças revisáveis, sem implantar nesta tarefa.
6. **Lançamento posterior:** somente mediante autorização correspondente, implantar o backend e observar quatro contas reais, catálogo, acesso e fluxos permitidos. Registrar aceite observado, sem convertê-lo em aprovação de documentos.

O host acrescenta `runtime_instructions` a `meu_acesso` e ao `get_operator_context` HTTP, sem mudar suas assinaturas antigas. O bootstrap consulta domínios autorizados e versão; as tools novas são `loki_obter_instrucoes(dominio, empresa_id=None)` e `loki_verificar_versao(client_plugin_version=None, client_contract_version=None)`. Isso entrega orientação atual para clientes antigos que consultem essas tools de identidade, sem garantir consulta pelo modelo.

`compatible` e `manual_update_required` permanecem desconhecidos quando faltam versões do cliente. `refresh_tools_required` não é inferido da versão do pacote. A versão recomendada 0.5.0 não torna 0.4.0 incompatível. O [runbook](MCP_UPDATES.md) separa promoção, implantação, refresh e aceite.
