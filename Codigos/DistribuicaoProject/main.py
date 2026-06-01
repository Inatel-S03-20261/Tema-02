import sys
import os

# Ajusta o path para permitir importações locais sem o ponto relativo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clients import PokeApiClient
from services import DistribuicaoService
from controllers import DistribuicaoController
from interfaces import InterfaceCartasRepository
from typing import List

# Mock implementation of the external repository (Cartas project)
class MockCartasRepository(InterfaceCartasRepository):
    def adicionarCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        print(f"[CartasProject] Adicionando {len(idsPokemon)} cartas para o jogador {idJogador}: {idsPokemon}")
        return True

def main():
    print("--- Inicializando DistribuicaoProject ---")
    
    # Setup dependências
    repo = MockCartasRepository()
    client = PokeApiClient()
    service = DistribuicaoService(repo, client)
    controller = DistribuicaoController(service)

    # Simulação de fluxo
    jogador_id = controller.getJogadorID()
    print(f"Iniciando distribuição para Jogador ID: {jogador_id}")

    novas_cartas_data = controller.getPokemonAleatorio(5)
    
    import json
    # Retorna o JSON formatado das cartas geradas
    print("\n[Output JSON]")
    print(json.dumps(novas_cartas_data, indent=4, ensure_ascii=False))

    print("\nDistribuindo cartas...")
    ids_apenas = [p['id'] for p in novas_cartas_data]
    controller.distribuirCartas(jogador_id, ids_apenas)
    
    print("--- Operação Finalizada com Sucesso ---")

if __name__ == "__main__":
    main()
