from fastapi import APIRouter
from app.services.CursoService import get_all_cursos, get_cursos_by_tipo

router = APIRouter()

@router.get("/api/cursos", tags=["Documental - Cursos"])
def get_cursos():
    return get_all_cursos()

@router.get("/api/cursos/tipo/{tipo}", tags=["Documental - Cursos"])
def get_cursos_por_tipo(tipo: str):
    return get_cursos_by_tipo(tipo)
