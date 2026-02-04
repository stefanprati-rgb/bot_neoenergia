from selenium.webdriver.common.by import By
from datetime import datetime

class Selectors:
    """
    Seletores do WhatsApp Web
    Última atualização: 03/02/2026
    Versão do WhatsApp Web: Atual (Fevereiro 2026)
    Testado em: Neoenergia Pernambuco, Neoenergia Brasília, Coelba, Cosern
    
    Estratégia de Prioridade:
    1. ID único (mais estável)
    2. Atributos ARIA (semânticos)
    3. Data attributes (para testes)
    4. Estrutura DOM (ancestrais/descendentes)
    5. Classes CSS (último recurso - WhatsApp ofusca)
    """

    # ============================================
    # 1. BARRA DE PESQUISA (SEARCH_BOX)
    # ============================================
    SEARCH_BOX = (By.XPATH, "//div[@contenteditable='true'][@aria-autocomplete='list']")
    SEARCH_BOX_ALT1 = (By.CSS_SELECTOR, "div[role='textbox'][aria-autocomplete='list']")
    SEARCH_BOX_ALT2 = (By.XPATH, "//div[@id='side']//div[@contenteditable='true']")

    # ============================================
    # 2. RESULTADO DE BUSCA (SEARCH_RESULT)
    # ============================================
    # Nota: O placeholder {} será substituído pelo nome do contato
    SEARCH_RESULT = (By.XPATH, "//div[@id='side']//span[@title='{}']/ancestor::div[@role='row'] | //div[@id='side']//span[contains(text(), '{}')]/ancestor::div[@role='row']")
    SEARCH_RESULT_ALT1 = (By.XPATH, "//div[@role='listitem']")
    SEARCH_RESULT_ALT2 = (By.XPATH, "//div[@id='pane-side']//div[@role='row']")

    # ============================================
    # 3. CABEÇALHO DO CHAT (CHAT_HEADER_TITLE)
    # ============================================
    CHAT_HEADER_TITLE = (By.XPATH, "//header//span[@title='{}'] | //header//span[contains(text(), '{}')]")
    CHAT_HEADER_TITLE_ALT1 = (By.XPATH, "//header//span[@title]")
    CHAT_HEADER_TITLE_ALT2 = (By.CSS_SELECTOR, "header span[title]")

    # ============================================
    # 4. BADGE DE NÃO LIDA (UNREAD_BADGE)
    # ============================================
    UNREAD_BADGE = (By.XPATH, ".//span[@aria-label and contains(@aria-label, 'não lida')]")
    UNREAD_BADGE_ALT1 = (By.XPATH, ".//span[contains(@aria-label, 'mensagem') and contains(@aria-label, 'não lida')]")
    UNREAD_BADGE_ALT2 = (By.XPATH, ".//div[@role='gridcell']//span[contains(@aria-label, 'mensagem')]")

    # ============================================
    # 5. LINHAS DA SIDEBAR (SIDEBAR_ROW)
    # ============================================
    SIDEBAR_ROW = (By.XPATH, "//div[@id='pane-side']//div[@role='row']")
    SIDEBAR_ROW_ALT1 = (By.XPATH, "//div[@role='row']")
    SIDEBAR_ROW_ALT2 = (By.XPATH, "//div[@role='listitem']")

    # ============================================
    # 6. CAIXA DE TEXTO DO CHAT (CHAT_INPUT) - CRÍTICO
    # ============================================
    CHAT_INPUT = (By.XPATH, "//div[@id='main']//footer//div[@contenteditable='true']")
    CHAT_INPUT_ALT1 = (By.XPATH, "//div[@contenteditable='true' and contains(@aria-label, 'Digitar')]")
    CHAT_INPUT_ALT2 = (By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']")

    # ============================================
    # 7. BOTÃO ENVIAR (SEND_BUTTON)
    # ============================================
    SEND_BUTTON = (By.XPATH, "//button[@aria-label='Enviar']")
    SEND_BUTTON_ALT1 = (By.XPATH, "//button[.//span[@data-icon='send']]")
    SEND_BUTTON_ALT2 = (By.CSS_SELECTOR, "button[aria-label*='Enviar']")

    # ============================================
    # 8. MENSAGENS RECEBIDAS (ALL_MESSAGES)
    # ============================================
    ALL_MESSAGES = (By.XPATH, "//div[contains(@class, 'message-in')]")
    ALL_MESSAGES_ALT1 = (By.XPATH, "//div[@data-pre-plain-text and not(contains(@class, 'message-out'))]")
    ALL_MESSAGES_ALT2 = (By.XPATH, "//div[@data-pre-plain-text][ancestor::div[@id='main']]")

    # ============================================
    # 9. TEXTO DA MENSAGEM (LAST_MESSAGE_TEXT)
    # ============================================
    LAST_MESSAGE_TEXT = (By.XPATH, ".//span[contains(@class, '_ao3e')] | .//span[contains(@class, 'selectable-text')]")
    LAST_MESSAGE_TEXT_ALT1 = (By.XPATH, ".//span[@class and contains(@class, 'selectable-text')]")
    LAST_MESSAGE_TEXT_ALT2 = (By.XPATH, ".//div[@class='copyable-text']//span")

    # ============================================
    # 10. BOTÃO VER OPÇÕES (BTN_VER_OPCOES) - CRÍTICO
    # ============================================
    BTN_VER_OPCOES = (By.XPATH, "//button[contains(., 'Ver opções') or contains(., 'Ver Opções') or contains(., 'VER OPÇÕES')]")
    BTN_VER_OPCOES_ALT1 = (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ver opções')]")
    BTN_VER_OPCOES_ALT2 = (By.XPATH, "//button[@role='button'][contains(., 'opções')]")

    # ============================================
    # 11. MODAL DE OPÇÕES (MODAL_DIALOG)
    # ============================================
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")
    MODAL_DIALOG_ALT1 = (By.XPATH, "//div[@role='dialog'][@aria-modal='true']")
    MODAL_DIALOG_ALT2 = (By.CSS_SELECTOR, "div[role='dialog']")

    # ============================================
    # 12. OPÇÕES DO MODAL (MODAL_OPTIONS_LIST)
    # ============================================
    MODAL_OPTIONS_LIST = (By.XPATH, "//div[@role='dialog']//div[@role='radio']")
    MODAL_OPTIONS_LIST_ALT1 = (By.XPATH, "//div[@role='dialog']//label[@role='radio']")
    MODAL_OPTIONS_LIST_ALT2 = (By.XPATH, "//div[@role='dialog']//span[contains(@class, 'selectable-text')]")

    # ============================================
    # 13. BOTÃO ENVIAR DO MODAL (MODAL_SEND_BTN) - CRÍTICO
    # ============================================
    MODAL_SEND_BTN = (By.XPATH, "//div[@role='dialog']//span[@data-icon='send']/ancestor::div[@role='button'] | //div[@role='dialog']//button[@aria-label='Enviar']")
    MODAL_SEND_BTN_ALT1 = (By.XPATH, "//div[@role='dialog']//button[.//span[@data-icon='send']]")
    MODAL_SEND_BTN_ALT2 = (By.XPATH, "//div[@role='dialog']//div[@role='button'][.//span[@data-icon='send']]")

    # ============================================
    # 14. ANEXOS/ARQUIVOS (ATTACHMENT_FILE)
    # ============================================
    ATTACHMENT_FILE = (By.XPATH, "//div[contains(@class, 'message-in')]//div[@role='button']//span[contains(@class, '_')] | //a[contains(@href, 'blob:')]")
    ATTACHMENT_FILE_ALT1 = (By.XPATH, "//div[contains(@class, 'message-in')]//span[@data-icon]")
    ATTACHMENT_FILE_ALT2 = (By.XPATH, "//span[@data-icon='document'] | //span[@data-icon='audio-file']")
    
    # Seletor específico para PDFs
    ATTACHMENT_PDF = (By.XPATH, ".//span[@data-icon='audio-file'] | .//span[contains(text(), '.pdf')]")

    # ============================================
    # 15. SINAL DE CARREGAMENTO (APP_LOADED_SIGNAL) - CRÍTICO
    # ============================================
    APP_LOADED_SIGNAL = (By.ID, "pane-side")
    APP_LOADED_SIGNAL_ALT1 = (By.XPATH, "//div[@id='pane-side']")
    APP_LOADED_SIGNAL_ALT2 = (By.ID, "side")

    # ============================================
    # ELEMENTOS CRÍTICOS PARA O BOT
    # ============================================
    CRITICAL_ELEMENTS = [
        'SEARCH_BOX',        # Sem isso, não consegue buscar contatos
        'CHAT_INPUT',        # Sem isso, não consegue enviar mensagens
        'LAST_MESSAGE_TEXT', # Sem isso, não consegue ler respostas
        'BTN_VER_OPCOES',    # Sem isso, não abre menus interativos
        'MODAL_SEND_BTN',    # Sem isso, não envia seleções do modal
        'APP_LOADED_SIGNAL', # Sem isso, não detecta carregamento
    ]

    @staticmethod
    def get_selector(element_name, use_alternative=0):
        """
        Obtém seletor por nome do elemento com suporte a fallback.
        
        Args:
            element_name (str): Nome do elemento (ex: 'SEARCH_BOX')
            use_alternative (int): 0=principal, 1=ALT1, 2=ALT2
        
        Returns:
            tuple: (By, selector_string)
        
        Raises:
            AttributeError: Se o seletor não existir
        """
        if use_alternative == 0:
            selector_name = element_name
        else:
            selector_name = f"{element_name}_ALT{use_alternative}"
        
        if hasattr(Selectors, selector_name):
            return getattr(Selectors, selector_name)
        raise AttributeError(f"Seletor '{selector_name}' não encontrado")

    @staticmethod
    def print_metadata():
        """Imprime informações sobre os seletores"""
        print("=" * 60)
        print("📋 Seletores do WhatsApp Web")
        print("=" * 60)
        print(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"Versão: Fevereiro 2026")
        print(f"Elementos críticos: {len(Selectors.CRITICAL_ELEMENTS)}")
        print(f"Total de seletores: 15 elementos × 3 variantes = 45 seletores")
        print("=" * 60)

# Instância para facilitar o acesso
selectors = Selectors()