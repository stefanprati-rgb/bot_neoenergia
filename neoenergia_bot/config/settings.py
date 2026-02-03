import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# API Key do Google Gemini (Carregada via .env para segurança no GitHub)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Modelo utilizado (conforme project_context.md)
GEMINI_MODEL_NAME = "gemini-1.5-flash"

# --- Caminhos Globais ---
# Caminho raiz do projeto
BASE_DIR = os.getcwd()

# Pasta onde o Chrome salvará o QR Code e a sessão do WhatsApp
CHROME_PROFILE_PATH = os.path.join(BASE_DIR, 'chrome_session')

# Pasta onde as faturas (PDFs) serão baixadas
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Faturas')

# Caminho padrão para a planilha de entrada
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'input', 'base.xlsx')

# --- Configurações de Atendimento ---
# Mapeamento de distribuidoras para os contatos reais no WhatsApp
MAPA_DISTRIBUIDORAS = {
    'COELBA': 'Neoenergia Coelba',
    'PERNAMBUCO': 'Neoenergia Pernambuco',
    'BRASILIA': 'Neoenergia Brasília',
    'ELEKTRO': 'Neoenergia Elektro',
    'COSERN': 'Cosern WhatsApp BT'
}

# Timeout padrão se distribuidora não for identificada
CONTATO_NEOENERGIA = "Neoenergia"

# --- Timeouts e Delays ---
WAIT_TIMEOUT = 20        # Tempo máximo de espera por elemento (segundos)
BOT_RESPONSE_DELAY = 5   # Tempo para o bot 'pensar' e responder (segundos)