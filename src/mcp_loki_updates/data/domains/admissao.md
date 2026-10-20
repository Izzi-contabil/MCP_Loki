# Admissão

Consulte `list_workflows` e `get_dp_capabilities` para confirmar o estado atual de admissão e os gates aplicáveis. Trate fluxos partial/shadow como apoio à análise; não apresente admissão como concluída por existir um registro ou uma extração.

O host exige capacidade `consultar` e escopo do processo `admissao` antes de entregar estas instruções. Outras operações mantêm suas próprias verificações de autorização. Para documentos, consulte `get_document_processing_contract` e use somente canais autorizados; mantenha PII e evidências em seus repositórios privados de origem.

Separe dado extraído, dado ausente, divergência e decisão humana. Não preencha faltas com zero nem invente exigências legais, prazos ou validações. Obtenha a revisão humana indicada pelo runtime antes de avançar; aprovação técnica não concede aceite. Não publique ou transmita admissão a sistemas externos por inferência destas instruções.
