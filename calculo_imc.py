from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto
import re

class ClassificacaoIMC(Enum):
    """Enumeração para classificação do IMC"""
    ABAIXO_PESO = (0, 18.5, "Abaixo do peso")
    PESO_NORMAL = (18.5, 25, "Peso normal")
    SOBREPESO = (25, 30, "Sobrepeso")
    OBESIDADE_I = (30, 35, "Obesidade Grau I")
    OBESIDADE_II = (35, 40, "Obesidade Grau II")
    OBESIDADE_III = (40, float('inf'), "Obesidade Grau III")

@dataclass
class ResultadoIMC:
    """Classe para armazenar o resultado do cálculo de IMC"""
    valor: float
    classificacao: str
    peso: float
    altura: float

class CalculadoraIMC:
    """
    Classe para cálculo de Índice de Massa Corporal (IMC).
    
    Complexidade de espaço: O(1) - usa espaço constante independente da entrada
    """
    
    @staticmethod
    def validar_entrada(valor: str, tipo: str = 'float') -> Tuple[bool, float]:
        """
        Valida a entrada do usuário.
        
        Args:
            valor: Valor de entrada como string
            tipo: Tipo de validação ('float' ou 'altura')
            
        Returns:
            Tupla (sucesso, valor) onde sucesso é booleano e valor é o número convertido
            
        Complexidade de tempo: O(1) - operações de tempo constante
        """
        try:
            num = float(valor.replace(',', '.'))
            if num <= 0:
                print(f"O valor deve ser maior que zero.")
                return False, 0.0
                
            if tipo == 'altura' and num > 3.0:
                print("A altura deve ser menor que 3.0 metros.")
                return False, 0.0
                
            return True, num
            
        except ValueError:
            print("Por favor, digite um valor numérico válido.")
            return False, 0.0
    
    @staticmethod
    def calcular_imc(peso: float, altura: float) -> float:
        """
        Calcula o IMC com base no peso e altura fornecidos.
        
        Args:
            peso: Peso em quilogramas
            altura: Altura em metros
            
        Returns:
            Valor do IMC arredondado para 2 casas decimais
            
        Complexidade de tempo: O(1) - operações aritméticas básicas
        """
        if peso <= 0 or altura <= 0:
            raise ValueError("Peso e altura devem ser valores positivos.")
        return round(peso / (altura ** 2), 2)
    
    @classmethod
    def classificar_imc(cls, imc: float) -> str:
        """
        Classifica o IMC de acordo com as faixas de referência.
        
        Args:
            imc: Valor do IMC calculado
            
        Returns:
            String com a classificação do IMC
            
        Complexidade de tempo: O(1) - número fixo de comparações
        """
        for classificacao in ClassificacaoIMC:
            lim_inf, lim_sup, descricao = classificacao.value
            if lim_inf <= imc < lim_sup:
                return descricao
        return "Classificação não disponível"
    
    @classmethod
    def obter_dados_usuario(cls) -> Optional[Tuple[float, float]]:
        """
        Obtém e valida os dados de peso e altura do usuário.
        
        Returns:
            Tupla (peso, altura) ou None se houver erro
            
        Complexidade de tempo: O(n) onde n é o número de tentativas do usuário
        """
        while True:
            try:
                # Obter peso
                entrada_peso = input("\nDigite o peso (em kg): ").strip()
                if not entrada_peso:
                    print("Entrada vazia. Tente novamente.")
                    continue
                    
                sucesso, peso = cls.validar_entrada(entrada_peso)
                if not sucesso:
                    continue
                
                # Obter altura
                entrada_altura = input("Digite a altura (em metros): ").strip()
                if not entrada_altura:
                    print("Entrada vazia. Tente novamente.")
                    continue
                    
                sucesso, altura = cls.validar_entrada(entrada_altura, 'altura')
                if not sucesso:
                    continue
                
                return peso, altura
                
            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário.")
                return None
    
    @classmethod
    def executar(cls) -> Optional[ResultadoIMC]:
        """
        Executa o fluxo principal da calculadora de IMC.
        
        Returns:
            Objeto ResultadoIMC com os resultados ou None se cancelado
            
        Complexidade de tempo: O(n) onde n é o número de tentativas do usuário
        """
        print("\n" + "="*50)
        print(f"{'CALCULADORA DE IMC':^50}")
        print("="*50)
        
        # Obter dados do usuário
        dados = cls.obter_dados_usuario()
        if dados is None:
            return None
            
        peso, altura = dados
        
        # Calcular IMC
        try:
            imc = cls.calcular_imc(peso, altura)
            classificacao = cls.classificar_imc(imc)
            
            # Exibir resultados
            print("\n" + "="*50)
            print(f"{'RESULTADO':^50}")
            print("="*50)
            print(f"Peso: {peso:.2f} kg")
            print(f"Altura: {altura:.2f} m")
            print(f"\nIMC: {imc:.2f}")
            print(f"Classificação: {classificacao}")
            print("="*50 + "\n")
            
            return ResultadoIMC(imc, classificacao, peso, altura)
            
        except ValueError as e:
            print(f"\nErro: {str(e)}")
            return None

# Executar o programa
if __name__ == "__main__":
    while True:
        resultado = CalculadoraIMC.executar()
        
        if resultado is None:
            break
            
        continuar = input("Deseja calcular outro IMC? (s/n): ").strip().lower()
        if continuar != 's':
            print("\nObrigado por usar a Calculadora de IMC!")
            break
