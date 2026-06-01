from typing import List
from .interfaces import InterfaceCartasRepository

class DatabaseConnection:
    pass

class CartasRepository(InterfaceCartasRepository):
    def __init__(self, db: DatabaseConnection):
        self._db = db

    def consultarCartas(self, idJogador: int) -> List[int]:
        return []

    def adicionarCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        return True

    def removerCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        return True

    def validarJogador(self, idJogador: int) -> bool:
        return True
