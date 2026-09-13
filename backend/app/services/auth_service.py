"""Capa SERVICES - autenticacion del agente (POST /login)."""
from app.exceptions import CredencialesInvalidasError
from app.models import agente_model
from app.security import crear_token, verificar_password


def login(username: str, password: str) -> str:
    """Verifica las credenciales del agente y devuelve un access_token JWT."""
    agente = agente_model.obtener_por_username(username)
    if agente is None or not verificar_password(password, agente["password_hash"]):
        raise CredencialesInvalidasError()

    return crear_token(agente["username"])
