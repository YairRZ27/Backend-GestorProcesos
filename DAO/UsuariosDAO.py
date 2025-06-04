from bson import ObjectId
from Models.UsuariosModel import UsuarioInsert, Salida, UsuariosSalida, CambioPassword, CambioCorreo, \
    UsuarioSalida
from fastapi.encoders import jsonable_encoder

class UsuarioDAO:
    def __init__(self,db):
        self.db = db

    def consultarUsuarioPorID(self,idUsuario:str):
        respuesta = False
        try:
            Usuario = self.db.UsuariosView.find_one({"idUsuario":idUsuario})
            if Usuario:
                respuesta=True
        except Exception as e:
            print(e)
            respuesta = False
        return respuesta

    def consultarUsuarioPorCorreo(self,correo:str):
        respuesta = False
        try:
            Usuario = self.db.UsuariosView.find_one({"correo":correo})
            if Usuario:
                respuesta=True
        except Exception as e:
            print(e)
            respuesta = False
        return respuesta


    def agregar(self, Usuario: UsuarioInsert):
        salida = Salida(estatus='', mensaje='')
        try:
            if self.consultarUsuarioPorCorreo(Usuario.correo):
                salida.estatus = "OK"
                salida.mensaje = "No se puede crear el Usuario, porque ya existe un Usuario con ese correo."
            else:
                Usuario_dict = jsonable_encoder(Usuario)
                Usuario_dict["estatus"] = "Activo"
                result = self.db.Usuarios.insert_one(Usuario_dict)
                salida.estatus = "OK"
                salida.mensaje = "El Usuario se ha registrado correctamente."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "El Usuario no se ha podido crear, consulta al administrador."
        return salida

    def consultarUsuarios(self):
        salida = UsuariosSalida(estatus='',mensaje='', usuarios=[])
        try:
            usuarios = []
            usuarios = list(self.db.UsuariosView.find())
            salida.estatus = 'OK'
            if usuarios != []:
                salida.mensaje = 'Listado de Usuarios encontrado.'
                salida.usuarios = usuarios
            else:
                salida.mensaje = 'No hay Usuarios registrados.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los Usuarios, consulta al administrador."
        return salida

    def consultarUsuarioIndividual(self, idUsuario:str):
        salida = UsuarioSalida(estatus='',mensaje='',usuario=None)
        try:
            usuario = self.db.UsuariosView.find_one({"idUsuario":idUsuario})
            salida.estatus='OK'
            if usuario:
                salida.mensaje = 'Usuario encontrado correctamente.'
                salida.usuario = usuario
            else:
                salida.mensaje = 'No se encontro el Usuario.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar el Usuario, consulta al administrador."
        return salida

    def compararPassword(self, idUsuario:str, password:str):
        resultado = False
        Usuario = None
        Usuario =  self.db.Usuarios.find_one({'_id':ObjectId(idUsuario),'password':password})
        if Usuario != None:
            resultado = True
        else:
            resultado = False
        return resultado

    def cambiarPassword(self,idUsuario:str,cambio:CambioPassword):
        salida = Salida(estatus='',mensaje='')
        try:
            salida.estatus = 'OK'
            if self.consultarUsuarioPorID(idUsuario):
                if self.compararPassword(idUsuario,cambio.passwordAnterior):
                    self.db.Usuarios.update_one({'_id':ObjectId(idUsuario), 'password':cambio.passwordAnterior},{'$set':{'password':cambio.passwordNueva}})
                    salida.mensaje = "Se cambio correctamente la contraseña."
                else:
                    salida.mensaje = "La contraseña anterior no coincide."
            else:
                salida.mensaje = 'No se encontro un Usuario registrado con ese ID.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Se produjo un error al cambiar la contraseña."
        return salida

    def cambiarCorreo(self, idUsuario: str, cambio: CambioCorreo):
        salida = Salida(estatus='', mensaje='')
        try:
            salida.estatus = 'OK'
            if self.consultarUsuarioPorID(idUsuario):
                usuario_actual = self.db.UsuariosView.find_one({"idUsuario": idUsuario,'correo': cambio.correo})
                if not usuario_actual:
                    salida.mensaje = 'No se encontro un Usuario registrado con ese ID y correo.'
                    return salida

                if usuario_actual['correo'] == cambio.nuevoCorreo:
                    salida.mensaje = "El correo es el mismo."
                    return salida

                # Busca si ya existe ese correo en otro usuario
                correo_existente = self.db.UsuariosView.find_one({"correo": cambio.nuevoCorreo})
                if correo_existente and correo_existente['idUsuario'] != idUsuario:
                    salida.mensaje = 'El correo ya esta registrado, use uno distinto'
                else:
                    self.db.Usuarios.update_one({'_id': ObjectId(idUsuario)}, {'$set': {'correo': cambio.nuevoCorreo}})
                    salida.mensaje = "Se cambio correctamente el correo."
            else:
                salida.mensaje = 'No se encontro un Usuario registrado con ese ID.'
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Se produjo un error al cambiar el correo, consulta al administrador."
        return salida

    def autenticar(self, email,password):
        respuesta = UsuarioSalida(estatus='',mensaje='',usuario= None)
        print("validarUsuario - email:", email)
        print("validarUsuario - password:", password)
        try:
            print(f'email:{email}, password: {password}')
            usuario = self.db.Usuarios.find_one({'correo':email,'password':password,'estatus':'Activo'})
            print(usuario)
            if usuario:
                usuario['_id'] = str(usuario['_id'])
                respuesta.estatus = 'OK'
                respuesta.mensaje = "Usuario autenticado con exito."
                respuesta.usuario = usuario
            else:
                respuesta.estatus = 'ERROR'
                respuesta.mensaje = 'Datos incorrectos.'
        except Exception as e:
            print(e)
            respuesta.estatus = 'ERROR'
            respuesta.mensaje = 'Se produjo en error al autenticar el usuario.'
        return respuesta