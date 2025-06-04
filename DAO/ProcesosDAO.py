from bson import ObjectId
from Models.ProcesosModel import ProcesoInsert, Salida, ProcesosSalida, ProcesoSalida, CambioEstado
from fastapi.encoders import jsonable_encoder

class ProcesosDAO:
    def __init__(self, db):
        self.db = db

    def consultarProcesoPorID(self, idProceso: str):
        respuesta = False
        try:
            proceso = self.db.ProcesosView.find_one({"idProceso": idProceso})
            if proceso:
                respuesta = True
        except Exception as e:
            print(e)
            respuesta = False
        return respuesta

    def crearProceso(self, proceso: ProcesoInsert):
        salida = Salida(estatus='', mensaje='')
        try:
            solicitud = self.db.SolicitudesView.find_one({"idSolicitud": proceso.idSolicitud})
            if not solicitud:
                salida.estatus = "ERROR"
                salida.mensaje = "No se puede crear el proceso porque el idSolicitud no existe."
                return salida
            proceso_dict = jsonable_encoder(proceso)
            proceso_dict["estatus"] = "Pendiente"
            self.db.Procesos.insert_one(proceso_dict)
            salida.estatus = "OK"
            salida.mensaje = "El proceso se ha registrado correctamente."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "El proceso no se ha podido crear, consulta al administrador."
        return salida

    def consultarProcesos(self):
        salida = ProcesosSalida(estatus='', mensaje='', procesos=[])
        try:
            procesos = list(self.db.ProcesosView.find())
    
            if procesos:
                salida.estatus = 'OK'
                salida.mensaje = 'Listado de procesos encontrado.'
                salida.procesos = procesos
            else:
                salida.estatus = 'OK'
                salida.mensaje = 'No hay procesos registrados.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los procesos, consulta al administrador."
        return salida

    def consultarProcesoIndividual(self, idProceso: str):
        salida = ProcesoSalida(estatus='', mensaje='', proceso=None)
        try:
            proceso = self.db.ProcesosView.find_one({"idProceso": idProceso})
            if proceso:
                salida.estatus = 'OK'
                salida.mensaje = 'Proceso encontrado correctamente.'
                salida.proceso = proceso
            else:
                salida.estatus = 'ERROR'
                salida.mensaje = 'No se encontró el proceso.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar el proceso, consulta al administrador."
        return salida

    def cambiarEstado(self, idProceso: str, cambio: CambioEstado):
        salida = ProcesoSalida(estatus='', mensaje='', proceso=None)
        try:
            resultado = self.db.Procesos.update_one(
                {'_id': ObjectId(idProceso)},
                {'$set': {'estatus': cambio.nuevoEstado}}
            )
            if resultado.matched_count == 1:
                proceso = self.db.ProcesosView.find_one({'idProceso': idProceso})
                salida.estatus = "OK"
                salida.mensaje = "Se cambió correctamente el estado del proceso."
                salida.proceso = proceso
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró un proceso con ese ID."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Se produjo un error al cambiar el estado del proceso."
        return salida

    def eliminarProceso(self, idProceso: str):
        salida = ProcesoSalida(estatus='', mensaje='', proceso=None)
        try:
            resultado = self.db.Procesos.delete_one({'_id': ObjectId(idProceso)})
            if resultado.deleted_count == 1:
                salida.estatus = "OK"
                salida.mensaje = "El proceso se eliminó correctamente."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró un proceso con ese ID."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al eliminar el proceso, consulta al administrador."
        return salida

    def consultarProcesosPorPrioridad(self):
        salida = ProcesosSalida(estatus='', mensaje='', procesos=[])
        try:
            prioridad_orden = {"Urgente": 1, "Cumplimiento": 2, "Auditoría": 3}
            procesos = list(self.db.ProcesosView.find())
            procesos.sort(key=lambda x: prioridad_orden.get(x.get("prioridad", "Cumplimiento"), 2))
            if procesos:
                salida.estatus = 'OK'
                salida.mensaje = 'Procesos ordenados por prioridad.'
                salida.procesos = procesos
            else:
                salida.estatus = 'OK'
                salida.mensaje = 'No hay procesos registrados.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los procesos por prioridad."
        return salida

