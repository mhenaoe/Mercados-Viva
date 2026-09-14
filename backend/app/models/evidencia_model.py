"""
Capa MODELS - acceso a datos de la tabla 'evidencias' y al bucket de
Supabase Storage donde se guardan los archivos adjuntos.
"""
from storage3.exceptions import StorageApiError

from app.models.db import get_supabase

TABLA = "evidencias"
BUCKET = "evidencias"

_bucket_listo = False


def asegurar_bucket() -> None:
    """Crea el bucket de Storage la primera vez que se necesita (privado)."""
    global _bucket_listo
    if _bucket_listo:
        return
    try:
        get_supabase().storage.create_bucket(BUCKET, options={"public": False})
    except StorageApiError as exc:
        if exc.status != 409:
            raise
    _bucket_listo = True


def subir_archivo(path: str, contenido: bytes, content_type: str) -> None:
    """Sube un archivo al bucket de evidencias."""
    asegurar_bucket()
    get_supabase().storage.from_(BUCKET).upload(path, contenido, {"content-type": content_type})


def generar_url_firmada(path: str, expira_segundos: int = 3600) -> str | None:
    """Genera una URL temporal para ver/descargar un archivo del bucket."""
    resp = get_supabase().storage.from_(BUCKET).create_signed_url(path, expira_segundos)
    return resp.get("signedURL") or resp.get("signedUrl")


def crear_texto(caso_id: str, contenido_texto: str) -> dict:
    """Registra una nota de texto como evidencia de un caso."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({"caso_id": caso_id, "tipo": "texto", "contenido_texto": contenido_texto})
        .execute()
    )
    return resp.data[0]


def crear_archivo(caso_id: str, archivo_path: str, archivo_nombre: str) -> dict:
    """Registra un archivo ya subido a Storage como evidencia de un caso."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({
            "caso_id": caso_id,
            "tipo": "archivo",
            "archivo_path": archivo_path,
            "archivo_nombre": archivo_nombre,
        })
        .execute()
    )
    return resp.data[0]


def listar_por_caso(caso_id: str) -> list[dict]:
    """Lista las evidencias de un caso en orden cronologico."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("caso_id", caso_id)
        .order("creado_en", desc=False)
        .execute()
    )
    return resp.data or []
