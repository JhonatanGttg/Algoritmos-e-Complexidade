# =============================================================================
# ARQUIVO PRINCIPAL - MAIN.PY
# =============================================================================
# Este é o arquivo principal que coordena toda a aplicação
# Funciona como um menu interativo para escolher entre duas funcionalidades:
# 1. Scraper de notícias (livros)
# 2. Bot do Instagram para extrair bio de perfis
# =============================================================================

# Importação de bibliotecas padrão do Python
import os      # Para acessar variáveis de ambiente do sistema
import sys     # Para controle do sistema (como encerrar o programa)

def main():
    """
    Função principal que controla o fluxo da aplicação.
    
    Esta função:
    1. Exibe um menu com as opções disponíveis
    2. Recebe a escolha do usuário
    3. Executa a funcionalidade correspondente
    4. Trata opções inválidas
    """
    
    # =========================================================================
    # EXIBIÇÃO DO MENU PRINCIPAL
    # =========================================================================
    print("Escolha uma opção:")
    print("1 - Scraper de Notícias (Books to Scrape)")  # Opção para web scraping
    print("2 - Bot Login e Scraper de Bio Instagram")   # Opção para Instagram bot
    
    # Recebe a entrada do usuário e remove espaços em branco
    escolha = input("Opção: ").strip()
    
    # =========================================================================
    # PROCESSAMENTO DA ESCOLHA DO USUÁRIO
    # =========================================================================
    
    if escolha == "1":
        # OPÇÃO 1: SCRAPER DE NOTÍCIAS
        # Importa o módulo responsável pelo scraping de livros
        import news_scraper
        
        # Executa a função de scraping que vai:
        # - Acessar o site books.toscrape.com
        # - Extrair informações dos livros
        # - Salvar tudo em um arquivo JSON
        news_scraper.scrape_books_to_scrape()
        
        # Informa ao usuário que o arquivo foi criado
        print("manchetes.json gerado.")
        
    elif escolha == "2":
        # OPÇÃO 2: BOT DO INSTAGRAM
        # Importa o módulo responsável pelo bot do Instagram
        import ig_bio_bot
        
        # =====================================================================
        # COLETA DE CREDENCIAIS DO INSTAGRAM
        # =====================================================================
        # Tenta primeiro obter as credenciais das variáveis de ambiente
        # Se não existirem, solicita ao usuário que digite
        IG_USER = os.getenv("IG_USER") or input("Seu usuário IG: ")
        IG_PASS = os.getenv("IG_PASS") or input("Sua senha IG: ")
        
        # Solicita o perfil que o usuário quer analisar
        TARGET = input("Perfil alvo (ex: computacaounifavip_): ")
        
        # =====================================================================
        # EXECUÇÃO DO BOT DO INSTAGRAM
        # =====================================================================
        # Chama a função que vai:
        # - Abrir o Safari
        # - Fazer login no Instagram
        # - Navegar até o perfil alvo
        # - Extrair a bio do perfil
        # - Salvar em arquivo JSON
        res = ig_bio_bot.get_instagram_bio(TARGET, IG_USER, IG_PASS)
        
        # Informa ao usuário sobre o sucesso da operação
        print("bio_instagram.json gerado.")
        print(res)  # Mostra o resultado na tela
        
    else:
        # TRATAMENTO DE ERRO: OPÇÃO INVÁLIDA
        print("Opção inválida.")
        sys.exit(1)  # Encerra o programa com código de erro

# =============================================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# =============================================================================
# Esta estrutura garante que o código só execute quando o arquivo for
# executado diretamente (não quando importado como módulo)
if __name__ == "__main__":
    main()  # Chama a função principal
