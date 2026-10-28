# Loki orientações — plugin2.0.2

O nome `loki-orientacoes@loki-equipe` permanece para atualização nativa. O contrato
operacional2.0.0 exige dados estruturados e fontes por campo: consulte
`get_process_contract`, capture `get_case.input_snapshot` e use `receive_case_data`.
Depois execute cálculo, geração e revisão. Versões internas preservam auditoria.
A empresa de teste usa o mesmo fluxo e gates, sem modo especial.

Leitores externos continuam offline no Mac, Windows e Linux; a harness interpreta
os documentos e compara resultados fora do Loki. `case-request` prepara um pedido
para o writer atual e não envia. CSVs de leitura permanecem evidência externa;
CSVs de cadastro/histórico usam somente os contratos próprios autorizados.

Consulte [operar-loki](skills/operar-loki/SKILL.md),
[WORKFLOWS](skills/operar-loki/references/WORKFLOWS.md),
[ROUTINES](skills/operar-loki/references/ROUTINES.md) e
[investigar-regras-dp](skills/investigar-regras-dp/SKILL.md).
Use [registrar-problema-loki](skills/registrar-problema-loki/SKILL.md) conforme
escopo/autorização de suporte, preservando UUID/recibo e sem dados de RH.

A candidata acompanha provider0.2.2/instruções2.0.2. Build, publicação, instalação,
carregamento, catálogo e execução precisam de evidências separadas. Não altera
OAuth, assinatura/pin do kit antigo ou agenda. Dados e recibos ficam em workspace
privado fora do plugin; nenhum pacote ou documento concede decisão humana.
