from pydantic import BaseModel
from Models.ProcesosModel import Salida

class Usuario(BaseModel):
    idUsuario:str
    nombre:str
    correo:str
    password:str
    estatus:bool
    rol:str

class UsuarioSalida(Salida):
    usuario:Usuario | None

class CambioPassword(BaseModel):
    passwordAnterior:str
    passwordNueva:str

class CambioCorreo(BaseModel):
    correo:str
    nuevoCorreo:str

class UsuariosSalida(Salida):
    usuarios:list[Usuario] | None

class UsuarioInsert(BaseModel):
    nombre: str
    correo: str
    password: str
    estatus:bool
    rol: str
