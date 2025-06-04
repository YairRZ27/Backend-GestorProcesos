from pymongo import MongoClient

DATABASE_URL = 'mongodb+srv://armandoyairruiz27:T81FaD9KMVVGDcjo@gestorprocesos.hgopuvm.mongodb.net/?retryWrites=true&w=majority&appName=GestorProcesos'
DATABASE_NAME = 'GestorProcesosBD'

class Conexion:
    def __init__(self):
        self.cliente = MongoClient(DATABASE_URL)
        self.db = self.cliente[DATABASE_NAME]

    def cerrar(self):
        self.cliente.close()

    def getDB(self):
        return self.db