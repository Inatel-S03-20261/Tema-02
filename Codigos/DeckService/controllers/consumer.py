import json
from ..trocas_entity import TrocaEntity
from ..interface import InterfaceCartasService

class CartasConsumerController:
    def __init__(self, service: InterfaceCartasService):
        self.service = service

    def on_troca_solicitada(self, payload: str):
        try:
            dados_json = json.loads(payload)
            
            dados_troca = TrocaEntity(**dados_json)
            
            sucesso = self.service.requisicaoTroca(dados_troca)
            
            if sucesso:
                print("✅ Troca processada com sucesso.")
            else:
                print("❌ Falha ao efetivar a troca nas regras de negócio.")
                
        except json.JSONDecodeError:
            print("⚠️ Erro: Payload inválido ou não é um JSON.")
        except Exception as e:
            print(f"⚠️ Erro interno ao processar a mensagem do broker: {e}")