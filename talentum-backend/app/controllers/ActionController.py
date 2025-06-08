from fastapi import APIRouter
from app.services.ActionService import get_recent_actions

router = APIRouter()

@router.get("/api/actions/recent", tags=["Clave-Valor - Acciones Recientes"])
def obtener_acciones_recientes():
    return {"recent_actions": get_recent_actions()}
