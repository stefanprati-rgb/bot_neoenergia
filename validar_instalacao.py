#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validação da instalação do Bot Neoenergia.
Execute este script para verificar se todas as dependências estão instaladas corretamente.
"""

import sys
import os
import re

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - INCOMPATÍVEL")
        print("   ⚠️  Requer Python 3.10 ou superior")
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    print("\n📦 Verificando dependências...")
    
    dependencies = {
        'selenium': 'Selenium WebDriver',
        'pandas': 'Pandas',
        'openpyxl': 'OpenPyXL',
        'google.generativeai': 'Google Generative AI',
        'webdriver_manager': 'WebDriver Manager',
        'unidecode': 'Unidecode',
        'dotenv': 'Python Dotenv'
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - NÃO INSTALADO")
            all_ok = False
    
    return all_ok

def check_file_structure():
    """Verifica se a estrutura de diretórios está correta."""
    print("\n📁 Verificando estrutura de arquivos...")
    
    required_paths = {
        'data/input': 'Pasta de entrada de dados',
        'data/logs': 'Pasta de logs',
        'Faturas': 'Pasta de faturas',
        '.env.example': 'Arquivo de exemplo de configuração',
        'requirements.txt': 'Arquivo de dependências',
        'neoenergia_bot/core/worker.py': 'Motor principal',
        'neoenergia_bot/config/settings.py': 'Configurações',
    }
    
    all_ok = True
    for path, description in required_paths.items():
        if os.path.exists(path):
            print(f"   ✅ {description}")
        else:
            print(f"   ⚠️  {description} - NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Verifica se o arquivo .env está configurado."""
    print("\n🔑 Verificando configuração da API Key...")
    
    if not os.path.exists('.env'):
        print("   ⚠️  Arquivo .env não encontrado")
        print("   💡 Execute: copy .env.example .env")
        print("   💡 Depois edite o arquivo .env e adicione sua API Key")
        return False
    
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'GEMINI_API_KEY=SUA_CHAVE_AQUI' in content or 'GEMINI_API_KEY=' not in content:
        print("   ⚠️  API Key do Gemini não configurada")
        print("   💡 Edite o arquivo .env e adicione sua chave")
        print("   💡 Obtenha em: https://makersuite.google.com/app/apikey")
        return False
    
    print("   ✅ Arquivo .env configurado")
    return True

def check_excel_file():
    """Verifica se existe um arquivo Excel de entrada."""
    print("\n📊 Verificando planilha de entrada...")
    
    excel_path = 'data/input/base.xlsx'
    if os.path.exists(excel_path):
        print(f"   ✅ Planilha encontrada: {excel_path}")
        
        # Tenta ler a planilha
        try:
            import pandas as pd
            df = pd.read_excel(excel_path, dtype=str, nrows=1)
            # Normaliza colunas igual ao data_handler.py
            df.columns = [re.sub(r'[\s\n\r]+', '', str(col)).upper() for col in df.columns]
            required_cols = ['NUMEROCLIENTE', 'CNPJ', 'DISTRIBUIDORA', 'RAZÃOSOCIALFATURAMENTO']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                print(f"   ⚠️  Colunas faltando: {', '.join(missing_cols)}")
                return False
            else:
                print(f"   ✅ Colunas obrigatórias presentes")
                return True
        except Exception as e:
            print(f"   ⚠️  Erro ao ler planilha: {e}")
            return False
    else:
        print(f"   ⚠️  Planilha não encontrada em: {excel_path}")
        print("   💡 Coloque seu arquivo Excel neste caminho")
        return False

def check_chrome():
    """Verifica se o Chrome está instalado."""
    print("\n🌐 Verificando Google Chrome...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"   ✅ Chrome encontrado: {path}")
            return True
    
    print("   ⚠️  Google Chrome não encontrado")
    print("   💡 Instale o Chrome em: https://www.google.com/chrome/")
    return False

def main():
    """Executa todas as verificações."""
    print("=" * 60)
    print("🔍 VALIDAÇÃO DE INSTALAÇÃO - BOT NEOENERGIA")
    print("=" * 60)
    
    results = {
        'Python': check_python_version(),
        'Dependências': check_dependencies(),
        'Estrutura': check_file_structure(),
        'Configuração': check_env_file(),
        'Planilha': check_excel_file(),
        'Chrome': check_chrome()
    }
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
    
    all_ok = all(results.values())
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 TUDO PRONTO! Você pode executar o bot com: python main.py")
    else:
        print("⚠️  ATENÇÃO: Corrija os problemas acima antes de executar o bot")
        print("💡 Consulte o QUICKSTART.md para mais informações")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
