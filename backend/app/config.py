"""
Configuracion central del backend.
Lee las variables de entorno necesarias para Supabase y para el JWT.
En local se pueden cargar desde un archivo .env (ver .env.example);
en Render se definen en el panel del servicio.
"""
import os

# Carga opcional de un archivo .env en desarrollo local.
# python-dotenv es solo una utilidad de arranque; no reemplaza
# ninguna de las tecnologias del stack (FastAPI, Supabase, JWT, bcrypt).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Supabase (base de datos) ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# --- JWT propio (autenticacion de agentes, RNF1) ---
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET no esta configurado. Definelo en el archivo .env (local) "
        "o en las variables de entorno de Render (produccion)."
    )
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", "120"))
