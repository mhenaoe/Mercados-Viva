"""
Capa de seguridad: hash/verificacion de contrasenas (bcrypt) y
creacion/validacion de tokens JWT propios (PyJWT), usados para
proteger las rutas del agente (RNF1).
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import JWT_ALGORITHM, JWT_EXP_MINUTES, JWT_SECRET

_bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Devuelve el hash bcrypt de una contrasena en texto plano."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    """Compara una contrasena en texto plano contra su hash bcrypt."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def crear_token(username: str) -> str:
    """Genera un JWT firmado que identifica al agente autenticado."""
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=JWT_EXP_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decodificar_token(token: str) -> dict:
    """Valida un JWT y devuelve su payload. Lanza jwt.PyJWTError si es invalido."""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def obtener_agente_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> str:
    """Dependencia de FastAPI: valida el JWT del header Authorization y
    devuelve el username del agente autenticado."""
    if credenciales is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el token de autenticacion.",
        )
    try:
        payload = decodificar_token(credenciales.credentials)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado.",
        )
    return payload["sub"]
