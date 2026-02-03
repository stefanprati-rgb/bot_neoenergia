# Contexto do Projeto: Automação Neoenergia WhatsApp

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
Você (Agente da IDE) pode usar seus modelos internos livremente para *escrever* o código. Porém, o *código gerado* deve economizar ao máximo as chamadas de API durante a execução.