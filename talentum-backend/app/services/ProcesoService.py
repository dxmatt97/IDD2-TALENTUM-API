from app.config.db import db

def get_all_procesos():
    return list(db["procesos_seleccion"].find({}, {"_id": 0}))

def get_procesos_by_candidato(candidato_id: str):
    return list(db["procesos_seleccion"].find({"candidato_id": candidato_id}, {"_id": 0}))
