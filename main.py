import tkinter as tk
from neoenergia_bot.interface.app_ui import AppUI

def main():
    """
    Ponto de entrada principal da aplicação.
    Inicializa a Interface Gráfica e inicia o loop principal do Tkinter.
    """
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

if __name__ == "__main__":
    # A verificação __name__ == "__main__" é essencial no Windows 
    # para evitar problemas ao usar multiprocessing ou gerar executáveis (.exe)
    main()
