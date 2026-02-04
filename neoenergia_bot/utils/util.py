import re

def limpar_cpf_cnpj(doc):
    """Remove caracteres não numéricos e garante 11 ou 14 dígitos."""
    if not doc:
        return ""
    clean_doc = re.sub(r'\D', '', str(doc))
    
    # Lógica Inteligente de Padding (Zeros à esquerda)
    # Excel costuma comer o zero à esquerda.
    
    # Se tem 11 dígitos ou menos (ex: 1234567890 -> 10 dígitos), assume que é CPF e preenche.
    if len(clean_doc) <= 11:
        return clean_doc.zfill(11)
        
    # Se tem entre 12 e 14, assume CNPJ (ex: 12345678000199 sem zeros).
    if len(clean_doc) <= 14:
        return clean_doc.zfill(14)
        
    # Se for maior que 14, retorna como está (provavelmente erro ou concatenação)
    return clean_doc
