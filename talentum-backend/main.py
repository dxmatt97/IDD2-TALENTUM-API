from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.RootController import router as root_router
from app.controllers.AdminController import router as admin_router
from app.controllers.SesionController import router as session_router
from app.controllers.ActionController import router as action_router
from app.controllers.CandidatoController import router as candidato_router
from app.controllers.CursoController import router as curso_router
from app.controllers.BusquedaController import router as busqueda_router
from app.controllers.ProcesoController import router as proceso_router
from app.controllers.GrafoController import router as grafo_router

app = FastAPI(title="Talentum+", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(admin_router)
app.include_router(session_router)
app.include_router(action_router)
app.include_router(candidato_router)
app.include_router(curso_router)
app.include_router(busqueda_router)
app.include_router(proceso_router)
app.include_router(grafo_router)
