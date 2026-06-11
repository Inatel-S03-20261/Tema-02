from dataclasses import dataclass
from typing import List

@dataclass
class TrocaEntity:
    idJogadorOrigem: int
    idJogadorDestino: int
    idsPokemonsRecebidos: List[int]
    idsPokemonsEnviados: List[int]