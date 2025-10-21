from arvore_binaria import No, ArvoreBinaria

class NoAVL(No):
    def __init__(self, chave, valor):
        super().__init__(chave, valor)
        self.altura = 1

class ArvoreAVL(ArvoreBinaria):
    """
    Implementação de uma Árvore AVL, uma árvore binária de busca balanceada.
    Complexidades:
    - Inserção: O(log n)
    - Busca: O(log n)
    - Remoção: O(log n)
    - Percursos: O(n)
    """
    
    def _altura(self, no):
        if no is None:
            return 0
        return no.altura
    
    def _atualizar_altura(self, no):
        if no is not None:
            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
    
    def _fator_balanceamento(self, no):
        if no is None:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)
    
    def _rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita
        
        # Realiza a rotação
        x.direita = y
        y.esquerda = T2
        
        # Atualiza alturas
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        
        return x
    
    def _rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda
        
        # Realiza a rotação
        y.esquerda = x
        x.direita = T2
        
        # Atualiza alturas
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        
        return y
    
    def _balancear(self, no):
        if no is None:
            return no
            
        # Atualiza altura do nó atual
        self._atualizar_altura(no)
        
        # Obtém o fator de balanceamento
        balanceamento = self._fator_balanceamento(no)
        
        # Casos de desbalanceamento
        
        # Esquerda-Esquerda
        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)
        
        # Direita-Direita
        if balanceamento < -1 and self._fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)
        
        # Esquerda-Direita
        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        
        # Direita-Esquerda
        if balanceamento < -1 and self._fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)
        
        return no
    
    def inserir(self, chave, valor):
        """Insere um nó na árvore AVL."""
        self.raiz = self._inserir(self.raiz, chave, valor)
    
    def _inserir(self, no, chave, valor):
        # Inserção normal de BST
        if no is None:
            return NoAVL(chave, valor)
        
        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, valor)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, valor)
        else:
            no.valor = valor  # Atualiza o valor se a chave já existe
            return no
        
        # Atualiza a altura do nó ancestral
        self._atualizar_altura(no)
        
        # Retorna o nó balanceado
        return self._balancear(no)
    
    def remover(self, chave):
        """Remove um nó da árvore AVL."""
        self.raiz = self._remover(self.raiz, chave)
    
    def _remover(self, no, chave):
        if no is None:
            return no
        
        # Passo 1: Remoção padrão de BST
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
        
        # Se a árvore tinha apenas um nó, retorne
        if no is None:
            return no
            
        # Passo 2: Atualiza a altura do nó atual
        self._atualizar_altura(no)
        
        # Passo 3: Balanceia o nó
        return self._balancear(no)
    
    def _min_valor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
