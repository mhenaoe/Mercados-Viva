"""
Esquemas Pydantic de un caso (PQR) y de su actualizacion de estado
(PATCH /casos/{id}).
"""
from datetime import datetime

from pydantic import BaseModel, Field


class CasoActualizar(BaseModel):
    estado_nuevo: str = Field(..., min_length=1, description="Nuevo estado solicitado para el caso")
    responsable: str = Field(..., min_length=1)


class CasoActualizado(BaseModel):
    id: str
    estado: str
    actualizado_en: datetime


class EventoHistorial(BaseModel):
    id: str
    estado_anterior: str | None
    estado_nuevo: str
    responsable: str
    canal: str
    fecha: datetime


class CasoOut(BaseModel):
    id: str
    tipo: str
    descripcion: str
    estado: str
    canal_origen: str
    creado_en: datetime
    actualizado_en: datetime
    historial: list[EventoHistorial] = []
