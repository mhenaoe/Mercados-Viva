"""
Capa SERVICES - ciclo de estados de un caso (PQR).

Aqui vive la unica fuente de verdad sobre que transiciones de estado
son validas. Ni el router ni el modelo deciden esto.
"""
from app.exceptions import NoEncontradoError, TransicionInvalidaError
from app.models import caso_model, historial_model

TRANSICIONES_VALIDAS: dict[str, list[str]] = {
    "abierta": ["en_proceso", "escalada", "cerrada_sin_respuesta"],
    "en_proceso": ["pendiente_info", "escalada", "resuelta_cerrada", "cerrada_sin_acuerdo"],
    "pendiente_info": ["en_proceso", "cerrada_sin_respuesta"],
    "escalada": ["en_proceso", "resuelta_cerrada", "cerrada_sin_acuerdo"],
    "reabierta": ["en_proceso", "escalada"],
    "resuelta_cerrada": ["reabierta"],
    "cerrada_sin_respuesta": ["reabierta"],
    "cerrada_sin_acuerdo": ["reabierta"],
}


def actualizar_estado(caso_id: int, nuevo_estado: str, responsable: str, canal: str) -> dict:
    """Valida la transicion de estado de un caso y, si es valida, actualiza
    el caso y deja constancia del cambio en el historial."""
    caso = caso_model.obtener_por_id(caso_id)
    if caso is None:
        raise NoEncontradoError(f"No existe un caso con id {caso_id}.")

    estado_actual = caso["estado"]
    siguientes_validos = TRANSICIONES_VALIDAS.get(estado_actual, [])

    if nuevo_estado not in siguientes_validos:
        raise TransicionInvalidaError(estado_actual, siguientes_validos)

    caso_actualizado = caso_model.actualizar_estado(caso_id, nuevo_estado)

    historial_model.crear(
        caso_id=caso_id,
        estado_anterior=estado_actual,
        estado_nuevo=nuevo_estado,
        canal=canal,
        responsable=responsable,
    )

    caso_actualizado["historial"] = historial_model.listar_por_caso(caso_id)
    return caso_actualizado
