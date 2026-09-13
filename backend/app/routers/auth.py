"""Router de autenticacion: POST /login."""
from fastapi import APIRouter

from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest):
    token = auth_service.login(datos.username, datos.password)
    return TokenResponse(access_token=token)
