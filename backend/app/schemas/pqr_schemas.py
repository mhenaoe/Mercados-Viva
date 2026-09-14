"""
Esquemas Pydantic para radicar una PQR (POST /pqr).

Toda validacion de entrada (tipo, canal, campos obligatorios) vive
aqui, no como validaciones manuales dentro del router.
"""
from typing import Literal

from pydantic import BaseModel, Field

TipoPQR = Literal["peticion", "queja", "reclamo", "sugerencia"]
CanalOrigen = Literal["web", "tienda"]


class PQRCrear(BaseModel):
    identificacion: str = Field(..., min_length=1, description="Documento o email del cliente")
    nombre: str = Field(..., min_length=1)
    tipo: TipoPQR
    descripcion: str = Field(..., min_length=1)
    canal_origen: CanalOrigen


class PQRCreada(BaseModel):
    id: str
    estado: str
