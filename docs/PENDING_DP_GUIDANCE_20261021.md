# Instruções dos fluxos pendentes de DP — candidata local

Pacote candidato `0.1.4`, instruções `1.3.0`, contrato MCP `1.0.0`. A origem
remota `main` foi conferida em `a80ed78`, com pacote `0.1.3`; não havia tags nem
artefato `0.1.4` neste worktree. Esse corte não comprova reserva global de versão.
Conferir novamente antes de construir/promover uma release imutável.

Os cinco novos domínios `alteracao_cadastral`, `ocorrencia`, `adiantamento`,
`aviso_ferias` e `aviso_rescisao` usam versão `1.0.0` e requerem `consultar`
mais o respectivo processo. Os oito domínios anteriores continuam disponíveis;
geral/documentos passam a `1.2.0`, afastamento/aprovações a `1.1.0`; os outros preservam
conteúdo e versões. Versões mínima/recomendada do cliente continuam `0.4.0` e
`0.5.0`, com cliente desconhecido ainda desconhecido. O plugin nativo com
leitores locais mantém sua versão e sua distribuição próprias.

Os guias descrevem o caminho somente quando `get_dp_capabilities`,
`list_workflows` e `get_document_processing_contract` correntes confirmarem
executor, schemas e modo de execução. Distinguem pacotes factuais JSON sem PDF
e sem aplicação operacional, avisos documentais autônomos e adiantamento
automático por política vigente. O guia de adiantamento exige fontes/regras
qualificadas e conserva resultados dependentes ausentes como `None`/pendência.
Não substitui cálculo por valor pronto nem presume pagamento ou compensação.

`PROCESS_TYPES` valida os 18 identificadores aceitos pelo enum do host candidato,
independentemente dos 13 domínios de orientação. O provider valida dados e
devolve metadados; o host autentica, filtra o bootstrap e confere capacidade,
processo e empresa a cada consulta. Os testes do provider não comprovam essa
fronteira de autorização. A integração deve testar os cinco novos domínios
com e sem `consultar`, com processo diferente, empresa fora do escopo e usuário
restrito, incluindo o caminho antigo de `runtime_instructions`.

O guia de aprovações distingue a ferramenta legada `preparar_autorizacao`,
com enum original de 13 processos validado também em runtime, da tela autenticada
`/admin` existente. Os cinco novos processos são concedidos pela tela, mantendo
prévia, confirmação, CSRF e revisão. Isso não amplia permissões da conta.

Antes da promoção, conferir nomes/raízes tipadas, marcadores request/input/output,
`execution_modes`/`package_kind`, executor, captura, freshness, artefatos e gates
de review do host integrado. Os descritores das ferramentas antigas continuam
sob os testes de compatibilidade do backend; este pacote não os modifica.

Build, smoke fora do fonte, revisão de provenance/lock, promoção, implantação e
jornada autenticada precisam de recibos próprios. Esta preparação local não
comprova publicação, execução real, aceite humano, validação financeira ou 98%.
Não houve migração de hospedagem/banco/DNS nem mudança no sistema da Ana.
