import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import queue
import threading
import os
from neoenergia_bot.core.worker import BotWorker

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity - Automação Neoenergia")
        self.root.geometry("600x650")
        self.root.resizable(True, True)
        
        # Variáveis de controle
        self.log_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker_thread = None
        self.current_file_path = tk.StringVar(value=os.path.abspath("data/input/base.xlsx"))
        self.resume_var = tk.BooleanVar(value=True)

        self._setup_styles()
        self._build_ui()
        
        # Iniciar o servidor de monitoramento da fila
        self._check_queue()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Start.TButton", foreground="white", background="#28a745")
        style.configure("Stop.TButton", foreground="white", background="#dc3545")

    def _build_ui(self):
        # --- Frame Superior (Configuração) ---
        top_frame = ttk.LabelFrame(self.root, text=" Configuração de Entrada ", padding=10)
        top_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(top_frame, text="Arquivo de Clientes:").pack(side="left", padx=5)
        
        self.entry_path = ttk.Entry(top_frame, textvariable=self.current_file_path, state="readonly", width=60)
        self.entry_path.pack(side="left", padx=5, expand=True, fill="x")

        ttk.Button(top_frame, text="Selecionar Outro", command=self._select_file).pack(side="left", padx=5)

        # --- Frame Inferior (Controles) ---
        # Pack bottom first to ensure it stays at the bottom
        control_frame = tk.Frame(self.root) 
        control_frame.pack(side="bottom", fill="x", padx=15, pady=10)

        # Status Bar (at the very bottom)
        self.status_var = tk.StringVar(value="Pronto para iniciar.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        # --- Frame Central (Logs) ---
        # Pack middle last with expand=True to take available space
        log_frame = ttk.LabelFrame(self.root, text=" Logs de Execução ", padding=10)
        log_frame.pack(side="top", fill="both", expand=True, padx=15, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, state="disabled", font=("Consolas", 9), background="#f8f9fa")
        self.log_area.pack(fill="both", expand=True)

        self.btn_start = tk.Button(
            control_frame, text="▶ INICIAR ROBÔ", 
            bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"),
            command=self._start_bot, width=15, height=2
        )
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = tk.Button(
            control_frame, text="⏹ PARAR", 
            bg="#dc3545", fg="white", font=("Segoe UI", 10, "bold"),
            command=self._stop_bot, width=15, height=2,
            state="disabled"
        )
        self.btn_stop.pack(side="left", padx=10)

        # Retomar Checkbox
        self.check_resume = ttk.Checkbutton(
            control_frame, text="Ignorar clientes já concluídos (Retomar)", 
            variable=self.resume_var
        )
        self.check_resume.pack(side="left", padx=20)

    def _select_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Planilha de Clientes",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file_path.set(file_path)
            self.update_log(f"📁 Arquivo selecionado: {file_path}")

    def _start_bot(self):
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showwarning("Aviso", "O robô já está em execução!")
            return

        self.stop_event.clear()
        self.log_area.configure(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state="disabled")
        
        self.update_log("🚀 Preparando inicialização...")
        
        # Instancia o worker
        # Nota: O worker usará o caminho do arquivo selecionado na GUI e a opção de retomar
        self.worker_thread = BotWorker(
            self.log_queue, 
            self.stop_event, 
            file_path=self.current_file_path.get(),
            resume_enabled=self.resume_var.get()
        )
        
        # Alterar estados da UI
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status_var.set("🤖 Robô em execução...")

        self.worker_thread.start()

    def _stop_bot(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.update_log("🛑 Solicitando parada segura...")
            self.stop_event.set()
            self.btn_stop.configure(state="disabled")
            self.status_var.set("⏳ Aguardando finalização...")

    def update_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, f"[{threading.current_thread().name}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def _check_queue(self):
        """Monitora a fila de mensagens a cada 100ms."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.update_log(message)
                
                # Se o worker avisar que finalizou, restaurar botões
                if "Worker finalizado" in message:
                    self._reset_ui()
                
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._check_queue)

    def _reset_ui(self):
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.status_var.set("✅ Operação concluída ou interrompida.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()
