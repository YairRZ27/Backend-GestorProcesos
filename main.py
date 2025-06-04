from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from DAO.database import Conexion
from Router import ProcesosRouter, SolicitudesRouter, UsuariosRouter

app = FastAPI()

origins = [
    "http://localhost",         # Si tu frontend se sirve desde aquí
    "http://localhost:3000",    # Origen común para React, Vue, etc.
    "http://127.0.0.1:5500",  # Origen común para Live Server de VSCode
    "http://172.21.128.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Lista de orígenes permitidos
    allow_credentials=True,        # Permite cookies (importante si usas cookies para sesión)
    allow_methods=["*"],           # Permite todos los métodos (o especifica GET, POST, etc.)
    allow_headers=["*"],           # Permite todos los encabezados (o especifica "Authorization", "Content-Type")
)

app.include_router(UsuariosRouter.router)
app.include_router(ProcesosRouter.router)
app.include_router(SolicitudesRouter.router)

@app.get('/')
async def home():
    salida = {'mensaje':'Bienvenido a GestorProcesosAPI'}
    return salida

@app.on_event('startup')
async def startup():
    print('Estableciendo conexion')
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()

@app.on_event('shutdown')
async def shutdown():
    print('Cerrando conexion')
    app.conexion.cerrar()

if __name__ == '__main__':
    uvicorn.run('main:app',host='127.0.0.1',reload=True,port=8001)