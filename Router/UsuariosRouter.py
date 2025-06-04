from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from DAO.UsuariosDAO import UsuarioDAO
from Models.UsuariosModel import UsuarioSalida, UsuarioInsert, UsuariosSalida, CambioCorreo, CambioPassword
from Models.ProcesosModel import Salida

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

security = HTTPBasic()

def validarUsuario(request:Request,credenciales:HTTPBasicCredentials=Depends(security))->UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.autenticar(credenciales.username,credenciales.password)

@router.get('/login', response_model=UsuarioSalida)
async def login(request: Request, respuesta: UsuarioSalida = Depends(validarUsuario)) -> UsuarioSalida:
    return respuesta

@router.post('/', response_model=Salida)
async def crear_usuario(usuario: UsuarioInsert, request: Request) -> Salida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.agregar(usuario)

@router.get('/', response_model=UsuariosSalida)
async def consultar_usuarios(request: Request) -> UsuariosSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.consultarUsuarios()

@router.get('/{idUsuario}/', response_model=UsuarioSalida)
async def consultar_usuario_individual(idUsuario: str, request: Request) -> UsuarioSalida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.consultarUsuarioIndividual(idUsuario)

@router.put('/{idUsuario}/cambiarPassword', response_model=Salida)
async def cambiar_Password(idUsuario: str, cambioPassword: CambioPassword, request: Request) -> Salida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.cambiarPassword(idUsuario, cambioPassword)

@router.put('/{idUsuario}/cambiarCorreo', response_model=Salida)
async def cambiar_Correo(idUsuario: str, cambioCorreo: CambioCorreo, request: Request) -> Salida:
    usuarioDAO = UsuarioDAO(request.app.db)
    return usuarioDAO.cambiarCorreo(idUsuario, cambioCorreo)