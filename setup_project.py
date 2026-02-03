import os

# Estrutura de diretórios e arquivos
structure = {
    ".agent": {
        "project_context.md": """# Contexto do Projeto: Automação Neoenergia WhatsApp

## Objetivo
Desenvolver um robô RPA (Robotic Process Automation) em Python que utiliza Selenium para interagir com o WhatsApp Web da Neoenergia (PE/BA). O objetivo é iterar sobre uma lista de clientes, solicitar a segunda via da conta de energia e baixar o PDF.

## Entradas
1. **Base de Dados (`base.xlsx`):** Contém `NUMERO CLIENTE` (Código da conta) e `CNPJ` (Documento do titular).
2. **Histórico de Treino (`_chat.txt`):** Log de conversas reais usado para mapear o fluxo de interação.

## Restrição Crítica (A Regra de Ouro)
Estamos usando o modelo `gemini-2.5-flash-lite` no plano gratuito para a *execução do robô*, que tem um limite estrito de **20 requisições por dia**.
* **Regra:** O código deve usar lógica determinística (Regex/String Matching) para 95% das interações.
* **Exceção:** A API do Gemini só deve ser chamada pelo código Python se o robô encontrar uma mensagem de erro não mapeada ou um fluxo desconhecido.

## Observação para o Agente Antigravity
Você (Agente da IDE) pode usar seus modelos internos livremente para *escrever* o código. Porém, o *código gerado* deve economizar ao máximo as chamadas de API durante a execução.""",

        "data_rules.md": """# Regras de Dados e Estruturas

## Tratamento da Planilha (`base.xlsx`)
A base de dados possui colunas que o Pandas/Excel podem interpretar erroneamente.
* **Fonte:** `data/input/base.xlsx`
* **Coluna `CNPJ`:** Deve ser lida sempre como **STRING**.
    * *Problema:* O arquivo original removeu os zeros à esquerda.
    * *Solução:* Aplicar `.zfill(11)` para CPFs e `.zfill(14)` para CNPJs e remover pontuação (`.`, `-`, `/`).
* **Coluna `NUMERO CLIENTE`:** Tratar como **STRING**.
* **Distribuidoras:** A base contém clientes da **Coelba (BA)**, mas o log de treino é de **Pernambuco**. O código deve ser resiliente a pequenas variações no menu (busca por "2ª via" deve ser por palavra-chave, não texto exato).""",

        "interaction_flow.md": """# Fluxo de Interação (Mapeamento)

## 1. Fluxo Feliz (Happy Path - Regex)
| Gatilho (Bot Neoenergia) | Ação do Robô | Variável |
| :--- | :--- | :--- |
| "escolha o serviço" OU "para começar" | Enviar Opção | "2ª via" |
| "Código do Cliente" | Enviar Código | `cliente['NUMERO CLIENTE']` |
| "CPF" OU "CNPJ" | Enviar Documento | `cliente['DOC_FORMATADO']` |
| "Posso seguir" OU "unidade consumidora" | Confirmar | "Sim" |
| "Boleto.pdf" OU "Pix copia e cola" | Baixar/Salvar | Extrair PDF e Código PIX |

## 2. Exceções Hardcoded (Sem Gasto de API)
| Gatilho | Ação |
| :--- | :--- |
| "não tem nenhuma fatura" | Log: "NADA CONSTA" -> Próximo Cliente |
| "não consegui localizar o cadastro" | Log: "ERRO CADASTRO" -> Próximo Cliente |
| "Dica de Segurança" | Timeout detectado -> Reiniciar com "Olá" |

## 3. Uso da IA (Gemini Runtime)
Acionar APENAS se:
1. Texto não der match com regras acima após 3 tentativas.
2. Decisão de múltiplos imóveis (Endereço mascarado vs CSV).""",

        "coding_standards.md": """# Padrões de Código

## Stack
* Python 3.10+
* Selenium WebDriver (Chrome)
* Pandas
* google-generativeai

## Requisitos Selenium
1. **Persistência:** `webdriver.ChromeOptions` DEVE usar `user-data-dir` (ex: `./chrome_profile`) para salvar o login do WhatsApp.
2. **Seletores:** Use seletores robustos (XPATH por texto ou `data-testid`), pois classes CSS mudam.
3. **Waits:** Use `WebDriverWait`, nunca `time.sleep` fixo para elementos.

## Robustez
* O loop principal deve ter `try/except` para que um erro em um cliente não pare a fila inteira.
* Logs devem ser salvos em `data/logs/execucao.csv`."""
    },
    "neoenergia_bot": {
        "__init__.py": "",
        "main.py": "# Entry point do robô",
        "config": {
            "__init__.py": "",
            "settings.py": "# Configurações globais (Paths, Keys)",
            "selectors.py": "# Mapeamento de elementos do WhatsApp Web"
        },
        "core": {
            "__init__.py": "",
            "driver.py": "# Gerenciamento do Selenium WebDriver",
            "navigator.py": "# Lógica de navegação e interação",
            "ai_client.py": "# Cliente Gemini (Gestor de Exceções)"
        },
        "utils": {
            "__init__.py": "",
            "data_handler.py": "# Leitura e limpeza do Excel/CSV",
            "text_parser.py": "# Motor de Regras (Regex)"
        }
    },
    "data": {
        "input": {},  # Pasta vazia para colocar o excel
        "output": {}, # Pasta vazia para os PDFs
        "logs": {}    # Pasta vazia para logs
    },
    "": { # Raiz
        "requirements.txt": "selenium\npandas\ngoogle-generativeai\nopenpyxl\nwebdriver-manager",
        "README.md": "# Bot Neoenergia\n\nExecute `pip install -r requirements.txt` e depois `python neoenergia_bot/main.py`."
    }
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Criado arquivo: {path}")

if __name__ == "__main__":
    create_structure(".", structure)
    print("\n✅ Estrutura do projeto 'Antigravity' criada com sucesso!")
    print("👉 Mova seu arquivo 'base.xlsx' para a pasta 'data/input/' antes de começar.")