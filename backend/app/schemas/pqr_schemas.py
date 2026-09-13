"""
Esquemas Pydantic para radicar una PQR (POST /pqr).

Toda validacion de entrada (tipo, canal, campos obligatorios) vive
aqui, no como validaciones manuales dentro del router.
"""
from typing import Literal

from pydantic import BaseModel, Field

TipoPQR = Literal["peticion", "queja", "reclamo", "sugerencia"]
CanalOrigen = Literal["web", "tienda_fisica"]


class PQRCrear(BaseModel):
    identificacion: str = Field(..., min_length=1, description="Documento o email del cliente")
    tipo: TipoPQR
    descripcion: str = Field(..., min_length=1)
    canal_origen: CanalOrigen
    responsable: str = Field(..., min_length=1, description="Quien radica: 'cliente' o el nombre del agente")
