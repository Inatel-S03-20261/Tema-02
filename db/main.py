import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from DeckService.repository import CartasRepository
from DeckService.services import CartasService
from DeckService.controllers.api import router as deck_router, CartasApiController

from produtor import criar_jogador, simular_troca

cartas_repo = CartasRepository()
deck_service = CartasService(cartas_repo)
deck_api_controller = CartasApiController(deck_service)


app = FastAPI(title="Sistema de Distribuição de Cartas - Tema 02")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deck_router, prefix="/cartas", tags=["Inventário"])

class NovoJogadorPayload(BaseModel):
    id_jogador: int

class TrocaPayload(BaseModel):
    idJogadorOrigem: int
    idJogadorDestino: int
    idsPokemonsEnviados: List[int]
    idsPokemonsRecebidos: List[int]

@app.post("/jogador", tags=["Eventos MQTT"])
def endpoint_criar_jogador(payload: NovoJogadorPayload):
    criar_jogador(payload.id_jogador)
    return {"status": "success", "message": f"Evento de criação do jogador {payload.id_jogador} enviado ao broker!"}

@app.post("/trocas", tags=["Eventos MQTT"])
def endpoint_solicitar_troca(payload: TrocaPayload):
    simular_troca(
        origem=payload.idJogadorOrigem,
        destino=payload.idJogadorDestino,
        enviados=payload.idsPokemonsEnviados,
        recebidos=payload.idsPokemonsRecebidos
    )
    return {"status": "success", "message": "Evento de troca enviado ao broker para validação!"}

@app.get("/", response_class=FileResponse, tags=["Frontend"])
def renderizar_pokedex():
    return FileResponse("index.html")

if __name__ == "__main__":
    print("🚀 Iniciando API Gateway e Pokédex na porta 8000...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)