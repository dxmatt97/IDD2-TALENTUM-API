from app.config.db import db

def get_all_cursos():
    return list(db["cursos"].find({}, {"_id": 0}))

def get_cursos_by_tipo(tipo: str):
    return list(db["cursos"].find({"tipo": tipo}, {"_id": 0}))
