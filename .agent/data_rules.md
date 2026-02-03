# Regras de Dados e Estruturas

## Tratamento da Planilha (`base.xlsx`)
A base de dados possui colunas que o Pandas/Excel podem interpretar erroneamente.
* **Fonte:** `data/input/base.xlsx`
* **Coluna `CNPJ`:** Deve ser lida sempre como **STRING**.
    * *Problema:* O arquivo original removeu os zeros à esquerda.
    * *Solução:* Aplicar `.zfill(11)` para CPFs e `.zfill(14)` para CNPJs e remover pontuação (`.`, `-`, `/`).
* **Coluna `NUMERO CLIENTE`:** Tratar como **STRING**.
* **Distribuidoras:** A base contém clientes da **Coelba (BA)**, mas o log de treino é de **Pernambuco**. O código deve ser resiliente a pequenas variações no menu (busca por "2ª via" deve ser por palavra-chave, não texto exato).