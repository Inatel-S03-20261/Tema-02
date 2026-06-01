from typing import List
from .dto import TrocasRequestDTO
from .interfaces import InterfaceCartasService

class CartasController:
    def __init__(self, service: InterfaceCartasService):
        self.service = service

    def consultarCartas(self, idJogador: int) -> List[int]:
        return self.service.consultarCartas(idJogador)

    def requisicaoTroca(self, dadosTroca: TrocasRequestDTO) -> bool:
        return self.service.requisicaoTroca(dadosTroca)
