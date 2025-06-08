from fastapi import APIRouter, HTTPException, Depends
from app.config.db import redis_client
from app.services.SesionService import (
    get_sesion,
    get_all_sesiones,
    delete_sesion,
    add_action,
    crear_sesion
)
from app.models.schemas import Action, ActionResponse
from app.utils.logger import log_recent_action

router = APIRouter()

@router.get("/sesion/{candidato_id}", tags=["Clave-Valor - Sesiones"])
def obtener_sesion(candidato_id: str):
    session_data = get_sesion(redis_client, candidato_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return session_data

@router.get("/sesiones", tags=["Clave-Valor - Sesiones"])
def obtener_todas_sesiones():
    return get_all_sesiones(redis_client)

@router.delete("/sesion/{candidato_id}", tags=["Clave-Valor - Sesiones"])
def eliminar_sesion(candidato_id: str):
    result = delete_sesion(redis_client, candidato_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Sesión no encontrada para eliminar.")
    log_recent_action(f"Session deleted for candidate '{candidato_id}' (logout).")
    return {"message": f"Sesión para el candidato '{candidato_id}' eliminada."}

@router.post("/sesion/{candidato_id}/action", response_model=ActionResponse, tags=["Clave-Valor - Sesiones"])
def agregar_accion_sesion(candidato_id: str, action: Action):
    result = add_action(redis_client, candidato_id, action.action_name)
    if not result:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    log_recent_action(f"Action '{action.action_name}' added to session for '{candidato_id}'.")
    return {"message": "Acción añadida a la sesión.", "session_data": result}

@router.post("/sesion/{candidato_id}", tags=["Clave-Valor - Sesiones"])
def crear_sesion_para_candidato(candidato_id: str):
    result = crear_sesion(redis_client, candidato_id)
    if not result:
        raise HTTPException(status_code=400, detail="La sesión ya existe.")
    log_recent_action(f"Sesión creada para '{candidato_id}'.")
    return {"message": f"Sesión creada para '{candidato_id}'."}
