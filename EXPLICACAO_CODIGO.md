# 📖 Explicação Detalhada do Código

Este documento explica cada parte do bot Selenium de forma detalhada para ajudar você a entender como tudo funciona.

## 🏗️ Estrutura Geral do Projeto

```
Atividade 17.09/
├── selenium_bot.py          # Código principal do bot
├── setup_safari.py          # Script para configurar Safari
├── requirements.txt         # Dependências do Python
├── run_bot.sh              # Script para executar o bot
├── README.md               # Documentação do projeto
└── EXPLICACAO_CODIGO.md    # Este arquivo
```

## 📦 Bibliotecas Utilizadas

### 1. Bibliotecas Padrão do Python
- `logging`: Para criar arquivos de log
- `time`: Para pausas entre ações
- `datetime`: Para timestamps nos logs

### 2. Bibliotecas do Selenium
- `selenium.webdriver`: Controla o navegador
- `selenium.webdriver.common.by`: Localiza elementos na página
- `selenium.webdriver.support.ui.WebDriverWait`: Espera elementos aparecerem
- `selenium.webdriver.support.expected_conditions`: Condições de espera
- `selenium.common.exceptions`: Trata erros do Selenium

### 3. Gerenciadores de WebDriver
- `webdriver_manager.chrome.ChromeDriverManager`: Baixa ChromeDriver automaticamente
- `webdriver_manager.microsoft.EdgeChromiumDriverManager`: Baixa EdgeDriver automaticamente

## 🏛️ Arquitetura da Classe LoginBot

### Atributos da Classe
```python
self.driver = None    # Armazena o navegador (Safari, Chrome ou Edge)
self.logger = None    # Objeto para escrever logs
```

### Métodos Principais

#### 1. `__init__(self)`
**O que faz:** Inicializa o bot
**Quando é chamado:** Quando você cria uma instância da classe
```python
bot = LoginBot()  # Chama __init__
```

#### 2. `setup_logging(self)`
**O que faz:** Configura o sistema de logs
**Detalhes:**
- Cria arquivo com nome: `login_bot_log_YYYYMMDD_HHMMSS.txt`
- Configura para salvar logs em arquivo E mostrar na tela
- Define formato: `2025-09-17 10:44:33,453 - INFO - Mensagem`

#### 3. `setup_driver(self)`
**O que faz:** Configura o navegador para automação
**Ordem de tentativas:**
1. **Safari** (primeira opção - nativo do macOS)
2. **Microsoft Edge** (segunda opção)
3. **Google Chrome** (terceira opção)

**Por que esta ordem?**
- Safari já vem instalado no macOS
- Edge e Chrome precisam ser baixados

#### 4. `navigate_to_login_page(self)`
**O que faz:** Abre a página de login
**URL usada:** https://the-internet.herokuapp.com/login
**Verificação:** Espera o campo username aparecer (confirma que carregou)

#### 5. `perform_login(self, username, password)`
**O que faz:** Executa o processo de login
**Passos:**
1. Localiza campo username pelo ID "username"
2. Limpa o campo e digita o username
3. Localiza campo password pelo ID "password"  
4. Limpa o campo e digita a senha
5. Localiza botão submit e clica
6. Espera 2 segundos para processar

#### 6. `capture_login_result(self)`
**O que faz:** Captura mensagens de sucesso ou erro
**Como funciona:**
1. Procura elemento com classe `.flash.success` (sucesso)
2. Se encontrar, verifica se foi redirecionado para `/secure`
3. Se não encontrar sucesso, procura `.flash.error` (erro)
4. Salva a mensagem encontrada no log

## 🔄 Fluxo de Execução

### 1. Iniciação
```python
if __name__ == "__main__":
    main()
```
- Verifica se script foi executado diretamente
- Chama função `main()`

### 2. Função main()
```python
def main():
    bot = LoginBot()        # Cria instância
    success = bot.run_tests()  # Executa testes
    # Mostra resultado final
```

### 3. run_tests()
```python
def run_tests(self):
    self.setup_driver()     # Configura navegador
    
    # Teste 1: Credenciais inválidas
    self.test_with_invalid_credentials()
    
    # Teste 2: Credenciais válidas  
    self.test_with_valid_credentials()
    
    self.cleanup()          # Fecha navegador
```

### 4. Cada Teste
```python
def test_with_valid_credentials(self):
    self.navigate_to_login_page()    # Vai para login
    self.perform_login()             # Faz login
    self.capture_login_result()      # Captura resultado
```

## 🧪 Testes Realizados

### Teste 1: Credenciais Inválidas
**Objetivo:** Ver mensagem de erro
**Dados usados:**
- Username: "invalid_user"
- Password: "invalid_password"
**Resultado esperado:** Mensagem "Your username is invalid!"

### Teste 2: Credenciais Válidas
**Objetivo:** Ver mensagem de sucesso e acessar área protegida
**Dados usados:**
- Username: "tomsmith"
- Password: "SuperSecretPassword!"
**Resultado esperado:** 
- Mensagem "You logged into a secure area!"
- Redirecionamento para `/secure`

## 📁 Sistema de Logs

### Formato do Arquivo
```
login_bot_log_20250917_104433.txt
```
- `20250917`: Data (17 de setembro de 2025)
- `104433`: Hora (10:44:33)

### Tipos de Mensagens
- **INFO**: Informações normais
- **WARNING**: Avisos (não é erro, mas atenção)
- **ERROR**: Erros que impediram o funcionamento

### Exemplo de Log
```
2025-09-17 10:44:33,453 - INFO - Bot iniciado
2025-09-17 10:44:34,123 - INFO - Safari WebDriver configurado com sucesso
2025-09-17 10:44:35,456 - INFO - Navegando para: https://the-internet.herokuapp.com/login
2025-09-17 10:44:36,789 - INFO - Username 'tomsmith' inserido
2025-09-17 10:44:37,123 - INFO - Senha inserida
2025-09-17 10:44:37,456 - INFO - Botão de login clicado
2025-09-17 10:44:38,789 - INFO - LOGIN SUCESSO: You logged into a secure area!
2025-09-17 10:44:39,123 - INFO - Redirecionado para área autenticada: https://the-internet.herokuapp.com/secure
```

## 🛠️ Tratamento de Erros

### Tipos de Erros Tratados
1. **TimeoutException**: Elemento não apareceu no tempo esperado
2. **NoSuchElementException**: Elemento não foi encontrado na página
3. **Exception**: Qualquer outro erro inesperado

### Estratégia de Fallback
Se um navegador não funcionar, tenta o próximo:
Safari → Edge → Chrome

## 🔧 Configurações Importantes

### Navegadores Suportados
- **Safari**: Requer "Allow Remote Automation" habilitado
- **Chrome**: Download automático do ChromeDriver
- **Edge**: Download automático do EdgeDriver

### Tempos de Espera
- **Carregar página**: 10 segundos
- **Encontrar mensagens**: 5 segundos  
- **Entre testes**: 3 segundos
- **Após login**: 2 segundos

## 🎯 Objetivos Alcançados

✅ **Login automatizado** no site de testes
✅ **Navegação** para área autenticada  
✅ **Captura de mensagens** de sucesso e erro
✅ **Salvamento em logs** com timestamp
✅ **Suporte múltiplos navegadores**
✅ **Tratamento de erros** robusto
✅ **Código bem documentado** com comentários explicativos

---

**Autor:** Jhonatan Gttg  
**Data:** 17/09/2025  
**Objetivo:** Demonstrar automação web com Selenium