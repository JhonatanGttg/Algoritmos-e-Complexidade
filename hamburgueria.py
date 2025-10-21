from typing import Dict, List, Tuple, Optional
import time
from collections import defaultdict

class Hamburgueria:
    """
    Classe principal do sistema da Hamburgueria.
    Complexidade de espaço: O(n), onde n é o número de itens no cardápio
    """
    def __init__(self):
        # Dicionário de ingredientes com seus preços (O(1) para acesso)
        self.ingredientes = {
            'paes': {
                1: {'nome': 'Pão de batata', 'preco': 15.0},
                2: {'nome': 'Pão francês', 'preco': 12.0},
                3: {'nome': 'Pão de gergelim', 'preco': 13.0}
            },
            'carnes': {
                1: {'nome': 'Picanha', 'preco': 18.0},
                2: {'nome': 'Costela', 'preco': 15.0},
                3: {'nome': 'Linguiça', 'preco': 12.0}
            },
            'queijos': {
                1: {'nome': 'Cheddar', 'preco': 7.0},
                2: {'nome': 'Mussarela', 'preco': 5.0},
                3: {'nome': 'Prato', 'preco': 6.0}
            },
            'adicionais': {
                1: {'nome': 'Bacon', 'preco': 4.0},
                2: {'nome': 'Ovo', 'preco': 3.0},
                3: {'nome': 'Alface', 'preco': 2.0},
                4: {'nome': 'Tomate', 'preco': 2.0},
                5: {'nome': 'Cebola Caramelizada', 'preco': 3.0}
            }
        }
        
        # Lista para armazenar pedidos (O(n) de espaço, onde n é o número de pedidos)
        self.pedidos = []
        
        # Contador para IDs de pedidos
        self.contador_pedidos = 1

    def mostrar_menu_principal(self) -> None:
        """
        Exibe o menu principal da hamburgueria.
        Complexidade de tempo: O(1)
        """
        print("\n" + "="*50)
        print(f"{'HAMBURGUERIA DO SEU ZÉ':^50}")
        print("="*50)
        print("1. Fazer pedido")
        print("2. Ver cardápio")
        print("3. Buscar pedido")
        print("4. Sair")
        print("="*50 + "\n")

    def mostrar_cardapio(self) -> None:
        """
        Exibe o cardápio completo da hamburgueria.
        Complexidade de tempo: O(m), onde m é o número total de itens no cardápio
        """
        print("\n" + "="*50)
        print(f"{'CARDÁPIO':^50}")
        print("="*50)
        
        for categoria, itens in self.ingredientes.items():
            print(f"\n{categoria.upper()}:")
            for codigo, info in itens.items():
                print(f"  {codigo}. {info['nome']} - R$ {info['preco']:.2f}")
        
        print("\n" + "="*50 + "\n")

    def fazer_pedido(self) -> None:
        """
        Processa um novo pedido.
        Complexidade de tempo: O(1) para cada seleção de item (constante)
        """
        print("\n" + "="*50)
        print(f"{'NOVO PEDIDO':^50}")
        print("="*50)
        
        # Selecionar pão
        pao = self._selecionar_item('paes', "Escolha o tipo de pão:")
        if pao is None:
            return
            
        # Selecionar carne
        carne = self._selecionar_item('carnes', "\nEscolha o tipo de carne:")
        if carne is None:
            return
            
        # Selecionar queijo
        queijo = self._selecionar_item('queijos', "\nEscolha o tipo de queijo:")
        if queijo is None:
            return
            
        # Selecionar adicionais
        adicionais = self._selecionar_adicionais()
        
        # Calcular valor total (O(1) - operações constantes)
        total = (
            self.ingredientes['paes'][pao]['preco'] +
            self.ingredientes['carnes'][carne]['preco'] +
            self.ingredientes['queijos'][queijo]['preco']
        )
        
        # Adicionar preço dos adicionais (O(k), onde k é o número de adicionais)
        for adicional in adicionais:
            total += self.ingredientes['adicionais'][adicional]['preco']
        
        # Criar pedido
        pedido = {
            'id': self.contador_pedidos,
            'pao': pao,
            'carne': carne,
            'queijo': queijo,
            'adicionais': adicionais,
            'total': total,
            'hora': time.strftime('%d/%m/%Y %H:%M:%S')
        }
        
        self.pedidos.append(pedido)
        self.contador_pedidos += 1
        
        # Exibir resumo do pedido (O(k), onde k é o número de adicionais)
        self._exibir_resumo_pedido(pedido)

    def _selecionar_item(self, categoria: str, mensagem: str) -> Optional[int]:
        """
        Método auxiliar para selecionar um item de uma categoria.
        Complexidade de tempo: O(n), onde n é o número de tentativas do usuário
        """
        print(mensagem)
        for codigo, info in self.ingredientes[categoria].items():
            print(f"{codigo}. {info['nome']} - R$ {info['preco']:.2f}")
        
        while True:
            try:
                opcao = input("\nDigite o número da opção desejada (ou 'voltar' para cancelar): ")
                if opcao.lower() == 'voltar':
                    return None
                    
                opcao = int(opcao)
                if opcao in self.ingredientes[categoria]:
                    return opcao
                print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")

    def _selecionar_adicionais(self) -> List[int]:
        """
        Seleciona os adicionais do pedido.
        Complexidade de tempo: O(n), onde n é o número de itens no menu de adicionais
        """
        adicionais = []
        print("\nAdicionais (digite os números separados por vírgula):")
        
        for codigo, info in self.ingredientes['adicionais'].items():
            print(f"{codigo}. {info['nome']} - R$ {info['preco']:.2f}")
        
        while True:
            try:
                entrada = input("\nDigite os números dos adicionais (ou 'pular' para nenhum): ").strip()
                if not entrada or entrada.lower() == 'pular':
                    return adicionais
                
                # Processar entrada (O(k), onde k é o número de itens na entrada)
                selecionados = [int(x.strip()) for x in entrada.split(',') if x.strip().isdigit()]
                
                # Verificar se todos os itens são válidos (O(k))
                if all(1 <= x <= len(self.ingredientes['adicionais']) for x in selecionados):
                    return list(dict.fromkeys(selecionados))  # Remove duplicatas
                
                print(f"Por favor, digite números entre 1 e {len(self.ingredientes['adicionais'])}.")
            except ValueError:
                print("Entrada inválida. Tente novamente.")

    def _exibir_resumo_pedido(self, pedido: Dict) -> None:
        """
        Exibe um resumo do pedido.
        Complexidade de tempo: O(k), onde k é o número de adicionais
        """
        print("\n" + "="*50)
        print(f"{'PEDIDO Nº ' + str(pedido['id']):^50}")
        print("="*50)
        
        # Obtém os itens do pedido (O(1) para cada acesso)
        pao = self.ingredientes['paes'][pedido['pao']]
        carne = self.ingredientes['carnes'][pedido['carne']]
        queijo = self.ingredientes['queijos'][pedido['queijo']]
        
        # Exibe os itens principais
        print(f"\n{'ITEM':<30} {'VALOR':>15}")
        print("-"*50)
        print(f"{pao['nome']:<30} R$ {pao['preco']:>8.2f}")
        print(f"{carne['nome'] + ' (carne)':<30} R$ {carne['preco']:>8.2f}")
        print(f"{queijo['nome'] + ' (queijo)':<30} R$ {queijo['preco']:>8.2f}")
        
        # Exibe os adicionais (O(k), onde k é o número de adicionais)
        for cod_adicional in pedido['adicionais']:
            adicional = self.ingredientes['adicionais'][cod_adicional]
            print(f"{adicional['nome'] + ' (adicional)':<30} R$ {adicional['preco']:>8.2f}")
        
        # Exibe o total
        print("-"*50)
        print(f"{'TOTAL':<30} R$ {pedido['total']:>8.2f}")
        print("="*50)
        print(f"\nPedido realizado com sucesso!")
        print(f"Hora do pedido: {pedido['hora']}")
        print("="*50 + "\n")

    def buscar_pedido(self) -> None:
        """
        Busca um pedido pelo ID.
        Complexidade de tempo: O(n), onde n é o número de pedidos
        """
        if not self.pedidos:
            print("\nNenhum pedido realizado ainda.")
            return
            
        try:
            id_pedido = int(input("\nDigite o número do pedido: "))
            
            # Busca linear (O(n) no pior caso)
            for pedido in self.pedidos:
                if pedido['id'] == id_pedido:
                    self._exibir_resumo_pedido(pedido)
                    return
                    
            print(f"\nPedido nº {id_pedido} não encontrado.")
            
        except ValueError:
            print("\nNúmero de pedido inválido.")

    def executar(self) -> None:
        """
        Método principal que executa o sistema da hamburgueria.
        Complexidade de tempo: O(m*n), onde m é o número de iterações do menu e n é o número de pedidos
        """
        print("\nBem-vindo à Hamburgueria do Seu Zé!")
        
        while True:
            self.mostrar_menu_principal()
            
            try:
                opcao = input("Escolha uma opção: ").strip()
                
                if opcao == '1':
                    self.fazer_pedido()
                elif opcao == '2':
                    self.mostrar_cardapio()
                elif opcao == '3':
                    self.buscar_pedido()
                elif opcao == '4':
                    print("\nObrigado por usar o sistema da Hamburgueria do Seu Zé!")
                    print("Volte sempre!\n")
                    break
                else:
                    print("\nOpção inválida. Tente novamente.")
                    
            except (ValueError, KeyboardInterrupt):
                print("\nOperação cancelada pelo usuário.")
                break

# Executar o programa
if __name__ == "__main__":
    hamburgueria = Hamburgueria()
    hamburgueria.executar()
