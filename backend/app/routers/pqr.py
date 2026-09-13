"""Router de PQR: POST /pqr y GET /historial/{identificacion}."""
from fastapi import APIRouter

from app.schemas.caso_schemas import CasoOut
from app.schemas.cliente_schemas import HistorialClienteOut
from app.schemas.pqr_schemas import PQRCrear
from app.services import pqr_service

router = APIRouter(tags=["pqr"])


@router.post("/pqr", response_model=CasoOut, status_code=201)
def crear_pqr(datos: PQRCrear):
    return pqr_service.crear_pqr(datos)


@router.get("/historial/{identificacion}", response_model=HistorialClienteOut)
def obtener_historial(identificacion: str):
    return pqr_service.obtener_historial(identificacion)
