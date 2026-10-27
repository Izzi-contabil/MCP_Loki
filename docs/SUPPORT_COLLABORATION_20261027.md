# Apoio e falhas de execução — TMO-2297

O plugin1.1.7 orienta classificação e registro ao concluir execução Loki com falha
inesperada no escopo de suporte já autorizado. Pendência prevista, negativa de
permissão conforme contrato, fluxo parcial declarado e teste negativo intencional
não viram defeito automaticamente. Melhorias/processos/dúvidas têm enquadramento
próprio; host antigo usa ajuste conforme contrato observado.

O leitor offline retorna support_handoff em falha, com UUID e próxima ação para
a harness. Ele não acessa rede/OAuth nem envia relatos. A IA carrega a skill e
chama o MCP existente com relato sanitizado; preserva o ID/conteúdo nas retomadas.
Sem autorização, aguarda a escrita. Falha do próprio suporte não gera recursão.

Provider0.1.7, instruções1.3.3 e geral1.3.0 entregam a orientação pelas consultas
existentes. O backend consumidor implementa triagem somente leitura, perguntas
a contatos cadastrados, avisos de bloqueio e orientação sem código aguardando
confirmação humana. Isso não concede decisão de software ou efeito de DP.

Atualizar pelo marketplace/Gitmain existente e reiniciar/recarregar o cliente
conforme sua instalação. Conferir a versão da skill realmente carregada, os
schemas/instruções do host e um recibo de relato real antes de declarar entrega.
Publicar no GitHub ou instalar neste servidor não prova atualização/uso pelo
executor da Ana, nem intercepta automaticamente toda falha de qualquer harness.
Não foi alterado o sistema dela.
