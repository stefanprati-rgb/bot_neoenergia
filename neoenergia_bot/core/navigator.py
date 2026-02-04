import time
import os
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from neoenergia_bot.config.selectors import selectors
from neoenergia_bot.utils.text_parser import analisar_mensagem, Acao
from neoenergia_bot.core.ai_client import consultar_gemini
from neoenergia_bot.config.settings import WAIT_TIMEOUT, BOT_RESPONSE_DELAY

logger = logging.getLogger(__name__)

class WhatsAppNavigator:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)
        self.short_wait = WebDriverWait(driver, 5) # Mantém 5s para elementos rápidos

    # --- Helpers Robustos ---
    def _click_js(self, element):
        """Clique forçado via JS para elementos bloqueados ou ocultos"""
        self.driver.execute_script("arguments[0].click();", element)

    def _encontrar_elemento(self, by, selector, timeout=5):
        """Busca elemento com tratamento de Stale Reference"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                element = self.wait.until(EC.presence_of_element_located((by, selector)))
                return element
            except StaleElementReferenceException:
                time.sleep(0.1)
                continue
            except:
                return None
        return None

    def escanear_mensagens_nao_lidas(self, lista_bots_alvo):
        """
        Escaneia a barra lateral em busca de mensagens não lidas nos bots alvo.
        Retorna o nome do primeiro bot encontrado com notificação.
        """
        try:
            # Pega as linhas visíveis na sidebar
            linhas = self.driver.find_elements(*selectors.SIDEBAR_ROW)
            
            for linha in linhas:
                try:
                    conteudo = linha.text
                    # Verifica se o texto da linha contém algum dos bots monitorados
                    bot_encontrado = None
                    for bot_nome in lista_bots_alvo:
                        if bot_nome in conteudo:
                            bot_encontrado = bot_nome
                            break
                    
                    if bot_encontrado:
                        # Verifica se existe o badge de não lida DENTRO desta linha específica
                        badges = linha.find_elements(*selectors.UNREAD_BADGE)
                        if badges:
                            return bot_encontrado
                except:
                    continue
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao escanear sidebar: {e}")
            return None

    def buscar_contato(self, nome_contato):
        """Busca um contato na barra lateral e garante que a conversa foi aberta via teclado (ENTER)."""
        try:
            # 1. Encontra e Limpa a Caixa de Busca
            search_box = self.wait.until(EC.element_to_be_clickable(selectors.SEARCH_BOX))
            search_box.click()
            
            # Atalho para limpar tudo (Ctrl+A -> Delete)
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.DELETE)
            time.sleep(1)
            
            # 2. Digita o Nome
            logger.info(f"⌨️ Digitando busca: {nome_contato}")
            search_box.send_keys(nome_contato)
            time.sleep(2) # Espera a lista filtrar
            
            # 3. Pressiona ENTER (Força a abertura do primeiro resultado)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2) # Espera o chat carregar
            
            # 4. VALIDAÇÃO CRÍTICA
            # Verifica se o nome no TOPO do chat (Header) contém o nome buscado
            header_xpath = f"//header//span[contains(@title, '{nome_contato}')] | //header//span[contains(text(), '{nome_contato}')]"
            self.wait.until(EC.presence_of_element_located((By.XPATH, header_xpath)))
            
            logger.info(f"✅ Chat aberto com sucesso: {nome_contato}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Falha ao abrir contato {nome_contato}: {e}")
            # Tenta limpar a busca para não travar o próximo cliente
            try: 
                btn_cancel = self.driver.find_element(By.XPATH, "//button[@aria-label='Cancelar pesquisa'] | //span[@data-icon='x-alt']")
                btn_cancel.click()
            except: 
                pass
            return False

    def enviar_mensagem(self, texto):
        """Envia uma mensagem de texto no chat ativo com garantia de foco e limpeza."""
        try:
            # Aguarda a caixa de texto aparecer (garante que o chat carregou)
            caixa_msg = self.wait.until(EC.element_to_be_clickable(selectors.CHAT_INPUT))
            
            caixa_msg.click() # Garante o foco no elemento
            time.sleep(0.5)  # Pequena pausa humana para estabilidade
            
            # Limpa rascunhos anteriores enviando comando de seleção total e backspace
            caixa_msg.send_keys(Keys.CONTROL + "a")
            caixa_msg.send_keys(Keys.BACKSPACE)
            
            caixa_msg.send_keys(texto)
            time.sleep(0.5)
            caixa_msg.send_keys(Keys.ENTER)
            
            time.sleep(3) # Delay pós-envio (anti-bloqueio)
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao digitar mensagem: {e}")
            raise e # Propaga o erro para o worker registrar no log da GUI

    # --- Interação com Modal ---
    def selecionar_opcao_menu(self, texto_alvo):
        logger.info(f"🖱️ [Navigator] Tentando selecionar opção: '{texto_alvo}'")
        
        # 1. Abre o Modal se necessário
        max_tentativas_abrir = 3
        for tentativa in range(max_tentativas_abrir):
            if self._is_modal_open():
                logger.info("✅ Modal já está aberto.")
                break
                
            try:
                # Tentativa Robusta com Seletores Múltiplos
                found_btn = None
                for i in range(3):
                    try:
                        by, xpath = selectors.get_selector('BTN_VER_OPCOES', i)
                        btn_opcoes = self.wait.until(EC.element_to_be_clickable((by, xpath)))
                        found_btn = btn_opcoes
                        logger.info(f"✅ Botão 'Ver opções' encontrado (estratégia {i})")
                        break
                    except:
                        continue
                
                if not found_btn:
                    raise Exception("Botão 'Ver opções' não encontrado com nenhum seletor.")
                
                # Garante visibilidade
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", found_btn)
                time.sleep(0.5)
                
                # Clique via JS (mais confiável)
                self.driver.execute_script("arguments[0].click();", found_btn)
                logger.info("🖱️ Clique no botão 'Ver opções' executado.")
                
                # Aguarda o modal aparecer
                modal_xpath = selectors.get_selector('MODAL_DIALOG', 0)[1]
                self.wait.until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))
                time.sleep(1)  # Estabilização da animação
                break
                
            except Exception as e:
                logger.warning(f"⚠️ Tentativa {tentativa + 1}/{max_tentativas_abrir} falhou ao abrir modal: {e}")
                if tentativa == max_tentativas_abrir - 1:
                    logger.error("❌ Não foi possível abrir o modal após todas as tentativas.")
                    return False
                time.sleep(2)
        
        # 2. Seleciona a Opção
        try:
            # XPath robusto para encontrar a opção desejada
            xpath_opcao = f"//div[@role='dialog']//div[@role='radio'][.//span[contains(text(), '{texto_alvo}')]]"
            
            elemento_clicavel = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_opcao)))
            
            # Garante visibilidade
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_clicavel)
            time.sleep(0.5)
            
            # Clique JS no Elemento
            self.driver.execute_script("arguments[0].click();", elemento_clicavel)
            logger.info(f"✅ Opção '{texto_alvo}' marcada com sucesso.")
            time.sleep(0.5)

            # 3. Clica em Enviar (Robusto)
            btn_enviar = None
            for i in range(3):
                try:
                    by_send, xpath_send = selectors.get_selector('MODAL_SEND_BTN', i)
                    btn_enviar = self.wait.until(EC.element_to_be_clickable((by_send, xpath_send)))
                    break
                except:
                    continue
            
            if btn_enviar:
                self.driver.execute_script("arguments[0].click();", btn_enviar)
                logger.info("📤 Opção enviada com sucesso.")
            else:
                logger.error("❌ Botão de enviar do modal não encontrado.")
                return False
            
            # Aguarda o modal sumir
            try:
                modal_xpath = selectors.get_selector('MODAL_DIALOG', 0)[1]
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, modal_xpath)))
            except:
                pass # Se não sumir, tudo bem, vamos em frente
            
            time.sleep(2)  # Aguarda o bot processar
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao selecionar opção no modal: {e}")
            self.fechar_modal_se_aberto()
            return False

    def _is_modal_open(self):
        try:
            # Usa o seletor principal do modal
            by, xpath = selectors.get_selector('MODAL_DIALOG', 0)
            return self.driver.find_element(by, xpath).is_displayed()
        except:
            return False

    def fechar_modal_se_aberto(self):
        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        except:
            pass



    def ler_ultima_mensagem(self):
        """
        Retorna uma tupla (texto, autor) da última mensagem visível no chat.
        autor: 'BOT' (message-in) ou 'ME' (message-out)
        """
        try:
            # Pega TODAS as mensagens (in e out) ordenadas por ordem de aparição no DOM
            # O WhatsApp Web estrutura as mensagens sequencialmente, então a última div é a mais recente.
            todas_msgs = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in') or contains(@class, 'message-out')]")
            
            if not todas_msgs:
                return "", "VAZIO"
            
            # Pega a última mensagem absoluta
            ultima_msg = todas_msgs[-1]
            
            # Determina o autor pela classe
            classes = ultima_msg.get_attribute("class")
            if "message-in" in classes:
                autor = "BOT"
            elif "message-out" in classes:
                autor = "ME"
            else:
                autor = "DESCONHECIDO"
            
            # Extrai o texto (se houver)
            try:
                texto_el = ultima_msg.find_element(*selectors.LAST_MESSAGE_TEXT)
                texto = texto_el.text
            except:
                texto = "[Mídia/Arquivo/Outros]"
                
            return texto, autor
            
        except Exception as e:
            # logger.error(f"Erro ao ler mensagens: {e}") # Log opcional para não poluir
            return "", "ERRO"

    def _baixar_anexo(self):
        """Tenta baixar a fatura usando múltiplas estratégias e monitora a pasta de destino."""
        logger.info("📂 Tentando baixar fatura...")
        from neoenergia_bot.config.settings import DOWNLOAD_DIR
        caminho_download = DOWNLOAD_DIR
        
        if not os.path.exists(caminho_download):
            os.makedirs(caminho_download)

        # Lista de tentativas de seletores (do mais específico para o genérico)
        seletores_download = [
            # 1. Botão de Download explícito (ícone de seta para baixo)
            (By.XPATH, "//div[contains(@class, 'message-in')]//span[@data-icon='download']"),
            
            # 2. Link direto de arquivo (blob ou normal) dentro da mensagem
            (By.XPATH, "//div[contains(@class, 'message-in')]//a[contains(@href, 'blob:') or contains(@href, '.pdf')]"),
            
            # 3. O próprio container do arquivo (clique no ícone de documento)
            (By.XPATH, "//div[contains(@class, 'message-in')]//span[@data-icon='audio-file']") 
        ]
        
        sucesso = False
        for by, xpath in seletores_download:
            try:
                # Tenta encontrar elementos visíveis
                botoes = self.driver.find_elements(by, xpath)
                if botoes:
                    # Pega sempre o ÚLTIMO botão encontrado (mensagem mais recente)
                    botao_alvo = botoes[-1]
                    self.driver.execute_script("arguments[0].click();", botao_alvo)
                    logger.info(f"🖱️ Clique de download realizado via: {xpath}")
                    sucesso = True
                    break
            except Exception:
                continue
                
        if not sucesso:
            logger.warning("❌ Nenhum botão de download detectado no chat.")
            return False

        # Espera Inteligente pelo Arquivo
        logger.info("🕒 Aguardando conclusão do download...")
        tempo_max = 20 # Aumentado para 20s para maior segurança
        arquivos_antes = set(os.listdir(caminho_download))
        for _ in range(tempo_max):
            arquivos_agora = set(os.listdir(caminho_download))
            novos = arquivos_agora - arquivos_antes
            if novos:
                arquivo_baixado = list(novos)[0]
                # Verifica se não é um arquivo temporário de download do Chrome
                if not arquivo_baixado.endswith('.crdownload') and not arquivo_baixado.startswith('.com.google.Chrome'):
                    logger.info(f"✅ Arquivo baixado com sucesso: {arquivo_baixado}")
                    return True
            time.sleep(1)

        logger.error("❌ Timeout: O clique foi feito, mas o arquivo não apareceu na pasta.")
        return False

    def baixar_fatura_e_salvar(self, cliente):
        """Tenta baixar o anexo e renomear com o nome do cliente."""
        nome_cliente = str(cliente.get('RAZÃOSOCIALFATURAMENTO', 'Cliente')).strip()
        num_cliente = str(cliente.get('NUMEROCLIENTE', '000'))
        
        from neoenergia_bot.config.settings import DOWNLOAD_DIR
        caminho_download = DOWNLOAD_DIR
        
        # Guardamos a lista de arquivos antes do download
        arquivos_antes = set(os.listdir(caminho_download))
        
        if self._baixar_anexo():
            # Espera um pouco para o sistema de arquivos registrar o novo arquivo
            time.sleep(2)
            arquivos_depois = set(os.listdir(caminho_download))
            novos = arquivos_depois - arquivos_antes
            
            if novos:
                arquivo_original = list(novos)[0]
                # Não renomeia se for temporário
                if arquivo_original.endswith('.crdownload'):
                    logger.info("⏳ Aguardando conclusão do download...")
                    time.sleep(3) # Espera mais um pouco
                    arquivos_depois = set(os.listdir(caminho_download))
                    novos = arquivos_depois - arquivos_antes
                    if not novos: 
                        logger.warning("⚠️ Arquivo temporário não finalizou")
                        return False
                    arquivo_original = list(novos)[0]

                # Valida o arquivo baixado
                origem = os.path.join(caminho_download, arquivo_original)
                tamanho_arquivo = os.path.getsize(origem)
                
                if tamanho_arquivo < 1024:  # Menos de 1KB é suspeito
                    logger.warning(f"⚠️ Arquivo muito pequeno ({tamanho_arquivo} bytes). Possível erro.")
                    return False

                ext = os.path.splitext(arquivo_original)[1] or ".pdf"
                # Limpa o nome para evitar caracteres inválidos em caminhos
                nome_limpo = "".join([c if c.isalnum() or c in " _-" else "_" for c in nome_cliente])
                novo_nome = f"{num_cliente}_{nome_limpo}{ext}"
                
                try:
                    destino = os.path.join(caminho_download, novo_nome)
                    
                    # Se o destino já existir, adiciona timestamp para não sobrescrever
                    if os.path.exists(destino):
                         timestamp = int(time.time())
                         novo_nome = f"{num_cliente}_{nome_limpo}_{timestamp}{ext}"
                         destino = os.path.join(caminho_download, novo_nome)
                         logger.info(f"📝 Arquivo já existe, adicionando timestamp: {timestamp}")
                         
                    os.rename(origem, destino)
                    tamanho_kb = tamanho_arquivo / 1024
                    logger.info(f"📂 Fatura salva: {novo_nome} ({tamanho_kb:.1f} KB)")
                    return True
                except Exception as e:
                    logger.error(f"❌ Erro ao renomear arquivo: {e}")
                    # Tenta manter o arquivo original ao menos
                    if os.path.exists(origem):
                        logger.info(f"📂 Arquivo mantido com nome original: {arquivo_original}")
                        return True
                    return False
            else:
                logger.warning("⚠️ Nenhum arquivo novo detectado após download")
                return False
        return False

    def executar_passo(self, cliente_dados, nome_bot_alvo, log_callback=None):
        """
        Executa um único passo de interação para o cliente e retorna o novo estado.
        Baseado na arquitetura Round-Robin para permitir multi-atendimento.
        """
        def log(msg):
            logger.info(msg)
            if log_callback:
                log_callback(msg)

        estado_atual = cliente_dados.get('ESTADO_ATUAL', 'INICIO')
        ultima_msg_lida = cliente_dados.get('ULTIMA_MSG_PROCESSADA', '')
        inicio_atendimento = cliente_dados.get('INICIO_ATENDIMENTO', 0.0)
        tentativas_ia = cliente_dados.get('TENTATIVAS_DESCONHECIDAS', 0)

        # 1. Timeout Global para este cliente (2 min)
        agora = time.time()
        if inicio_atendimento > 0 and agora - inicio_atendimento > 120:
             log(f"⚠️ Timeout para cliente {cliente_dados.get('NUMEROCLIENTE')}")
             return 'FINALIZADO', 'TIMEOUT'

        # 2. Abre o chat do cliente (Passo obrigatório em cada ciclo stateless)
        if not self.buscar_contato(nome_bot_alvo):
            return estado_atual, 'EM_ANDAMENTO' # Tenta novamente na próxima rodada

        # 3. Lógica de Estados
        # 3. Lógica de Estados
        if estado_atual == 'INICIO':
            log(f"🚀 Iniciando atendimento para {cliente_dados.get('NUMEROCLIENTE')}...")
            
            # Verificação: Se o menu já está visível, pula a saudação
            msg_existente = self.ler_ultima_mensagem()
            if msg_existente:
                acao_existente = analisar_mensagem(msg_existente)
                if acao_existente == Acao.SELECIONAR_MENU:
                    log("📋 Menu já detectado. Pulando saudação...")
                    if self.selecionar_opcao_menu("2ª via"):
                        cliente_dados['ULTIMA_MSG_PROCESSADA'] = msg_existente
                        cliente_dados['INICIO_ATENDIMENTO'] = time.time()
                        return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'
                    else:
                        # Se falhar ao usar o modal, tenta texto
                        self.enviar_mensagem("2ª via")
                        cliente_dados['INICIO_ATENDIMENTO'] = time.time()
                        return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'
            
            # Só envia "Olá" se realmente precisar iniciar
            log("💬 Enviando saudação inicial...")
            if self.enviar_mensagem("Olá"):
                cliente_dados['INICIO_ATENDIMENTO'] = time.time()
                return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'
            return 'INICIO', 'EM_ANDAMENTO'

        # 4. Leitura da Resposta do Bot
        msg_bot, autor = self.ler_ultima_mensagem()

        # Se a última mensagem foi minha (ME), ainda estamos aguardando resposta.
        if autor == 'ME':
            # log("⏳ Última mensagem é minha. Aguardando parceiro...")
            return estado_atual, 'EM_ANDAMENTO'

        # Só processa se houver uma mensagem nova (diferente da última que o robô reagiu)
        if msg_bot == ultima_msg_lida:
            # log("⏳ Aguardando nova resposta do bot...")
            return estado_atual, 'EM_ANDAMENTO'
            
        if not msg_bot:
            return estado_atual, 'EM_ANDAMENTO'

        log(f"📥 Novo do Bot: {msg_bot[:50]}...")
        cliente_dados['ULTIMA_MSG_PROCESSADA'] = msg_bot
        
        # 5. Análise e Ação Única
        acao = analisar_mensagem(msg_bot)
        
        if acao == Acao.DESCONHECIDO:
            cliente_dados['TENTATIVAS_DESCONHECIDAS'] = tentativas_ia + 1
            log(f"🤔 Parser local não entendeu ({cliente_dados['TENTATIVAS_DESCONHECIDAS']}/3). Consultando Gemini...")
            
            try:
                from neoenergia_bot.utils.text_parser import WhatsAppBotParser
                resposta_ia = consultar_gemini(msg_bot)
                if resposta_ia:
                    acao_ia = WhatsAppBotParser.converter_string_para_acao(resposta_ia)
                    if acao_ia != Acao.DESCONHECIDO:
                        log(f"🤖 Gemini decidiu: {acao_ia.value}")
                        acao = acao_ia
                    else:
                        log("⚠️ Gemini também não soube classificar.")
                
                if acao == Acao.DESCONHECIDO and cliente_dados['TENTATIVAS_DESCONHECIDAS'] >= 3:
                    log("❌ Limite de tentativas desconhecidas atingido.")
                    return 'FINALIZADO', 'ERRO_IA'
            except Exception as e:
                log(f"❌ Erro na consulta ao Gemini: {e}")
                if cliente_dados['TENTATIVAS_DESCONHECIDAS'] >= 3:
                     return 'FINALIZADO', 'ERRO_IA'

        # Execução da Ação (Local ou IA)
        log(f"⚙️ Executando: {acao.value}")

        if acao == Acao.SELECIONAR_MENU:
            if not self.selecionar_opcao_menu("2ª via"):
                self.enviar_mensagem("2ª via")
            return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'

        elif acao == Acao.ENVIAR_CODIGO:
            self.enviar_mensagem(cliente_dados.get('NUMEROCLIENTE'))
            return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'

        elif acao == Acao.ENVIAR_DOCUMENTO:
            doc = cliente_dados.get('CNPJ', '')
            self.enviar_mensagem(doc)
            return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'

        elif acao == Acao.CONFIRMAR_DADOS:
            self.enviar_mensagem("Sim")
            return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'

        elif acao == Acao.BAIXAR_FATURA:
            if self._baixar_anexo():
                return 'FINALIZADO', 'SUCESSO'
            return 'AGUARDANDO_BOT', 'ERRO_DOWNLOAD'

        elif acao == Acao.NADA_CONSTA:
            return 'FINALIZADO', 'NADA_CONSTA'

        elif acao == Acao.ERRO_CADASTRO:
            return 'FINALIZADO', 'ERRO_CADASTRO'

        elif acao == Acao.RECUPERAR:
            log("🏁 Bot perguntou se ainda estou aqui. Recuperando fluxo...")
            self.enviar_mensagem("Sim")
            return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'

        elif acao == Acao.REINICIAR:
            log("🔄 Conversa encerrada pelo bot. Reiniciando fluxo...")
            self.enviar_mensagem("Olá")
            time.sleep(3)
            return 'AGUARDANDO_BOT', 'EM_ANDAMENTO'

        elif acao == Acao.HUMANO:
            log("⚠️ Atendimento humano detectado. Parando processamento para este cliente.")
            return 'FINALIZADO', 'ERRO_HUMANO'

        return estado_atual, 'EM_ANDAMENTO'
