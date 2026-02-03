import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from neoenergia_bot.config.settings import CHROME_PROFILE_PATH, DOWNLOAD_DIR
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

def iniciar_driver():
    """
    Configura e inicia o Google Chrome com persistência de dados e 
    configurações otimizadas para o WhatsApp Web e downloads automáticos.
    """
    try:
        # Definir caminhos usando as constantes do settings.py (Garantindo que sejam absolutos)
        profile_path = os.path.abspath(CHROME_PROFILE_PATH)
        download_path = os.path.abspath(DOWNLOAD_DIR)

        # Criar pasta de faturas e de sessão se não existirem
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            logger.info(f"Pasta de faturas criada em: {download_path}")
        
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
            logger.info(f"Pasta de sessão (perfil) criada em: {profile_path}")

        # 2. Configurar Opções do Chrome
        chrome_options = Options()
        
        # Manter sessão do WhatsApp logada (Argumentos Críticos)
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        chrome_options.add_argument("--profile-directory=Default")
        
        # Estética e estabilidade
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        
        # Configurações de Download e comportamento de PDF
        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True, # Força o download em vez de abrir no browser
            "profile.default_content_settings.popups": 0
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Evitar detecção de bot básica
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 3. Gerenciar e Iniciar Driver
        logger.info("Verificando/Instalando ChromeDriver via webdriver_manager...")
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        logger.info("✅ Selenium Driver iniciado com sucesso.")
        return driver

    except Exception as e:
        logger.error(f"❌ Erro ao iniciar o driver: {str(e)}")
        raise e

if __name__ == "__main__":
    # Teste de inicialização
    logging.basicConfig(level=logging.INFO)
    try:
        dr = iniciar_driver()
        dr.get("https://web.whatsapp.com")
        print("Driver iniciado e carregando WhatsApp Web...")
        # Mantém aberto por 5 segundos para validar
        import time
        time.sleep(5)
        dr.quit()
    except Exception as err:
        print(f"Falha no teste: {err}")