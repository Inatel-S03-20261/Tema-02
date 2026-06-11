import os
import ssl
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from dotenv import load_dotenv

from DeckService.repository import CartasRepository
from DeckService.services import CartasService
from DeckService.controllers.consumer import CartasConsumerController

from DistribuicaoService.services import DistribuicaoService
from DistribuicaoService.controllers import DistribuicaoController

load_dotenv()

print("⚙️ Inicializando os microsserviços e injetando dependências...")

cartas_repo = CartasRepository()

deck_service = CartasService(cartas_repo)
distribuicao_service = DistribuicaoService(cartas_repo)

deck_controller = CartasConsumerController(deck_service)
dist_controller = DistribuicaoController(distribuicao_service)

TOPICO_NOVO_JOGADOR = "pokemon/jogadores/criado"
TOPICO_TROCA = "pokemon/trocas/solicitada"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Conectado ao HiveMQ Cloud com sucesso!")
        client.subscribe(TOPICO_NOVO_JOGADOR)
        client.subscribe(TOPICO_TROCA)
        print(f"🎧 Escutando os tópicos:\n - {TOPICO_NOVO_JOGADOR}\n - {TOPICO_TROCA}\n")
    else:
        print(f"❌ Falha ao conectar ao broker. Código de retorno: {reason_code}")

def on_message(client, userdata, msg):
    topico = msg.topic
    payload = msg.payload.decode('utf-8')
    
    if topico == TOPICO_NOVO_JOGADOR:
        dist_controller.on_jogador_criado(payload)
        
    elif topico == TOPICO_TROCA:
        deck_controller.on_troca_solicitada(payload)

def iniciar_worker():
    broker_url = os.getenv("HIVEMQ_HOST")
    broker_port = int(os.getenv("HIVEMQ_PORT", 8883))
    broker_user = os.getenv("HIVEMQ_USER")
    broker_pass = os.getenv("HIVEMQ_PASSWORD")

    if not broker_url:
        print("⚠️ ERRO: Arquivo .env não configurado corretamente. Verifique as credenciais do HiveMQ.")
        return

    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="Pokemon_Worker_01")
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(broker_user, broker_pass)

    client.on_connect = on_connect
    client.on_message = on_message

    print("🚀 Conectando à rede MQTT...")
    try:
        client.connect(broker_url, broker_port, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Worker desligado manualmente.")
    except Exception as e:
        print(f"❌ Erro crítico de conexão: {e}")

if __name__ == "__main__":
    iniciar_worker()