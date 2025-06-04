from fastapi import APIRouter, Request, HTTPException
from DAO.ProcesosDAO import ProcesosDAO
from Models.ProcesosModel import ProcesoInsert, ProcesosSalida, ProcesoSalida, Salida, CambioEstado

router = APIRouter(prefix='/procesos', tags=['procesos'])

@router.post('/', response_model=Salida)
async def crear_proceso(proceso: ProcesoInsert, request: Request) -> Salida:
    procesosDAO = ProcesosDAO(request.app.db)
    return procesosDAO.crearProceso(proceso)

@router.get('/', response_model=ProcesosSalida)
async def consultar_procesos(request: Request) -> ProcesosSalida:
    procesosDAO = ProcesosDAO(request.app.db)
    return procesosDAO.consultarProcesos()

@router.get('/prioridad/', response_model=ProcesosSalida)
async def consultar_procesos_por_prioridad(request: Request) -> ProcesosSalida:
    print('Entrando a consultar procesos por prioridad')
    procesosDAO = ProcesosDAO(request.app.db)
    return procesosDAO.consultarProcesosPorPrioridad()

@router.get('/{idProceso}/', response_model=ProcesoSalida)
async def consultar_proceso(idProceso: str, request: Request) -> ProcesoSalida:
    procesosDAO = ProcesosDAO(request.app.db)
    return procesosDAO.consultarProcesoIndividual(idProceso)

@router.put('/{idProceso}/', response_model=ProcesoSalida)
async def cambiar_estado(idProceso: str, cambio: CambioEstado, request: Request) -> ProcesoSalida:
    procesosDAO = ProcesosDAO(request.app.db)
    return procesosDAO.cambiarEstado(idProceso, cambio)

@router.delete('/{idProceso}/', response_model=ProcesoSalida)
async def eliminar_proceso(idProceso: str, request: Request) -> ProcesoSalida:
    procesosDAO = ProcesosDAO(request.app.db)
    return procesosDAO.eliminarProceso(idProceso)

