from pydantic import BaseModel
from datetime import datetime

class Salida(BaseModel):
    estatus:str
    mensaje:str

class Proceso(BaseModel):
    idProceso:str
    nombre:str
    descripcion:str
    idSolicitud:str
    fechaRegistro:datetime
    prioridad:str | None

class ProcesoSalida(Salida):
    proceso:Proceso | None

class ProcesosSalida(Salida):
    procesos: list[Proceso] | None

class ProcesoInsert(BaseModel):
    nombre: str
    descripcion: str
    idSolicitud: str
    fechaRegistro: datetime
    prioridad:str | None 

class CambioEstado(BaseModel):
    nuevoEstado: str

