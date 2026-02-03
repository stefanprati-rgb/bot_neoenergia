from selenium.webdriver.common.by import By

class Selectors:
    """
    Seletores robustos baseados em XPATH e atributos ARIA para o WhatsApp Web.
    Evita classes CSS ofuscadas e foca na estrutura semântica dos elementos.
    """
    # --- Área de Busca e Chat ---
    # Seletor de alta robustez para a barra de pesquisa
    SEARCH_BOX = (By.XPATH, "//div[@contenteditable='true'][@aria-autocomplete='list']")
    
    # Seletor Híbrido: Tenta pelo Title (mais exato) ou Texto, restrito à barra lateral (id='side')
    # O '/ancestor::div[@role='row']' garante que clicamos na linha inteira da conversa
    SEARCH_RESULT = (By.XPATH, "//div[@id='side']//span[@title='{}']/ancestor::div[@role='row'] | //div[@id='side']//span[contains(text(), '{}')]/ancestor::div[@role='row']")
    
    # Seletor de Validação: Título do Chat Principal (para saber se o chat abriu mesmo)
    CHAT_HEADER_TITLE = (By.XPATH, "//header//span[@title='{}'] | //header//div[@role='button']//span[contains(text(), '{}')]")

    # Seletor para a bolinha verde (Unread Badge) na barra lateral
    UNREAD_BADGE = (By.XPATH, ".//span[@aria-label and contains(@aria-label, 'não lida')]")
    # Linhas de conversa no painel lateral para iteração
    SIDEBAR_ROW = (By.XPATH, "//div[@id='pane-side']//div[@role='row']")

    # Estratégia Blindada: Procura a div editável DENTRO do rodapé (footer) DENTRO do painel principal (main)
    CHAT_INPUT = (By.XPATH, "//div[@id='main']//footer//div[@contenteditable='true']")
    SEND_BUTTON = (By.XPATH, "//button[@aria-label='Enviar']")

    # --- Leitura de Mensagens ---
    ALL_MESSAGES = (By.XPATH, "//div[contains(@class, 'message-in')]")
    # Classe de texto interna com fallback para garantir captura
    LAST_MESSAGE_TEXT = (By.XPATH, ".//span[contains(@class, '_ao3e')] | .//span[contains(@class, 'selectable-text')]")

    # --- Interação com Botões (Fluxo Neoenergia) ---
    # Botão que abre o modal de serviços
    BTN_VER_OPCOES = (By.XPATH, "//button[contains(., 'Ver opções')]")

    # --- Modal de Serviços (Correção) ---
    # Container principal do modal
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")
    # Pega TODOS os botões de opção (Radio Buttons) dentro do modal
    MODAL_OPTIONS_LIST = (By.XPATH, "//div[@role='dialog']//div[@role='radio']")
    # Botão de Enviar a seleção (ícone send ou botão Enviar no rodapé do modal)
    MODAL_SEND_BTN = (By.XPATH, "//div[@role='dialog']//span[@data-icon='send']/ancestor::div[@role='button'] | //div[@role='dialog']//button[@aria-label='Enviar']")

    # --- Anexos e Arquivos ---
    # Seletor genérico para arquivos (PDFs/Documentos) em mensagens recebidas
    ATTACHMENT_FILE = (By.XPATH, "//div[contains(@class, 'message-in')]//div[@role='button']//span[contains(@class, '_')] | //a[contains(@href, 'blob:')]")
    ATTACHMENT_PDF = (By.XPATH, ".//span[@data-icon='audio-file'] | .//span[contains(text(), '.pdf')]")

    # --- Sinais de Carregamento ---
    APP_LOADED_SIGNAL = (By.ID, "pane-side")

# Instância para facilitar o acesso
selectors = Selectors()