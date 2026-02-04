from neoenergia_bot.utils.util import limpar_cpf_cnpj

casos_teste = [
    ("7075377902", "07075377902", "CPF sem zero à esquerda"),
    ("7069183276", "07069183276", "CPF sem zero à esquerda"),
    ("12345678901", "12345678901", "CPF completo"),
    ("13038318000101", "13038318000101", "CNPJ completo"),
    ("3038318000101", "03038318000101", "CNPJ sem zero à esquerda (13 dígitos)"),
    ("123456789", "00123456789", "CPF muito curto"),
]

print("=== TESTE DE PADDING CPF/CNPJ ===")
todos_passaram = True

for entrada, esperado, descricao in casos_teste:
    resultado = limpar_cpf_cnpj(entrada)
    if resultado == esperado:
        print(f"✅ [{descricao}] Entrada: {entrada} -> Saída: {resultado}")
    else:
        print(f"❌ [{descricao}] FALHOU! Entrada: {entrada} -> Esperado: {esperado} -> Obtido: {resultado}")
        todos_passaram = False

if todos_passaram:
    print("\n🎉 TODOS OS TESTES PASSARAM!")
else:
    print("\n⚠️ ALGUNS TESTES FALHARAM.")
