import tkinter as tk
from neoenergia_bot.interface.app_ui import AppUI
from neoenergia_bot.utils.logger_config import setup_logger

def main():
    """
    Ponto de entrada principal da aplicação.
    Inicializa a Interface Gráfica e inicia o loop principal do Tkinter.
    """
    # 1. Configura Logging Centralizado (Com Flush Imediato)
    log_file = setup_logger()
    
    # 2. Inicia Interface
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

if __name__ == "__main__":
    # A verificação __name__ == "__main__" é essencial no Windows 
    # para evitar problemas ao usar multiprocessing ou gerar executáveis (.exe)
    main()
