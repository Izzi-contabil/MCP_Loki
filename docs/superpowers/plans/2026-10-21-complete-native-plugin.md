# Plugin completo — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** distribuir leitores locais e operação pela harness no plugin Git já instalado.
**Architecture:** scripts offline portáveis, dependências com hashes, skill operacional
e bootstrap compatível; envio pela conexão MCP existente.
**Tech Stack:** Python3.11, uv script lock, pypdf/pypdfium2/Pillow, openpyxl/xlrd,
defusedxml/jsonschema, Claude Code e Codex nativos.
**Spec:** ../specs/2026-10-21-complete-native-plugin-design.md

## Global Constraints

- Mac/Windows/Linux; somente parâmetros e CSVs enviados pela harness.
- OAuth/configuração existente intocados; sem rede nos leitores.
- Sem ZIP de distribuição, scheduler ou dependência do backend Python.
- Manter nome do plugin; versão1.1.0; estado fora do cache Git.
- Dados sintéticos nos testes, sem segredos ou dados pessoais no Git.

## Review Focus

- Arquivos ativos, ZIP traversal/bomb, XML DTD e PDF JavaScript devem ser recusados.
- PDF digitalizado sem texto deve gerar imagens e permanecer pendente de visão.
- Saída existente/symlink, entrada alterada e caminhos com espaços não podem perder dados.
- CSV deve preservar zero/null/false/listas e fonte real, sem alegar arquivo original remoto.
- Atualização nativa deve carregar scripts/lock novos sem tocar em OAuth ou estado local.

### Task1 — leitores offline

- [x] Escrever testes de formatos, limites, saída privada e conteúdo ativo; observar RED.
- [x] Implementar `read_document(path, output, encoding='utf-8-sig')` e inventário
      em `plugins/loki-bootstrap/skills/operar-loki/scripts/loki_readers/`.
- [x] Adicionar CLI `loki_local.py` com PEP723 e lock; observar GREEN real.

### Task2 — parâmetros e CSVs

- [x] Escrever testes de schema local, CSV determinístico e tipo/proveniência; observar RED.
- [x] Implementar `render_records(records, contract)` e `csv_request(...)`, sem
      execução MCP. Validar com parser real do Project-loki fora do pacote.
- [x] Testar recibos/retries e impedir envio acidental de PDF por helper.

### Task3 — integração e publicação

- [x] Skill `operar-loki`, bootstrap compatível e manifest1.1.0; manter cópias iguais.
- [x] Atualizar guias por plataforma, CI com matriz e teste do pacote completo.
- [ ] Executar suíte, lint, tipos, smoke offline, instalação/upgrade Git e revisão.
- [ ] Integrar PR autorizada, atualizar Codex local, reconferir main e documentar limites.

## Ledger

- 21/10: execução nesta sessão e liberação já autorizadas pelo usuário; manter
  os gates técnicos, sem repetir perguntas de autorização do mesmo trabalho.
- Worktree nativo não suporta a raiz agregadora (retornou Not a git repository);
  usado worktree Git isolado em diretório operacional existente.
- Contrato revisado no backend/main5636193: CSV pode ser fonte real; onboarding
  exige papel administrativo. Não copiar batch_sync antigo que envia PDFs.
- Revisão preliminar achou travessia de saída por '..', primeira linha CSV não
  validada, número não finito, formato de data e qualificação sem fundamento.
  Todos reproduzidos RED e corrigidos GREEN antes do checkpoint125testes.
- Ruff, formato e mypy9sources passaram. Diagnóstico pelo uv/lock real passou
  fora do checkout. Wheels dos três módulos nativos cobrem as cinco combinações
  anunciadas. Wheel provider0.1.3 apenas smoke local; fontes/provider inalterados.
