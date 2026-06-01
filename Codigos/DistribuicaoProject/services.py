from typing import List
from .interfaces import InterfaceDistribuicaoService, InterfaceCartasRepository
from .clients import PokeApiClient

class DistribuicaoService(InterfaceDistribuicaoService):
    def __init__(self, repository: InterfaceCartasRepository, pokeapi_client: PokeApiClient):
        self.repository = repository
        self.pokeapi_client = pokeapi_client

    def distribuirCartas(self, idJogador: int, idsPokemon: List[int]) -> None:
        self.repository.adicionarCartas(idJogador, idsPokemon)

    def gerar_cartas_aleatorias(self, quantidade: int = 5) -> List[int]:
        return [self.pokeapi_client.obter_pokemon_aleatorio() for _ in range(quantidade)]
