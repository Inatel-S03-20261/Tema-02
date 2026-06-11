from typing import Any, Dict
import random
import requests

class PokeApiClient:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"

    def obter_pokemon_aleatorio(self) -> Dict[str, Any]:
        # Delimitando aos 151 principais (Geração 1)
        pokemon_id = random.randint(1, 151)
        try:
            response = requests.get(f"{self.base_url}/{pokemon_id}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "id": data['id'],
                    "nome": data['name'],
                    "tipos": [t['type']['name'] for t in data['types']]
                }
        except Exception as e:
            print(f"Erro ao acessar PokeAPI: {e}")
        
        # Fallback básico em caso de erro
        return {"id": pokemon_id, "nome": "Desconhecido", "tipos": []}
