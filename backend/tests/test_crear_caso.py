"""Prueba 1: crear un caso valido via POST /pqr."""


def test_crear_caso_valido(client):
    resp = client.post(
        "/pqr",
        json={
            "identificacion": "123456",
            "nombre": "Ana Ramirez",
            "tipo": "queja",
            "descripcion": "El producto llego danado.",
            "canal_origen": "web",
        },
    )

    assert resp.status_code == 201
    cuerpo = resp.json()
    assert cuerpo["estado"] == "abierta"
    assert "id" in cuerpo
