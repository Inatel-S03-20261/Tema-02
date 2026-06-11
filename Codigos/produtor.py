import os
import json
import ssl
import time
import requests
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

HOST = os.getenv("HIVEMQ_HOST", "").strip()
PORT = int(os.getenv("HIVEMQ_PORT", 8883))
USER = os.getenv("HIVEMQ_USER", "").strip()
PASSWORD = os.getenv("HIVEMQ_PASSWORD", "").strip()

TOPICO_JOGADOR = os.getenv("TOPICO_JOGADOR", "pokemon/jogadores/criado").strip()
TOPICO_TROCA = os.getenv("TOPICO_TROCA", "pokemon/trocas/solicitada").strip()

API_URL = "http://127.0.0.1:8000/api/v1"

def get_mqtt_client(client_id):
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(USER, PASSWORD)
    client.connect(HOST, PORT)
    return client


def simular_criacao_jogador(id_jogador: int):
    client = get_mqtt_client(f"Produtor_NovoJogador_{id_jogador}")
    client.loop_start()
    
    mensagem = json.dumps({"id_jogador": id_jogador})
    client.publish(TOPICO_JOGADOR, mensagem)
    print(f"📡 [Publicado] Novo jogador {id_jogador} no tópico {TOPICO_JOGADOR}")
    
    time.sleep(1) 
    client.disconnect()
    client.loop_stop()


def simular_troca(origem: int, destino: int, enviados: list, recebidos: list):
    client = get_mqtt_client("Produtor_Troca")
    client.loop_start() 
    
    mensagem = json.dumps({
        "idJogadorOrigem": origem,
        "idJogadorDestino": destino,
        "idsPokemonsEnviados": enviados,
        "idsPokemonsRecebidos": recebidos
    })
    client.publish(TOPICO_TROCA, mensagem)
    print(f"📡 [Publicado] Troca solicitada no tópico {TOPICO_TROCA}")
    
    time.sleep(1)
    client.disconnect()
    client.loop_stop()

def consultar_deck(id_jogador: int):
    print(f"🔍 [App Externa] Consultando inventário do jogador {id_jogador} via API...")
    try:
        response = requests.get(f"{API_URL}/{id_jogador}", timeout=5)
        if response.status_code == 200:
            cartas = response.json()
            print(f"🎒 Inventário do Jogador {id_jogador}: {cartas}")
        else:
            print(f"❌ Erro na API: Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Falha de conexão. O 'main.py' está rodando?")


# ==========================================
# ÁREA DE TESTES
# ==========================================
if __name__ == "__main__":
    print("Iniciando simulação de eventos...\n")
    
    # 1. Simular a criação
    simular_criacao_jogador(1)
    simular_criacao_jogador(2)
    
    # 2. Simular a consulta (Requer main.py rodando)
    # consultar_deck(89)
    # consultar_deck(78)
    
    # 3. Simular a troca
    # simular_troca(89, 78, [822, 286], [86, 22])