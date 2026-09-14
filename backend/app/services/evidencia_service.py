"""
Capa SERVICES - logica de negocio para adjuntar evidencia (texto y/o
archivos) a un caso ya radicado.
"""
import uuid

from fastapi import UploadFile

from app.exceptions import EvidenciaInvalidaError, NoEncontradoError
from app.models import caso_model, evidencia_model

TIPOS_PERMITIDOS = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
    "application/pdf": "pdf",
}
TAMANO_MAXIMO_BYTES = 5 * 1024 * 1024  # 5 MB por archivo


def _con_url(evidencia: dict) -> dict:
    """Agrega la URL firmada (temporal) si la evidencia es un archivo."""
    if evidencia["tipo"] == "archivo" and evidencia.get("archivo_path"):
        evidencia["archivo_url"] = evidencia_model.generar_url_firmada(evidencia["archivo_path"])
    else:
        evidencia["archivo_url"] = None
    return evidencia


def listar_para_caso(caso_id: str) -> list[dict]:
    """Lista las evidencias de un caso, con URL firmada para las que son archivo."""
    return [_con_url(e) for e in evidencia_model.listar_por_caso(caso_id)]


async def agregar_evidencia(caso_id: str, texto: str | None, archivos: list[UploadFile]) -> list[dict]:
    """Adjunta una nota de texto y/o uno o mas archivos como evidencia de
    un caso ya radicado. Valida el tipo y el tamano de cada archivo."""
    caso = caso_model.obtener_por_id(caso_id)
    if caso is None:
        raise NoEncontradoError(f"No existe un caso con id {caso_id}.")

    if texto:
        evidencia_model.crear_texto(caso_id, texto)

    for archivo in archivos:
        if not archivo.filename:
            continue

        content_type = archivo.content_type or ""
        if content_type not in TIPOS_PERMITIDOS:
            raise EvidenciaInvalidaError(
                f"Tipo de archivo no permitido para '{archivo.filename}': '{content_type}'. "
                f"Se aceptan: {', '.join(sorted(TIPOS_PERMITIDOS))}."
            )

        contenido = await archivo.read()
        if len(contenido) > TAMANO_MAXIMO_BYTES:
            raise EvidenciaInvalidaError(
                f"El archivo '{archivo.filename}' supera el tamano maximo permitido (5 MB)."
            )

        extension = TIPOS_PERMITIDOS[content_type]
        path = f"casos/{caso_id}/{uuid.uuid4()}.{extension}"
        evidencia_model.subir_archivo(path, contenido, content_type)
        evidencia_model.crear_archivo(caso_id, path, archivo.filename)

    return listar_para_caso(caso_id)
