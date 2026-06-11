from typing import List
from .interface import InterfaceCartasRepository
from shared.database import Database

class CartasRepository(InterfaceCartasRepository):
    def __init__(self):
        database_instance = Database()        
        self.db = database_instance.get_db() 
    
        self.collection = self.db.collection('decks')

    def validarJogador(self, idJogador: int) -> bool:
        doc_ref = self.collection.document(str(idJogador))
        return doc_ref.get().exists

    def consultarCartas(self, idJogador: int) -> List[int]:
        doc_ref = self.collection.document(str(idJogador))
        doc = doc_ref.get()
        
        if doc.exists:
            dados = doc.to_dict()
            return dados.get("pokemons", [])
        
        return []

    def adicionarCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        try:
            doc_ref = self.collection.document(str(idJogador))
            doc = doc_ref.get()
            
            if doc.exists:
                cartas_atuais = doc.to_dict().get("pokemons", [])
                
                for nova_carta in idsPokemon:
                    if nova_carta in cartas_atuais:
                        print(f"❌ [Repositório] Integridade violada: O jogador {idJogador} já possui a carta {nova_carta}.")
                        return False
                    cartas_atuais.append(nova_carta)
                    
                doc_ref.update({"pokemons": cartas_atuais})
            else:
                if len(idsPokemon) != len(set(idsPokemon)):
                    print("❌ [Repositório] Integridade violada: Tentativa de inserção inicial com cartas duplicadas.")
                    return False
                doc_ref.set({"pokemons": idsPokemon})
                
            return True
            
        except Exception as e:
            print(f"❌ [Repositório] Erro ao adicionar cartas: {e}")
            return False

    def removerCartas(self, idJogador: int, idsPokemon: List[int]) -> bool:
        try:
            doc_ref = self.collection.document(str(idJogador))
            doc = doc_ref.get()
            
            if not doc.exists:
                print(f"❌ [Repositório] Jogador {idJogador} não encontrado.")
                return False
                
            cartas_atuais = doc.to_dict().get("pokemons", [])
            
            for pokemon_id in idsPokemon:
                if pokemon_id in cartas_atuais:
                    cartas_atuais.remove(pokemon_id)
                else:
                    print(f"❌ [Repositório] O jogador {idJogador} não possui a carta {pokemon_id}.")
                    return False
                    
            doc_ref.update({"pokemons": cartas_atuais})
            return True
            
        except Exception as e:
            print(f"❌ [Repositório] Erro ao remover cartas: {e}")
            return False