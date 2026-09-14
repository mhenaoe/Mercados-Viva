"""
Capa MODELS - acceso a datos de la tabla 'historial_casos'.

Cada fila es un evento de trazabilidad de un caso: un cambio de estado
con su fecha, canal y responsable. Regla de negocio: toda actualizacion
de estado queda registrada aqui.
"""
from app.models.db import get_supabase

TABLA = "historial_casos"


def crear(caso_id: str, estado_anterior: str | None, estado_nuevo: str,
          responsable: str, canal: str) -> dict:
    """Registra un evento de trazabilidad para un caso."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({
            "caso_id": caso_id,
            "estado_anterior": estado_anterior,
            "estado_nuevo": estado_nuevo,
            "responsable": responsable,
            "canal": canal,
        })
        .execute()
    )
    return resp.data[0]


def listar_por_caso(caso_id: str) -> list[dict]:
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
