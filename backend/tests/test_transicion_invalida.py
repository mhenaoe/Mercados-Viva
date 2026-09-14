"""Caso excepcional: una transicion de estado no permitida por el ciclo
de PQR responde 400 con el estado actual y los estados validos."""


def _login(client):
    resp = client.post("/login", json={"username": "agente1", "password": "clave123"})
    return resp.json()["access_token"]


def test_transicion_invalida_responde_400(client):
    creado = client.post(
        "/pqr",
        json={
            "identificacion": "555",
            "nombre": "Marta Lopez",
            "tipo": "sugerencia",
            "descripcion": "Ampliar horario de atencion.",
            "canal_origen": "web",
        },
    ).json()

    token = _login(client)

    resp = client.patch(
        f"/casos/{creado['id']}",
        json={"estado_nuevo": "resuelta_cerrada", "responsable": "agente1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 400
    cuerpo = resp.json()
    assert cuerpo["estado_actual"] == "abierta"
    assert "resuelta_cerrada" not in cuerpo["estados_validos_siguientes"]
