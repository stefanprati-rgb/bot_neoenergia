import threading
import logging
import time
import traceback
from neoenergia_bot.utils.data_handler import get_clients_to_process
from neoenergia_bot.core.driver import iniciar_driver
from neoenergia_bot.core.navigator import WhatsAppNavigator
from neoenergia_bot.config.settings import CONTATO_NEOENERGIA, MAPA_DISTRIBUIDORAS
from neoenergia_bot.utils.text_parser import WhatsAppBotParser, Acao
from neoenergia_bot.utils import util

# Configuração de logging
logger = logging.getLogger(__name__)

class BotWorker(threading.Thread):
    """
    Worker que executa a automação em uma thread separada para não travar a GUI.
    """
    def __init__(self, log_queue, stop_event, file_path=None, resume_enabled=True):
        super().__init__()
        self.log_queue = log_queue
        self.stop_event = stop_event
        self.file_path = file_path
        self.resume_enabled = resume_enabled
        self.parser = WhatsAppBotParser()
        self.daemon = True # Garante que a thread morra se o programa principal fechar

    def log(self, message):
        """Envia mensagem para a fila de logs que será lida pela GUI."""
        self.log_queue.put(message)
        logger.info(message)

    def run(self):
        self.driver = None
        try:
            self.log("🤖 Iniciando motor do robô...")
            
            # 1. Carregamento de dados
            self.log("📂 Carregando base de clientes...")
            df = get_clients_to_process(self.file_path)
            total_clientes = len(df)
            self.log(f"✅ {total_clientes} clientes carregados com sucesso.")

            # 2. Inicialização do Selenium
            self.log("🌐 Abrindo navegador e conectando ao WhatsApp...")
            self.driver = iniciar_driver()
            self.navigator = WhatsAppNavigator(self.driver)
            
            self.log("🕒 Aguardando login no WhatsApp Web (leia o QR Code se necessário)...")
            self.driver.get("https://web.whatsapp.com")
            
            # Aguarda o WhatsApp carregar (seletor da lista de chats)
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from neoenergia_bot.config.selectors import selectors
            
            try:
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(selectors.APP_LOADED_SIGNAL))
                self.log("✅ WhatsApp carregado!")
            except:
                self.log("⚠️ Tempo esgotado para login ou carregamento lento.")

            # 3. Gerenciamento de Fila Circular Híbrida (Prioridade + Round-Robin)
            from neoenergia_bot.utils.state_manager import StateManager
            state_manager = StateManager()

            # Converte o DataFrame para dicionários, filtrando quem já foi processado
            fila_completa = [row.to_dict() for _, row in df.iterrows()]
            fila_clientes = []
            
            for c in fila_completa:
                id_cliente = str(c.get('NUMEROCLIENTE', ''))
                if self.resume_enabled and state_manager.verificar_cliente(id_cliente):
                    # self.log(f"⏩ Cliente {id_cliente} já processado anteriormente. Pulando...")
                    continue
                fila_clientes.append(c)

            bots_monitorados = list(MAPA_DISTRIBUIDORAS.values())
            self.log(f"🔄 Iniciando motor Híbrido com {len(fila_clientes)} clientes ativos.")

            # --- MODO SEQUENCIAL (DEBUG/STABILITY) ---
            # Processa um cliente por vez até o final
            
            while fila_clientes:
                if self.stop_event.is_set():
                    self.log("🛑 Interrupção solicitada. Parando fila...")
                    break

                # Pega o próximo cliente da fila (não devolve para o final imediatamente)
                cliente_atual = fila_clientes[0] 
                
                # Identificação
                nome_cliente = cliente_atual.get('RAZÃOSOCIALFATURAMENTO', 'Cliente')
                distribuidora_raw = str(cliente_atual.get('DISTRIBUIDORA', '')).upper()
                
                # Busca nome do bot
                nome_bot = None
                for chave, nome_contato in MAPA_DISTRIBUIDORAS.items():
                    if chave in distribuidora_raw:
                        nome_bot = nome_contato
                        break
                
                if not nome_bot:
                    self.log(f"⚠️ Distribuidora '{distribuidora_raw}' não mapeada. Removendo cliente {nome_cliente}.")
                    fila_clientes.pop(0) # Remove e segue
                    continue

                # Loop de processamento do MESMO cliente
                self.log(f"🔄 Iniciando processamento sequencial de: {nome_cliente}")
                
                cliente_finalizado = False
                while not cliente_finalizado and not self.stop_event.is_set():
                    try:
                        # Executa um passo
                        status_passo = self.processar_cliente(cliente_atual, nome_bot)
                        
                        # Se terminou ou deu erro fatal, marca como finalizado
                        if status_passo not in ["EM_ANDAMENTO", "AGUARDANDO_BOT"]:
                            self.log(f"🏁 Cliente {nome_cliente} finalizado. Resultado: {status_passo}")
                            
                            # Atualiza status persistente
                            state_manager.atualizar_status(
                                cliente_atual.get('NUMEROCLIENTE'),
                                distribuidora_raw,
                                status_passo
                            )
                            
                            cliente_finalizado = True
                            fila_clientes.pop(0) # Remove da fila só agora
                            
                        else:
                            # Se continua, apenas dorme um pouco para não fritar a CPU
                            time.sleep(1)
                            
                    except Exception as e:
                        self.log(f"❌ Erro grave processando {nome_cliente}: {e}")
                        logger.error(traceback.format_exc())
                        fila_clientes.pop(0) # Remove para não travar
                        cliente_finalizado = True

            if not self.stop_event.is_set():
                self.log("🏁 Processamento de todos os clientes finalizado!")
            else:
                self.log("⚠️ Processamento interrompido com clientes ainda na fila.")

        except Exception as e:
            error_msg = f"❌ Erro crítico no motor: {str(e)}"
            self.log(error_msg)
            logger.error(traceback.format_exc())
        
        finally:
            if self.driver:
                self.log("🔌 Fechando navegador...")
                try:
                    self.driver.quit()
                except:
                    pass
            self.log("💤 Worker finalizado.")

    def processar_cliente(self, cliente, nome_bot):
        """Implementa a máquina de estados completa para um único cliente."""
        # Identificação do cliente para logs
        cliente_id = str(cliente.get('NUMEROCLIENTE', 'DESCONHECIDO'))
        razao_social = str(cliente.get('RAZÃOSOCIALFATURAMENTO', 'Cliente'))[:30]
        
        # Inicializa estado se não existir
        if 'ESTADO_ATUAL' not in cliente or not cliente.get('ESTADO_ATUAL'):
            cliente['ESTADO_ATUAL'] = 'INICIO'
            cliente['ULTIMA_MSG_PROCESSADA'] = ''
            cliente['TENTATIVAS_DESCONHECIDAS'] = 0
            self.log(f"🆕 [{cliente_id}] {razao_social} - Iniciando novo atendimento")
        
        # 1. Abre o chat (Garante foco)
        if not self.navigator.buscar_contato(nome_bot):
            self.log(f"⚠️ [{cliente_id}] Falha ao abrir chat com {nome_bot}")
            return "EM_ANDAMENTO"

        # 2. Inicia se necessário
        if cliente.get('ESTADO_ATUAL') == 'INICIO':
            self.log(f"👋 [{cliente_id}] Enviando saudação inicial")
            self.navigator.enviar_mensagem("Olá")
            cliente['ESTADO_ATUAL'] = 'AGUARDANDO_BOT'
            return "EM_ANDAMENTO"

        tentativas = 0
        ultima_msg_processada = cliente.get('ULTIMA_MSG_PROCESSADA', '')
        
        while tentativas < 10:
            if self.stop_event.is_set(): return "INTERROMPIDO"
            
            ultima_msg = self.navigator.ler_ultima_mensagem()
            
            # Se a mensagem é a mesma que já processamos, aguarda nova resposta
            if ultima_msg and ultima_msg == ultima_msg_processada:
                if tentativas % 3 == 0:  # Log a cada 3 tentativas para não poluir
                    self.log(f"⏳ [{cliente_id}] Aguardando nova resposta do bot... (tentativa {tentativas}/10)")
                time.sleep(3)
                tentativas += 1
                continue
            
            acao = self.parser.analisar(ultima_msg)
            msg_preview = ultima_msg[:50] if ultima_msg else "(vazio)"
            self.log(f"🤖 [{cliente_id}] Ação: {acao.name} | Msg: {msg_preview}...")
            
            if acao == Acao.SELECIONAR_MENU or acao == Acao.RECUPERAR:
                self.log(f"📋 [{cliente_id}] Menu detectado. Abrindo modal...")
                if self.navigator.selecionar_opcao_menu("2ª via"):
                    self.log(f"✅ [{cliente_id}] Opção '2ª via' selecionada com sucesso")
                else:
                    self.log(f"⚠️ [{cliente_id}] Falha ao usar modal. Tentando via texto...")
                    self.navigator.enviar_mensagem("2ª via")
                
            elif acao == Acao.ENVIAR_CODIGO:
                codigo = str(cliente.get('NUMEROCLIENTE', ''))
                self.log(f"🔢 [{cliente_id}] Enviando código do cliente: {codigo}")
                self.navigator.enviar_mensagem(codigo)
                
            elif acao == Acao.ENVIAR_DOCUMENTO:
                # Limpa e valida CPF/CNPJ
                doc_raw = cliente.get('CNPJ', cliente.get('CNPJ_CPF', ''))
                doc = util.limpar_cpf_cnpj(doc_raw)
                
                if not doc or len(doc) not in [11, 14]:
                    self.log(f"❌ [{cliente_id}] Documento inválido: '{doc_raw}' -> '{doc}'")
                    return "ERRO_DOCUMENTO"
                
                doc_tipo = "CPF" if len(doc) == 11 else "CNPJ"
                self.log(f"📄 [{cliente_id}] Enviando {doc_tipo}: {doc[:3]}***{doc[-2:]}")
                self.navigator.enviar_mensagem(doc)
                
            elif acao == Acao.CONFIRMAR_DADOS:
                self.log(f"✔️ [{cliente_id}] Confirmando dados")
                self.navigator.enviar_mensagem("Sim")
                
            elif acao == Acao.BAIXAR_FATURA:
                self.log(f"💾 [{cliente_id}] Fatura disponível! Iniciando download...")
                
                # Retry de download (até 3 tentativas)
                max_tentativas_download = 3
                for tentativa_dl in range(1, max_tentativas_download + 1):
                    self.log(f"📥 [{cliente_id}] Tentativa de download {tentativa_dl}/{max_tentativas_download}")
                    if self.navigator.baixar_fatura_e_salvar(cliente):
                        self.log(f"✅ [{cliente_id}] Download concluído com sucesso!")
                        return "SUCESSO"
                    
                    if tentativa_dl < max_tentativas_download:
                        self.log(f"⚠️ [{cliente_id}] Falha no download. Aguardando 3s para retry...")
                        time.sleep(3)
                
                self.log(f"❌ [{cliente_id}] Falha no download após {max_tentativas_download} tentativas")
                return "ERRO_DOWNLOAD"
                
            elif acao == Acao.NADA_CONSTA:
                self.log(f"ℹ️ [{cliente_id}] Sem faturas pendentes (Nada Consta)")
                return "NADA_CONSTA"
                
            elif acao == Acao.ERRO_CADASTRO:
                self.log(f"❌ [{cliente_id}] Erro de cadastro detectado pelo bot")
                return "ERRO_CADASTRO"
                
            elif acao == Acao.REINICIAR:
                self.log(f"🔄 [{cliente_id}] Bot encerrou conversa. Reiniciando fluxo...")
                self.navigator.enviar_mensagem("Olá")
                time.sleep(3)
                
            elif acao == Acao.HUMANO:
                self.log(f"👤 [{cliente_id}] Transferido para atendimento humano. Abortando.")
                return "ERRO_HUMANO"

            elif acao == Acao.DESCONHECIDO:
                # Se não entendeu e já mandamos algo, espera um pouco para ver se chega msg nova
                time.sleep(2)
            
            # Marca a mensagem como processada para não repetir ação
            cliente['ULTIMA_MSG_PROCESSADA'] = ultima_msg
            ultima_msg_processada = ultima_msg
                
            tentativas += 1
            time.sleep(2) # Ritmo de leitura
            
        self.log(f"⏱️ [{cliente_id}] Timeout atingido após {tentativas} tentativas")
        return "TIMEOUT"
