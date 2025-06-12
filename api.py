from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from neo4j import GraphDatabase
from decouple import config
from pydantic import BaseModel
import subprocess
import sys
import json
import redis
from datetime import datetime

# Pydantic model for the request body of the update endpoint
class SeniorityUpdate(BaseModel):
    seniority: str

class Action(BaseModel):
    action_name: str

class ActionResponse(BaseModel):
    message: str
    session_data: dict

# --- Configuración ---
MONGO_URI = config("MONGO_URI")
NEO4J_URI = config("NEO4J_URI")
NEO4J_USER = config("NEO4J_USER")
NEO4J_PASSWORD = config("NEO4J_PASSWORD")
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379")

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
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# --- Helper Functions ---
def log_recent_action(action_description: str):
    """Adds an action to the global recent actions list in Redis."""
    key = "global:recent_actions"
    # LPUSH adds the new action to the start of the list
    redis_client.lpush(key, f"{datetime.utcnow().isoformat()}: {action_description}")
    # LTRIM keeps the list at a max size of 10
    redis_client.ltrim(key, 0, 9)

@app.on_event("shutdown")
def shutdown_event():
    mongo_client.close()
    neo4j_driver.close()
    redis_client.close()

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

@app.get("/api/busquedas/{busqueda_id}/match-candidatos", tags=["Grafo - Matching"])
def get_matching_candidatos(busqueda_id: str):
    """
    Encuentra los 10 mejores candidatos para una búsqueda.
    Los resultados se cachean en Redis por 5 minutos para mejorar el rendimiento.
    """
    cache_key = f"cache:matching:{busqueda_id}"
    cached_result = redis_client.get(cache_key)

    if cached_result:
        return {
            "source": "cache",
            "data": json.loads(cached_result)
        }

    # Si no está en caché, ejecutar la consulta en Neo4j
    query = """
        MATCH (b:Busqueda {id: $busqueda_id})-[:REQUIERE_TECNOLOGIA]->(req_skill:Tecnologia)
        WITH b, collect(req_skill) AS required_skills
        MATCH (b)-[:REQUIERE_IDIOMA]->(req_lang:Idioma)
        WITH b, required_skills, collect(req_lang) AS required_languages
        
        MATCH (c:Candidato)
        WHERE NOT (c)-[:APLICA_A]->(b)

        CALL {
            WITH c, required_skills
            UNWIND required_skills AS req_skill
            MATCH (c)-[:TIENE_SKILL]->(req_skill)
            RETURN count(req_skill) AS skill_matches
        }

        CALL {
            WITH c, required_languages
            UNWIND required_languages AS req_lang
            MATCH (c)-[:HABLA]->(req_lang)
            RETURN count(req_lang) AS lang_matches
        }

        WITH c, skill_matches, lang_matches,
             toFloat(skill_matches) / size(required_skills) AS skill_score,
             toFloat(lang_matches) / size(required_languages) AS lang_score
        WHERE skill_matches > 0 // Requisito mínimo: al menos un skill en común

        RETURN
            c.id AS candidato_id,
            c.nombre AS nombre,
            skill_matches,
            lang_matches,
            (skill_score * 0.75) + (lang_score * 0.25) AS match_score
        ORDER BY match_score DESC
        LIMIT 10
    """
    with neo4j_driver.session() as session:
        result = session.run(query, busqueda_id=busqueda_id)
        data = [record.data() for record in result]
    
    # Guardar en caché con un TTL de 5 minutos (300 segundos)
    redis_client.setex(cache_key, 300, json.dumps(data))
    
    log_recent_action(f"Smart matching query executed for search '{busqueda_id}'")
    return {
        "source": "database",
        "data": data
    }

@app.get("/sesion/{candidato_id}", tags=["Clave-Valor - Sesiones"])
def get_sesion_candidato(candidato_id: str):
    """
    Obtiene los datos de sesión de un candidato desde Redis.
    Las sesiones se almacenan como JSON strings.
    """
    session_data = redis_client.get(f"session:{candidato_id}")
    if session_data is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return json.loads(session_data)

@app.get("/sesiones", tags=["Clave-Valor - Sesiones"])
def get_todas_sesiones():
    """
    Obtiene todas las sesiones activas desde Redis.
    Usa SCAN para iterar sobre las claves sin bloquear el servidor.
    """
    all_sessions = []
    # Usamos scan para no bloquear Redis en producción si hay muchas llaves
    for key in redis_client.scan_iter("session:*"):
        session_data = redis_client.get(key)
        if session_data:
            session_id = key.split(":")[1]
            all_sessions.append({
                "candidato_id": session_id,
                **json.loads(session_data)
            })
    return all_sessions

@app.delete("/sesion/{candidato_id}", tags=["Clave-Valor - Sesiones"])
def delete_sesion_candidato(candidato_id: str):
    """
    Elimina una sesión de candidato de Redis (simula un logout).
    """
    session_key = f"session:{candidato_id}"
    deleted_count = redis_client.delete(session_key)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sesión no encontrada para eliminar.")
    
    log_recent_action(f"Session deleted for candidate '{candidato_id}' (logout).")
    return {"message": f"Sesión para el candidato '{candidato_id}' eliminada."}

@app.post("/sesion/{candidato_id}/action", response_model=ActionResponse, tags=["Clave-Valor - Sesiones"])
def add_action_a_sesion(candidato_id: str, action: Action):
    """
    Añade una nueva acción a la lista de acciones recientes de una sesión de candidato.
    """
    session_key = f"session:{candidato_id}"
    session_data_str = redis_client.get(session_key)
    
    if not session_data_str:
        raise HTTPException(status_code=404, detail="Sesión de candidato no encontrada.")
        
    session_data = json.loads(session_data_str)
    
    if "recent_actions" not in session_data:
        session_data["recent_actions"] = []
        
    session_data["recent_actions"].append(action.action_name)
    
    # Actualizar la sesión en Redis
    redis_client.set(session_key, json.dumps(session_data))
    
    log_recent_action(f"Action '{action.action_name}' added to session for '{candidato_id}'.")
    return {
        "message": "Acción añadida a la sesión.",
        "session_data": session_data
    }

# --- Recent Actions Endpoint ---
@app.get("/api/actions/recent", tags=["Clave-Valor - Acciones Recientes"])
def get_recent_actions():
    """
    Obtiene las 10 acciones más recientes de la plataforma desde una lista en Redis.
    """
    key = "global:recent_actions"
    # LRANGE obtiene un rango de elementos de la lista. 0 a 9 son los primeros 10.
    recent_actions = redis_client.lrange(key, 0, 9)
    return {"recent_actions": recent_actions}

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

@app.post("/api/admin/populate-redis", tags=["Administración"])
def populate_redis_db():
    """
    Ejecuta el script de población de Redis y devuelve un log estructurado.
    ¡Cuidado! Esto borrará todos los datos existentes en la base de datos Redis.
    """
    try:
        script_path = "utils/clave_valor/poblar_redis.py"
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
    
    log_recent_action(f"Candidate '{candidato_id}' seniority updated to '{update.seniority}'.")
    return {"message": f"Seniority del candidato '{candidato_id}' actualizado a '{update.seniority}'."}

@app.delete("/api/candidatos/{candidato_id}", tags=["Documental - Candidatos"])
def delete_candidato(candidato_id: str):
    """
    Elimina un candidato de la base de datos por su ID.
    """
    result = db["candidatos"].delete_one({"id": candidato_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Candidato con id '{candidato_id}' no encontrado.")
    
    log_recent_action(f"Candidate '{candidato_id}' was deleted.")
    return {"message": f"Candidato con id '{candidato_id}' eliminado exitosamente."}