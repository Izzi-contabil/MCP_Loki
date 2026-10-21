# Alteração cadastral

Antes de preparar este processo, consulte `get_dp_capabilities`, `list_workflows` e `get_document_processing_contract` com o processo correspondente. Confira `execution_modes`, `standalone_available`, `available_via` e o contrato `versioned_case` atual. Siga somente o caminho disponível e autorizado; ausência de executor ou schema mantém a pendência. Estas instruções não comprovam implantação, paridade ou validação financeira.

A leitura deste guia exige `consultar` e o escopo do processo no host. Preparação, anexos, extração, simulação e revisão exigem suas próprias permissões e empresa autorizada; receber o guia não as concede. Confirme identidade do vínculo, competência e referência estável da ocorrência. Use os schemas e fontes por campo aceitos pelo host, preservando ausentes e conflitos.

Quando o contrato atual oferecer o modo versionado factual, prepare `dados_alteracao_cadastral` e use `simulate_case_version` para a versão explícita. A proposta compara valores anteriores do perfil datado com valores novos fonteados, vigência e contexto capturado. Não declare anteriores apenas por relato nem substitua o hash esperado para contornar conflito de perfil.

O pacote factual contém recibo e artefatos JSON, sem PDF; `supports_apply=false` indica ausência de aplicação ao cadastro operacional. `apply_document_extraction(destination='case_payload')`, quando autorizado, prepara dados do caso; não aplica a proposta ao perfil do empregado. Confira contexto, diferenças, fontes, hashes e pendências pelos checks do contrato e mecanismos de verificação/revisão da versão. Perfil alterado exige nova captura/versionamento.

Revisão e aprovação documental não aplicam salário, cargo, jornada ou outros dados ao cadastro. Qualquer efeito operacional exige fluxo e intenção humana específicos que o host efetivamente suporte. Preserve a proposta parcial se faltar fato, vigência ou fonte.
