# Afastamento

Use `list_workflows` e `get_dp_capabilities` para verificar capacidades e gates atuais de afastamento. Trate partial/shadow como apoio e preserve pendências: existência de fluxo ou documento não comprova registro efetivado nem conclusão operacional.

A leitura exige `consultar` e escopo `afastamento` no host. Outras ações exigem suas autorizações próprias. Consulte `get_document_processing_contract` para documentos e limite o tratamento de informações pessoais ou de saúde ao canal e escopo autorizados; não copie PII para instruções, Git ou logs compartilhados.

Não invente diagnóstico, motivo, duração, enquadramento, legislação ou prazo. Preserve dados ausentes, fontes e divergências sem converter ausência em zero. Submeta decisões aos responsáveis e cumpra os gates humanos declarados no runtime. Não publique ou transmita alterações por conclusão automática de leitura ou extração.

Quando `execution_modes` declarar `versioned_factual`, consulte `get_document_processing_contract` para o schema de afastamento e use `simulate_case_version` no caminho autorizado. O pacote factual versionado registra contexto, fontes, período, pendências e hashes em recibo/artefatos JSON, sem PDF obrigatório. Confira-o pelos checks factuais e mecanismos de verificação/revisão da versão; ausência de gerador PDF não basta para concluir que esse executor factual está indisponível.

Respeite os requisitos correntes de cenário, identidade e fontes. Preparar ou aprovar a versão documental não aplica afastamento ao vínculo nem transmite evento; permissões e gates de cada operação continuam no host. Não anuncie execução canônica, conclusão operacional ou validação financeira pelo simples registro do caminho factual.
