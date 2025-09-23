# =============================================================================
# NEWS SCRAPER - SCRAPER DE NOTÍCIAS (LIVROS)
# =============================================================================
# Este módulo é responsável por fazer web scraping do site "Books to Scrape"
# Extrai informações sobre livros como título, link e resumo
# e salva tudo em um arquivo JSON organizado
# =============================================================================

# Importação das bibliotecas necessárias
import requests              # Para fazer requisições HTTP (GET/POST)
from bs4 import BeautifulSoup # Para parsing e navegação em HTML
import json                  # Para manipulação de arquivos JSON
from urllib.parse import urljoin  # Para construir URLs completas

def scrape_books_to_scrape():
    """
    Função principal que executa o web scraping do site Books to Scrape.
    
    Processo:
    1. Acessa a página principal do site
    2. Encontra todos os livros listados
    3. Para cada livro, extrai: título, link e resumo
    4. Visita a página individual de cada livro para obter o resumo
    5. Salva todas as informações em um arquivo JSON
    
    Retorna:
        Nada - salva o resultado em 'manchetes.json'
    """
    
    # =========================================================================
    # CONFIGURAÇÃO INICIAL E ACESSO À PÁGINA PRINCIPAL
    # =========================================================================
    
    # URL base do site que vamos fazer scraping
    base = "http://books.toscrape.com/"
    
    # Faz uma requisição GET para a página principal
    # timeout=10 significa que vai esperar no máximo 10 segundos pela resposta
    resp = requests.get(base, timeout=10)
    
    # Cria um objeto BeautifulSoup para navegar pelo HTML da página
    # 'html.parser' é o analisador que vai interpretar o HTML
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Lista para armazenar todas as informações dos livros
    items = []
    
    # =========================================================================
    # ITERAÇÃO PELOS LIVROS NA PÁGINA PRINCIPAL
    # =========================================================================
    
    # Busca todos os elementos HTML que representam um livro
    # 'article.product_pod' é um seletor CSS que encontra artigos com classe 'product_pod'
    for article in soup.select("article.product_pod"):
        
        # =====================================================================
        # EXTRAÇÃO DO TÍTULO E LINK DO LIVRO
        # =====================================================================
        
        # Dentro de cada artigo, encontra o elemento h3 e depois o link (a)
        a = article.find("h3").find("a")
        
        # Extrai o título do livro do atributo 'title' do link
        # .strip() remove espaços em branco no início e fim
        title = a["title"].strip()
        
        # Constrói a URL completa do livro combinando a URL base com o link relativo
        # urljoin garante que a URL seja formada corretamente
        link = urljoin(base, a["href"])
        
        # =====================================================================
        # ACESSO À PÁGINA INDIVIDUAL DO LIVRO PARA OBTER O RESUMO
        # =====================================================================
        
        # Faz uma nova requisição para a página específica do livro
        p = requests.get(link, timeout=10)
        
        # Cria um novo objeto BeautifulSoup para a página do livro
        ps = BeautifulSoup(p.text, "html.parser")
        
        # =====================================================================
        # EXTRAÇÃO DO RESUMO DO LIVRO
        # =====================================================================
        
        # Procura pelo elemento que contém a descrição do produto
        desc_el = ps.select_one("#product_description")
        
        # Inicializa a variável do resumo como string vazia
        summary = ""
        
        # Se encontrou o elemento de descrição
        if desc_el:
            # Procura pelo próximo elemento irmão que seja um parágrafo (p)
            # Este é onde geralmente está o resumo do livro
            nxt = desc_el.find_next_sibling("p")
            
            # Se encontrou o parágrafo com o resumo
            if nxt:
                # Extrai o texto do resumo, removendo espaços extras
                summary = nxt.get_text(strip=True)
        
        # =====================================================================
        # ARMAZENAMENTO DAS INFORMAÇÕES DO LIVRO
        # =====================================================================
        
        # Cria um dicionário com todas as informações do livro
        # e adiciona à lista principal
        items.append({
            "title": title,      # Título do livro
            "link": link,        # URL completa da página do livro
            "summary": summary   # Resumo/descrição do livro
        })
    
    # =========================================================================
    # SALVAMENTO DOS DADOS EM ARQUIVO JSON
    # =========================================================================
    
    # Abre/cria o arquivo 'manchetes.json' para escrita
    # 'w' = modo de escrita (sobrescreve se já existir)
    # encoding="utf-8" garante que caracteres especiais sejam salvos corretamente
    with open("manchetes.json", "w", encoding="utf-8") as f:
        # Converte a lista de dicionários para formato JSON e salva no arquivo
        # ensure_ascii=False permite caracteres não-ASCII (acentos, etc.)
        # indent=2 formata o JSON de forma legível com indentação
        json.dump(items, f, ensure_ascii=False, indent=2)

# =============================================================================
# EXECUÇÃO INDEPENDENTE DO MÓDULO
# =============================================================================
# Se este arquivo for executado diretamente (não importado)
# executa a função de scraping
if __name__ == "__main__":
    scrape_books_to_scrape()
