import time
from typing import List
import random
from .interface import InterfaceSorteadorPokemons
from .pokeapi_client import PokeApiClient

# ==========================================
#       PADRÃO ESTRUTURAL: PROXY
# ==========================================

class PokeApiSmartProxy(InterfaceSorteadorPokemons):
    def __init__(self, pokeapi_adapter: PokeApiClient):
        self._pokeapi_adapter = pokeapi_adapter
        self._cache_total_pokemons = None
        self._ultima_atualizacao = 0
        self._TEMPO_EXPIRACAO_CACHE = 86400 # 24 horas
        self._FALLBACK = 1025 

    def sortear_ids_iniciais(self, quantidade: int = 5) -> List[int]:
        agora = time.time()
        
        if self._cache_total_pokemons and (agora - self._ultima_atualizacao) < self._TEMPO_EXPIRACAO_CACHE:
            print(f"⚡ [Proxy] Usando Cache: {self._cache_total_pokemons} Pokémons disponíveis.")
            total = self._cache_total_pokemons 
            
        else:
            print("🌐 [Proxy] Cache expirado/vazio. Tentando acessar a PokéAPI...")
            try:
                total = self._pokeapi_adapter.obter_quantidade_total_pokemons()
                
                self._cache_total_pokemons = total
                self._ultima_atualizacao = agora
                print("✅ [Proxy] Rede acessada com sucesso. Cache atualizado.")
                
            except Exception as e:
                print(f"⚠️ [Proxy] A PokéAPI está OFFLINE ({e}). Ativando Fallback de Segurança!")
                
                if self._cache_total_pokemons:
                    print("🚗 [Proxy] Usando cache antigo como fallback temporário.")
                    total = self._cache_total_pokemons
                else:
                    print(f"🚒 [Proxy] Sem cache prévio. Usando constante estática: {self._FALLBACK}")
                    total = self._FALLBACK

        return random.sample(range(1, total + 1), quantidade)