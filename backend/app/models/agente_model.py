"""
Capa MODELS - acceso a datos de la tabla 'agentes'.

Solo operaciones de persistencia. La verificacion de la contrasena
(bcrypt) y la generacion del token (JWT) NO ocurren aqui: eso es
logica de negocio y vive en la capa services (auth_service).
"""
from app.models.db import get_supabase

TABLA = "agentes"


def obtener_por_username(username: str) -> dict | None:
    """Devuelve la fila del agente con ese username, o None si no existe."""
    resp = (
        get_supabase()
        .table(TABLA)
        .select("*")
        .eq("username", username)
        .limit(1)
        .execute()
    )
    filas = resp.data or []
    return filas[0] if filas else None


def crear(username: str, password_hash: str, nombre: str) -> dict:
    """Inserta un agente nuevo. Recibe el hash bcrypt ya calculado."""
    resp = (
        get_supabase()
        .table(TABLA)
        .insert({
            "username": username,
            "password_hash": password_hash,
            "nombre": nombre,
        })
        .execute()
    )
    return resp.data[0]
