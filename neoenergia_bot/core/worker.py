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

            while fila_clientes:
                if self.stop_event.is_set():
                    self.log("🛑 Interrupção solicitada. Parando fila...")
                    break

                # --- FASE 1: PRIORIDADE (Notificações) ---
                bot_prioritario = self.navigator.escanear_mensagens_nao_lidas(bots_monitorados)
                cliente_turno = None
                
                if bot_prioritario:
                    for i, c in enumerate(fila_clientes):
                        dist_xls = str(c.get('DISTRIBUIDORA', '')).upper()
                        if any(k in dist_xls and v == bot_prioritario for k, v in MAPA_DISTRIBUIDORAS.items()):
                            cliente_turno = fila_clientes.pop(i)
                            break
                
                # --- FASE 2: PROGRESSO NORMAL (Round-Robin) ---
                if not cliente_turno:
                    cliente_turno = fila_clientes.pop(0)
                    tempo_desde_ultima = time.time() - cliente_turno.get('ULTIMA_INTERACAO', 0)
                    if tempo_desde_ultima < 5:
                        fila_clientes.append(cliente_turno)
                        time.sleep(1)
                        continue

                # --- EXECUÇÃO DO TURNO ---
                try:
                    distribuidora_raw = str(cliente_turno.get('DISTRIBUIDORA', '')).upper()
                    nome_bot = None
                    for chave, nome_contato in MAPA_DISTRIBUIDORAS.items():
                        if chave in distribuidora_raw:
                            nome_bot = nome_contato
                            break
                    
                    if not nome_bot:
                        self.log(f"⚠️ Distribuidora '{distribuidora_raw}' não mapeada. Removendo.")
                        continue

                    # Executa o processamento completo para o cliente no seu turno
                    status_passo = self.processar_cliente(cliente_turno, nome_bot)
                    
                    if status_passo != "EM_ANDAMENTO":
                        self.log(f"🏁 Cliente {cliente_turno.get('RAZÃOSOCIALFATURAMENTO')} concluído. Status: {status_passo}")
                        self.log_queue.put(f"Status: {status_passo}")
                        state_manager.atualizar_status(
                            cliente_turno.get('NUMEROCLIENTE'),
                            distribuidora_raw,
                            status_passo
                        )
                    else:
                        cliente_turno['ULTIMA_INTERACAO'] = time.time()
                        fila_clientes.append(cliente_turno)
                
                except Exception as e:
                    self.log(f"❌ Erro no turno de {cliente_turno.get('RAZÃOSOCIALFATURAMENTO')}: {str(e)}")
                    continue

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
        # 1. Abre o chat (Garante foco)
        if not self.navigator.buscar_contato(nome_bot):
            return "EM_ANDAMENTO"

        # 2. Inicia se necessário
        if cliente.get('ESTADO_ATUAL') == 'INICIO':
            self.navigator.enviar_mensagem("Olá")
            cliente['ESTADO_ATUAL'] = 'AGUARDANDO_BOT'
            return "EM_ANDAMENTO"

        tentativas = 0
        while tentativas < 10:
            if self.stop_event.is_set(): return "INTERROMPIDO"
            
            ultima_msg = self.navigator.ler_ultima_mensagem()
            acao = self.parser.analisar(ultima_msg)
            
            self.log(f"🤖 Estado: {acao.name} | Msg: {ultima_msg[:30]}...")
            
            if acao == Acao.SELECIONAR_MENU or acao == Acao.RECUPERAR:
                self.log("📋 Menu detectado. Abrindo modal...")
                if self.navigator.selecionar_opcao_menu("2ª via"):
                    self.log("✅ Opção '2ª via' selecionada.")
                else:
                    self.log("⚠️ Falha ao usar modal. Tentando via texto...")
                    self.navigator.enviar_mensagem("2ª via")
                
            elif acao == Acao.ENVIAR_CODIGO:
                self.navigator.enviar_mensagem(str(cliente.get('NUMEROCLIENTE')))
                
            elif acao == Acao.ENVIAR_DOCUMENTO:
                # Limpa pontuação do CPF/CNPJ (utilizando o util criado)
                doc = util.limpar_cpf_cnpj(cliente.get('CNPJ', cliente.get('CNPJ_CPF', '')))
                self.navigator.enviar_mensagem(doc)
                
            elif acao == Acao.CONFIRMAR_DADOS:
                self.navigator.enviar_mensagem("Sim")
                
            elif acao == Acao.BAIXAR_FATURA:
                self.log("✅ Fatura gerada! Baixando...")
                if self.navigator.baixar_fatura_e_salvar(cliente):
                    return "SUCESSO"
                return "ERRO_DOWNLOAD"
                
            elif acao == Acao.NADA_CONSTA:
                return "NADA_CONSTA"
                
            elif acao == Acao.ERRO_CADASTRO:
                return "ERRO_CADASTRO"
                
            elif acao == Acao.REINICIAR:
                self.navigator.enviar_mensagem("Olá")
                time.sleep(3)
                
            elif acao == Acao.HUMANO:
                self.log("⚠️ Bot transferiu para humano. Abortando cliente.")
                return "ERRO_HUMANO"

            elif acao == Acao.DESCONHECIDO:
                # Se não entendeu e já mandamos algo, espera um pouco para ver se chega msg nova
                time.sleep(2)
                
            tentativas += 1
            time.sleep(2) # Ritmo de leitura
            
        return "TIMEOUT"
