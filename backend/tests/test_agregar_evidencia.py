"""Adjuntar evidencia (texto y/o archivos) a un caso ya radicado, y
confirmar que aparece en el historial unificado."""
import io


def _crear_caso(client, identificacion="ev-1"):
    return client.post(
        "/pqr",
        json={
            "identificacion": identificacion,
            "nombre": "Cliente Evidencia",
            "tipo": "queja",
            "descripcion": "El producto llego danado.",
            "canal_origen": "web",
        },
    ).json()


def test_agregar_evidencia_texto_y_archivo(client):
    creado = _crear_caso(client)

    resp = client.post(
        f"/casos/{creado['id']}/evidencias",
        data={"texto": "El sello del paquete venia roto."},
        files={"archivos": ("foto.png", io.BytesIO(b"contenido-de-prueba"), "image/png")},
    )

    assert resp.status_code == 201
    cuerpo = resp.json()
    assert len(cuerpo) == 2
    tipos = {e["tipo"] for e in cuerpo}
    assert tipos == {"texto", "archivo"}

    archivo = next(e for e in cuerpo if e["tipo"] == "archivo")
    assert archivo["archivo_nombre"] == "foto.png"
    assert archivo["archivo_url"] is not None

    historial = client.get("/historial/ev-1").json()
    assert len(historial["casos"][0]["evidencias"]) == 2


def test_agregar_evidencia_solo_texto(client):
    creado = _crear_caso(client, identificacion="ev-2")

    resp = client.post(
        f"/casos/{creado['id']}/evidencias",
        data={"texto": "Adjunto solo un comentario."},
    )

    assert resp.status_code == 201
    cuerpo = resp.json()
    assert len(cuerpo) == 1
    assert cuerpo[0]["tipo"] == "texto"


def test_agregar_evidencia_tipo_no_permitido_da_422(client):
    creado = _crear_caso(client, identificacion="ev-3")

    resp = client.post(
        f"/casos/{creado['id']}/evidencias",
        files={"archivos": ("virus.exe", io.BytesIO(b"x"), "application/octet-stream")},
    )

    assert resp.status_code == 422


def test_agregar_evidencia_caso_inexistente_da_404(client):
    resp = client.post(
        "/casos/00000000-0000-0000-0000-000000000000/evidencias",
        data={"texto": "no deberia guardarse"},
    )

    assert resp.status_code == 404
