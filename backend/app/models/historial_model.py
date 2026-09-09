"""
Capa MODELS - acceso a datos de la tabla 'historial'.

Cada fila es un evento de trazabilidad de un caso: un cambio de estado
(o una respuesta) con su fecha, canal y responsable. Regla de negocio
del punto 1.4: toda actualizacion queda registrada aqui.
"""
from app.models.db import get_supabase

TABLA = "historial"


def crear(caso_id: int, estado_anterior: str | None, estado_nuevo: str,
          canal: str, responsable: str, respuesta: str | None = None) -> dict:
    """Registra un evento de trazabilidad para un caso."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({
            "caso_id": caso_id,
            "estado_anterior": estado_anterior,
            "estado_nuevo": estado_nuevo,
            "canal": canal,
            "responsable": responsable,
            "respuesta": respuesta,
        })
        .execute()
    )
    return resp.data[0]


def listar_por_caso(caso_id: int) -> list[dict]:
    """Lista los eventos de un caso en orden cronologico (mas antiguo primero)."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("caso_id", caso_id)
        .order("fecha", desc=False)
        .execute()
    )
    return resp.data or []
