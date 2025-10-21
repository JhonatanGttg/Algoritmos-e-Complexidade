import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto
import time
from collections import defaultdict

class ResultadoJogada(Enum):
    """Enumeração para resultados possíveis de uma jogada"""
    VITORIA_J1 = auto()
    VITORIA_J2 = auto()
    EMPATE = auto()

@dataclass
class EstatisticasJogador:
    """Classe para armazenar estatísticas de um jogador"""
    vitorias: int = 0
    derrotas: int = 0
    empates: int = 0
    maior_pontuacao: int = 0
    lancamentos: List[int] = None
    
    def __post_init__(self):
        self.lancamentos = []
    
    def adicionar_lancamento(self, valor: int) -> None:
        """Adiciona um lançamento às estatísticas do jogador"""
        self.lancamentos.append(valor)
        if valor > self.maior_pontuacao:
            self.maior_pontuacao = valor
    
    def media_lancamentos(self) -> float:
        """Calcula a média dos lançamentos do jogador"""
        if not self.lancamentos:
            return 0.0
        return sum(self.lancamentos) / len(self.lancamentos)

class JogoDados:
    """
    Classe principal do jogo de dados.
    
    Complexidade de espaço: O(n), onde n é o número de rodadas jogadas
    """
    
    def __init__(self):
        self.estatisticas = {
            1: EstatisticasJogador(),  # Jogador 1
            2: EstatisticasJogador()   # Jogador 2
        }
        self.historico_rodadas = []
        self.rodada_atual = 0
    
    def _rolar_dado(self) -> int:
        """
        Rola um dado de 6 lados.
        
        Returns:
            Número aleatório entre 1 e 6
            
        Complexidade de tempo: O(1) - operação de tempo constante
        """
        return random.randint(1, 6)
    
    def _jogar_rodada(self) -> Tuple[int, int, ResultadoJogada]:
        """
        Executa uma rodada do jogo.
        
        Returns:
            Tupla (valor_jogador1, valor_jogador2, resultado)
            
        Complexidade de tempo: O(1) - operações de tempo constante
        """
        # Jogador 1 joga o dado
        dado1 = self._rolar_dado()
        self.estatisticas[1].adicionar_lancamento(dado1)
        
        # Jogador 2 joga o dado
        dado2 = self._rolar_dado()
        self.estatisticas[2].adicionar_lancamento(dado2)
        
        # Determinar o vencedor
        if dado1 > dado2:
            resultado = ResultadoJogada.VITORIA_J1
            self.estatisticas[1].vitorias += 1
            self.estatisticas[2].derrotas += 1
        elif dado2 > dado1:
            resultado = ResultadoJogada.VITORIA_J2
            self.estatisticas[2].vitorias += 1
            self.estatisticas[1].derrotas += 1
        else:
            resultado = ResultadoJogada.EMPATE
            self.estatisticas[1].empates += 1
            self.estatisticas[2].empates += 1
        
        # Registrar rodada no histórico
        self.rodada_atual += 1
        self.historico_rodadas.append((dado1, dado2, resultado))
        
        return dado1, dado2, resultado
    
    def _exibir_resultado_rodada(self, dado1: int, dado2: int, resultado: ResultadoJogada) -> None:
        """
        Exibe o resultado de uma rodada.
        
        Complexidade de tempo: O(1) - operações de saída constantes
        """
        print(f"\n" + "="*50)
        print(f"{'RODADA ' + str(self.rodada_atual):^50}")
        print("="*50)
        print(f"Jogador 1: {dado1} {'' * dado1}")
        print(f"Jogador 2: {dado2} {'' * dado2}")
        print("-" * 50)
        
        if resultado == ResultadoJogada.VITORIA_J1:
            print(" Jogador 1 venceu a rodada!")
        elif resultado == ResultadoJogada.VITORIA_J2:
            print(" Jogador 2 venceu a rodada!")
        else:
            print(" Empate!")
        
        print(f"{'='*50}\n")
    
    def _exibir_estatisticas(self) -> None:
        """
        Exibe as estatísticas do jogo.
        
        Complexidade de tempo: O(1) - operações de saída constantes
        """
        print("\n" + "="*50)
        print(f"{'ESTATÍSTICAS':^50}")
        print("="*50)
        
        for jogador in [1, 2]:
            stats = self.estatisticas[jogador]
            print(f"\nJogador {jogador}:")
            print(f"  Vitórias: {stats.vitorias}")
            print(f"  Derrotas: {stats.derrotas}")
            print(f"  Empates: {stats.empates}")
            print(f"  Maior pontuação: {stats.maior_pontuacao}")
            print(f"  Média de pontos: {stats.media_lancamentos():.2f}")
            
            # Análise de distribuição dos lançamentos
            if stats.lancamentos:
                distribuicao = defaultdict(int)
                for valor in stats.lancamentos:
                    distribuicao[valor] += 1
                
                print("  Distribuição de lançamentos:")
                for face in range(1, 7):
                    count = distribuicao.get(face, 0)
                    percentual = (count / len(stats.lancamentos)) * 100 if stats.lancamentos else 0
                    print(f"    {face}: {'' * count} ({percentual:.1f}%)")
        
        print("\n" + "="*50 + "\n")
    
    def _jogar_novamente(self) -> bool:
        """
        Pergunta ao usuário se deseja jogar novamente.
        
        Returns:
            True se o usuário quiser jogar novamente, False caso contrário
            
        Complexidade de tempo: O(1) - entrada do usuário
        """
        while True:
            resposta = input("Deseja jogar novamente? (s/n): ").strip().lower()
            if resposta in ['s', 'sim']:
                return True
            elif resposta in ['n', 'nao', 'não']:
                return False
            print("Por favor, responda com 's' para sim ou 'n' para não.")
    
    def executar(self) -> None:
        """
        Executa o jogo principal.
        
        Complexidade de tempo: O(n), onde n é o número de rodadas jogadas
        """
        print("\n" + "="*50)
        print(f"{'JOGO DE DADOS':^50}")
        print("="*50)
        print("Regras:")
        print("- Dois jogadores lançam um dado de 6 faces")
        print("- O maior número vence a rodada")
        print("- Em caso de empate, os jogadores lançam novamente")
        print("- O jogo continua até que um jogador vença")
        print("="*50 + "\n")
        
        while True:
            try:
                input("Pressione Enter para lançar os dados (ou Ctrl+C para sair)...")
                
                # Jogar uma rodada
                dado1, dado2, resultado = self._jogar_rodada()
                self._exibir_resultado_rodada(dado1, dado2, resultado)
                
                # Se não for empate, perguntar se quer jogar novamente
                if resultado != ResultadoJogada.EMPATE:
                    self._exibir_estatisticas()
                    if not self._jogar_novamente():
                        print("\nObrigado por jogar! Até a próxima! \n")
                        break
                
            except KeyboardInterrupt:
                print("\n\nJogo interrompido. Exibindo estatísticas finais...\n")
                self._exibir_estatisticas()
                print("Obrigado por jogar! Até a próxima! \n")
                break

# Executar o jogo
if __name__ == "__main__":
    jogo = JogoDados()
    jogo.executar()
