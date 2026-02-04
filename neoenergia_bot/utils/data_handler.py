import pandas as pd
import os
import re
import logging

# Configuração de logging básica
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# REMOVIDO: Usar logger centralizado do neoenergia_bot.utils.logger_config

def clean_document(doc):
    """
    Limpa o documento (CPF/CNPJ) removendo pontuação e adicionando zeros à esquerda.
    Regra conforme data_rules.md:
    - CPF: .zfill(11)
    - CNPJ: .zfill(14)
    """
    if pd.isna(doc) or doc == '':
        return ''
    
    # Converte para string e remove caracteres não numéricos
    clean_doc = re.sub(r'\D', '', str(doc))
    
    if not clean_doc:
        return ''

    # Define o tamanho com base na quantidade de dígitos (simplificado)
    # CPFs têm 11 dígitos ou menos (antes do zfill)
    # CNPJs têm entre 12 e 14 dígitos
    if len(clean_doc) <= 11:
        return clean_doc.zfill(11)
    else:
        return clean_doc.zfill(14)

def load_excel_data(file_path: str) -> pd.DataFrame:
    """
    Lê a planilha na pasta data/input e aplica as regras de limpeza.
    """
    if not os.path.exists(file_path):
        logging.error(f"Arquivo não localizado em: {file_path}")
        raise FileNotFoundError(f"Planilha de entrada não encontrada: {file_path}")

    logging.info(f"Carregando dados de: {file_path}")
    
    # Lemos tudo como string
    df = pd.read_excel(file_path, dtype=str)
    
    # Normalização robusta de colunas: 
    # 1. Remove quebras de linha e espaços extras internos
    # 2. Converte para UPPERCASE
    # 3. Remove caracteres invisíveis/nulos
    df.columns = [re.sub(r'[\s\n\r]+', '', str(col)).upper() for col in df.columns]

    logging.info(f"Colunas identificadas: {df.columns.tolist()}")

    # Regras de limpeza conforme data_rules.md
    if 'CNPJ' in df.columns:
        logging.info("Aplicando limpeza na coluna CNPJ.")
        df['CNPJ'] = df['CNPJ'].apply(clean_document)
    
    if 'NUMEROCLIENTE' in df.columns:
        logging.info("Tratando coluna NUMERO CLIENTE.")
        df['NUMEROCLIENTE'] = df['NUMEROCLIENTE'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    return df

def get_clients_to_process(file_path: str = None) -> pd.DataFrame:
    """
    Função facilitadora para obter os dados prontos para o loop principal.
    """
    if file_path is None:
        # Assume caminho relativo padrão do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, "data", "input", "base.xlsx")
    
    df = load_excel_data(file_path)

    # -----------------------------------------------------------
    # CORREÇÃO DE DUPLICATAS (Fix Loop Issue)
    # Remove clientes duplicados mantendo apenas a primeira ocorrência
    # -----------------------------------------------------------
    if 'NUMEROCLIENTE' in df.columns:
        total_antes = len(df)
        df.drop_duplicates(subset=['NUMEROCLIENTE', 'DISTRIBUIDORA'], keep='first', inplace=True)
        total_depois = len(df)
        if total_antes != total_depois:
            logging.warning(f"⚠️ Removidos {total_antes - total_depois} clientes duplicados da lista.")
    
    # Inicializa colunas de controle para arquitetura Round-Robin
    df['ESTADO_ATUAL'] = 'INICIO'
    df['ULTIMA_INTERACAO'] = 0.0 # Timestamp
    df['ULTIMA_MSG_PROCESSADA'] = ""
    df['TENTATIVAS_DESCONHECIDAS'] = 0
    df['INICIO_ATENDIMENTO'] = 0.0
    
    return df

if __name__ == "__main__":
    # Teste de carregamento
    try:
        df = get_clients_to_process()
        print("\n--- Preview dos Dados ---")
        print(df.head())
        print("\n--- Colunas Encontradas ---")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Erro no teste: {e}")