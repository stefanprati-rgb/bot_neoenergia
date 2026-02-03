# Fluxo de Interação (Mapeamento)

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
2. Decisão de múltiplos imóveis (Endereço mascarado vs CSV).