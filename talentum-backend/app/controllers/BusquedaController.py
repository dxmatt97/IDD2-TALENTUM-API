from fastapi import APIRouter
from app.services.BusquedaService import get_all_busquedas, get_busquedas_by_empresa

router = APIRouter()

@router.get("/api/busquedas", tags=["Documental - Búsquedas"])
def get_busquedas():
    return get_all_busquedas()

@router.get("/api/busquedas/empresa/{empresa}", tags=["Documental - Búsquedas"])
def get_busquedas_por_empresa(empresa: str):
    return get_busquedas_by_empresa(empresa)
