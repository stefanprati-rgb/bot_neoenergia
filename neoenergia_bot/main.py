import tkinter as tk
from neoenergia_bot.interface.app_ui import AppUI

def main():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()