from dataclasses import dataclass
from typing import List

@dataclass
class TrocasRequestDTO:
    idJogadorOrigem: int
    idJogadorDestino: int
    idsPokemonsRecebidos: List[int]
    idsPokemonsEnviados: List[int]
