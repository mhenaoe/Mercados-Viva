"""
Capa MODELS - conexion a la base de datos.

Crea (una sola vez) el cliente de Supabase que usaran los demas
modulos de la capa de acceso a datos (caso_model, cliente_model,
agente_model). Ningun router ni service crea la conexion por su
cuenta: siempre pasan por aqui.
"""
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

_supabase: Client | None = None


def get_supabase() -> Client:
    """Devuelve el cliente de Supabase, creandolo la primera vez."""
    global _supabase
    if _supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "Faltan las variables SUPABASE_URL / SUPABASE_KEY. "
                "Definelas en el archivo .env (local) o en Render (produccion)."
            )
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase
