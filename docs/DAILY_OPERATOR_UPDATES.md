# Atualização diária — Ana e Samuel

Este procedimento mantém a instalação HTTPS e o OAuth Loki já configurados.
O kit consulta releases assinadas em `T0minh0/MCP_Loki`; ninguém precisa receber
outro ZIP por mensagem. O programa baixa e verifica os bundles automaticamente.

O canal deve ser **privado** porque os bundles incluem código do Project Loki.
Antônio adicionará os operadores aos autorizados posteriormente. O acesso de
leitura ao GitHub é separado do Google/OAuth que eles já usam no Loki.

## Antes de configurar os computadores — Antônio

1. Publicar a versão validada do backend que contém o atualizador, seguindo os
   gates de release do Project Loki. Conferir o build completo no `/healthz`.
2. Garantir que `T0minh0/MCP_Loki` está privado e liberar leitura para cada pessoa.
3. No computador administrativo com a chave já provisionada, construir o bundle
   assinado desse **mesmo commit** pelo `scripts/operator_release.py construir`.
   A chave de assinatura permanece com Antônio; não entra em CI ou nos PCs deles.
4. Publicar pelo novo comando do Project Loki:

   ```text
   uv run --no-sync python scripts/publish_operator_release.py --bundle CAMINHO_DO_BUNDLE_ASSINADO --verifier scripts/operator_release.py --signers plugins/loki-operador/setup/release_signers --dry-run
   uv run --no-sync python scripts/publish_operator_release.py --bundle CAMINHO_DO_BUNDLE_ASSINADO --verifier scripts/operator_release.py --signers plugins/loki-operador/setup/release_signers
   ```

5. Conservar o recibo com tag, SHA do bundle e `bootstrap_sha256`. A tag publicada
   será `operator-<build completo>` e os assets serão o bundle desse build e
   `install-repository.ps1`. O publicador verifica assinatura, recusa canal público
   e não substitui um asset existente por bytes diferentes.

Sem uma release assinada correspondente ao build servido, o atualizador conserva
a instalação e registra falha. Repositório/branch atualizado sozinho não entrega
uma versão instalável. Na primeira migração, coordenar publicação e configuração
antes de considerar o fluxo pronto para os operadores.

## Configurar uma vez no computador da pessoa

Executar como o **mesmo usuário Windows** que já usa o Loki, sem executar como
outro administrador. Repetir independentemente para Ana e Samuel.

1. Confirmar que o kit funciona e localizar sua pasta. O padrão é
   `%LOCALAPPDATA%/Izzi-Loki`, contendo `active.json`. Se usou outra pasta, informar
   esse caminho em `-Root`. A migração recusa instalações de outro formato;
   não remove nem converte configurações OAuth nativas/SSH automaticamente.
2. Localizar a pasta **trusted** da instalação original, com
   `operator_release.py`, `release_signers`, `privacy.py` e
   `private_directory.ps1`. Ela fornece o verificador/pin já confiáveis.
   Preservar esses arquivos; se não estiverem disponíveis, Antônio deve
   reconciliar a instalação antes do bootstrap. Não usar um pin novo do download.
3. Ter [GitHub CLI](https://cli.github.com/) e o CLI da harness utilizada
   disponíveis no terminal. Entrar no GitHub com a conta pessoal autorizada:

   ```powershell
   gh auth login --hostname github.com --web --git-protocol https
   gh repo view T0minh0/MCP_Loki --json nameWithOwner,visibility
   codex plugin --help
   ```

   No Codex, o CLI precisa oferecer `plugin add` e `plugin marketplace`.
   Isso autentica a leitura do repositório; o OAuth Loki permanece no cofre.
4. Baixar somente o bootstrap da release correspondente ao servidor:

   ```powershell
   $lokiBuild = (Invoke-RestMethod 'https://loki.themindops.com/healthz').build
   if ($lokiBuild -notmatch '^[a-f0-9]{40}$') { throw 'Build invalido' }
   $lokiSetup = Join-Path $env:TEMP ('loki-setup-' + [guid]::NewGuid().ToString('N'))
   New-Item -ItemType Directory -Path $lokiSetup | Out-Null
   gh release download ('operator-' + $lokiBuild) --repo T0minh0/MCP_Loki --pattern install-repository.ps1 --dir $lokiSetup
   Get-FileHash -Algorithm SHA256 (Join-Path $lokiSetup 'install-repository.ps1')
   ```

   Conferir o hash com `bootstrap_sha256` do recibo administrativo antes de
   executar. Este é o preparo único do canal confiável.
5. Informar o caminho real da pasta trusted anterior e habilitar:

   ```powershell
   $lokiTrusted = Read-Host 'Caminho completo da pasta trusted original'
   powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $lokiSetup 'install-repository.ps1') -Action enable -TrustedDirectory $lokiTrusted -Harness codex
   ```

   Para Claude Code, usar `-Harness claude`; para ambos, `-Harness both`.
   Se a instalação não for a padrão, acrescentar `-Root 'CAMINHO_REAL'`.
   A ação verifica a instalação, baixa o bundle, confere-o com o pin anterior,
   extrai o atualizador, executa a primeira consulta e só então registra a tarefa.
6. Abrir nova conversa na harness e pedir `meu_acesso`,
   `loki_verificar_versao` e instruções `geral`/do processo. Confirmar a própria
   identidade e `active`, sem reproduzir dados pessoais. No Claude Code, usar o
   launcher `Abrir-Loki-Claude.ps1` da raiz da instalação.

## Conferir a rotina

A tarefa chama-se `Izzi-Loki-Update-<identificador da instalação>`. Ela executa
diariamente às **07h de Brasília** e no login do usuário, sem armazenar senha.
Se o PC estiver desligado/sem sessão, a consulta ocorre quando voltar a estar
disponível com o usuário conectado. O Shadow do servidor continua às 05h.

Na instalação padrão:

```powershell
$lokiUpdater = Join-Path $env:LOCALAPPDATA 'Izzi-Loki\repository-updater\install-repository.ps1'
powershell -NoProfile -ExecutionPolicy Bypass -File $lokiUpdater -Action status
powershell -NoProfile -ExecutionPolicy Bypass -File $lokiUpdater -Action run -Harness codex
Get-ScheduledTask -TaskName 'Izzi-Loki-Update-*' | Get-ScheduledTaskInfo
```

Conferir `LastTaskResult=0` e o estado retornado pelo atualizador. `atualizado`
significa nova release ativa; `sem_atualizacao` significa mesmo build;
`adiado_plugin_desativado` preserva um plugin que o usuário desligou. `falha` ou
`intervencao_necessaria` exigem diagnóstico; não equivalem a sucesso.

Para mudar o horário, repetir `-Action enable -Hour 7 -Minute 0` com o horário
desejado, sempre interpretado em Brasília. Usar o mesmo `-Harness` configurado.

## Falhas, desativação e rollback

- Sem acesso GitHub: conferir convite/conta e `gh auth status` localmente.
- Sem release do build: Antônio precisa publicar o bundle assinado correto.
- OAuth expirado/revogado: usar o login pessoal já existente (`Entrar-Loki.cmd`)
  e repetir a consulta. O job diário não abre navegador nem troca a identidade.
- Lotes em andamento conservam seu build; não editar `expected_build` para
  vencer o preflight. A mudança de versão pode exigir reconciliação do lote.
- Conversas abertas continuam usando o código carregado; abrir conversa nova
  ou reiniciar a harness após atualizar.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $lokiUpdater -Action disable
powershell -NoProfile -ExecutionPolicy Bypass -File $lokiUpdater -Action rollback -Harness codex
```

Desabilitar remove somente a tarefa. Rollback conserva documentos e OAuth, mas
exige que o build anterior seja compatível com o backend servido; não faz
rollback do servidor. Não apagar pastas de releases manualmente durante o uso.

## Aceite separado por pessoa

Registrar: acesso ao canal privado, bootstrap/hash conferidos, mesma identidade
OAuth, documentos/checkpoints preservados, versão efetivamente carregada e
execução manual/agendada da tarefa. Um teste Linux, um arquivo de configuração
ou o sucesso de Antônio não comprovam o aceite Windows da Ana ou do Samuel.
