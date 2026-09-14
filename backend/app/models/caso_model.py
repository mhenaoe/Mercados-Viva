"""
Capa MODELS - acceso a datos de la tabla 'casos' (las PQR).

CRUD puro. Las reglas (que transiciones de estado son validas, etc.)
viven en casos_service, no aqui.
"""
from datetime import datetime, timezone

from app.models.db import get_supabase

TABLA = "casos"


def crear(cliente_id: str, tipo: str, descripcion: str, estado: str, canal_origen: str) -> dict:
    """Inserta un caso nuevo y devuelve la fila creada."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({
            "cliente_id": cliente_id,
            "tipo": tipo,
            "descripcion": descripcion,
            "estado": estado,
            "canal_origen": canal_origen,
        })
        .execute()
    )
    return resp.data[0]


def obtener_por_id(caso_id: str) -> dict | None:
    """Devuelve el caso con ese id, o None."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("id", caso_id)
        .limit(1)
        .execute()
    )
    filas = resp.data or []
    return filas[0] if filas else None


def listar_por_cliente(cliente_id: str) -> list[dict]:
    """Lista todos los casos de un cliente, ordenados por fecha de creacion."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("cliente_id", cliente_id)
        .order("creado_en", desc=False)
        .execute()
    )
    return resp.data or []


def actualizar_estado(caso_id: str, nuevo_estado: str) -> dict:
    """Actualiza el estado del caso y su fecha de actualizacion."""
    ahora = datetime.now(timezone.utc).isoformat()
    resp = (
        get_supabase()
        .table(TABLA)
        .update({"estado": nuevo_estado, "actualizado_en": ahora})
        .eq("id", caso_id)
        .execute()
    )
    return resp.data[0]
