# =============================================================================
# INSTAGRAM BIO BOT - BOT PARA EXTRAIR BIO DE PERFIS DO INSTAGRAM
# =============================================================================
# Este módulo utiliza Selenium para automatizar o navegador Safari e:
# 1. Fazer login automático no Instagram
# 2. Navegar até um perfil específico
# 3. Extrair as informações da bio do perfil
# 4. Salvar os dados em um arquivo JSON
# =============================================================================

# Importação das bibliotecas necessárias
import os      # Para acessar variáveis de ambiente
import json    # Para manipulação de arquivos JSON
import time    # Para pausas/delays durante a execução

# Bibliotecas do Selenium para automação do navegador
from selenium import webdriver                           # Driver principal do Selenium
from selenium.webdriver.common.by import By             # Para localizar elementos na página
from selenium.webdriver.support.ui import WebDriverWait # Para esperas inteligentes
from selenium.webdriver.support import expected_conditions as EC  # Condições de espera

# Biblioteca para parsing de HTML
from bs4 import BeautifulSoup  # Para analisar e extrair dados do HTML


def get_instagram_bio(target_username, login_user, login_pass):
    """
    Função principal que executa todo o processo de extração da bio do Instagram.
    
    Parâmetros:
        target_username (str): Nome de usuário do perfil que queremos analisar
        login_user (str): Nosso nome de usuário para fazer login
        login_pass (str): Nossa senha para fazer login
    
    Retorna:
        dict: Dicionário com as informações extraidas (perfil, username, bio)
    
    Processo:
    1. Inicializa o navegador Safari
    2. Acessa a página de login do Instagram
    3. Faz login automaticamente
    4. Navega até o perfil alvo
    5. Extrai as informações da bio
    6. Salva em arquivo JSON
    7. Fecha o navegador
    """
    
    # =========================================================================
    # INICIALIZAÇÃO DO NAVEGADOR SAFARI
    # =========================================================================
    
    # Cria uma instância do navegador Safari
    # Safari é usado porque é nativo no macOS e não precisa de drivers externos
    driver = webdriver.Safari()
    
    # Configura um objeto de espera que vai aguardar até 15 segundos
    # por elementos aparecerem na página antes de dar timeout
    wait = WebDriverWait(driver, 15)
    
    # =========================================================================
    # ACESSO À PÁGINA DE LOGIN DO INSTAGRAM
    # =========================================================================
    
    # Navega até a página de login do Instagram
    driver.get("https://www.instagram.com/accounts/login/")
    
    # Espera até que o campo de nome de usuário apareça na página
    # Isso garante que a página foi carregada completamente
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    
    # =========================================================================
    # PROCESSO DE LOGIN AUTOMÁTICO
    # =========================================================================
    
    # Localiza o campo de nome de usuário e digita as credenciais
    driver.find_element(By.NAME, "username").send_keys(login_user)
    
    # Localiza o campo de senha e digita a senha
    driver.find_element(By.NAME, "password").send_keys(login_pass)
    
    # Localiza e clica no botão de login
    # Usa XPATH para encontrar um botão do tipo 'submit'
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # =========================================================================
    # AGUARDA O LOGIN SER PROCESSADO
    # =========================================================================
    
    try:
        # Espera até que a barra de navegação principal apareça
        # Isso indica que o login foi bem-sucedido
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
    except:
        # Se não conseguir encontrar a navegação, continua mesmo assim
        # Algumas vezes o Instagram tem comportamentos diferentes
        pass
    
    # =========================================================================
    # TRATAMENTO DE POPUPS DO INSTAGRAM
    # =========================================================================
    
    try:
        # O Instagram frequentemente mostra popups após o login
        # Procura por botões "Agora não" ou "Not Now" e clica neles
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(text(), 'Agora não') or contains(text(), 'Not Now')]"
            ))
        )
        btn.click()
    except:
        # Se não encontrar o popup, continua normalmente
        pass
    
    # =========================================================================
    # NAVEGAÇÃO ATÉ O PERFIL ALVO
    # =========================================================================
    
    # Constrói a URL do perfil que queremos analisar
    profile_url = f"https://www.instagram.com/{target_username}/"
    
    # Navega até a página do perfil
    driver.get(profile_url)
    
    # Espera até que o cabeçalho da página do perfil carregue
    # Isso garante que chegamos na página correta
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
    
    # Pausa de 2 segundos para garantir que todo o conteúdo foi carregado
    time.sleep(2)
    
    # =========================================================================
    # EXTRAÇÃO DO HTML DA PÁGINA
    # =========================================================================
    
    # Obtém o código HTML completo da página
    page = driver.page_source
    
    # Cria um objeto BeautifulSoup para navegar pelo HTML
    soup = BeautifulSoup(page, "html.parser")
    
    # =========================================================================
    # EXTRAÇÃO DA BIO DO PERFIL
    # =========================================================================
    
    # Inicializa a variável da bio como string vazia
    bio = ""
    
    # MÉTODO 1: Procura por dados estruturados JSON-LD
    # O Instagram frequentemente inclui metadados estruturados na página
    script = soup.find("script", type="application/ld+json")
    
    if script:
        try:
            # Verifica se o script existe e tem conteúdo
            if script and hasattr(script, 'string') and script.string:
                # Converte o JSON para dicionário Python
                data = json.loads(script.string)
                # Tenta extrair a descrição do perfil
                bio = data.get("description", "")
        except:
            # Se houver erro no parsing do JSON, continua com bio vazia
            bio = ""
    
    # MÉTODO 2: Se não encontrou a bio no JSON, procura nas meta tags
    if not bio:
        # Procura pela meta tag "description" que contém informações do perfil
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            # Extrai o conteúdo da meta tag
            bio = meta.get("content", "")
    
    # =========================================================================
    # PREPARAÇÃO DOS DADOS FINAIS
    # =========================================================================
    
    # Cria um dicionário com todas as informações coletadas
    result = {
        "profile": profile_url,      # URL do perfil
        "username": target_username, # Nome de usuário
        "bio": bio                   # Bio/descrição extraida
    }
    
    # =========================================================================
    # SALVAMENTO DOS DADOS EM ARQUIVO JSON
    # =========================================================================
    
    # Salva o resultado em um arquivo JSON
    with open("bio_instagram.json", "w", encoding="utf-8") as f:
        # Converte o dicionário para JSON formatado
        # ensure_ascii=False permite caracteres especiais
        # indent=2 deixa o arquivo legível com indentação
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # =========================================================================
    # FINALIZAÇÃO E LIMPEZA
    # =========================================================================
    
    # Fecha o navegador e libera recursos
    driver.quit()
    
    # Retorna o resultado para o programa principal
    return result

# =============================================================================
# EXECUÇÃO INDEPENDENTE DO MÓDULO
# =============================================================================
# Esta seção permite que o arquivo seja executado diretamente
# em vez de apenas ser importado como módulo

if __name__ == "__main__":
    """
    Se este arquivo for executado diretamente (não importado),
    executa um teste da funcionalidade solicitando as credenciais
    e o perfil alvo diretamente ao usuário.
    """
    
    # =========================================================================
    # COLETA DE CREDENCIAIS PARA TESTE
    # =========================================================================
    
    # Tenta obter o nome de usuário das variáveis de ambiente
    # Se não existir, solicita ao usuário
    IG_USER = os.getenv("IG_USER") or input("Usuário login: ")
    
    # Tenta obter a senha das variáveis de ambiente
    # Se não existir, solicita ao usuário
    IG_PASS = os.getenv("IG_PASS") or input("Senha login: ")
    
    # Solicita o perfil que o usuário quer analisar
    TARGET = input("Perfil alvo: ")
    
    # =========================================================================
    # EXECUÇÃO DO BOT E EXIBIÇÃO DO RESULTADO
    # =========================================================================
    
    # Chama a função principal e exibe o resultado na tela
    print(get_instagram_bio(TARGET, IG_USER, IG_PASS))
