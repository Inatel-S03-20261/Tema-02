from fastapi import APIRouter, HTTPException
from typing import List
from ..interface import InterfaceCartasService

router = APIRouter()

class CartasApiController:
    def __init__(self, service: InterfaceCartasService):
        self.service = service
        self._setup_routes()

    def _setup_routes(self):
        @router.get("/{id_jogador}", response_model=List[int])
        def consultar_cartas(id_jogador: int) -> List[int]:
            try:
                cartas = self.service.consultarCartas(id_jogador)
                return cartas
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))