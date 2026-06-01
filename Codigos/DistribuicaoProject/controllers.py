from typing import List
from .interfaces import InterfaceDistribuicaoService

class DistribuicaoController:
    def __init__(self, service: InterfaceDistribuicaoService):
        self.service = service

    def getJogadorID(self) -> int:
        return 0

    def getPokemonAleatorio(self) -> List[int]:
        return []

    def distribuirCartas(self, idJogador: int, idsPokemon: List[int]) -> None:
        self.service.distribuirCartas(idJogador, idsPokemon)
