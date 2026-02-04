# 🗺️ Guia de Mapeamento do WhatsApp Web

Este documento contém orientações para o agente que irá mapear os seletores do WhatsApp Web.

---

## 🎯 OBJETIVO

Mapear e atualizar os seletores CSS/XPATH do WhatsApp Web para garantir que o bot continue funcionando mesmo quando o WhatsApp atualizar sua interface.

---

## 📋 ELEMENTOS A MAPEAR

### 1. **BARRA DE PESQUISA (Search Box)**

**Localização:** Topo da barra lateral esquerda

**Características:**
- Campo de texto editável
- Placeholder: "Pesquisar ou começar uma nova conversa"
- Atributo `contenteditable="true"`
- Atributo `aria-autocomplete="list"`

**Seletor Atual:**
```python
SEARCH_BOX = (By.XPATH, "//div[@contenteditable='true'][@aria-autocomplete='list']")
```

**Como Identificar:**
1. Abra o WhatsApp Web
2. Inspecione o campo de busca no topo
3. Procure por:
   - `div` com `contenteditable="true"`
   - Que também tenha `aria-autocomplete="list"`
   - Dentro da área `id="side"` ou similar

**Alternativas Robustas:**
- `//div[@role='textbox'][@data-tab='3']`
- `//div[contains(@title, 'Pesquisar')]`
- `//div[@id='side']//div[@contenteditable='true']`

---

### 2. **RESULTADO DE BUSCA (Search Result)**

**Localização:** Lista de conversas filtradas após pesquisa

**Características:**
- Cada resultado é uma linha (`div[@role='row']`)
- Contém o nome do contato em um `span[@title]`
- Está dentro da área `id="pane-side"`

**Seletor Atual:**
```python
SEARCH_RESULT = (By.XPATH, "//div[@id='side']//span[@title='{}']/ancestor::div[@role='row']")
```

**Como Identificar:**
1. Digite algo na busca
2. Inspecione um resultado da lista
3. Procure por:
   - `div` com `role="row"`
   - Que contenha um `span` com `title` igual ao nome do contato
   - Dentro de `id="pane-side"` ou `id="side"`

**Alternativas Robustas:**
- `//div[@role='listitem']//span[@title='{}']`
- `//div[contains(@class, 'chat-list')]//span[text()='{}']`

---

### 3. **CABEÇALHO DO CHAT (Chat Header)**

**Localização:** Topo da área de conversa (direita)

**Características:**
- Mostra o nome do contato atual
- Dentro de um `header` element
- Contém `span` com `title` ou `data-testid`

**Seletor Atual:**
```python
CHAT_HEADER_TITLE = (By.XPATH, "//header//span[@title='{}']")
```

**Como Identificar:**
1. Abra uma conversa
2. Inspecione o nome do contato no topo
3. Procure por:
   - Elemento `header`
   - `span` com atributo `title` contendo o nome
   - Ou `div[@role='button']` com o nome

**Alternativas Robustas:**
- `//header//span[contains(text(), '{}')]`
- `//header[@data-testid='conversation-header']//span[@title]`

---

### 4. **BADGE DE NÃO LIDA (Unread Badge)**

**Localização:** Bolinha verde/número ao lado de conversas não lidas

**Características:**
- Pequeno círculo com número ou sem número
- Atributo `aria-label` contendo "não lida" ou "unread"
- Dentro de cada linha de conversa

**Seletor Atual:**
```python
UNREAD_BADGE = (By.XPATH, ".//span[@aria-label and contains(@aria-label, 'não lida')]")
```

**Como Identificar:**
1. Encontre uma conversa com mensagem não lida
2. Inspecione a bolinha verde/número
3. Procure por:
   - `span` com `aria-label`
   - Texto contendo "não lida", "unread", ou número
   - Classe contendo "badge" ou "unread"

**Alternativas Robustas:**
- `.//span[contains(@class, 'unread')]`
- `.//div[@role='gridcell']//span[contains(@aria-label, 'mensagem')]`

---

### 5. **LINHAS DA SIDEBAR (Sidebar Rows)**

**Localização:** Lista de conversas na barra lateral

**Características:**
- Cada conversa é um `div[@role='row']`
- Dentro de `id="pane-side"`
- Contém nome, última mensagem, hora

**Seletor Atual:**
```python
SIDEBAR_ROW = (By.XPATH, "//div[@id='pane-side']//div[@role='row']")
```

**Como Identificar:**
1. Inspecione a lista de conversas
2. Procure por:
   - `div` com `role="row"` ou `role="listitem"`
   - Dentro de `id="pane-side"` ou similar
   - Cada um representa uma conversa

**Alternativas Robustas:**
- `//div[@id='pane-side']//div[@role='listitem']`
- `//div[contains(@class, 'chat-list-item')]`

---

### 6. **CAIXA DE TEXTO (Chat Input)**

**Localização:** Rodapé da área de conversa (onde você digita)

**Características:**
- Campo editável no rodapé
- `contenteditable="true"`
- Dentro de `footer` ou `div[@id='main']`
- Placeholder: "Digite uma mensagem"

**Seletor Atual:**
```python
CHAT_INPUT = (By.XPATH, "//div[@id='main']//footer//div[@contenteditable='true']")
```

**Como Identificar:**
1. Abra uma conversa
2. Inspecione o campo de texto no rodapé
3. Procure por:
   - `div` com `contenteditable="true"`
   - Dentro de `footer`
   - Dentro de `div[@id='main']`
   - Atributo `role="textbox"`

**Alternativas Robustas:**
- `//div[@role='textbox'][@contenteditable='true'][@data-tab='10']`
- `//footer//div[@contenteditable='true']`
- `//div[@id='main']//div[@role='textbox']`

---

### 7. **BOTÃO ENVIAR (Send Button)**

**Localização:** Ao lado direito da caixa de texto

**Características:**
- Botão com ícone de avião de papel
- `aria-label="Enviar"`
- Aparece quando há texto digitado

**Seletor Atual:**
```python
SEND_BUTTON = (By.XPATH, "//button[@aria-label='Enviar']")
```

**Como Identificar:**
1. Digite algo no chat
2. Inspecione o botão de enviar
3. Procure por:
   - `button` com `aria-label="Enviar"` ou "Send"
   - `span[@data-icon='send']`
   - Dentro do rodapé

**Alternativas Robustas:**
- `//span[@data-icon='send']/ancestor::button`
- `//button[contains(@aria-label, 'Enviar')]`

---

### 8. **MENSAGENS RECEBIDAS (Incoming Messages)**

**Localização:** Bolhas de mensagem do lado esquerdo

**Características:**
- `div` com classe contendo "message-in"
- Alinhadas à esquerda
- Fundo branco/cinza claro

**Seletor Atual:**
```python
ALL_MESSAGES = (By.XPATH, "//div[contains(@class, 'message-in')]")
```

**Como Identificar:**
1. Inspecione uma mensagem recebida
2. Procure por:
   - `div` com classe contendo "message-in" ou "incoming"
   - Atributo `data-pre-plain-text` (contém hora e remetente)
   - Dentro de `div[@id='main']`

**Alternativas Robustas:**
- `//div[@data-pre-plain-text and not(contains(@class, 'message-out'))]`
- `//div[contains(@class, 'focusable-list-item')]//div[contains(@class, 'message-in')]`

---

### 9. **TEXTO DA MENSAGEM (Message Text)**

**Localização:** Dentro de cada bolha de mensagem

**Características:**
- `span` com classe contendo texto selecionável
- Classe comum: `selectable-text`
- Pode ter múltiplos spans para formatação

**Seletor Atual:**
```python
LAST_MESSAGE_TEXT = (By.XPATH, ".//span[contains(@class, '_ao3e')] | .//span[contains(@class, 'selectable-text')]")
```

**Como Identificar:**
1. Inspecione o texto de uma mensagem
2. Procure por:
   - `span` com classe contendo "selectable-text"
   - Ou classe ofuscada (ex: `_ao3e`, `_11JPr`)
   - Dentro da bolha de mensagem

**Alternativas Robustas:**
- `.//span[@class and contains(@class, 'selectable-text')]`
- `.//div[@class='copyable-text']//span`

---

### 10. **BOTÃO "VER OPÇÕES" (Modal Trigger)**

**Localização:** Dentro de mensagens do bot com menu interativo

**Características:**
- Botão que abre modal de opções
- Texto: "Ver opções" ou "Ver Opções"
- Aparece em mensagens de bots

**Seletor Atual:**
```python
BTN_VER_OPCOES = (By.XPATH, "//button[contains(., 'Ver opções')]")
```

**Como Identificar:**
1. Encontre uma mensagem com menu interativo
2. Inspecione o botão
3. Procure por:
   - `button` contendo texto "Ver opções"
   - Pode ter variações: "Ver Opções", "VER OPÇÕES"
   - Dentro de uma mensagem recebida

**Alternativas Robustas:**
- `//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ver opções')]`
- `//button[@role='button'][contains(., 'opções')]`

---

### 11. **MODAL DE OPÇÕES (Options Dialog)**

**Localização:** Popup que aparece ao clicar "Ver opções"

**Características:**
- `div[@role='dialog']`
- Contém lista de opções (radio buttons)
- Tem botão "Enviar" no rodapé

**Seletor Atual:**
```python
MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")
```

**Como Identificar:**
1. Clique em "Ver opções"
2. Inspecione o popup
3. Procure por:
   - `div` com `role="dialog"`
   - Contém `div[@role='radio']` para cada opção
   - Tem overlay/backdrop escuro

**Alternativas Robustas:**
- `//div[@role='dialog'][@aria-modal='true']`
- `//div[contains(@class, 'modal')]`

---

### 12. **OPÇÕES DO MODAL (Radio Buttons)**

**Localização:** Dentro do modal de opções

**Características:**
- `div[@role='radio']`
- Cada opção é clicável
- Contém `span` com o texto da opção

**Seletor Atual:**
```python
MODAL_OPTIONS_LIST = (By.XPATH, "//div[@role='dialog']//div[@role='radio']")
```

**Como Identificar:**
1. Abra o modal de opções
2. Inspecione uma opção
3. Procure por:
   - `div` com `role="radio"`
   - Contém `span` com texto da opção
   - Dentro de `div[@role='dialog']`

**Alternativas Robustas:**
- `//div[@role='dialog']//div[@role='radio'][.//span[contains(text(), '{}')]]`
- `//div[@role='dialog']//label[@role='radio']`

---

### 13. **BOTÃO ENVIAR DO MODAL (Modal Send Button)**

**Localização:** Rodapé do modal de opções

**Características:**
- Botão com ícone de enviar (avião)
- `span[@data-icon='send']`
- `aria-label="Enviar"` ou similar

**Seletor Atual:**
```python
MODAL_SEND_BTN = (By.XPATH, "//div[@role='dialog']//span[@data-icon='send']/ancestor::div[@role='button']")
```

**Como Identificar:**
1. Abra o modal e selecione uma opção
2. Inspecione o botão de enviar
3. Procure por:
   - `span` com `data-icon='send'`
   - Dentro de `div[@role='dialog']`
   - Ancestral `div[@role='button']` ou `button`

**Alternativas Robustas:**
- `//div[@role='dialog']//button[@aria-label='Enviar']`
- `//div[@role='dialog']//span[@data-icon='send']/ancestor::button`

---

### 14. **ANEXOS/ARQUIVOS (Attachments)**

**Localização:** Mensagens com PDFs ou documentos

**Características:**
- Ícone de documento/arquivo
- Link com `href` contendo "blob:" ou ".pdf"
- `span[@data-icon='audio-file']` ou similar

**Seletor Atual:**
```python
ATTACHMENT_FILE = (By.XPATH, "//div[contains(@class, 'message-in')]//div[@role='button']//span[contains(@class, '_')]")
ATTACHMENT_PDF = (By.XPATH, ".//span[@data-icon='audio-file'] | .//span[contains(text(), '.pdf')]")
```

**Como Identificar:**
1. Encontre uma mensagem com arquivo anexado
2. Inspecione o elemento do arquivo
3. Procure por:
   - `span` com `data-icon='audio-file'` ou `data-icon='document'`
   - `a` com `href` contendo "blob:"
   - Botão de download com ícone de seta

**Alternativas Robustas:**
- `//div[contains(@class, 'message-in')]//a[contains(@href, 'blob:')]`
- `//span[@data-icon='download']`
- `//div[@role='button'][contains(@aria-label, 'Download')]`

---

### 15. **SINAL DE CARREGAMENTO (App Loaded Signal)**

**Localização:** Elemento que indica que o WhatsApp carregou

**Características:**
- `div[@id='pane-side']` (painel lateral)
- Aparece quando o app está pronto
- Usado para aguardar login

**Seletor Atual:**
```python
APP_LOADED_SIGNAL = (By.ID, "pane-side")
```

**Como Identificar:**
1. Carregue o WhatsApp Web
2. Aguarde o login
3. Procure por:
   - `div` com `id="pane-side"`
   - Ou `div` com `id="side"`
   - Elemento que sempre aparece após login

**Alternativas Robustas:**
- `(By.ID, "side")`
- `(By.XPATH, "//div[@id='app']//div[@id='pane-side']")`

---

## 🔍 ESTRATÉGIAS DE MAPEAMENTO

### **1. Prioridade de Seletores**

Use nesta ordem de preferência:

1. **IDs únicos** (`id="pane-side"`)
   - Mais estáveis
   - Raramente mudam

2. **Atributos ARIA** (`role="dialog"`, `aria-label="Enviar"`)
   - Semânticos
   - Mantidos para acessibilidade

3. **Data Attributes** (`data-testid`, `data-icon`)
   - Usados para testes
   - Relativamente estáveis

4. **Estrutura DOM** (ancestrais/descendentes)
   - `//header//span[@title]`
   - Mais robusto que classes

5. **Classes CSS** (último recurso)
   - Mudam frequentemente
   - WhatsApp ofusca classes

### **2. Técnicas de Inspeção**

1. **DevTools do Chrome:**
   - F12 → Elements
   - Ctrl+Shift+C (seletor de elementos)
   - Copiar XPath: Botão direito → Copy → Copy XPath

2. **Testar Seletores:**
   ```javascript
   // No console do Chrome
   $x("//div[@id='pane-side']") // Testa XPATH
   $$("div[role='dialog']")     // Testa CSS
   ```

3. **Verificar Unicidade:**
   ```javascript
   // Deve retornar apenas 1 elemento
   $x("//seu-xpath-aqui").length
   ```

### **3. Padrões de XPATH Robustos**

```xpath
# Busca por texto (case-insensitive)
//button[contains(translate(., 'ABC', 'abc'), 'texto')]

# Múltiplas condições (OR)
//span[@title='{}'] | //span[text()='{}']

# Ancestral específico
//div[@id='main']//footer//div[@contenteditable='true']

# Atributo parcial
//div[contains(@class, 'message-in')]

# Combinação de atributos
//div[@role='dialog'][@aria-modal='true']
```

---

## 📝 TEMPLATE DE ATUALIZAÇÃO

Quando mapear um novo seletor, use este formato:

```python
# [NOME DO ELEMENTO]
# Descrição: [O que é este elemento]
# Localização: [Onde está na interface]
# Última atualização: [Data]
# Testado em: WhatsApp Web versão [X.X.X]
NOME_SELETOR = (By.XPATH, "//xpath-aqui")

# Alternativas (caso o principal falhe):
NOME_SELETOR_ALT1 = (By.XPATH, "//xpath-alternativo-1")
NOME_SELETOR_ALT2 = (By.CSS_SELECTOR, "css-selector")
```

---

## 🧪 CHECKLIST DE VALIDAÇÃO

Após mapear/atualizar seletores, verifique:

- [ ] Seletor funciona em página carregada
- [ ] Seletor funciona após login
- [ ] Seletor é único (retorna 1 elemento)
- [ ] Seletor funciona em diferentes conversas
- [ ] Seletor funciona com/sem mensagens não lidas
- [ ] Seletor funciona em modo claro e escuro
- [ ] Seletor funciona em diferentes resoluções
- [ ] Alternativas foram testadas

---

## 🚨 ELEMENTOS CRÍTICOS (PRIORIDADE ALTA)

Estes elementos são essenciais para o funcionamento do bot:

1. ✅ **SEARCH_BOX** - Sem isso, não consegue buscar contatos
2. ✅ **CHAT_INPUT** - Sem isso, não consegue enviar mensagens
3. ✅ **LAST_MESSAGE_TEXT** - Sem isso, não consegue ler respostas
4. ✅ **BTN_VER_OPCOES** - Sem isso, não abre menus interativos
5. ✅ **MODAL_SEND_BTN** - Sem isso, não envia seleções

---

## 📊 FORMATO DE SAÍDA

Após mapear, atualize o arquivo `neoenergia_bot/config/selectors.py`:

```python
from selenium.webdriver.common.by import By

class Selectors:
    """
    Seletores do WhatsApp Web
    Última atualização: [DATA]
    Versão do WhatsApp: [X.X.X]
    """
    
    # [Seus seletores aqui]
    SEARCH_BOX = (By.XPATH, "//xpath")
    # ...

selectors = Selectors()
```

---

## 🔄 QUANDO ATUALIZAR

Atualize os seletores quando:

1. ❌ Bot não consegue encontrar elementos
2. ❌ Logs mostram "Element not found"
3. ❌ WhatsApp Web mudou visualmente
4. ❌ Testes automatizados falharem
5. ⚠️ WhatsApp anunciar atualização de interface

---

## 💡 DICAS IMPORTANTES

1. **Sempre teste em ambiente real** (WhatsApp Web aberto)
2. **Mantenha alternativas** para cada seletor crítico
3. **Documente mudanças** no CHANGELOG.md
4. **Teste em diferentes idiomas** (PT-BR, EN)
5. **Verifique modo escuro** e modo claro
6. **Use seletores semânticos** (ARIA) quando possível

---

## 📞 SUPORTE

Se encontrar dificuldades:

1. Consulte a documentação do Selenium: https://selenium-python.readthedocs.io/
2. Use o DevTools do Chrome para inspecionar
3. Teste seletores no console antes de implementar
4. Mantenha backup dos seletores antigos

---

**Boa sorte no mapeamento! 🗺️**
