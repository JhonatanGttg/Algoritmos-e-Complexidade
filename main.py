from arvore_avl import ArvoreAVL
from grafo import Grafo
import sys

class SistemaNavegacao:
    def __init__(self):
        self.arvore_cidades = ArvoreAVL()
        self.grafos_cidades = {}  # Mapeia ID da cidade para seu grafo
    
    def adicionar_cidade(self, id_cidade, nome):
        """Adiciona uma nova cidade ao sistema."""
        self.arvore_cidades.inserir(id_cidade, {"nome": nome, "bairros": {}})
        self.grafos_cidades[id_cidade] = Grafo()
        print(f"Cidade '{nome}' (ID: {id_cidade}) adicionada com sucesso!")
    
    def remover_cidade(self, id_cidade):
        """Remove uma cidade do sistema."""
        cidade = self.arvore_cidades.buscar(id_cidade)
        if cidade:
            nome = cidade.valor["nome"]
            self.arvore_cidades.remover(id_cidade)
            if id_cidade in self.grafos_cidades:
                del self.grafos_cidades[id_cidade]
            print(f"Cidade '{nome}' (ID: {id_cidade}) removida com sucesso!")
        else:
            print(f"Cidade com ID {id_cidade} não encontrada.")
    
    def adicionar_bairro(self, id_cidade, nome_bairro):
        """Adiciona um bairro a uma cidade."""
        cidade = self.arvore_cidades.buscar(id_cidade)
        if cidade:
            if nome_bairro not in cidade.valor["bairros"]:
                cidade.valor["bairros"][nome_bairro] = {}
                print(f"Bairro '{nome_bairro}' adicionado à cidade '{cidade.valor['nome']}'.")
            else:
                print(f"Bairro '{nome_bairro}' já existe na cidade '{cidade.valor['nome']}'.")
        else:
            print(f"Cidade com ID {id_cidade} não encontrada.")
    
    def adicionar_rota(self, id_cidade, origem, destino, distancia):
        """Adiciona uma rota entre dois bairros em uma cidade."""
        if id_cidade not in self.grafos_cidades:
            print(f"Cidade com ID {id_cidade} não encontrada.")
            return
        
        cidade = self.arvore_cidades.buscar(id_cidade)
        if not cidade:
            print(f"Cidade com ID {id_cidade} não encontrada.")
            return
        
        if origem not in cidade.valor["bairros"] or destino not in cidade.valor["bairros"]:
            print("Um ou ambos os bairros não existem nesta cidade.")
            return
        
        self.grafos_cidades[id_cidade].adicionar_aresta(origem, destino, float(distancia))
        print(f"Rota adicionada: {origem} <-> {destino} ({distancia} km)")
    
    def mostrar_percursos(self):
        """Mostra os percursos da árvore de cidades."""
        print("\n=== Percursos da Árvore de Cidades ===")
        print("Pré-ordem:", [c[1]["nome"] for c in self.arvore_cidades.pre_ordem()])
        print("Em-ordem:", [c[1]["nome"] for c in self.arvore_cidades.em_ordem()])
        print("Pós-ordem:", [c[1]["nome"] for c in self.arvore_cidades.pos_ordem()])
    
    def buscar_caminho(self, id_cidade, origem, destino):
        """Busca o caminho mais curto entre dois bairros usando Dijkstra."""
        if id_cidade not in self.grafos_cidades:
            print(f"Cidade com ID {id_cidade} não encontrada.")
            return
        
        grafo = self.grafos_cidades[id_cidade]
        distancia, caminho = grafo.dijkstra(origem, destino)
        
        if distancia is None:
            print(f"Não foi possível encontrar um caminho entre {origem} e {destino}.")
        else:
            print(f"\nCaminho mais curto de {origem} para {destino}:")
            print(f"Distância: {distancia} km")
            print("Rota:", " -> ".join(caminho))
    
    def mostrar_cidades(self):
        """Mostra todas as cidades cadastradas no sistema."""
        cidades = self.arvore_cidades.em_ordem()
        if not cidades:
            print("\nNenhuma cidade cadastrada no sistema.")
            return
        
        print("\n=== Cidades Cadastradas ===")
        print(f"{'ID':<5} | {'Nome':<20} | Nº de Bairros")
        print("-" * 40)
        for id_cidade, dados in cidades:
            num_bairros = len(dados["bairros"])
            print(f"{id_cidade:<5} | {dados['nome']:<20} | {num_bairros}")
        print("\nTotal de cidades:", len(cidades))
    
    def menu_principal(self):
        """Exibe o menu principal do sistema."""
        while True:
            print("\n=== Sistema de Navegação de Rotas ===")
            print("1. Adicionar Cidade")
            print("2. Remover Cidade")
            print("3. Listar Cidades")
            print("4. Adicionar Bairro")
            print("5. Adicionar Rota")
            print("6. Mostrar Percursos")
            print("7. Buscar Caminho")
            print("8. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                try:
                    id_cidade = int(input("ID da cidade: "))
                    nome = input("Nome da cidade: ")
                    self.adicionar_cidade(id_cidade, nome)
                except ValueError:
                    print("ID deve ser um número inteiro.")
            
            elif opcao == "2":
                try:
                    id_cidade = int(input("ID da cidade a remover: "))
                    self.remover_cidade(id_cidade)
                except ValueError:
                    print("ID deve ser um número inteiro.")
            
            elif opcao == "3":
                self.mostrar_cidades()
            
            elif opcao == "4":
                try:
                    id_cidade = int(input("ID da cidade: "))
                    nome_bairro = input("Nome do bairro: ")
                    self.adicionar_bairro(id_cidade, nome_bairro)
                except ValueError:
                    print("ID deve ser um número inteiro.")
            
            elif opcao == "5":
                try:
                    id_cidade = int(input("ID da cidade: "))
                    origem = input("Bairro de origem: ")
                    destino = input("Bairro de destino: ")
                    distancia = float(input("Distância (km): "))
                    self.adicionar_rota(id_cidade, origem, destino, distancia)
                except ValueError:
                    print("Entrada inválida. Certifique-se de que a distância é um número.")
            
            elif opcao == "6":
                self.mostrar_percursos()
            
            elif opcao == "7":
                try:
                    id_cidade = int(input("ID da cidade: "))
                    origem = input("Bairro de origem: ")
                    destino = input("Bairro de destino: ")
                    self.buscar_caminho(id_cidade, origem, destino)
                except ValueError:
                    print("ID deve ser um número inteiro.")
            
            elif opcao == "8":
                print("Saindo do sistema...")
                break
            
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    sistema = SistemaNavegacao()
    
    # Adiciona algumas cidades de exemplo
    sistema.adicionar_cidade(1, "São Paulo")
    sistema.adicionar_cidade(2, "Rio de Janeiro")
    sistema.adicionar_cidade(3, "Belo Horizonte")
    
    # Adiciona alguns bairros de exemplo
    sistema.adicionar_bairro(1, "Moema")
    sistema.adicionar_bairro(1, "Pinheiros")
    sistema.adicionar_bairro(1, "Vila Madalena")
    sistema.adicionar_bairro(2, "Copacabana")
    sistema.adicionar_bairro(2, "Ipanema")
    
    # Adiciona algumas rotas de exemplo
    sistema.adicionar_rota(1, "Moema", "Pinheiros", 8.5)
    sistema.adicionar_rota(1, "Pinheiros", "Vila Madalena", 3.2)
    sistema.adicionar_rota(2, "Copacabana", "Ipanema", 5.0)
    
    print("\n=== Sistema de Navegação de Rotas ===")
    print("Bem-vindo! O sistema já vem com alguns dados de exemplo.")
    print("Use o menu para explorar as funcionalidades.\n")
    
    sistema.menu_principal()
