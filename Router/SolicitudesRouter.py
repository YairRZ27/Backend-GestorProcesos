from fastapi import APIRouter, Request
from DAO.SolicitudesDAO import SolicitudesDAO
from Models.SolicitudesModel import SolicitudInsert, SolicitudesSalida, SolicitudSalida, CambioEstado, AprobacionSolicitud
from Models.ProcesosModel import Salida

router = APIRouter(prefix='/solicitudes', tags=['solicitudes'])

@router.post('/', response_model=Salida)
async def crear_solicitud(solicitud: SolicitudInsert, request: Request) -> Salida:
    solicitudesDAO = SolicitudesDAO(request.app.db)
    return solicitudesDAO.crearSolicitud(solicitud)

@router.get('/', response_model=SolicitudesSalida)
async def consultar_solicitudes(request: Request) -> SolicitudesSalida:
    solicitudesDAO = SolicitudesDAO(request.app.db)
    solicitudesDAO.actualizarSolicitudesPendientes()
    return solicitudesDAO.consultarSolicitudes()

@router.get('/{idSolicitud}/', response_model=SolicitudSalida)
async def consultar_solicitud(idSolicitud: str, request: Request) -> SolicitudSalida:
    solicitudesDAO = SolicitudesDAO(request.app.db)
    return solicitudesDAO.consultarSolicitudIndividual(idSolicitud)

@router.put('/{idSolicitud}/', response_model=Salida)
async def cambiar_estado_solicitud(idSolicitud: str, cambio: CambioEstado, request: Request):
    solicitudesDAO = SolicitudesDAO(request.app.db)
    return solicitudesDAO.cambiarEstado(idSolicitud, cambio)

@router.delete('/{idSolicitud}/', response_model=Salida)
async def eliminar_solicitud(idSolicitud: str, request: Request):
    solicitudesDAO = SolicitudesDAO(request.app.db)
    return solicitudesDAO.eliminarSolicitud(idSolicitud)

@router.put('/{idSolicitud}/aprobar', response_model=Salida)
async def aprobar_solicitud(idSolicitud: str, aprobacion: AprobacionSolicitud, request: Request):
    solicitudesDAO = SolicitudesDAO(request.app.db)
    return solicitudesDAO.aprobarSolicitud(idSolicitud, aprobacion)

