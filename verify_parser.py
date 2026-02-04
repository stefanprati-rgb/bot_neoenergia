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

# Teste 3: Mensagem RETRY de CPF (Conflito anterior)
msg_retry_cpf = "Hmm... Não deu certo com essa informação. Confere e me passa de novo os 11 dígitos do CPF ou os 14 dígitos do CNPJ..."
acao3 = parser.analisar(msg_retry_cpf)
print(f"Msg 3 (Retry CPF): {acao3} -> Esperado: Acao.ENVIAR_DOCUMENTO")

# Teste 4: Novos Gatilhos (Dívidas e Reiniciar)
msg_dividas = "Você quer consultar se existem dívidas para este imóvel?"
acao4 = parser.analisar(msg_dividas)
print(f"Msg 4 (Dívidas): {acao4} -> Esperado: Acao.CONFIRMAR_DADOS")

msg_reiniciar = "Poxa! Acho que não estamos conseguindo nos entender. Mas, você pode entrar em contato..."
acao5 = parser.analisar(msg_reiniciar)
print(f"Msg 5 (Reiniciar): {acao5} -> Esperado: Acao.REINICIAR")

if acao1 == Acao.ENVIAR_CODIGO and acao2 == Acao.ENVIAR_CODIGO and acao3 == Acao.ENVIAR_DOCUMENTO and acao4 == Acao.CONFIRMAR_DADOS and acao5 == Acao.REINICIAR:
    print("✅ TODOS OS TESTES PASSARAM")
else:
    print("❌ ALGUNS TESTES FALHARAM")
