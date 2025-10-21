import heapq
from collections import defaultdict, deque

class Grafo:
    """
    Implementação de um grafo ponderado não-direcionado usando lista de adjacência.
    Complexidades:
    - Adicionar aresta: O(1)
    - BFS/DFS: O(V + E)
    - Dijkstra: O((V + E) log V)
    """
    
    def __init__(self):
        self.grafo = defaultdict(dict)  # {vértice: {vizinho: peso}}
    
    def adicionar_aresta(self, u, v, peso=1):
        """Adiciona uma aresta entre os vértices u e v com peso opcional."""
        self.grafo[u][v] = peso
        self.grafo[v][u] = peso  # Para grafo não-direcionado
    
    def remover_aresta(self, u, v):
        """Remove a aresta entre os vértices u e v."""
        if u in self.grafo and v in self.grafo[u]:
            del self.grafo[u][v]
            del self.grafo[v][u]
    
    def bfs(self, inicio):
        """Busca em Largura (BFS) a partir de um vértice."""
        visitados = set()
        fila = deque([inicio])
        resultado = []
        
        while fila:
            vertice = fila.popleft()
            if vertice not in visitados:
                visitados.add(vertice)
                resultado.append(vertice)
                for vizinho in sorted(self.grafo[vertice]):
                    if vizinho not in visitados:
                        fila.append(vizinho)
        
        return resultado
    
    def dfs(self, inicio):
        """Busca em Profundidade (DFS) a partir de um vértice."""
        visitados = set()
        resultado = []
        
        def _dfs(vertice):
            visitados.add(vertice)
            resultado.append(vertice)
            for vizinho in sorted(self.grafo[vertice]):
                if vizinho not in visitados:
                    _dfs(vizinho)
        
        _dfs(inicio)
        return resultado
    
    def dijkstra(self, inicio, fim=None):
        """
        Algoritmo de Dijkstra para encontrar o caminho mínimo de um vértice para todos os outros.
        Retorna um dicionário com as distâncias e os caminhos.
        Se um vértice final for especificado, retorna apenas a distância e o caminho para ele.
        """
        # Inicialização
        distancias = {v: float('infinity') for v in self.grafo}
        distancias[inicio] = 0
        
        # Fila de prioridade: (distância, vértice)
        fila_prioridade = [(0, inicio)]
        
        # Dicionário para armazenar o caminho
        caminhos = {v: [] for v in self.grafo}
        caminhos[inicio] = [inicio]
        
        while fila_prioridade:
            distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)
            
            # Se já encontramos um caminho melhor, ignoramos
            if distancia_atual > distancias[vertice_atual]:
                continue
            
            # Se chegamos ao destino e ele foi especificado, podemos parar
            if fim is not None and vertice_atual == fim:
                break
            
            for vizinho, peso in self.grafo[vertice_atual].items():
                distancia = distancia_atual + peso
                
                # Se encontrarmos um caminho mais curto para o vizinho
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    caminhos[vizinho] = caminhos[vertice_atual] + [vizinho]
                    heapq.heappush(fila_prioridade, (distancia, vizinho))
        
        if fim is not None:
            if distancias[fim] == float('infinity'):
                return None, None  # Caminho não encontrado
            return distancias[fim], caminhos[fim]
        
        return distancias, caminhos
    
    def __str__(self):
        """Representação em string do grafo."""
        resultado = []
        for vertice, vizinhos in self.grafo.items():
            vizinhos_str = ", ".join(f"{v}({p})" for v, p in vizinhos.items())
            resultado.append(f"{vertice}: {vizinhos_str}")
        return "\n".join(resultado)
