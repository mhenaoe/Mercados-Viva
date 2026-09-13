"""
Capa SERVICES - logica de negocio para radicar casos (PQR) y consultar
el historial unificado de un cliente.
"""
from app.exceptions import NoEncontradoError
from app.models import caso_model, cliente_model, historial_model
from app.schemas.pqr_schemas import PQRCrear


def _generar_numero_caso() -> str:
    """Genera un numero_caso correlativo tipo PQR-00001."""
    consecutivo = caso_model.contar() + 1
    return f"PQR-{consecutivo:05d}"


def crear_pqr(datos: PQRCrear) -> dict:
    """Busca (o crea) el cliente por identificacion, crea el caso en
    estado 'abierta' y registra el evento inicial en el historial."""
    cliente = cliente_model.obtener_por_identificacion(datos.identificacion)
    if cliente is None:
        cliente = cliente_model.crear(datos.identificacion)

    caso = caso_model.crear(
        cliente_id=cliente["id"],
        numero_caso=_generar_numero_caso(),
        tipo=datos.tipo,
        descripcion=datos.descripcion,
        estado="abierta",
        canal_origen=datos.canal_origen,
    )

    historial_model.crear(
        caso_id=caso["id"],
        estado_anterior=None,
        estado_nuevo="abierta",
        canal=datos.canal_origen,
        responsable=datos.responsable,
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

    return {"cliente": cliente, "casos": casos}
