# 🤖 Bot Neoenergia - Automação de Download de Faturas

Robô RPA (Robotic Process Automation) desenvolvido em Python que utiliza Selenium para interagir com o WhatsApp Web da Neoenergia (PE/BA/Brasília/Elektro/Cosern) e automatizar o download de segunda via de contas de energia.

## 📋 Características

- ✅ **Automação Completa**: Interage com o bot do WhatsApp da Neoenergia para solicitar e baixar faturas
- 🔄 **Processamento em Lote**: Processa múltiplos clientes de uma planilha Excel
- 🧠 **Inteligência Híbrida**: Usa regex para 95% das interações + Gemini AI para casos excepcionais
- 💾 **Persistência de Estado**: Retoma de onde parou em caso de interrupção
- 🎯 **Sistema de Prioridades**: Fila circular híbrida (prioridade + round-robin)
- 📊 **Interface Gráfica**: GUI em Tkinter para fácil operação
- 🔐 **Sessão Persistente**: Mantém login do WhatsApp entre execuções

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.10 ou superior
- Google Chrome instalado
- Conta Google com API Key do Gemini (gratuita)

### 2. Clone ou baixe o projeto

```bash
cd "c:\Projetos\Bot Neoenergia"
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key do Gemini

1. Obtenha sua chave em: https://makersuite.google.com/app/apikey
2. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env
   ```
3. Edite o arquivo `.env` e insira sua chave:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

### 5. Prepare sua planilha de clientes

Coloque seu arquivo Excel em `data/input/base.xlsx` com as seguintes colunas:

- **NUMEROCLIENTE**: Código do cliente na distribuidora
- **CNPJ**: CPF ou CNPJ do titular (será formatado automaticamente)
- **DISTRIBUIDORA**: Nome da distribuidora (COELBA, PERNAMBUCO, BRASILIA, ELEKTRO, COSERN)
- **RAZÃOSOCIALFATURAMENTO**: Nome do cliente (para renomear o arquivo)

## 🎮 Como Usar

### Modo GUI (Recomendado)

```bash
python main.py
```

1. A janela será aberta
2. Clique em **"Iniciar Robô"**
3. Na primeira execução, escaneie o QR Code do WhatsApp Web
4. O robô começará a processar automaticamente

### Modo Avançado

Para processar um arquivo específico ou desabilitar o resume:

```python
from neoenergia_bot.core.worker import BotWorker
import queue

log_queue = queue.Queue()
stop_event = threading.Event()

worker = BotWorker(
    log_queue=log_queue,
    stop_event=stop_event,
    file_path="caminho/para/planilha.xlsx",  # Opcional
    resume_enabled=True  # False para reprocessar tudo
)
worker.start()
```

## 📁 Estrutura do Projeto

```
Bot Neoenergia/
├── .agent/                      # Documentação de contexto do projeto
│   ├── project_context.md       # Objetivo e restrições
│   ├── data_rules.md            # Regras de tratamento de dados
│   ├── interaction_flow.md      # Mapeamento do fluxo de conversação
│   └── coding_standards.md      # Padrões de código
├── neoenergia_bot/
│   ├── config/
│   │   ├── settings.py          # Configurações globais
│   │   └── selectors.py         # Seletores do WhatsApp Web
│   ├── core/
│   │   ├── driver.py            # Gerenciamento do Selenium
│   │   ├── navigator.py         # Lógica de navegação
│   │   ├── worker.py            # Motor principal (máquina de estados)
│   │   └── ai_client.py         # Cliente Gemini
│   ├── utils/
│   │   ├── data_handler.py      # Leitura e limpeza de dados
│   │   ├── text_parser.py       # Parser de mensagens (regex)
│   │   ├── state_manager.py     # Persistência de estado
│   │   └── util.py              # Funções auxiliares
│   └── interface/
│       └── app_ui.py            # Interface gráfica
├── data/
│   ├── input/                   # Planilhas de entrada
│   ├── logs/                    # Logs de execução
│   └── output/                  # (Reservado)
├── Faturas/                     # PDFs baixados
├── chrome_session/              # Sessão do WhatsApp (gerada automaticamente)
├── .env                         # Configurações sensíveis (não versionado)
├── requirements.txt
└── main.py                      # Ponto de entrada
```

## 🔧 Configurações Avançadas

### Timeouts e Delays

Edite `neoenergia_bot/config/settings.py`:

```python
WAIT_TIMEOUT = 20        # Tempo máximo de espera por elemento (segundos)
BOT_RESPONSE_DELAY = 5   # Tempo para o bot 'pensar' (segundos)
```

### Mapeamento de Distribuidoras

```python
MAPA_DISTRIBUIDORAS = {
    'COELBA': 'Neoenergia Coelba',
    'PERNAMBUCO': 'Neoenergia Pernambuco',
    'BRASILIA': 'Neoenergia Brasília',
    'ELEKTRO': 'Neoenergia Elektro',
    'COSERN': 'Cosern WhatsApp BT'
}
```

## 📊 Status de Processamento

Os status possíveis são:

- **SUCESSO**: Fatura baixada com sucesso
- **NADA_CONSTA**: Cliente sem faturas pendentes
- **ERRO_CADASTRO**: Dados não encontrados no sistema da distribuidora
- **ERRO_DOCUMENTO**: CPF/CNPJ inválido
- **ERRO_DOWNLOAD**: Falha ao baixar o arquivo
- **ERRO_HUMANO**: Bot transferiu para atendimento humano
- **TIMEOUT**: Tempo limite excedido
- **INTERROMPIDO**: Usuário parou o processo

O histórico fica salvo em: `data/logs/status_processamento.csv`

## 🐛 Troubleshooting

### "Erro ao iniciar o driver"
- Verifique se o Google Chrome está instalado
- Tente deletar a pasta `chrome_session` e executar novamente

### "API Key do Gemini não configurada"
- Verifique se o arquivo `.env` existe e contém a chave correta
- A chave deve estar no formato: `GEMINI_API_KEY=AIza...`

### "Arquivo não localizado em: data/input/base.xlsx"
- Certifique-se de que a planilha está no caminho correto
- Verifique se o nome do arquivo está exatamente como `base.xlsx`

### WhatsApp desconecta frequentemente
- O WhatsApp Web tem limite de dispositivos conectados
- Evite usar o WhatsApp no celular durante a execução
- A pasta `chrome_session` mantém a sessão, não delete

### Bot não detecta mensagens
- Aguarde alguns segundos após cada interação
- Verifique se os seletores estão atualizados (WhatsApp muda periodicamente)
- Consulte os logs em `data/logs/`

## 🔒 Segurança e Privacidade

- ⚠️ **Nunca compartilhe seu arquivo `.env`** (contém sua API Key)
- ⚠️ **Não versione a pasta `chrome_session`** (contém sessão do WhatsApp)
- ⚠️ **Não versione planilhas com dados reais** (LGPD)
- ✅ O `.gitignore` já está configurado para proteger esses arquivos

## 📈 Otimização de Uso da API Gemini

O plano gratuito do Gemini tem **20 requisições/dia**. O bot economiza chamadas usando:

1. **Parser Local (Regex)**: 95% das interações
2. **Gemini AI**: Apenas para mensagens desconhecidas (após 3 tentativas locais)

Média esperada: **1-2 chamadas por dia** em operação normal.

## 📝 Licença

Este projeto é de uso interno. Consulte a equipe antes de distribuir.

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique a seção **Troubleshooting** acima
2. Consulte os logs em `data/logs/`
3. Entre em contato com a equipe de desenvolvimento

---

**Desenvolvido com ❤️ usando Python, Selenium e Gemini AI**