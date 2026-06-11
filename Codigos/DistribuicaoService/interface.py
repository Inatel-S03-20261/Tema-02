from abc import ABC, abstractmethod

class InterfaceDistribuicaoService(ABC):
    @abstractmethod
    def distribuirCartas(self, idJogador: int) -> None:
        pass