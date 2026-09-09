"""
Capa MODELS - acceso a datos de la tabla 'casos' (las PQR).

CRUD puro. Las reglas (que transiciones de estado son validas, como se
arma el numero de caso, etc.) viven en caso_service, no aqui.
"""
from datetime import datetime, timezone
from app.models.db import get_supabase

TABLA = "casos"


def crear(cliente_id: int, numero_caso: str, tipo: str,
          descripcion: str, estado: str, canal_origen: str) -> dict:
    """Inserta un caso nuevo y devuelve la fila creada."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({
            "cliente_id": cliente_id,
            "numero_caso": numero_caso,
            "tipo": tipo,
            "descripcion": descripcion,
            "estado": estado,
            "canal_origen": canal_origen,
        })
        .execute()
    )
    return resp.data[0]


def obtener_por_id(caso_id: int) -> dict | None:
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


def obtener_por_numero(numero_caso: str) -> dict | None:
    """Devuelve el caso con ese numero_caso, o None."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("numero_caso", numero_caso)
        .limit(1)
        .execute()
    )
    filas = resp.data or []
    return filas[0] if filas else None


def listar_por_cliente(cliente_id: int) -> list[dict]:
    """Lista todos los casos de un cliente, ordenados por fecha de creacion."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("cliente_id", cliente_id)
        .order("fecha_creacion", desc=False)
        .execute()
    )
    return resp.data or []


def actualizar_estado(caso_id: int, nuevo_estado: str) -> dict:
    """Actualiza el estado del caso y su fecha de actualizacion."""
    ahora = datetime.now(timezone.utc).isoformat()
    resp = (
        get_supabase()
        .table(TABLA)
        .update({"estado": nuevo_estado, "fecha_actualizacion": ahora})
        .eq("id", caso_id)
        .execute()
    )
    return resp.data[0]


def contar() -> int:
    """Cuenta cuantos casos existen (se usa para generar el numero de caso)."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("id", count="exact")
        .execute()
    )
    return resp.count or 0
