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
            "tipo": "peticion",
            "descripcion": "Solicito copia de la factura.",
            "canal_origen": "web",
            "responsable": "cliente",
        },
    ).json()

    token = _login(client)

    resp = client.patch(
        f"/casos/{creado['id']}",
        json={"estado": "en_proceso", "responsable": "agente1", "canal": "tienda_fisica"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    cuerpo = resp.json()
    assert cuerpo["estado"] == "en_proceso"
    assert len(cuerpo["historial"]) == 2
    assert cuerpo["historial"][-1]["estado_anterior"] == "abierta"
    assert cuerpo["historial"][-1]["estado_nuevo"] == "en_proceso"
