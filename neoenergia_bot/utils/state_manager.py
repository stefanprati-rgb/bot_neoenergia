import os
import pandas as pd
import datetime
import logging

logger = logging.getLogger(__name__)

class StateManager:
    """
    Gerencia a persistência do status de processamento dos clientes em CSV.
    Permite que o robô retome o trabalho de onde parou em caso de falha.
    """
    def __init__(self, file_path=None):
        if file_path is None:
            # Caminho padrão: data/logs/status_processamento.csv
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.file_path = os.path.join(base_dir, "data", "logs", "status_processamento.csv")
        else:
            self.file_path = file_path
        
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        """Cria o arquivo e o diretório caso não existam."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['NUMERO_CLIENTE', 'DISTRIBUIDORA', 'STATUS', 'TIMESTAMP'])
            df.to_csv(self.file_path, index=False, encoding='utf-8')
            logger.info(f"🆕 Arquivo de status criado em: {self.file_path}")

    def verificar_cliente(self, cliente_id):
        """
        Retorna True se o cliente já foi processado com sucesso ou nada consta.
        Retorna False se precisar ser processado (ERRO ou Não Existe).
        """
        try:
            if not os.path.exists(self.file_path):
                return False
            
            df = pd.read_csv(self.file_path, dtype=str)
            if df.empty:
                return False
                
            # Filtra pelo cliente mais recente (última linha)
            historico = df[df['NUMERO_CLIENTE'] == str(cliente_id)]
            if not historico.empty:
                ultimo_status = historico.iloc[-1]['STATUS']
                return ultimo_status in ['SUCESSO', 'NADA_CONSTA']
            
            return False
        except Exception as e:
            logger.error(f"⚠️ Erro ao verificar status do cliente {cliente_id}: {e}")
            return False

    def atualizar_status(self, cliente_id, distribuidora, status):
        """Grava uma nova linha de status para o cliente no CSV."""
        try:
            novo_registro = {
                'NUMERO_CLIENTE': str(cliente_id),
                'DISTRIBUIDORA': str(distribuidora),
                'STATUS': str(status),
                'TIMESTAMP': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Append mode para segurança e performance
            df_novo = pd.DataFrame([novo_registro])
            df_novo.to_csv(self.file_path, mode='a', header=False, index=False, encoding='utf-8')
            # logger.info(f"📝 Status atualizado para {cliente_id}: {status}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao gravar status no CSV: {e}")
