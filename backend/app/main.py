"""
Punto de entrada de la aplicacion.

Crea la app de FastAPI, registra los manejadores de error, incluye los
routers de la API y sirve el frontend estatico (HTML/CSS/JS vanilla)
desde el mismo servicio, sin necesidad de configurar CORS.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.exceptions import registrar_manejadores_de_error
from app.routers import auth, casos, evidencias, pqr

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

app = FastAPI(title="Mercado Viva - Gestion de PQR")

registrar_manejadores_de_error(app)

app.include_router(pqr.router)
app.include_router(casos.router)
app.include_router(auth.router)
app.include_router(evidencias.router)

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
