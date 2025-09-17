# Selenium Login Bot

Este projeto implementa um bot automatizado usando Selenium que realiza login em um site de testes e captura mensagens de sucesso/erro.

## Funcionalidades

- ✅ Login automatizado no site https://the-internet.herokuapp.com/login
- ✅ Navegação para área autenticada
- ✅ Captura de mensagens de sucesso e erro
- ✅ Salvamento de logs em arquivo com timestamp
- ✅ Teste com credenciais válidas e inválidas

## Requisitos

- Python 3.7+
- Google Chrome instalado
- Conexão com internet

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure o Safari para automação (recomendado):
```bash
python setup_safari.py
```

3. Execute o bot:
```bash
python selenium_bot.py
```

### Configuração do Safari

Para usar o Safari (recomendado no macOS):

1. Abra o Safari
2. Vá em Safari > Configurações (ou Preferências)
3. Clique na aba "Avançado"
4. Marque "Mostrar menu Desenvolver na barra de menus"
5. Vá em Desenvolver > Permitir Automação Remota

### Navegadores Alternativos

O bot tenta usar navegadores nesta ordem:
1. **Safari** (recomendado para macOS)
2. **Microsoft Edge** 
3. **Google Chrome**

Se nenhum estiver disponível, instale um deles.

## Como funciona

O bot realiza os seguintes passos:

1. **Configuração**: Inicializa o WebDriver Chrome e configura logging
2. **Navegação**: Acessa a página de login
3. **Teste com credenciais inválidas**: Testa login com dados incorretos para capturar mensagem de erro
4. **Teste com credenciais válidas**: Realiza login correto para capturar mensagem de sucesso
5. **Captura de logs**: Salva todas as mensagens em arquivo com timestamp

## Credenciais de teste

**Válidas:**
- Username: `tomsmith`
- Password: `SuperSecretPassword!`

**Inválidas:**
- Username: `invalid_user`
- Password: `invalid_password`

## Arquivos de saída

O bot gera arquivos de log com nome no formato:
`login_bot_log_YYYYMMDD_HHMMSS.txt`

Exemplo: `login_bot_log_20240917_143052.txt`

## Exemplo de log

```
2024-09-17 14:30:52,123 - INFO - Bot iniciado - Log salvo em: login_bot_log_20240917_143052.txt
2024-09-17 14:30:52,456 - INFO - WebDriver configurado com sucesso
2024-09-17 14:30:53,789 - INFO - Navegando para: https://the-internet.herokuapp.com/login
2024-09-17 14:30:54,123 - INFO - Página de login carregada com sucesso
2024-09-17 14:30:54,456 - INFO - Username 'invalid_user' inserido
2024-09-17 14:30:54,789 - INFO - Senha inserida
2024-09-17 14:30:55,123 - INFO - Botão de login clicado
2024-09-17 14:30:55,456 - ERROR - LOGIN ERRO: Your username is invalid!
```