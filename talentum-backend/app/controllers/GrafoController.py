from fastapi import APIRouter
from app.services.GrafoService import (
    get_cursos_de_candidato, get_candidatos_de_curso, get_contactos_directos,
    get_contactos_indirectos, get_busquedas_aplicadas, get_empresas_y_busquedas,
    get_candidatos_matcheados
)
from app.config.db import redis_client
from app.utils.logger import log_recent_action
import json

router = APIRouter()

@router.get("/api/candidatos/{candidato_id}/cursos", tags=["Grafo - Cursos"])
def cursos_por_candidato(candidato_id: str):
    return get_cursos_de_candidato(candidato_id)

@router.get("/api/cursos/{curso_id}/candidatos", tags=["Grafo - Candidatos"])
def candidatos_por_curso(curso_id: str):
    return get_candidatos_de_curso(curso_id)

@router.get("/api/candidatos/{candidato_id}/contactos", tags=["Grafo - Contactos"])
def contactos_directos(candidato_id: str):
    return get_contactos_directos(candidato_id)

@router.get("/api/candidatos/{candidato_id}/contactos-de-contactos", tags=["Grafo - Contactos"])
def contactos_indirectos(candidato_id: str):
    return get_contactos_indirectos(candidato_id)

@router.get("/api/candidatos/{candidato_id}/busquedas", tags=["Grafo - Búsquedas"])
def busquedas_aplicadas(candidato_id: str):
    return get_busquedas_aplicadas(candidato_id)

@router.get("/api/empresas/busquedas", tags=["Grafo - Empresas"])
def empresas_y_busquedas():
    return get_empresas_y_busquedas()

@router.get("/api/busquedas/{busqueda_id}/match-candidatos", tags=["Grafo - Matching"])
def candidatos_matcheados(busqueda_id: str):
    cache_key = f"cache:matching:{busqueda_id}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return {"source": "cache", "data": json.loads(cached)}
    
    data = get_candidatos_matcheados(busqueda_id)
    redis_client.setex(cache_key, 300, json.dumps(data))
    
    log_recent_action(f"Matching ejecutado para búsqueda {busqueda_id}")
    return {"source": "database", "data": data}
