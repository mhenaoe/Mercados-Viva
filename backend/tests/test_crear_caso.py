"""Prueba 1: crear un caso valido via POST /pqr."""


def test_crear_caso_valido(client):
    resp = client.post(
        "/pqr",
        json={
            "identificacion": "123456",
            "tipo": "queja",
            "descripcion": "El producto llego danado.",
            "canal_origen": "web",
            "responsable": "cliente",
        },
    )

    assert resp.status_code == 201
    cuerpo = resp.json()
    assert cuerpo["numero_caso"] == "PQR-00001"
    assert cuerpo["estado"] == "abierta"
    assert cuerpo["tipo"] == "queja"
