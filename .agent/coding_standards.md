# Padrões de Código

## Stack
* Python 3.10+
* Selenium WebDriver (Chrome)
* Pandas
* google-generativeai

## Requisitos Selenium
1. **Persistência:** `webdriver.ChromeOptions` DEVE usar `user-data-dir` (ex: `./chrome_profile`) para salvar o login do WhatsApp.
2. **Seletores:** Use seletores robustos (XPATH por texto ou `data-testid`), pois classes CSS mudam.
3. **Waits:** Use `WebDriverWait`, nunca `time.sleep` fixo para elementos.

## Robustez
* O loop principal deve ter `try/except` para que um erro em um cliente não pare a fila inteira.
* Logs devem ser salvos em `data/logs/execucao.csv`.