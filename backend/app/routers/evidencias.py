"""Router de evidencias: POST /casos/{caso_id}/evidencias."""
from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.evidencia_schemas import EvidenciaOut
from app.services import evidencia_service

router = APIRouter(tags=["evidencias"])


@router.post("/casos/{caso_id}/evidencias", response_model=list[EvidenciaOut], status_code=201)
async def agregar_evidencia(
    caso_id: str,
    texto: str | None = Form(None),
    archivos: list[UploadFile] = File(default=[]),
):
    return await evidencia_service.agregar_evidencia(caso_id, texto, archivos)
