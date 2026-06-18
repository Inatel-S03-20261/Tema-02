from abc import ABC, abstractmethod
from typing import List
from .trocas_entity import TrocaEntity

class InterfaceCartasRepository(ABC):
    @abstractmethod
    def consultarCartas(self, idJogador: int) -> List[int]:
        pass

    @abstractmethod
    def adicionarCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        pass

    @abstractmethod
    def removerCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        pass

    @abstractmethod
    def validarJogador(self, idJogador: int) -> bool:
        pass


class InterfaceCartasService(ABC):
    @abstractmethod
    def consultarCartas(self, idJogador: int) -> List[int]:
        pass

    @abstractmethod
    def requisicaoTroca(self, dadosTroca: TrocaEntity) -> bool:
        pass