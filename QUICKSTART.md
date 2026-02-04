# 🚀 Guia de Início Rápido - Bot Neoenergia

Este guia te levará do zero ao primeiro download de fatura em **5 minutos**.

## ✅ Checklist Pré-Execução

Antes de começar, certifique-se de ter:

- [ ] Python 3.10+ instalado
- [ ] Google Chrome instalado
- [ ] Planilha `base.xlsx` preparada
- [ ] API Key do Gemini configurada

## 📝 Passo a Passo

### 1️⃣ Instalar Dependências (1 min)

Abra o terminal no diretório do projeto e execute:

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key do Gemini (2 min)

**Opção A - Já tenho a chave:**
```bash
copy .env.example .env
notepad .env
```
Cole sua chave no arquivo e salve.

**Opção B - Preciso criar:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada
5. Execute os comandos da Opção A

### 3️⃣ Preparar Planilha (1 min)

Coloque seu arquivo Excel em: `data/input/base.xlsx`

**Colunas obrigatórias:**
- `NUMEROCLIENTE` - Ex: 123456789
- `CNPJ` - Ex: 12345678901 ou 12345678901234
- `DISTRIBUIDORA` - Ex: COELBA, PERNAMBUCO, etc.
- `RAZÃOSOCIALFATURAMENTO` - Ex: Empresa Exemplo LTDA

**Exemplo de linha:**
```
NUMEROCLIENTE | CNPJ          | DISTRIBUIDORA | RAZÃOSOCIALFATURAMENTO
123456789     | 12345678901   | COELBA        | Empresa Exemplo LTDA
```

### 4️⃣ Executar o Bot (1 min)

```bash
python main.py
```

**O que acontecerá:**

1. Uma janela será aberta
2. Clique no botão **"Iniciar Robô"**
3. O Chrome abrirá automaticamente
4. **PRIMEIRA VEZ:** Escaneie o QR Code do WhatsApp Web com seu celular
5. O bot começará a processar!

## 🎯 O que Esperar

### Durante a Execução

Você verá logs como:

```
🤖 Iniciando motor do robô...
📂 Carregando base de clientes...
✅ 10 clientes carregados com sucesso.
🌐 Abrindo navegador e conectando ao WhatsApp...
✅ WhatsApp carregado!
🆕 [123456789] Empresa Exemplo LTDA - Iniciando novo atendimento
👋 [123456789] Enviando saudação inicial
📋 [123456789] Menu detectado. Abrindo modal...
✅ [123456789] Opção '2ª via' selecionada com sucesso
🔢 [123456789] Enviando código do cliente: 123456789
📄 [123456789] Enviando CNPJ: 123***01
✔️ [123456789] Confirmando dados
💾 [123456789] Fatura disponível! Iniciando download...
📥 [123456789] Tentativa de download 1/3
✅ [123456789] Download concluído com sucesso!
📂 Fatura salva: 123456789_Empresa_Exemplo_LTDA.pdf (245.3 KB)
🏁 Cliente Empresa Exemplo LTDA concluído. Status: SUCESSO
```

### Arquivos Gerados

- **Faturas baixadas:** `Faturas/123456789_Empresa_Exemplo_LTDA.pdf`
- **Log de status:** `data/logs/status_processamento.csv`
- **Sessão do WhatsApp:** `chrome_session/` (não delete!)

## 🛑 Como Parar

- Clique no botão **"Parar Robô"** na interface
- Ou feche a janela
- O progresso será salvo automaticamente

## 🔄 Executar Novamente

Na próxima execução:
- ✅ Não precisará escanear QR Code (sessão salva)
- ✅ Clientes já processados serão pulados automaticamente
- ✅ Continuará de onde parou

Para reprocessar tudo, delete: `data/logs/status_processamento.csv`

## ⚠️ Problemas Comuns

### "ModuleNotFoundError: No module named 'selenium'"
**Solução:** Execute `pip install -r requirements.txt`

### "FileNotFoundError: Planilha de entrada não encontrada"
**Solução:** Verifique se `data/input/base.xlsx` existe

### "API Key do Gemini não configurada"
**Solução:** Verifique se o arquivo `.env` existe e contém a chave

### Chrome não abre
**Solução:** 
1. Verifique se o Chrome está instalado
2. Delete a pasta `chrome_session` e tente novamente

### WhatsApp desconecta
**Solução:**
- Não use o WhatsApp no celular durante a execução
- Mantenha a pasta `chrome_session` intacta

## 📞 Precisa de Ajuda?

1. Consulte o [README.md](README.md) completo
2. Verifique os logs em `data/logs/`
3. Entre em contato com a equipe

---

**Pronto! Você está pronto para automatizar o download de faturas! 🎉**
