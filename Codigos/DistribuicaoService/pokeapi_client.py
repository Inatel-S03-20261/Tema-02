import random
import requests
from typing import List
from .interface import InterfaceSorteadorPokemons

# ==========================================
#       PADRÃO ESTRUTURAL: ADAPTER
# ==========================================

class PokeApiClient(InterfaceSorteadorPokemons):
    def __init__(self):
        self.species_url = "https://pokeapi.co/api/v2/pokemon-species"

    def obter_quantidade_total_pokemons(self) -> int:
        # PROXY
        response = requests.get(f"{self.species_url}?limit=1", timeout=5)
        response.raise_for_status() 
        
        data = response.json()
        total = data.get("count") 
        print(f"📡 [PokeAPI] Consulta realizada na rede. Total de espécies: {total}.")
        return total

    def sortear_ids_iniciais(self, quantidade: int = 5) -> List[int]:
        total_pokemons = self.obter_quantidade_total_pokemons()
        return random.sample(range(1, total_pokemons + 1), quantidade)