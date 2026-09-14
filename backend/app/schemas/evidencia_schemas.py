"""Esquema Pydantic de una evidencia (texto o archivo) de un caso."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class EvidenciaOut(BaseModel):
    id: str
    tipo: Literal["texto", "archivo"]
    contenido_texto: str | None
    archivo_nombre: str | None
    archivo_url: str | None
    creado_en: datetime
