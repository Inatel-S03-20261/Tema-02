from .interface import InterfaceDistribuicaoService
from .pokeapi_client import PokeApiClient

from DeckService.interface import InterfaceCartasRepository

class DistribuicaoService(InterfaceDistribuicaoService):
    def __init__(self, cartas_repository: InterfaceCartasRepository):
        self.poke_api = PokeApiClient()
        self.cartas_repository = cartas_repository

    def distribuirCartas(self, idJogador: int) -> None:
        if self.cartas_repository.validarJogador(idJogador):
            print(f"❌ [Bloqueado] O jogador {idJogador} já possui cartas no sistema.")
            return

        print(f"🎲 [Novo Deck] Sorteando cartas para o novo jogador {idJogador}...")
        
        ids_sorteados = self.poke_api.sortear_ids_iniciais(quantidade=5)
        
        sucesso = self.cartas_repository.adicionarCartas(idJogador, ids_sorteados)
        
        if sucesso:
            print(f"✅ [Sucesso] Deck {ids_sorteados} salvo para o jogador {idJogador}.")
        else:
            print(f"❌ [Erro Crítico] Falha ao persistir as cartas no banco de dados.")