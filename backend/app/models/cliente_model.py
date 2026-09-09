"""
Capa MODELS - acceso a datos de la tabla 'clientes'.

Un cliente es simplemente una identificacion unica (documento o email).
La decision de "buscar y si no existe crearlo" es logica de negocio y
vive en cliente_service; aqui solo se ofrecen las operaciones sueltas.
"""
from app.models.db import get_supabase

TABLA = "clientes"


def obtener_por_identificacion(identificacion: str) -> dict | None:
    """Devuelve la fila del cliente con esa identificacion, o None."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("identificacion", identificacion)
        .limit(1)
        .execute()
    )
    filas = resp.data or []
    return filas[0] if filas else None


def crear(identificacion: str) -> dict:
    """Inserta un cliente nuevo con su identificacion."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({"identificacion": identificacion})
        .execute()
    )
    return resp.data[0]
