"""
Esquema de respuesta del historial unificado de un cliente
(GET /historial/{identificacion}).
"""
from datetime import datetime

from pydantic import BaseModel

from app.schemas.caso_schemas import CasoOut


class ClienteOut(BaseModel):
    id: str
    identificacion: str
    nombre: str
    creado_en: datetime


class HistorialClienteOut(BaseModel):
    cliente: ClienteOut
    casos: list[CasoOut]
