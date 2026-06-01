from abc import ABC, abstractmethod
from typing import List, Any, Dict

class InterfaceDistribuicaoService(ABC):
    @abstractmethod
    def distribuirCartas(self, idJogador: int, idsPokemon: List[int]) -> None:
        pass

    @abstractmethod
    def gerar_cartas_aleatorias(self, quantidade: int = 5) -> List[Dict[str, Any]]:
        pass

# This interface represents the dependency on the 'Cartas' project.
# In a real microservices scenario, this could be replaced by a Client calling an API.
class InterfaceCartasRepository(ABC):
    @abstractmethod
    def adicionarCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        pass
