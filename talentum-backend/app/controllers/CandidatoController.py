from fastapi import APIRouter, HTTPException
from app.services.CandidatoService import (
    get_all_candidatos,
    get_candidatos_por_skill,
    get_candidatos_por_experiencia,
    get_candidatos_por_seniority,
    update_seniority,
    delete_candidato
)
from app.models.schemas import SeniorityUpdate

router = APIRouter()

@router.get("/api/candidatos", tags=["Documental - Candidatos"])
def get_candidatos():
    return get_all_candidatos()

@router.get("/api/candidatos/skill/{skill}", tags=["Documental - Candidatos"])
def get_por_skill(skill: str):
    return get_candidatos_por_skill(skill)

@router.get("/api/candidatos/experiencia/{exp}", tags=["Documental - Candidatos"])
def get_por_experiencia(exp: str):
    return get_candidatos_por_experiencia(exp)

@router.get("/api/candidatos/seniority/{level}", tags=["Documental - Candidatos"])
def get_por_seniority(level: str):
    return get_candidatos_por_seniority(level)

@router.put("/api/candidatos/{candidato_id}/seniority", tags=["Documental - Candidatos"])
def update_por_seniority(candidato_id: str, update: SeniorityUpdate):
    return update_seniority(candidato_id, update)

@router.delete("/api/candidatos/{candidato_id}", tags=["Documental - Candidatos"])
def delete(candidato_id: str):
    return delete_candidato(candidato_id)
