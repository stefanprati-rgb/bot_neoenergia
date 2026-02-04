import logging
import os
import sys
from datetime import datetime

class ImmediateFileHandler(logging.FileHandler):
    """
    FileHandler que força o flush após cada log emitido.
    Garante que se o programa crashar, o log está salvo no disco.
    """
    def emit(self, record):
        super().emit(record)
        self.flush()

def setup_logger():
    """
    Configura o logger raiz para escrever em arquivo e console com flush imediato.
    """
    # 1. Definição de Caminhos
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except:
        base_dir = "."
        
    log_dir = os.path.join(base_dir, "data", "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Nome do Arquivo por Data
    filename = datetime.now().strftime("execution_%Y-%m-%d.log")
    log_file = os.path.join(log_dir, filename)

    # 2. Configuração do Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove handlers existentes para evitar duplicidade
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # 3. Formatador
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 4. Handler de Arquivo (Flush Imediato)
    file_handler = ImmediateFileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # 5. Handler de Console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    logging.info("="*60)
    logging.info(f"🚀 Logger iniciado. Escrevendo em: {log_file}")
    logging.info("="*60)

    # Redireciona stderr para o logger para pegar crashes não tratados
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.critical("🔥 Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    return log_file
