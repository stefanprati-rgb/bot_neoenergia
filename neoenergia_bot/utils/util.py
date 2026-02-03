import re

def limpar_cpf_cnpj(doc):
    """Remove caracteres não numéricos e garante 11 ou 14 dígitos."""
    if not doc:
        return ""
    clean_doc = re.sub(r'\D', '', str(doc))
    if len(clean_doc) <= 11:
        return clean_doc.zfill(11)
    return clean_doc.zfill(14)
