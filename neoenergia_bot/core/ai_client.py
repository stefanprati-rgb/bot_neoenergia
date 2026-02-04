import logging
import google.generativeai as genai
import json
from neoenergia_bot.config.settings import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# Configuração da API
genai.configure(api_key=GEMINI_API_KEY)

def consultar_gemini(historico_conversa: str):
    """
    Consulta o modelo Gemini para decidir o próximo passo quando a lógica 
    determinística falha ou encontra um fluxo desconhecido.
    
    # Limitação: Gemini 2.0 Flash (Gratuito: 2.000 RPM - RPM = Requisições Pr Mimuto).
    """
    if GEMINI_API_KEY == "SUA_CHAVE_AQUI" or not GEMINI_API_KEY:
        logger.warning("⚠️ API Key do Gemini não configurada em settings.py.")
        return None

    try:
        # Prompt de Sistema para classificação direta de ações
        system_instruction = (
            "Você é um assistente de automação que lê chats de energia. "
            "Classifique a última mensagem do bot em uma destas AÇÕES: "
            "[ENVIAR_CODIGO, ENVIAR_DOCUMENTO, SELECIONAR_MENU, BAIXAR_FATURA, CONFIRMAR, ERRO, RECUPERAR, REINICIAR, DESCONHECIDO]. "
            "Responda APENAS a ação."
        )

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash", 
            system_instruction=system_instruction
        )

        prompt = f"Última mensagem do bot: {historico_conversa}"
        
        response = model.generate_content(prompt)
        content = response.text.upper().strip()
        
        logger.info(f"🧠 Gemini classificou como: {content}")
        return content

    except Exception as e:
        logger.error(f"❌ Falha na comunicação com Gemini: {str(e)}")
        # Em caso de erro, retorna DESCONHECIDO para não travar o fluxo
        return "DESCONHECIDO"

if __name__ == "__main__":
    # Teste rápido (requer API Key válida)
    logging.basicConfig(level=logging.INFO)
    hist = "Bot: Olá! Escolha o serviço.\nUsuário: Quero falar com atendente."
    resultado = consultar_gemini(hist)
    print(f"Resultado do teste: {resultado}")