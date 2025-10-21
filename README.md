# 🗺️ Sistema de Navegação de Rotas e Dados Hierárquicos

**Aluno:** Jhonatan Inacio da Silva  
**Disciplina:** Algoritmos e Complexidade
**Professor:** Anderson Bispo
**Data:** Outubro/2025

## 📝 Descrição do Projeto

Este projeto implementa um sistema de gestão de cidades e rotas que utiliza estruturas de dados avançadas como Árvores Binárias de Busca, Árvores AVL e Grafos. O sistema permite o cadastro de cidades, bairros e rotas, além de fornecer funcionalidades avançadas de busca e navegação.

## 🎯 Objetivos

- Implementar estruturas de dados hierárquicas (árvores) e de rede (grafos)
- Aplicar algoritmos de busca e ordenação
- Desenvolver um sistema completo com interface de linha de comando
- Praticar conceitos de complexidade algorítmica

## 🏗️ Estrutura do Projeto

```
.
├── arvore_binaria.py  # Implementação da Árvore Binária de Busca
├── arvore_avl.py      # Implementação da Árvore AVL
├── grafo.py           # Implementação de Grafos com BFS, DFS e Dijkstra
└── main.py            # Interface do sistema
```

## 🔧 Funcionalidades

### 🌳 Gerenciamento de Cidades (Árvore AVL)
- [x] Cadastro de cidades
- [x] Remoção de cidades
- [x] Listagem de cidades cadastradas
- [x] Percursos em pré-ordem, em-ordem e pós-ordem

### 🏙️ Gerenciamento de Bairros
- [x] Adição de bairros às cidades
- [x] Visualização de bairros por cidade

### 🛣️ Gerenciamento de Rotas (Grafos)
- [x] Adição de rotas entre bairros
- [x] Busca em Largura (BFS)
- [x] Busca em Profundidade (DFS)
- [x] Cálculo do caminho mínimo (Dijkstra)

## 📊 Complexidade das Operações

| Operação           | Estrutura         | Complexidade  |
|--------------------|-------------------|---------------|
| Inserção          | Árvore Binária    | O(h)*         |
| Inserção          | AVL               | O(log n)      |
| Busca             | Árvore Binária/AVL| O(log n)      |
| Remoção           | Árvore Binária    | O(h)*         |
| Remoção           | AVL               | O(log n)      |
| BFS/DFS           | Grafo             | O(V + E)      |
| Caminho Mínimo    | Grafo (Dijkstra)  | O((V+E)log V) |

_* Onde h é a altura da árvore (O(n) no pior caso para árvore desbalanceada)_

## 🚀 Como Executar

1. Certifique-se de ter o Python 3.x instalado
2. Clone o repositório
3. Navegue até o diretório do projeto
4. Execute o comando:
   ```bash
   python3 main.py
   ```

## 🎮 Como Usar

1. **Adicionar Cidade**: Cadastre novas cidades com ID e nome
2. **Adicionar Bairro**: Adicione bairros às cidades existentes
3. **Adicionar Rota**: Crie conexões entre bairros com distâncias
4. **Buscar Caminho**: Encontre o caminho mais curto entre dois bairros
5. **Ver Percursos**: Visualize os diferentes percursos da árvore de cidades

## 📚 Aprendizados

- Implementação de estruturas de dados complexas
- Balanceamento de árvores (AVL)
- Algoritmos de busca em grafos
- Análise de complexidade algorítmica
- Desenvolvimento de interfaces de linha de comando

## 📋 Requisitos

- Python 3.6+
- Nenhuma dependência externa necessária
