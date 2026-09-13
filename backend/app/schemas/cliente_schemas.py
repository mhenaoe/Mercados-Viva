"""
Esquema de respuesta del historial unificado de un cliente
(GET /historial/{identificacion}).
"""
from datetime import datetime

from pydantic import BaseModel

from app.schemas.caso_schemas import CasoOut


class ClienteOut(BaseModel):
    id: int
    identificacion: str
    fecha_registro: datetime


class HistorialClienteOut(BaseModel):
    cliente: ClienteOut
    casos: list[CasoOut]
