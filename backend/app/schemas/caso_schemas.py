"""
Esquemas Pydantic de un caso (PQR) y de su actualizacion de estado
(PATCH /casos/{id}).
"""
from datetime import datetime

from pydantic import BaseModel, Field


class CasoActualizar(BaseModel):
    estado: str = Field(..., min_length=1, description="Nuevo estado solicitado para el caso")
    responsable: str = Field(..., min_length=1)
    canal: str = Field(..., min_length=1)


class EventoHistorial(BaseModel):
    id: int
    estado_anterior: str | None
    estado_nuevo: str
    canal: str
    responsable: str
    respuesta: str | None
    fecha: datetime


class CasoOut(BaseModel):
    id: int
    numero_caso: str
    tipo: str
    descripcion: str
    estado: str
    canal_origen: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    historial: list[EventoHistorial] = []
