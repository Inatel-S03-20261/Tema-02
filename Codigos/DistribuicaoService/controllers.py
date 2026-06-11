import json
from .interface import InterfaceDistribuicaoService

class DistribuicaoController:
    def __init__(self, service: InterfaceDistribuicaoService):
        self.service = service

    def on_jogador_criado(self, payload: str):
        try:
            dados = json.loads(payload)
            id_jogador = dados.get("id_jogador")
            
            if id_jogador is not None:
                print(f"📥 [Worker] Evento Recebido: Novo jogador {id_jogador}. Iniciando distribuição...")
                self.service.distribuirCartas(id_jogador)
            else:
                print("⚠️ [Worker] Payload inválido: Faltando a chave 'id_jogador'.")
                
        except json.JSONDecodeError:
            print("⚠️ [Worker] Erro de rede: A mensagem recebida não é um JSON válido.")
        except Exception as e:
            print(f"⚠️ [Worker] Erro interno durante a orquestração do evento: {e}")