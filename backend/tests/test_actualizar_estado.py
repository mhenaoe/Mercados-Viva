"""Prueba 3: una transicion de estado valida actualiza el caso y queda
registrada en el historial."""


def _login(client):
    resp = client.post("/login", json={"username": "agente1", "password": "clave123"})
    return resp.json()["access_token"]


def test_transicion_valida(client):
    creado = client.post(
        "/pqr",
        json={
            "identificacion": "789",
            "nombre": "Carlos Diaz",
            "tipo": "peticion",
            "descripcion": "Solicito copia de la factura.",
            "canal_origen": "web",
        },
    ).json()

    token = _login(client)

    resp = client.patch(
        f"/casos/{creado['id']}",
        json={"estado_nuevo": "en_proceso", "responsable": "agente1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    cuerpo = resp.json()
    assert cuerpo["id"] == creado["id"]
    assert cuerpo["estado"] == "en_proceso"
    assert "actualizado_en" in cuerpo

    historial = client.get("/historial/789").json()
    eventos = historial["casos"][0]["historial"]
    assert len(eventos) == 2
    assert eventos[-1]["estado_anterior"] == "abierta"
    assert eventos[-1]["estado_nuevo"] == "en_proceso"
