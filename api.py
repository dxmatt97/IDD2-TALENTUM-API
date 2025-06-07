from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from neo4j import GraphDatabase
from decouple import config
from pydantic import BaseModel
import subprocess
import sys
import json

# Pydantic model for the request body of the update endpoint
class SeniorityUpdate(BaseModel):
    seniority: str

# --- Configuración ---
MONGO_URI = config("MONGO_URI")
NEO4J_URI = config("NEO4J_URI")
NEO4J_USER = config("NEO4J_USER")
NEO4J_PASSWORD = config("NEO4J_PASSWORD")

# --- Inicialización de la App ---
app = FastAPI(
    title="Talentum+ API",
    description="API para interactuar con los diferentes modelos de datos de Talentum+",
    version="1.0.0"
)

# --- Middleware de CORS ---
# Permite que el frontend (ej: en localhost:3000) se comunique con el backend (ej: en localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cámbialo a la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Conexiones a Bases de Datos ---
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["talentum_demo"]

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Simulación en memoria (reemplaza por Redis si lo tienes)
sesiones = {
    "cand_001": {"estado": "activa", "acciones": ["login", "ver_curso"]},
    "cand_002": {"estado": "inactiva", "acciones": ["login"]}
}

@app.on_event("shutdown")
def shutdown_event():
    mongo_client.close()
    neo4j_driver.close()

# --- Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Talentum+"}

@app.get("/api/candidatos", tags=["Documental - Candidatos"])
def get_candidatos():
    return list(db["candidatos"].find({}, {"_id": 0}))

@app.get("/api/candidatos/skill/{skill}", tags=["Documental - Candidatos"])
def get_candidatos_por_skill(skill: str):
    """
    Obtiene todos los candidatos de MongoDB que poseen un determinado skill técnico.
    """
    return list(db["candidatos"].find({"skills_tecnicos": skill}, {"_id": 0}))

@app.get("/api/candidatos/experiencia/{exp}", tags=["Documental - Candidatos"])
def get_candidatos_por_experiencia(exp: str):
    return list(db["candidatos"].find({"experiencia": exp}, {"_id": 0}))

@app.get("/api/candidatos/seniority/{level}", tags=["Documental - Candidatos"])
def get_candidatos_por_seniority(level: str):
    """
    Obtiene candidatos de MongoDB por su nivel de seniority.
    """
    return list(db["candidatos"].find({"seniority": level}, {"_id": 0}))

@app.get("/api/cursos", tags=["Documental - Cursos"])
def get_cursos():
    return list(db["cursos"].find({}, {"_id": 0}))

@app.get("/api/cursos/tipo/{tipo}", tags=["Documental - Cursos"])
def get_cursos_por_tipo(tipo: str):
    return list(db["cursos"].find({"tipo": tipo}, {"_id": 0}))

@app.get("/api/busquedas", tags=["Documental - Búsquedas"])
def get_busquedas():
    return list(db["busquedas"].find({}, {"_id": 0}))

@app.get("/api/busquedas/empresa/{empresa}", tags=["Documental - Búsquedas"])
def get_busquedas_por_empresa(empresa: str):
    return list(db["busquedas"].find({"empresa": empresa}, {"_id": 0}))

@app.get("/api/procesos_seleccion", tags=["Documental - Procesos"])
def get_procesos():
    return list(db["procesos_seleccion"].find({}, {"_id": 0}))

@app.get("/api/procesos_seleccion/candidato/{candidato_id}", tags=["Documental - Procesos"])
def get_procesos_por_candidato(candidato_id: str):
    return list(db["procesos_seleccion"].find({"candidato_id": candidato_id}, {"_id": 0}))

@app.get("/api/candidatos/{candidato_id}/cursos", tags=["Grafo - Cursos"])
def get_cursos_de_candidato(candidato_id: str):
    """
    Obtiene los cursos que un candidato ha tomado, consultando el grafo en Neo4j.
    """
    query = (
        "MATCH (c:Candidato {id: $candidato_id})-[:TOMO]->(curso:Curso) "
        "RETURN curso.id AS id, curso.titulo AS titulo, curso.tipo as tipo"
    )
    with neo4j_driver.session() as session:
        result = session.run(query, candidato_id=candidato_id)
        cursos = [record.data() for record in result]
    return cursos

@app.get("/api/cursos/{curso_id}/candidatos", tags=["Grafo - Candidatos"])
def get_candidatos_de_curso(curso_id: str):
    query = (
        "MATCH (c:Candidato)-[:TOMO]->(cu:Curso {id: $curso_id}) "
        "RETURN c.id AS id, c.nombre AS nombre"
    )
    with neo4j_driver.session() as session:
        result = session.run(query, curso_id=curso_id)
        return [record.data() for record in result]

@app.get("/api/candidatos/{candidato_id}/contactos", tags=["Grafo - Contactos"])
def get_contactos_de_candidato(candidato_id: str):
    query = (
        "MATCH (c:Candidato {id: $candidato_id})-[:CONTACTO]->(otro:Candidato) "
        "RETURN otro.id AS id, otro.nombre AS nombre"
    )
    with neo4j_driver.session() as session:
        result = session.run(query, candidato_id=candidato_id)
        return [record.data() for record in result]

@app.get("/api/candidatos/{candidato_id}/contactos-de-contactos", tags=["Grafo - Contactos"])
def get_contactos_de_contactos(candidato_id: str):
    """
    Obtiene los contactos de segundo grado (contactos de mis contactos) de un candidato.
    """
    query = (
        "MATCH (c:Candidato {id: $candidato_id})-[:CONTACTO*2..2]->(coc:Candidato) "
        "WHERE NOT (c)-[:CONTACTO]->(coc) AND c <> coc "
        "RETURN DISTINCT coc.id AS id, coc.nombre AS nombre"
    )
    with neo4j_driver.session() as session:
        result = session.run(query, candidato_id=candidato_id)
        return [record.data() for record in result]

@app.get("/api/candidatos/{candidato_id}/busquedas", tags=["Grafo - Búsquedas"])
def get_busquedas_aplicadas_por_candidato(candidato_id: str):
    query = (
        "MATCH (c:Candidato {id: $candidato_id})-[:APLICA_A]->(b:Busqueda) "
        "RETURN b.id AS id, b.fecha AS fecha"
    )
    with neo4j_driver.session() as session:
        result = session.run(query, candidato_id=candidato_id)
        return [record.data() for record in result]

@app.get("/api/empresas/busquedas", tags=["Grafo - Empresas"])
def get_empresas_y_busquedas():
    query = (
        "MATCH (e:Empresa)-[:PUBLICA]->(b:Busqueda) "
        "RETURN e.nombre AS empresa, b.id AS busqueda_id, b.fecha AS fecha"
    )
    with neo4j_driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

@app.get("/sesion/{candidato_id}")
def get_sesion_candidato(candidato_id: str):
    return sesiones.get(candidato_id, {})

@app.get("/sesiones")
def get_todas_sesiones():
    return [{"candidato_id": k, **v} for k, v in sesiones.items()]

# --- Admin Endpoints ---
@app.post("/api/admin/populate-mongo", tags=["Administración"])
def populate_mongo_db():
    """
    Ejecuta el script de población de MongoDB y devuelve un log estructurado.
    ¡Cuidado! Esto borrará los datos existentes en las colecciones.
    """
    try:
        script_path = "utils/documental/poblar_mongo.py"
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        # Parsea la salida JSON del script
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        # Intenta parsear el JSON del stderr si es posible
        try:
            error_output = json.loads(e.stdout)
            return {"status": "error", "message": "Falló la población de la base de datos.", "details": error_output}
        except json.JSONDecodeError:
            return {"status": "error", "message": "Falló la población de la base de datos.", "raw_output": e.stdout or e.stderr}
    except FileNotFoundError:
        return {"status": "error", "message": f"Error: script '{script_path}' no encontrado."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/admin/populate-neo4j", tags=["Administración"])
def populate_neo4j_db():
    """
    Ejecuta el script de población de Neo4j y devuelve un log estructurado.
    ¡Cuidado! Esto borrará todos los datos existentes en el grafo.
    """
    try:
        script_path = "utils/grafo/poblar_neo4j.py"
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        try:
            error_output = json.loads(e.stdout)
            return {"status": "error", "message": "Falló la población de la base de datos.", "details": error_output}
        except json.JSONDecodeError:
            return {"status": "error", "message": "Falló la población de la base de datos.", "raw_output": e.stdout or e.stderr}
    except FileNotFoundError:
        return {"status": "error", "message": f"Error: script '{script_path}' no encontrado."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.put("/api/candidatos/{candidato_id}/seniority", tags=["Documental - Candidatos"])
def update_candidato_seniority(candidato_id: str, update: SeniorityUpdate):
    """
    Actualiza el seniority de un candidato específico.
    """
    result = db["candidatos"].update_one(
        {"id": candidato_id},
        {"$set": {"seniority": update.seniority}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Candidato con id '{candidato_id}' no encontrado.")
    if result.modified_count == 0:
        return {"message": "El candidato ya tenía el seniority especificado."}
    return {"message": f"Seniority del candidato '{candidato_id}' actualizado a '{update.seniority}'."}

@app.delete("/api/candidatos/{candidato_id}", tags=["Documental - Candidatos"])
def delete_candidato(candidato_id: str):
    """
    Elimina un candidato de la base de datos por su ID.
    """
    result = db["candidatos"].delete_one({"id": candidato_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Candidato con id '{candidato_id}' no encontrado.")
    return {"message": f"Candidato con id '{candidato_id}' eliminado exitosamente."}