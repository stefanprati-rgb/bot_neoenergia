from neoenergia_bot.utils.text_parser import WhatsAppBotParser, Acao

msg_problematica = """
Para prosseguirmos, preciso que digite o Código do Cliente.
Esse número aparece na sua fatura, perto da data de vencimento.
Caso não saiba onde encontrá-lo, clique no botão abaixo que eu te explico.
"""

msg_retry = "Hmm... Não deu certo com essa informação. Confere e me passa de novo, por favor?"

parser = WhatsAppBotParser()

# Teste 1: Mensagem PROBLEMÁTICA
acao1 = parser.analisar(msg_problematica)
print(f"Msg 1 (Código + Botão): {acao1} -> Esperado: Acao.ENVIAR_CODIGO")

# Teste 2: Mensagem RETRY
acao2 = parser.analisar(msg_retry)
print(f"Msg 2 (Retry): {acao2} -> Esperado: Acao.ENVIAR_CODIGO")

if acao1 == Acao.ENVIAR_CODIGO and acao2 == Acao.ENVIAR_CODIGO:
    print("✅ TESTE PASSOU")
else:
    print("❌ TESTE FALHOU")
