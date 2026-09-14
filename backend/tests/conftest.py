"""
Fixtures compartidas para las pruebas del backend.

Las pruebas no llaman a Supabase real: sustituyen las funciones de la
capa models (caso_model, cliente_model, historial_model, agente_model)
por una base de datos en memoria, para poder probar routers y services
de forma aislada y repetible.
"""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import agente_model, caso_model, cliente_model, historial_model
from app.security import hash_password


class _BaseDatosMemoria:
    def __init__(self):
        self.clientes: list[dict] = []
        self.casos: list[dict] = []
        self.historial: list[dict] = []
        self.agentes: list[dict] = []


@pytest.fixture
def client(monkeypatch):
    db = _BaseDatosMemoria()

    def cliente_obtener_por_identificacion(identificacion):
        return next((c for c in db.clientes if c["identificacion"] == identificacion), None)

    def cliente_crear(identificacion, nombre):
        fila = {
            "id": str(uuid.uuid4()),
            "identificacion": identificacion,
            "nombre": nombre,
            "creado_en": "2026-01-01T00:00:00Z",
        }
        db.clientes.append(fila)
        return fila

    def caso_crear(cliente_id, tipo, descripcion, estado, canal_origen):
        fila = {
            "id": str(uuid.uuid4()),
            "cliente_id": cliente_id,
            "tipo": tipo,
            "descripcion": descripcion,
            "estado": estado,
            "canal_origen": canal_origen,
            "creado_en": "2026-01-01T00:00:00Z",
            "actualizado_en": "2026-01-01T00:00:00Z",
        }
        db.casos.append(fila)
        return fila

    def caso_obtener_por_id(caso_id):
        return next((c for c in db.casos if c["id"] == caso_id), None)

    def caso_listar_por_cliente(cliente_id):
        return [c for c in db.casos if c["cliente_id"] == cliente_id]

    def caso_actualizar_estado(caso_id, nuevo_estado):
        caso = caso_obtener_por_id(caso_id)
        caso["estado"] = nuevo_estado
        caso["actualizado_en"] = "2026-01-02T00:00:00Z"
        return dict(caso)

    def historial_crear(caso_id, estado_anterior, estado_nuevo, responsable, canal):
        fila = {
            "id": str(uuid.uuid4()),
            "caso_id": caso_id,
            "estado_anterior": estado_anterior,
            "estado_nuevo": estado_nuevo,
            "responsable": responsable,
            "canal": canal,
            "fecha": "2026-01-01T00:00:00Z",
        }
        db.historial.append(fila)
        return fila

    def historial_listar_por_caso(caso_id):
        return [h for h in db.historial if h["caso_id"] == caso_id]

    def agente_obtener_por_username(username):
        return next((a for a in db.agentes if a["username"] == username), None)

    monkeypatch.setattr(cliente_model, "obtener_por_identificacion", cliente_obtener_por_identificacion)
    monkeypatch.setattr(cliente_model, "crear", cliente_crear)
    monkeypatch.setattr(caso_model, "crear", caso_crear)
    monkeypatch.setattr(caso_model, "obtener_por_id", caso_obtener_por_id)
    monkeypatch.setattr(caso_model, "listar_por_cliente", caso_listar_por_cliente)
    monkeypatch.setattr(caso_model, "actualizar_estado", caso_actualizar_estado)
    monkeypatch.setattr(historial_model, "crear", historial_crear)
    monkeypatch.setattr(historial_model, "listar_por_caso", historial_listar_por_caso)
    monkeypatch.setattr(agente_model, "obtener_por_username", agente_obtener_por_username)

    db.agentes.append(
        {
            "id": str(uuid.uuid4()),
            "username": "agente1",
            "password_hash": hash_password("clave123"),
            "nombre": "Agente de Prueba",
        }
    )

    return TestClient(app)
