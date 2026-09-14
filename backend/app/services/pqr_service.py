"""
Capa SERVICES - logica de negocio para radicar casos (PQR) y consultar
el historial unificado de un cliente.
"""
from app.exceptions import NoEncontradoError
from app.models import caso_model, cliente_model, historial_model
from app.schemas.pqr_schemas import PQRCrear
from app.services import evidencia_service

# El contrato de POST /pqr no incluye un campo "responsable": se deriva
# del canal por el que se radica (el cliente radica desde la web, el
# agente desde la tienda), que es el unico dato disponible en el body.
RESPONSABLE_POR_CANAL = {
    "web": "cliente",
    "tienda": "agente",
}


def crear_pqr(datos: PQRCrear) -> dict:
    """Busca (o crea) el cliente por identificacion, crea el caso en
    estado 'abierta' y registra el evento inicial en el historial."""
    cliente = cliente_model.obtener_por_identificacion(datos.identificacion)
    if cliente is None:
        cliente = cliente_model.crear(datos.identificacion, datos.nombre)

    caso = caso_model.crear(
        cliente_id=cliente["id"],
        tipo=datos.tipo,
        descripcion=datos.descripcion,
        estado="abierta",
        canal_origen=datos.canal_origen,
    )

    historial_model.crear(
        caso_id=caso["id"],
        estado_anterior=None,
        estado_nuevo="abierta",
        responsable=RESPONSABLE_POR_CANAL[datos.canal_origen],
        canal=datos.canal_origen,
    )

    caso["historial"] = historial_model.listar_por_caso(caso["id"])
    return caso


def obtener_historial(identificacion: str) -> dict:
    """Devuelve el cliente y la lista completa de sus casos -con su
    bitacora de trazabilidad-, sin importar el canal de origen."""
    cliente = cliente_model.obtener_por_identificacion(identificacion)
    if cliente is None:
        raise NoEncontradoError(
            f"No existe un cliente con identificacion '{identificacion}'."
        )

    casos = caso_model.listar_por_cliente(cliente["id"])
    for caso in casos:
        caso["historial"] = historial_model.listar_por_caso(caso["id"])
        caso["evidencias"] = evidencia_service.listar_para_caso(caso["id"])

    return {"cliente": cliente, "casos": casos}
