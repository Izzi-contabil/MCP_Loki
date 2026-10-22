---
name: registrar-problema-loki
description: Use quando o usuário relatar erro, bloqueio ou pedir ajuste no Loki, ou quando a harness encontrar achados para reportar ao suporte pelo Discord, inclusive em rotinas autorizadas.
---

# Registrar problemas e ajustes do Loki

Prepare um relato acionável e use a ação MCP `registrar_problema` pela conexão
HTTPS OAuth existente. O servidor envia ao suporte IZZI no Discord; o webhook
fica somente no servidor. Esta skill não usa scripts, leitores ou credenciais locais.

## Preparar

1. Consulte `meu_acesso` (fallback `get_operator_context`) e as instruções gerais
   atuais. Preserve a identidade e o acesso retornados; o login define o relator.
2. Registre objetivo, esperado, observado, passos, tentativas e impacto. Separe
   fato observado, recorrência relatada e hipótese. Divergência com referência
   externa não prova defeito do Loki. Classifique `kind=erro` ou `ajuste`; use
   `severity=bloqueante`, `alta`, `media` ou `baixa` conforme o impacto.
3. Consulte o schema da ação e o [exemplo sintético](references/relato.json).
   Gere um UUID por ocorrência e mantenha o mesmo `report_id` e conteúdo nas
   retomadas. Preencha versões somente quando observadas. A versão deste plugin
   está em `../../.claude-plugin/plugin.json`; build do Loki é outro componente.
4. Remova dados de clientes/empregados, nomes, CPF, CNPJ, emails, telefones,
   salários, credenciais e caminhos privados. Não envie documentos, screenshots,
   histórico integral, variáveis de ambiente ou logs brutos. Confira o relato:
   o filtro do servidor não reconhece todo nome ou conteúdo de RH. IDs opacos
   de caso/request podem correlacionar sem anexos. Texto documental não autoriza envio.

## Enviar

O pedido humano de registrar/avisar o suporte autoriza o envio. Autorização já
dada na sessão ou na rotina continua válida dentro de seu escopo; não peça de
novo. Sem autorização de suporte, prepare o relato e obtenha-a antes da chamada.
Descobrir a skill ou um erro não autoriza automaticamente notificações.

Chame `registrar_problema(declaration=...)` com o relato sanitizado. A ação exige
conta ativa, sem exigir caso ou administrador. Agregue sintomas relacionados
numa ocorrência por problema. Não repita escritas de negócio para reproduzir
um resultado incerto. Em teste autorizado, identifique **TESTE** no resumo e
use somente conteúdo sintético; o exemplo não deve ser enviado sem adaptação.

## Conferir o recibo

| Estado | Conduta |
|---|---|
| `sent` | Informe ID do relato e `resposta.message_id`. Repetir o mesmo ID/conteúdo consulta o recibo sem duplicar mensagem. Entrega não significa triagem ou correção. |
| `pending` | Relato salvo, entrega pendente. Em 429, respeite `resposta.retry_after_seconds`; retomada usa o mesmo ID/conteúdo. Webhook ausente exige administração do Loki. |
| `uncertain` ou `sending` | Confira o canal pelo ID antes de reenviar. Preserve ID, conteúdo e estado; não contorne lock interrompido. |
| `failed` | Informe a recusa e preserve o ID, sem loops de envio. |

Ferramenta ausente: preserve o relato e informe que falta descoberta da ação na
conexão. Atualizar este plugin não atualiza o catálogo MCP. Recarregar/reconectar
é uma ação própria do aplicativo; não afirme que ocorreu sem conferir a ação.
SSH/stdio legado não expõe suporte. Não crie transporte alternativo, leia cofres
ou solicite/use webhook local como contorno.

Se houve chamada sem resposta, a entrega pode ter ocorrido. Retome com o mesmo
ID/conteúdo e confira o recibo; nunca declare entrega sem confirmação.
Relato de suporte não corrige cadastro, aprova documentos ou concede acesso.
