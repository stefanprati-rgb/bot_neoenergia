from enum import Enum
from unidecode import unidecode

class Acao(Enum):
    SELECIONAR_MENU = "selecionar_menu"
    ENVIAR_CODIGO = "enviar_codigo"
    ENVIAR_DOCUMENTO = "enviar_documento"
    CONFIRMAR_DADOS = "confirmar_dados"
    BAIXAR_FATURA = "baixar_fatura"
    NADA_CONSTA = "nada_consta"
    ERRO_CADASTRO = "erro_cadastro"
    RECUPERAR = "recuperar_fluxo"
    REINICIAR = "reiniciar"
    DESCONHECIDO = "desconhecido"
    HUMANO = "atendimento_humano"

class WhatsAppBotParser:
    @staticmethod
    def normalize(text):
        if not text:
            return ""
        # Remove acentos e converte para minúsculas para robustez total
        return unidecode(text).lower().strip()

    @staticmethod
    def converter_string_para_acao(acao_str):
        """Converte a saída de texto da IA para uma constante do Enum Acao."""
        mapeamento = {
            'ENVIAR_CODIGO': Acao.ENVIAR_CODIGO,
            'ENVIAR_DOCUMENTO': Acao.ENVIAR_DOCUMENTO,
            'SELECIONAR_MENU': Acao.SELECIONAR_MENU,
            'BAIXAR_FATURA': Acao.BAIXAR_FATURA,
            'CONFIRMAR': Acao.CONFIRMAR_DADOS,
            'ERRO': Acao.ERRO_CADASTRO,
            'REINICIAR': Acao.REINICIAR,
            'DESCONHECIDO': Acao.DESCONHECIDO
        }
        return mapeamento.get(acao_str.upper(), Acao.DESCONHECIDO)

    def analisar(self, mensagem):
        if not mensagem:
            return Acao.DESCONHECIDO
            
        msg = self.normalize(mensagem)
        
        # --- PRIORIDADE 1: GATILHOS ESPECÍFICOS (Evita falsos positivos do Menu) ---

        # 1. Pedido de Código (UC)
        # Adicionado: "nao deu certo", "confere e me passa" para retries
        if any(x in msg for x in ['codigo do cliente', 'digite o codigo', 'informe o codigo', 'nao deu certo', 'confere e me passa']):
            return Acao.ENVIAR_CODIGO
            
        # 2. Pedido de Documento (CPF/CNPJ)
        if 'cpf ou cnpj' in msg:
            return Acao.ENVIAR_DOCUMENTO
            
        # 3. Sucesso (Link PDF ou Pix)
        if any(x in msg for x in ['boleto.pdf', 'pix copia e cola', 'encontrei 1 fatura', 'informacoes para pagamento']):
            return Acao.BAIXAR_FATURA
            
        # 4. Nada Consta
        if 'nao tem nenhuma fatura' in msg or 'debitos quitados' in msg:
            return Acao.NADA_CONSTA
            
        # 5. Erro de Cadastro
        if any(x in msg for x in ['nao consegui localizar', 'cadastro esteja desatualizado']):
            return Acao.ERRO_CADASTRO

        # 6. Gatilho de segurança para evitar atendente humano
        if 'meu nome e' in msg and 'vou te auxiliar' in msg:
             return Acao.HUMANO

        # --- PRIORIDADE 2: FLUXO DE NAVEGAÇÃO ---

        # 7. Confirmação de Endereço / Fluxo
        if any(x in msg for x in ['sua unidade consumidora e', 'posso seguir com a solicitacao', 'posso te ajudar com algo mais']):
            return Acao.CONFIRMAR_DADOS

        # 8. Recuperação (Bot esperando)
        if any(x in msg for x in ['ainda estou aqui', 'o que gostaria de fazer agora', 'posso ajudar com mais alguma coisa']):
            return Acao.RECUPERAR
            
        # 9. Encerramento
        if any(x in msg for x in ['vou encerrar', 'agradecemos o seu contato', 'dica de seguranca', 'encerraremos seu atendimento']):
            return Acao.REINICIAR

        # --- PRIORIDADE 3: MENU (GENÉRICO/FALLBACK) ---
        # Fica por último pois 'clique no botao' aparece em várias mensagens acima
        if any(x in msg for x in ['escolha o servico', 'para comecar', 'ver opcoes', 'ver outro servico', 'clique no botao abaixo']):
            return Acao.SELECIONAR_MENU

        # Gatilho de segurança para evitar atendente humano
        if 'meu nome e' in msg and 'vou te auxiliar' in msg:
             return Acao.HUMANO

        return Acao.DESCONHECIDO

def analisar_mensagem(texto):
    """Wrapper para manter compatibilidade com o Navigator."""
    parser = WhatsAppBotParser()
    return parser.analisar(texto)