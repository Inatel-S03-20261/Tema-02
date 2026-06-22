import os
import ssl
import threading
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from dotenv import load_dotenv

from DeckService.repository import CartasRepository
from DeckService.services import CartasService
from DeckService.controllers.consumer import CartasConsumerController
from DistribuicaoService.services import DistribuicaoService
from DistribuicaoService.controllers import DistribuicaoController
from DistribuicaoService.pokeapi_client import PokeApiClient
from DistribuicaoService.proxy import PokeApiSmartProxy

load_dotenv()

print("⚙️ Inicializando os microsserviços...")
cartas_repo = CartasRepository()
sorteador_adapter = PokeApiClient()
sorteador_proxy = PokeApiSmartProxy(sorteador_adapter)

deck_service = CartasService(cartas_repo)
distribuicao_service = DistribuicaoService(cartas_repo, sorteador_proxy)

deck_controller = CartasConsumerController(deck_service)
dist_controller = DistribuicaoController(distribuicao_service)

TOPICO_NOVO_JOGADOR = "pokemon/jogadores/criado"
TOPICO_TROCA = "pokemon/trocas/solicitada"

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Worker do Pokemon operando normalmente!")
        
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def iniciar_servidor_fake():
    porta = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", porta), DummyHandler)
    server.serve_forever()

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Conectado ao HiveMQ Cloud com sucesso!")
        client.subscribe(TOPICO_NOVO_JOGADOR)
        client.subscribe(TOPICO_TROCA)
    else:
        print(f"❌ Falha ao conectar ao broker: {reason_code}")

def on_message(client, userdata, msg):
    topico = msg.topic
    payload = msg.payload.decode('utf-8')

    print(f"📥 [RADAR] Mensagem recebida! Tópico: {topico} | Payload: {payload}")
    
    if topico == TOPICO_NOVO_JOGADOR:
        dist_controller.on_jogador_criado(payload)
    elif topico == TOPICO_TROCA:
        deck_controller.on_troca_solicitada(payload)

def iniciar_worker():
    broker_url = os.getenv("HIVEMQ_HOST")
    broker_port = int(os.getenv("HIVEMQ_PORT", 8883))
    broker_user = os.getenv("HIVEMQ_USER")
    broker_pass = os.getenv("HIVEMQ_PASSWORD")

    meu_id_unico = f"Pokemon_Worker_{random.randint(1000, 9999)}"
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=meu_id_unico)
    
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(broker_user, broker_pass)
    client.on_connect = on_connect
    client.on_message = on_message

    print("🚀 Conectando à rede MQTT...")
    try:
        threading.Thread(target=iniciar_servidor_fake, daemon=True).start()
        
        client.connect(broker_url, broker_port, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Worker desligado manualmente.")

if __name__ == "__main__":
    iniciar_worker()