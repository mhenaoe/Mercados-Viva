"""Router de casos: PATCH /casos/{id}, protegido por JWT."""
from fastapi import APIRouter, Depends

from app.schemas.caso_schemas import CasoActualizar, CasoOut
from app.security import obtener_agente_actual
from app.services import casos_service

router = APIRouter(tags=["casos"])


@router.patch("/casos/{caso_id}", response_model=CasoOut)
def actualizar_estado(
    caso_id: int,
    datos: CasoActualizar,
    agente: str = Depends(obtener_agente_actual),
):
    return casos_service.actualizar_estado(
        caso_id=caso_id,
        nuevo_estado=datos.estado,
        responsable=datos.responsable,
        canal=datos.canal,
    )
