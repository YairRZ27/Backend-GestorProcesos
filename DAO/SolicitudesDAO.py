from bson import ObjectId
from Models.SolicitudesModel import SolicitudInsert, Salida, SolicitudesSalida, SolicitudSalida, CambioEstado, AprobacionSolicitud
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta



class SolicitudesDAO:
    def __init__(self, db):
        self.db = db

    def consultarSolicitudPorID(self, idSolicitud: str):
        respuesta = False
        try:
            solicitud = self.db.SolicitudesView.find_one({"idSolicitud": idSolicitud})
            if solicitud:
                respuesta = True
        except Exception as e:
            print(e)
            respuesta = False
        return respuesta

    def crearSolicitud(self, solicitud: SolicitudInsert):
        salida = Salida(estatus='', mensaje='')
        try:
            # Obtener el siguiente número de folio
            ultima = self.db.Solicitudes.find_one(
                {"folio": {"$regex": "^CCADPRC-\\d{4}$"}},
                sort=[("folio", -1)]
            )
            if ultima and "folio" in ultima:
                ultimo_num = int(ultima["folio"].split("-")[1])
                nuevo_num = ultimo_num + 1
            else:
                nuevo_num = 0
            folio = f"CCADPRC-{nuevo_num:04d}"

            solicitud_dict = jsonable_encoder(solicitud)
            solicitud_dict["estatus"] = "Pendiente"
            solicitud_dict["folio"] = folio

            self.db.Solicitudes.insert_one(solicitud_dict)
            salida.estatus = "OK"
            salida.mensaje = f"La solicitud se ha registrado correctamente con folio {folio}."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "La solicitud no se ha podido crear, consulta al administrador."
        return salida

    def consultarSolicitudes(self):
        salida = SolicitudesSalida(estatus='', mensaje='', solicitudes=[])
        try:
            solicitudes = list(self.db.SolicitudesView.find())
            salida.estatus = 'OK'
            if solicitudes:
                salida.mensaje = 'Listado de solicitudes encontrado.'
                salida.solicitudes = solicitudes
            else:
                salida.mensaje = 'No hay solicitudes registradas.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar las solicitudes, consulta al administrador."
        return salida

    def consultarSolicitudIndividual(self, idSolicitud: str):
        salida = SolicitudSalida(estatus='', mensaje='', solicitud=None)
        try:
            solicitud = self.db.SolicitudesView.find_one({"idSolicitud": idSolicitud})
            if solicitud:
                salida.estatus = 'OK'
                salida.mensaje = 'Solicitud encontrada correctamente.'
                salida.solicitud = solicitud
            else:
                salida.estatus = 'ERROR'
                salida.mensaje = 'No se encontró la solicitud.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar la solicitud, consulta al administrador."
        return salida

    def cambiarEstado(self, idSolicitud: str, cambio: CambioEstado):
        salida = Salida(estatus='', mensaje='')
        try:
            if self.consultarSolicitudPorID(idSolicitud):
                if cambio.nuevoEstado == "Finalizada":
                    solicitud = self.db.Solicitudes.find_one({'_id': ObjectId(idSolicitud)})
                    if (not solicitud or not solicitud.get('fechaAprobacion') or not solicitud.get('aprobadoPor')):
                        salida.estatus = 'ERROR'
                        salida.mensaje = 'No se puede finalizar la solicitud porque no ha sido aprobada formalmente por un director, gerente o coordinador.'
                        return salida
                self.db.Solicitudes.update_one({'_id': ObjectId(idSolicitud)}, {'$set': {'estatus': cambio.nuevoEstado}})
                salida.estatus = 'OK'
                salida.mensaje = "Se cambió correctamente el estado de la solicitud."
            else:
                salida.estatus = 'ERROR'
                salida.mensaje = 'No se encontró una solicitud registrada con ese ID.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Se produjo un error al cambiar el estado de la solicitud."
        return salida

    def eliminarSolicitud(self, idSolicitud: str):
        salida = Salida(estatus='', mensaje='')
        try:
            resultado = self.db.Solicitudes.delete_one({'_id': ObjectId(idSolicitud)})
            if resultado.deleted_count == 1:
                salida.estatus = "OK"
                salida.mensaje = "La solicitud se eliminó correctamente."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró una solicitud con ese ID."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al eliminar la solicitud, consulta al administrador."
        return salida

    def aprobarSolicitud(self, idSolicitud: str, aprobacion: AprobacionSolicitud):
        salida = Salida(estatus='', mensaje='')
        try:
            if self.consultarSolicitudPorID(idSolicitud):
                resultado = self.db.Solicitudes.update_one(
                    {'_id': ObjectId(idSolicitud)},
                    {'$set': {
                        'aprobadoPor': aprobacion.aprobadoPor,
                        'fechaAprobacion': aprobacion.fechaAprobacion
                    }}
                )
                if resultado.matched_count == 1:
                    salida.estatus = 'OK'
                    salida.mensaje = 'Solicitud aprobada correctamente.'
                else:
                    salida.estatus = 'ERROR'
                    salida.mensaje = 'No se encontró una solicitud con ese ID.'
            else:
                salida.estatus = 'ERROR'
                salida.mensaje = 'No se encontró una solicitud registrada con ese ID.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Se produjo un error al aprobar la solicitud."
        return salida
    
    def es_habil(self,fecha):
        # Lunes=0, Domingo=6
        return fecha.weekday() < 5
    
    def sumar_dias_habiles(self,fecha, dias):
        contador = 0
        resultado = fecha
        while contador < dias:
            resultado += timedelta(days=1)
            if self.es_habil(resultado):
                contador += 1
        return resultado
    
    def actualizarSolicitudesPendientes(self):
        try:
            hoy = datetime.now()
            solicitudes = list(self.db.Solicitudes.find({"estatus": {"$nin": ["Pendiente Evaluación", "Finalizada"]}}))
            for solicitud in solicitudes:
                if solicitud.get("fechaCreacion"):
                    fecha_creacion = solicitud["fechaCreacion"]
                    if isinstance(fecha_creacion, str):
                        try:
                            fecha_creacion = datetime.fromisoformat(fecha_creacion)
                        except Exception:
                            continue
                    if fecha_creacion.tzinfo is not None:
                        fecha_creacion = fecha_creacion.replace(tzinfo=None)
                    if hoy.tzinfo is not None:
                        hoy_naive = hoy.replace(tzinfo=None)
                    else:
                        hoy_naive = hoy
                    limite = self.sumar_dias_habiles(fecha_creacion, 3)
                    if hoy_naive > limite:
                        self.db.Solicitudes.update_one(
                            {"_id": solicitud["_id"]},
                            {"$set": {"estatus": "Pendiente Evaluación"}}
                        )
                        print(f"Solicitud {solicitud.get('idSolicitud', solicitud.get('_id'))} actualizada a 'Pendiente Evaluación'")
        except Exception as e:
            print(f"Error al actualizar solicitudes pendientes: {e}")
            return Salida(estatus="ERROR", mensaje="Error al actualizar solicitudes pendientes.")