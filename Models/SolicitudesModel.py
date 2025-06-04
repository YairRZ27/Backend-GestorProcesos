from pydantic import BaseModel
from datetime import datetime
from Models.ProcesosModel import Salida


class Solicitud(BaseModel):
    idSolicitud:str
    descripcion:str
    tipoArea:str
    responsableSeguimiento:str
    fechaCreacion:datetime
    fechaEstimacion:datetime
    estatus:str
    folio:str
    fechaAprobacion:str | None
    aprobadoPor: str | None

class SolicitudSalida(Salida):
    solicitud:Solicitud | None

class SolicitudInsert(BaseModel):
    descripcion:str
    tipoArea:str
    responsableSeguimiento:str
    fechaCreacion:datetime
    fechaEstimacion:datetime

class SolicitudesSalida(Salida):
    solicitudes: list[Solicitud] | None

class CambioEstado(BaseModel):
    nuevoEstado: str

class AprobacionSolicitud(BaseModel):
    aprobadoPor: str
    fechaAprobacion: datetime

