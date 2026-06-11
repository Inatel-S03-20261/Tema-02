import random
import requests
from typing import List

class PokeApiClient:
    def __init__(self):
        self.species_url = "https://pokeapi.co/api/v2/pokemon-species"

    def obter_quantidade_total_pokemons(self) -> int:
        try:
            response = requests.get(f"{self.species_url}?limit=1", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            total = data.get("count") 
            print(f"📡 [PokeAPI] Consulta realizada. Total de espécies: {total}.")
            return total
            
        except Exception as e:
            print(f"⚠️ Erro ao acessar PokeAPI: {e}. Usando fallback.")
            return 1025 # Fallback para 1025, que é o número total conhecido atualmente, caso a API esteja indisponível

    def sortear_ids_iniciais(self, quantidade: int = 5) -> List[int]:
        total_pokemons = self.obter_quantidade_total_pokemons()
        return random.sample(range(1, total_pokemons + 1), quantidade)