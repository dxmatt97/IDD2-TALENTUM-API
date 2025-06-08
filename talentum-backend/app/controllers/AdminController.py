from fastapi import APIRouter
from app.services.AdminService import ejecutar_script

router = APIRouter()

@router.post("/api/admin/populate-mongo", tags=["Administración"])
def poblar_mongo():
    return ejecutar_script("app/utils/documental/poblar_mongo.py")

@router.post("/api/admin/populate-neo4j", tags=["Administración"])
def poblar_neo4j():
    return ejecutar_script("app/utils/grafo/poblar_neo4j.py")

@router.post("/api/admin/populate-redis", tags=["Administración"])
def poblar_redis():
    return ejecutar_script("app/utils/clave_valor/poblar_redis.py")
