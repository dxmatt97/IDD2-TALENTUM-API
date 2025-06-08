from app.config.db import db

def get_all_busquedas():
    return list(db["busquedas"].find({}, {"_id": 0}))

def get_busquedas_by_empresa(empresa: str):
    return list(db["busquedas"].find({"empresa": empresa}, {"_id": 0}))
