class No:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreBinaria:
    """
    Implementação de uma Árvore Binária de Busca (BST).
    Complexidades:
    - Inserção: O(h) onde h é a altura da árvore (O(n) no pior caso)
    - Busca: O(h)
    - Remoção: O(h)
    - Percursos: O(n) onde n é o número de nós
    """
    
    def __init__(self):
        self.raiz = None
    
    def inserir(self, chave, valor):
        """Insere um nó na árvore."""
        self.raiz = self._inserir(self.raiz, chave, valor)
    
    def _inserir(self, no, chave, valor):
        if no is None:
            return No(chave, valor)
        
        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, valor)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, valor)
        else:
            no.valor = valor  # Atualiza o valor se a chave já existe
        
        return no
    
    def buscar(self, chave):
        """Busca um nó na árvore."""
        return self._buscar(self.raiz, chave)
    
    def _buscar(self, no, chave):
        if no is None or no.chave == chave:
            return no
        
        if chave < no.chave:
            return self._buscar(no.esquerda, chave)
        return self._buscar(no.direita, chave)
    
    def remover(self, chave):
        """Remove um nó da árvore."""
        self.raiz = self._remover(self.raiz, chave)
    
    def _remover(self, no, chave):
        if no is None:
            return no
        
        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)
        else:
            # Nó com apenas um filho ou nenhum
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            
            # Nó com dois filhos: pega o sucessor in-order
            temp = self._min_valor_no(no.direita)
            no.chave = temp.chave
            no.valor = temp.valor
            no.direita = self._remover(no.direita, temp.chave)
        
        return no
    
    def _min_valor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
    
    # Percursos
    def em_ordem(self):
        """Retorna uma lista com os nós em ordem."""
        return self._em_ordem(self.raiz, [])
    
    def _em_ordem(self, no, resultado):
        if no:
            self._em_ordem(no.esquerda, resultado)
            resultado.append((no.chave, no.valor))
            self._em_ordem(no.direita, resultado)
        return resultado
    
    def pre_ordem(self):
        """Retorna uma lista com os nós em pré-ordem."""
        return self._pre_ordem(self.raiz, [])
    
    def _pre_ordem(self, no, resultado):
        if no:
            resultado.append((no.chave, no.valor))
            self._pre_ordem(no.esquerda, resultado)
            self._pre_ordem(no.direita, resultado)
        return resultado
    
    def pos_ordem(self):
        """Retorna uma lista com os nós em pós-ordem."""
        return self._pos_ordem(self.raiz, [])
    
    def _pos_ordem(self, no, resultado):
        if no:
            self._pos_ordem(no.esquerda, resultado)
            self._pos_ordem(no.direita, resultado)
            resultado.append((no.chave, no.valor))
        return resultado
