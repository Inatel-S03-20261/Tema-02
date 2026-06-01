from typing import List, Any, Dict
try:
    from .interfaces import InterfaceDistribuicaoService
except ImportError:
    from interfaces import InterfaceDistribuicaoService

class DistribuicaoController:
    def __init__(self, service: InterfaceDistribuicaoService):
        self.service = service

    def getJogadorID(self) -> int:
        # Mock logic to represent getting an ID (could be from session or auth)
        import random
        return random.randint(1000, 9999)

    def getPokemonAleatorio(self, quantidade: int = 5) -> List[Dict[str, Any]]:
        return self.service.gerar_cartas_aleatorias(quantidade)

    def distribuirCartas(self, idJogador: int, idsPokemon: List[int]) -> None:
        self.service.distribuirCartas(idJogador, idsPokemon)
