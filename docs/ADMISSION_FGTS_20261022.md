# Admissão — opção pelo FGTS — candidata de 22/10/2026

O guia entregue pelo provider passa a explicar quando a harness pode preparar
`dados_admissao.contrato.fgts_opcao_em` igual à admissão. Antes, o campo podia
permanecer ausente mesmo quando a regra e os insumos permitiam uma derivação.
A assertiva normativa ancora-se na edição2022 conferida; o guia servido também explicita que a edição2026 é complemento localizado/indexado cujo acesso integral ficou bloqueado em22/10/2026. A candidata é provider `0.1.6`, instruções `1.3.2`, admissão `1.2.3`;
contrato `1.0.0` e plugin `1.1.4` são preservados.

O alcance é empregado CLT comum admitido depois de 04/10/1988, com regime,
categoria, empregador, episódio atual e admissão qualificados nos insumos.
A relação normativa entre datas não comprova esses fatos. A derivação usa
`field_sources`, `basis=derived` e fundamento em `derivation`, com norma,
vigência, operandos e referências, hashes e localizadores dos insumos.
Não se converte a derivação em leitura `documented`.

Admissão até 04/10/1988, doméstico104, diretor não empregado721, transferência,
reintegração, categoria ou episódio incertos e conflitos mantêm pendência
para regra específica. Valor declarado é preservado; o relatório da equipe
não serve como fonte. Casos em revisão conservam snapshot e pacote e seguem
o fluxo autorizado de ajuste e revisão humana.

## Fontes e alcance temporal

- [CAIXA — Manual SEFIP8.4, maio/2026](https://www.caixa.gov.br/Downloads/fgts-manuais-e-cartilhas-operacionais/Manual_SEFIP_8_4_05_2026.pdf), itens4.11/4.12, nota1: referência atual localizada na investigação. O download direto nesta preparação retornou bloqueio/redirecionamento; não se declara leitura integral dessa edição.
- [Receita Federal — Manual SEFIP8.4, outubro/2022](https://www.gov.br/receitafederalsimples/pt-br/assuntos/orientacao-tributaria/declaracoes-e-demonstrativos/gfip-sefip-guia-do-fgts-e-informacoes-a-previdencia-social-1/manuais-e-formularios/manual_sefip_8_4_17102022.pdf), mesmos itens, página52 do PDF/impressa50: texto histórico conferido; SHA256 `4f7fbbb1ce417c442faf0aadc25a60ba799fd13fdde5c65582a022aa1aa38af8`.
- [eSocial S-1.3, NT07/2026 — regras](https://www.gov.br/esocial/pt-br/documentacao-tecnica/leiautes-esocial-versao-s-1-3-nt-07-2026/regras.html), `REGRA_EVETRAB_VALIDA_OPCAO_FGTS`: validação relida na fonte oficial, com limites temporais e exceções104/721. Essa validação não estabelece, sozinha, igualdade universal entre datas.

A edição de2026 não é tratada como início da regra. A edição aplicável e o
alcance temporal precisam ser registrados para o episódio/competência em exame;
uma referência atual não substitui a qualificação histórica de cada caso.

## Verificação e limites

O plano desta correção é observar testes de entrega falhando pela ausência do
guia, editar somente instruções/metadados e identidade do pacote, conferir
hashes e lock e executar suíte, lint, formato, tipos, build e smoke fora do fonte.
Os testes novos consultam o provider real e verificam entrega das qualificações,
fontes e limites; não executam um agente nem certificam obediência semântica.

Nenhum default de data, cálculo, modelo de domínio ou caso real é alterado.
O wheel é candidato local sem commit, promoção ou implantação nesta preparação.
Efeito no operador, casos reais e assertividade exigem validações próprias após
revisão e entrega autorizada pelo backend.
