"""
Manejo centralizado de errores de la API.

Cada excepcion de negocio se traduce a un unico codigo HTTP y formato
de respuesta, para que routers y services no construyan HTTPException
a mano en cada punto.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class NoEncontradoError(Exception):
    """El recurso solicitado no existe (-> 404)."""


class TransicionInvalidaError(Exception):
    """El cambio de estado solicitado no esta permitido por el ciclo de PQR (-> 400)."""

    def __init__(self, estado_actual: str, estados_validos: list[str]):
        self.estado_actual = estado_actual
        self.estados_validos = estados_validos
        super().__init__(
            f"No se puede pasar del estado '{estado_actual}' al estado solicitado."
        )


class CredencialesInvalidasError(Exception):
    """Usuario o contrasena incorrectos (-> 401)."""


class EvidenciaInvalidaError(Exception):
    """El archivo adjunto no cumple el tipo o tamano permitido (-> 422)."""


def registrar_manejadores_de_error(app: FastAPI) -> None:
    """Registra los exception handlers de negocio sobre la app de FastAPI."""

    @app.exception_handler(NoEncontradoError)
    async def _no_encontrado(request: Request, exc: NoEncontradoError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(TransicionInvalidaError)
    async def _transicion_invalida(request: Request, exc: TransicionInvalidaError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": (
                    f"Transicion invalida desde el estado '{exc.estado_actual}'."
                ),
                "estado_actual": exc.estado_actual,
                "estados_validos_siguientes": exc.estados_validos,
            },
        )

    @app.exception_handler(CredencialesInvalidasError)
    async def _credenciales_invalidas(request: Request, exc: CredencialesInvalidasError):
        return JSONResponse(
            status_code=401,
            content={"detail": "Usuario o contrasena incorrectos."},
        )

    @app.exception_handler(EvidenciaInvalidaError)
    async def _evidencia_invalida(request: Request, exc: EvidenciaInvalidaError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})
