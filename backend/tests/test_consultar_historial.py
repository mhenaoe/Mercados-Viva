"""Prueba 2: el caso creado aparece en el historial unificado del cliente."""


def test_caso_aparece_en_historial(client):
    client.post(
        "/pqr",
        json={
            "identificacion": "123456",
            "nombre": "Ana Ramirez",
            "tipo": "reclamo",
            "descripcion": "Cobro duplicado en la factura.",
            "canal_origen": "tienda",
        },
    )

    resp = client.get("/historial/123456")

    assert resp.status_code == 200
    cuerpo = resp.json()
    assert cuerpo["cliente"]["identificacion"] == "123456"
    assert cuerpo["cliente"]["nombre"] == "Ana Ramirez"
    assert len(cuerpo["casos"]) == 1
    assert cuerpo["casos"][0]["tipo"] == "reclamo"
    assert len(cuerpo["casos"][0]["historial"]) == 1
