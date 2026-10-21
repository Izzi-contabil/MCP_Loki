# Ocorrência

Antes de preparar este processo, consulte `get_dp_capabilities`, `list_workflows` e `get_document_processing_contract` com o processo correspondente. Confira `execution_modes`, `standalone_available`, `available_via` e o contrato `versioned_case` atual. Siga somente o caminho disponível e autorizado; ausência de executor ou schema mantém a pendência. Estas instruções não comprovam implantação, paridade ou validação financeira.

A leitura deste guia exige `consultar` e o escopo do processo no host. Preparação, anexos, extração, simulação e revisão exigem suas próprias permissões e empresa autorizada; receber o guia não as concede. Confirme identidade do vínculo, competência e referência estável da ocorrência. Use os schemas e fontes por campo aceitos pelo host, preservando ausentes e conflitos.

Quando o contrato atual oferecer o modo versionado factual, prepare `dados_ocorrencia` e use `simulate_case_version`. Registre tipo aceito, data/intervalo, quantidade decimal exata, unidade, competência, referência estável e fontes. Ocorrências distintas conservam referências distintas; repetição da mesma ocorrência não cria um fato novo. Não infira classificação de falta, DSR, hora extra ou impacto financeiro pela quantidade isolada.

O pacote factual contém recibo/timeline e artefatos JSON, sem PDF; `supports_apply=false` preserva ausência de aplicação operacional. Extração aplicada ao `case_payload` prepara somente o caso. Confira unidade, quantidade, contexto, fontes, hashes e pendências pelos mecanismos de verificação/revisão da versão, sem exigir conferência de PDF inexistente.

Registrar ou aprovar o documento não insere rubrica, desconto ou lançamento na folha. Consumo financeiro depende de regra/rubrica vigentes, fonte e ato explícito pelo fluxo autorizado. Ausência, zero e não aplicável permanecem distintos; não converta pendência em lançamento.
