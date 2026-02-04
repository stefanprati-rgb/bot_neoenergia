# ✅ CHECKLIST FINAL - Bot Neoenergia

Use este checklist para verificar se tudo está pronto antes de executar o bot em produção.

---

## 📋 PRÉ-REQUISITOS

### **Sistema:**
- [ ] Python 3.10 ou superior instalado
- [ ] Google Chrome instalado
- [ ] Conexão estável com a internet
- [ ] Windows com PowerShell

### **Conta e API:**
- [ ] Conta Google criada
- [ ] API Key do Gemini obtida (https://makersuite.google.com/app/apikey)
- [ ] WhatsApp Web disponível para uso

---

## 🔧 INSTALAÇÃO

### **Dependências:**
- [ ] Executado: `pip install -r requirements.txt`
- [ ] Todas as dependências instaladas sem erros
- [ ] Verificado: `selenium`, `pandas`, `google-generativeai`, `openpyxl`, `webdriver-manager`, `unidecode`, `python-dotenv`

### **Configuração:**
- [ ] Arquivo `.env` criado (copiado de `.env.example`)
- [ ] API Key do Gemini adicionada ao `.env`
- [ ] Formato correto: `GEMINI_API_KEY=AIza...`

### **Validação:**
- [ ] Executado: `python validar_instalacao.py`
- [ ] Todas as verificações passaram (✅)
- [ ] Nenhum erro crítico reportado

---

## 📊 DADOS

### **Planilha de Entrada:**
- [ ] Arquivo `data/input/base.xlsx` existe
- [ ] Contém as colunas obrigatórias:
  - [ ] `NUMEROCLIENTE`
  - [ ] `CNPJ`
  - [ ] `DISTRIBUIDORA`
  - [ ] `RAZÃOSOCIALFATURAMENTO`
- [ ] Dados estão corretos e validados
- [ ] CPF/CNPJ sem formatação (apenas números) ou com formatação (será limpo automaticamente)

### **Distribuidoras Suportadas:**
- [ ] COELBA (Neoenergia Coelba)
- [ ] PERNAMBUCO (Neoenergia Pernambuco)
- [ ] BRASILIA (Neoenergia Brasília)
- [ ] ELEKTRO (Neoenergia Elektro)
- [ ] COSERN (Cosern WhatsApp BT)

---

## 🗂️ ESTRUTURA DE PASTAS

### **Pastas Criadas:**
- [ ] `data/input/` - Existe
- [ ] `data/logs/` - Existe
- [ ] `data/output/` - Existe
- [ ] `Faturas/` - Existe (será criada automaticamente se não existir)
- [ ] `chrome_session/` - Será criada na primeira execução

### **Permissões:**
- [ ] Pasta `Faturas/` tem permissão de escrita
- [ ] Pasta `data/logs/` tem permissão de escrita
- [ ] Pasta `chrome_session/` tem permissão de escrita

---

## 🔐 SEGURANÇA

### **Arquivos Sensíveis:**
- [ ] `.env` está no `.gitignore`
- [ ] `chrome_session/` está no `.gitignore`
- [ ] `data/input/base.xlsx` está no `.gitignore` (se contém dados reais)
- [ ] Nenhum dado sensível será versionado

### **Privacidade:**
- [ ] Logs não expõem CPF/CNPJ completos (mascarados: `123***01`)
- [ ] API Key não está hardcoded no código
- [ ] Sessão do WhatsApp está isolada

---

## 🧪 TESTES

### **Teste de Validação:**
```bash
python validar_instalacao.py
```
- [ ] ✅ Python 3.10+
- [ ] ✅ Dependências instaladas
- [ ] ✅ Estrutura de arquivos
- [ ] ✅ Configuração do .env
- [ ] ✅ Planilha de entrada
- [ ] ✅ Google Chrome

### **Teste Manual (Opcional):**
- [ ] Abrir WhatsApp Web manualmente
- [ ] Verificar se consegue enviar mensagens
- [ ] Verificar se consegue buscar contatos
- [ ] Verificar se consegue baixar arquivos

---

## 🚀 PRIMEIRA EXECUÇÃO

### **Preparação:**
- [ ] Celular com WhatsApp próximo (para escanear QR Code)
- [ ] WhatsApp Web não está aberto em outro navegador
- [ ] Planilha tem pelo menos 1 cliente para testar

### **Execução:**
```bash
python main.py
```

### **Passos Esperados:**
1. [ ] Interface gráfica abre
2. [ ] Clique em "▶ INICIAR ROBÔ"
3. [ ] Chrome abre automaticamente
4. [ ] WhatsApp Web carrega
5. [ ] QR Code aparece (primeira vez)
6. [ ] Escanear QR Code com celular
7. [ ] WhatsApp conecta
8. [ ] Bot começa a processar

### **Logs Esperados:**
- [ ] `🤖 Iniciando motor do robô...`
- [ ] `📂 Carregando base de clientes...`
- [ ] `✅ X clientes carregados com sucesso.`
- [ ] `🌐 Abrindo navegador e conectando ao WhatsApp...`
- [ ] `✅ WhatsApp carregado!`
- [ ] `🔄 Iniciando motor Híbrido com X clientes ativos.`

---

## 📥 DOWNLOAD DE FATURAS

### **Durante a Execução:**
- [ ] Bot envia mensagens automaticamente
- [ ] Bot seleciona opções no menu
- [ ] Bot envia código do cliente
- [ ] Bot envia CPF/CNPJ
- [ ] Bot confirma dados
- [ ] Bot baixa fatura

### **Após Download:**
- [ ] Arquivo aparece na pasta `Faturas/`
- [ ] Nome do arquivo: `[NUMEROCLIENTE]_[RAZAOSOCIAL].pdf`
- [ ] Tamanho do arquivo > 1KB
- [ ] Arquivo abre corretamente

### **Status Registrado:**
- [ ] Arquivo `data/logs/status_processamento.csv` criado
- [ ] Status registrado: `SUCESSO`, `NADA_CONSTA`, etc.
- [ ] Timestamp correto

---

## 🔄 EXECUÇÕES SUBSEQUENTES

### **Segunda Execução em Diante:**
- [ ] Não precisa escanear QR Code novamente
- [ ] Clientes já processados são pulados automaticamente
- [ ] Apenas clientes novos ou com erro são processados

### **Para Reprocessar Tudo:**
- [ ] Deletar arquivo: `data/logs/status_processamento.csv`
- [ ] Ou desmarcar opção "Ignorar clientes já concluídos" na interface

---

## 🐛 TROUBLESHOOTING

### **Se o Chrome não abrir:**
- [ ] Verificar se Chrome está instalado
- [ ] Deletar pasta `chrome_session/` e tentar novamente
- [ ] Verificar permissões de execução

### **Se WhatsApp não conectar:**
- [ ] Verificar conexão com internet
- [ ] Escanear QR Code novamente
- [ ] Verificar se WhatsApp Web não está aberto em outro lugar
- [ ] Deletar `chrome_session/` e reconectar

### **Se bot não encontra elementos:**
- [ ] Verificar se seletores estão atualizados
- [ ] Consultar `.agent/whatsapp_mapping_guide.md`
- [ ] Atualizar `neoenergia_bot/config/selectors.py`
- [ ] Reportar no CHANGELOG.md

### **Se download falha:**
- [ ] Verificar permissões da pasta `Faturas/`
- [ ] Verificar espaço em disco
- [ ] Verificar se arquivo não está aberto em outro programa
- [ ] Bot tentará 3 vezes automaticamente

### **Se API Gemini falha:**
- [ ] Verificar se API Key está correta no `.env`
- [ ] Verificar limite de 20 requisições/dia
- [ ] Verificar conexão com internet
- [ ] Bot usará regex como fallback

---

## 📊 MONITORAMENTO

### **Durante a Execução:**
- [ ] Acompanhar logs na interface gráfica
- [ ] Verificar pasta `Faturas/` periodicamente
- [ ] Monitorar arquivo `data/logs/status_processamento.csv`

### **Métricas Esperadas:**
- [ ] Taxa de sucesso > 80%
- [ ] Tempo médio por cliente: 30-60 segundos
- [ ] Uso de API Gemini: 1-2 chamadas/dia
- [ ] Erros de timeout < 10%

---

## 🎯 CRITÉRIOS DE SUCESSO

### **Execução Bem-Sucedida:**
- [ ] Todos os clientes processados
- [ ] Faturas baixadas na pasta `Faturas/`
- [ ] Status registrado em `status_processamento.csv`
- [ ] Nenhum erro crítico nos logs
- [ ] Bot finalizou sem travamentos

### **Qualidade dos Dados:**
- [ ] Arquivos PDF válidos
- [ ] Tamanho de arquivo razoável (> 1KB)
- [ ] Nomes de arquivo corretos
- [ ] Sem duplicatas desnecessárias

---

## 📝 PÓS-EXECUÇÃO

### **Verificação Final:**
- [ ] Conferir quantidade de faturas baixadas
- [ ] Validar alguns PDFs aleatoriamente
- [ ] Verificar status no CSV
- [ ] Identificar clientes com erro

### **Tratamento de Erros:**
- [ ] Listar clientes com `ERRO_CADASTRO`
- [ ] Listar clientes com `ERRO_DOCUMENTO`
- [ ] Listar clientes com `TIMEOUT`
- [ ] Corrigir dados e reprocessar

### **Backup:**
- [ ] Fazer backup da pasta `Faturas/`
- [ ] Fazer backup do `status_processamento.csv`
- [ ] Documentar problemas encontrados

---

## 🔄 MANUTENÇÃO

### **Semanal:**
- [ ] Verificar se WhatsApp Web mudou interface
- [ ] Testar seletores críticos
- [ ] Atualizar documentação se necessário

### **Mensal:**
- [ ] Revisar logs de erro
- [ ] Atualizar seletores se necessário
- [ ] Verificar uso da API Gemini
- [ ] Limpar arquivos temporários

### **Quando WhatsApp Atualizar:**
- [ ] Consultar `.agent/whatsapp_mapping_guide.md`
- [ ] Remapear seletores afetados
- [ ] Testar em ambiente de desenvolvimento
- [ ] Atualizar `selectors.py`
- [ ] Documentar no `CHANGELOG.md`

---

## ✅ CHECKLIST COMPLETO

### **Resumo:**
- [ ] ✅ Pré-requisitos atendidos
- [ ] ✅ Instalação concluída
- [ ] ✅ Dados preparados
- [ ] ✅ Estrutura de pastas OK
- [ ] ✅ Segurança verificada
- [ ] ✅ Testes passaram
- [ ] ✅ Primeira execução bem-sucedida
- [ ] ✅ Downloads funcionando
- [ ] ✅ Monitoramento ativo
- [ ] ✅ Critérios de sucesso atingidos

---

## 🎉 PRONTO PARA PRODUÇÃO!

Se todos os itens acima estão marcados, o **Bot Neoenergia** está **100% pronto** para uso em produção!

### **Próximo Passo:**
```bash
python main.py
```

**Boa automação! 🚀**

---

*Última atualização: 03/02/2026 17:40*  
*Versão: 1.1.0*
