from typing import List
from .dto import TrocasRequestDTO
from .interfaces import (
    InterfaceCartasService, 
    InterfaceCartasRepository
)

class CartasService(InterfaceCartasService):
    def __init__(self, repository: InterfaceCartasRepository):
        self.repository = repository

    def consultarCartas(self, idJogador: int) -> List[int]:
        return self.repository.consultarCartas(idJogador)

    def requisicaoTroca(self, dadosTroca: TrocasRequestDTO) -> bool:
        return True
