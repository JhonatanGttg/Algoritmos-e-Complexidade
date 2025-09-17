"""
Selenium Bot for Login Testing

Bot automatizado que:
1. Faz login no site https://the-internet.herokuapp.com/login
2. Navega até a área autenticada
3. Captura mensagens de sucesso/erro e salva em arquivo de log

Autor: Jhonatan Gttg
Data: 17/09/2025
"""

# Importações necessárias para o bot
import logging  # Para criar arquivos de log
import time  # Para pausas entre ações
from datetime import datetime  # Para timestamps nos logs

# Importações do Selenium (biblioteca de automação web)
from selenium import webdriver  # Driver principal do navegador
from selenium.webdriver.common.by import By  # Para localizar elementos na página
from selenium.webdriver.support.ui import WebDriverWait  # Para esperar elementos aparecerem
from selenium.webdriver.support import expected_conditions as EC  # Condições de espera
from selenium.webdriver.chrome.service import Service  # Serviço do Chrome
from selenium.webdriver.edge.service import Service as EdgeService  # Serviço do Edge
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # Exceções
from webdriver_manager.chrome import ChromeDriverManager  # Gerenciador automático do ChromeDriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # Gerenciador do EdgeDriver

class LoginBot:
    """
    Classe principal do bot de login.
    
    Esta classe contém todos os métodos necessários para:
    - Configurar o navegador
    - Fazer login no site
    - Capturar mensagens
    - Salvar logs
    """
    
    def __init__(self):
        """Inicializa o bot e configura o sistema de logs."""
        self.driver = None  # Variável que vai armazenar o navegador
        self.setup_logging()  # Chama a função para configurar logs
        
    def setup_logging(self):
        """
        Configura o sistema de logs para salvar mensagens em arquivo.
        
        O que esta função faz:
        1. Cria um nome de arquivo com timestamp (data e hora atual)
        2. Configura para salvar logs tanto em arquivo quanto na tela
        3. Define o formato das mensagens de log
        """
        # Cria timestamp no formato: YYYYMMDD_HHMMSS (ex: 20250917_143052)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"login_bot_log_{timestamp}.txt"
        
        # Configuração do sistema de logging
        logging.basicConfig(
            level=logging.INFO,  # Nível mínimo de log (INFO, WARNING, ERROR)
            format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),  # Salva em arquivo
                logging.StreamHandler()  # Mostra na tela também
            ]
        )
        
        # Cria o objeto logger que vamos usar para escrever mensagens
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Bot iniciado - Log salvo em: {log_filename}")
    
    def setup_driver(self):
        """Initialize WebDriver with Safari (best option for macOS)."""
        try:
            # Try Safari first (most reliable on macOS)
            try:
                self.driver = webdriver.Safari()
                self.driver.maximize_window()
                self.logger.info("Safari WebDriver configurado com sucesso")
                return True
            except Exception as safari_error:
                error_msg = str(safari_error)
                if "remote automation" in error_msg.lower():
                    self.logger.error("Safari precisa ser configurado para automação remota.")
                    self.logger.error("Execute: python setup_safari.py para instruções")
                else:
                    self.logger.warning(f"Safari não disponível: {error_msg}")
                
                # Try Edge as backup
                try:
                    edge_options = webdriver.EdgeOptions()
                    edge_options.add_argument("--no-sandbox")
                    edge_options.add_argument("--disable-dev-shm-usage")
                    
                    edge_service = EdgeService(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=edge_service, options=edge_options)
                    self.driver.maximize_window()
                    self.logger.info("Microsoft Edge WebDriver configurado com sucesso")
                    return True
                except Exception as edge_error:
                    self.logger.warning(f"Edge não disponível: {str(edge_error)}")
                    
                    # Try Chrome as last resort
                    try:
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_argument("--no-sandbox")
                        chrome_options.add_argument("--disable-dev-shm-usage")
                        
                        chrome_service = Service(ChromeDriverManager().install())
                        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                        self.driver.maximize_window()
                        self.logger.info("Chrome WebDriver configurado com sucesso")
                        return True
                    except Exception as chrome_error:
                        self.logger.error(f"Chrome também não disponível: {str(chrome_error)}")
                        
        except Exception as e:
            self.logger.error(f"Erro geral ao configurar WebDriver: {str(e)}")
            
        self.logger.error("="*50)
        self.logger.error("NENHUM NAVEGADOR DISPONÍVEL ENCONTRADO")
        self.logger.error("="*50)
        self.logger.error("Soluções possíveis:")
        self.logger.error("1. Execute: python setup_safari.py")
        self.logger.error("2. Instale Google Chrome")
        self.logger.error("3. Instale Microsoft Edge")
        self.logger.error("="*50)
        return False
    
    def navigate_to_login_page(self):
        """
        Navega até a página de login do site de testes.
        
        O que esta função faz:
        1. Abre o URL da página de login
        2. Espera a página carregar completamente
        3. Verifica se o campo de username apareceu (confirma que carregou)
        
        Retorna:
            True se conseguiu carregar a página
            False se deu erro
        """
        try:
            # URL do site de testes que vamos usar
            url = "https://the-internet.herokuapp.com/login"
            
            # Comando para abrir a página no navegador
            self.driver.get(url)
            self.logger.info(f"Navegando para: {url}")
            
            # Espera até 10 segundos pelo campo de username aparecer
            # Isso confirma que a página carregou completamente
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            self.logger.info("Página de login carregada com sucesso")
            return True
            
        except TimeoutException:
            # Se demorou mais de 10 segundos, deu timeout
            self.logger.error("Timeout ao carregar página de login")
            return False
        except Exception as e:
            # Qualquer outro erro
            self.logger.error(f"Erro ao navegar para página de login: {str(e)}")
            return False
    
    def perform_login(self, username="tomsmith", password="SuperSecretPassword!"):
        """
        Realiza o processo de login no site.
        
        Parâmetros:
            username: Nome de usuário (padrão: "tomsmith")
            password: Senha (padrão: "SuperSecretPassword!")
        
        O que esta função faz:
        1. Localiza o campo de username na página
        2. Limpa o campo e digita o username
        3. Localiza o campo de senha
        4. Limpa o campo e digita a senha
        5. Clica no botão de login
        6. Espera a página processar o login
        
        Retorna:
            True se conseguiu executar o login
            False se deu erro
        """
        try:
            # Localiza o campo de username pelo ID "username"
            username_field = self.driver.find_element(By.ID, "username")
            username_field.clear()  # Limpa qualquer texto que já esteja no campo
            username_field.send_keys(username)  # Digita o username
            self.logger.info(f"Username '{username}' inserido")
            
            # Localiza o campo de senha pelo ID "password"
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()  # Limpa o campo
            password_field.send_keys(password)  # Digita a senha
            self.logger.info("Senha inserida")
            
            # Localiza o botão de login pelo CSS selector (botão do tipo submit)
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()  # Clica no botão
            self.logger.info("Botão de login clicado")
            
            # Pausa de 2 segundos para a página processar o login
            time.sleep(2)
            return True
            
        except NoSuchElementException as e:
            # Erro quando não consegue encontrar algum elemento na página
            self.logger.error(f"Elemento não encontrado durante login: {str(e)}")
            return False
        except Exception as e:
            # Qualquer outro erro
            self.logger.error(f"Erro durante processo de login: {str(e)}")
            return False
    
    def capture_login_result(self):
        """
        Captura o resultado do login (sucesso ou erro) e salva no log.
        
        O que esta função faz:
        1. Procura por uma mensagem de sucesso na página
        2. Se encontrar sucesso, verifica se foi redirecionado para área segura
        3. Se não encontrar sucesso, procura por mensagem de erro
        4. Salva todas as informações no arquivo de log
        
        Retorna:
            True se login foi bem-sucedido
            False se login falhou
        """
        try:
            # Tenta encontrar mensagem de sucesso (tempo limite: 5 segundos)
            try:
                # Procura por elemento com classe CSS "flash success"
                success_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
                )
                # Pega o texto da mensagem de sucesso
                success_message = success_element.text
                self.logger.info(f"LOGIN SUCESSO: {success_message}")
                
                # Verifica se foi redirecionado para a área segura
                if "/secure" in self.driver.current_url:
                    self.logger.info(f"Redirecionado para área autenticada: {self.driver.current_url}")
                    
                    # Captura o conteúdo da área segura (título da página)
                    secure_content = self.driver.find_element(By.TAG_NAME, "h2").text
                    self.logger.info(f"Conteúdo da área segura: {secure_content}")
                
                return True  # Login foi bem-sucedido
                
            except TimeoutException:
                # Não encontrou mensagem de sucesso, vamos procurar erro
                try:
                    # Procura por elemento com classe CSS "flash error"
                    error_element = self.driver.find_element(By.CSS_SELECTOR, ".flash.error")
                    error_message = error_element.text
                    self.logger.error(f"LOGIN ERRO: {error_message}")
                    return False  # Login falhou
                    
                except NoSuchElementException:
                    # Não encontrou nem sucesso nem erro
                    self.logger.warning("Nenhuma mensagem de sucesso ou erro encontrada")
                    return False
                    
        except Exception as e:
            # Erro inesperado
            self.logger.error(f"Erro ao capturar resultado do login: {str(e)}")
            return False
    
    def test_with_invalid_credentials(self):
        """
        Testa login com credenciais inválidas para capturar mensagem de erro.
        
        Este teste é importante porque:
        1. Verifica se o site mostra mensagens de erro corretamente
        2. Permite ver como o sistema se comporta com dados inválidos
        3. Captura a mensagem de erro para o log
        """
        self.logger.info("=== TESTANDO COM CREDENCIAIS INVÁLIDAS ===")
        
        # Vai para a página de login
        if not self.navigate_to_login_page():
            return False
            
        # Tenta fazer login com dados inválidos
        if self.perform_login(username="invalid_user", password="invalid_password"):
            return self.capture_login_result()  # Captura a mensagem de erro
        return False
    
    def test_with_valid_credentials(self):
        """
        Testa login com credenciais válidas para capturar mensagem de sucesso.
        
        Este teste:
        1. Usa as credenciais corretas do site (tomsmith / SuperSecretPassword!)
        2. Verifica se consegue acessar a área protegida
        3. Captura a mensagem de sucesso para o log
        4. Confirma que foi redirecionado para /secure
        """
        self.logger.info("=== TESTANDO COM CREDENCIAIS VÁLIDAS ===")
        
        # Vai para a página de login
        if not self.navigate_to_login_page():
            return False
            
        # Tenta fazer login com credenciais válidas (padrão)
        if self.perform_login():
            return self.capture_login_result()  # Captura a mensagem de sucesso
        return False
    
    def run_tests(self):
        """
        Executa a suíte completa de testes do bot.
        
        Esta função coordena todo o processo:
        1. Configura o navegador
        2. Executa teste com credenciais inválidas (para ver mensagem de erro)
        3. Executa teste com credenciais válidas (para ver mensagem de sucesso)
        4. Fecha o navegador ao final
        
        Retorna:
            True se todos os testes foram executados
            False se houve erro na configuração
        """
        # Primeiro, tenta configurar o navegador (Safari, Edge ou Chrome)
        if not self.setup_driver():
            return False
        
        try:
            # Teste 1: Credenciais inválidas (para capturar mensagem de erro)
            self.test_with_invalid_credentials()
            time.sleep(3)  # Pausa de 3 segundos entre os testes
            
            # Teste 2: Credenciais válidas (para capturar mensagem de sucesso)
            self.test_with_valid_credentials()
            time.sleep(3)  # Pausa de 3 segundos
            
            self.logger.info("Testes concluídos com sucesso")
            return True
            
        except Exception as e:
            # Se der algum erro durante os testes
            self.logger.error(f"Erro durante execução dos testes: {str(e)}")
            return False
        finally:
            # SEMPRE executa esta parte, mesmo se der erro
            # Fecha o navegador e limpa recursos
            self.cleanup()
    
    def cleanup(self):
        """
        Limpa recursos e fecha o navegador.
        
        Esta função é muito importante porque:
        1. Fecha a janela do navegador
        2. Libera memória do computador
        3. Evita que o navegador fique aberto consumindo recursos
        
        É chamada automaticamente no final dos testes.
        """
        if self.driver:
            self.driver.quit()  # Fecha o navegador completamente
            self.logger.info("Browser fechado e recursos liberados")

def main():
    """
    Função principal do programa.
    
    Esta é a função que é executada quando você roda o script.
    Ela:
    1. Mostra uma mensagem de início
    2. Cria uma instância do bot
    3. Executa todos os testes
    4. Mostra o resultado final
    """
    print("🤖 Iniciando Selenium Bot para teste de login...")
    
    # Cria uma nova instância da classe LoginBot
    bot = LoginBot()
    
    # Executa todos os testes (com credenciais válidas e inválidas)
    success = bot.run_tests()
    
    # Mostra o resultado final para o usuário
    if success:
        print("✅ Bot executado com sucesso! Verifique o arquivo de log para detalhes.")
    else:
        print("❌ Erro durante execução do bot. Verifique o arquivo de log para detalhes.")

# Esta linha verifica se o script está sendo executado diretamente
# (não sendo importado por outro arquivo)
# Se for executado diretamente, chama a função main()
if __name__ == "__main__":
    main()