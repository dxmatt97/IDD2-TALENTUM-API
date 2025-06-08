from fastapi import HTTPException
from app.config.db import db
from app.models.schemas import SeniorityUpdate
from app.utils.logger import log_recent_action
from typing import List, Dict


def get_all_candidatos() -> List[Dict]:
    return list(db["candidatos"].find({}, {"_id": 0}))


def get_candidatos_por_skill(skill: str) -> List[Dict]:
    return list(db["candidatos"].find({"skills_tecnicos": skill}, {"_id": 0}))


def get_candidatos_por_experiencia(exp: str) -> List[Dict]:
    return list(db["candidatos"].find({"experiencia": exp}, {"_id": 0}))


def get_candidatos_por_seniority(level: str) -> List[Dict]:
    return list(db["candidatos"].find({"seniority": level}, {"_id": 0}))


def update_seniority(candidato_id: str, update: SeniorityUpdate) -> Dict:
    result = db["candidatos"].update_one(
        {"id": candidato_id},
        {"$set": {"seniority": update.seniority}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Candidato con id '{candidato_id}' no encontrado.")

    if result.modified_count == 0:
        return {"message": "El candidato ya tenía el seniority especificado."}

    log_recent_action(f"Candidate '{candidato_id}' seniority updated to '{update.seniority}'.")
    return {"message": f"Seniority del candidato '{candidato_id}' actualizado a '{update.seniority}'."}


def delete_candidato(candidato_id: str) -> Dict:
    result = db["candidatos"].delete_one({"id": candidato_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Candidato con id '{candidato_id}' no encontrado.")

    log_recent_action(f"Candidate '{candidato_id}' was deleted.")
    return {"message": f"Candidato con id '{candidato_id}' eliminado exitosamente."}
