from fastapi import APIRouter
from app.services.ProcesoService import get_all_procesos, get_procesos_by_candidato

router = APIRouter()

@router.get("/api/procesos_seleccion", tags=["Documental - Procesos"])
def get_procesos():
    return get_all_procesos()

@router.get("/api/procesos_seleccion/candidato/{candidato_id}", tags=["Documental - Procesos"])
def get_procesos_por_candidato(candidato_id: str):
    return get_procesos_by_candidato(candidato_id)
