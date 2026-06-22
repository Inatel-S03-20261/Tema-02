from abc import ABC, abstractmethod
from typing import List

class InterfaceDistribuicaoService(ABC):
    @abstractmethod
    def distribuirCartas(self, idJogador: int) -> None:
        pass

class InterfaceSorteadorPokemons(ABC):
    @abstractmethod
    def sortear_ids_iniciais(self, quantidade: int = 5) -> List[int]:
        pass