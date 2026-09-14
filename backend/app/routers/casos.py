"""Router de casos: PATCH /casos/{id}, protegido por JWT."""
from fastapi import APIRouter, Depends

from app.schemas.caso_schemas import CasoActualizado, CasoActualizar
from app.security import obtener_agente_actual
from app.services import casos_service

router = APIRouter(tags=["casos"])


@router.patch("/casos/{caso_id}", response_model=CasoActualizado)
def actualizar_estado(
    caso_id: str,
    datos: CasoActualizar,
    agente: str = Depends(obtener_agente_actual),
):
    return casos_service.actualizar_estado(
        caso_id=caso_id,
        nuevo_estado=datos.estado_nuevo,
        responsable=datos.responsable,
    )
