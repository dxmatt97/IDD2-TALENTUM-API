const consultas = [
  // Administración
  {
    title: "Poblar MongoDB",
    description: "Genera datos maestros (Candidatos, Cursos, etc.) y los guarda en MongoDB. Actúa como la 'única fuente de verdad' y también exporta los datos a archivos JSON para que otros sistemas los consuman.",
    endpoint: "/api/admin/populate-mongo",
    method: "POST",
    dbInfo: { name: "MongoDB", model: "Administración" },
    category: "Administración",
    codeSnippet: `
# utils/documental/poblar_mongo.py

def poblar_mongo():
    # ... (conecta, genera datos)
    client = MongoClient(MONGO_URI)
    db = client["talentum_demo"]
    
    # Limpiar colecciones
    db.candidatos.delete_many({})
    db.cursos.delete_many({})
    # ... (más colecciones)

    # Insertar nuevos datos
    db.candidatos.insert_many(candidatos)
    db.cursos.insert_many(cursos)
    # ... (más inserciones)

    return {
        "status": "success",
        "counts": {
            "candidatos": len(candidatos),
            # ... (más conteos)
        }
    }
`
  },
  {
    title: "Poblar Neo4j",
    description: "Lee los datos desde los archivos JSON (generados por el script de MongoDB) y construye un grafo de relaciones en Neo4j, asegurando la consistencia entre las bases de datos.",
    endpoint: "/api/admin/populate-neo4j",
    method: "POST",
    dbInfo: { name: "Neo4j", model: "Administración" },
    category: "Administración",
    codeSnippet: `
# utils/grafo/poblar_neo4j.py

def poblar_neo4j():
    # ... (conecta, genera datos)
    driver = GraphDatabase.driver(...)
    
    with driver.session() as session:
      # Limpiar BD
      session.run("MATCH (n) DETACH DELETE n")

      # Crear Nodos
      session.run("CREATE (c:Candidato ...)")
      session.run("CREATE (cu:Curso ...)")
      
      # Crear Relaciones
      session.run("MATCH ... CREATE (cand)-[:TOMO]->(cu)")
      session.run("MATCH ... CREATE (a)-[:CONTACTO]->(b)")

    return {
        "status": "success",
        "counts": { ... }
    }
`
  },
  {
    title: "Poblar Redis",
    description: "Ejecuta un script para conectar a MongoDB y Redis. Lee los IDs de los candidatos existentes y genera dinámicamente datos de sesión de prueba para un subconjunto de ellos en Redis. Devuelve el log de la operación.",
    endpoint: "/api/admin/populate-redis",
    method: "POST",
    dbInfo: { name: "Redis", model: "Administración" },
    category: "Administración",
    codeSnippet: `
# utils/clave_valor/poblar_redis.py

def populate_redis():
    # 1. Conectar a Redis y MongoDB
    r = redis.from_url(...)
    db = get_mongo_db()

    # 2. Obtener IDs de candidatos de Mongo
    candidate_ids = [c["id"] for c in db.candidatos.find()]
    
    # 3. Limpiar Redis
    r.flushdb()

    # 4. Generar y crear sesiones dinámicamente
    for cid in random.sample(candidate_ids, 15):
        session_data = generate_random_session(cid)
        r.set(f"session:{cid}", json.dumps(session_data))

    return { "status": "success", ... }
`
  },
  // Documental
  {
    title: "Todos los candidatos",
    description: "Lista completa de candidatos en la base documental.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Candidatos",
    codeSnippet: `db.candidatos.find({})`,
    endpoint: "/api/candidatos"
  },
  {
    title: "Candidatos con skill Python",
    description: "Candidatos que tienen Python como skill técnico.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Candidatos",
    codeSnippet: `db.candidatos.find({ skills_tecnicos: "Python" })`,
    endpoint: "/api/candidatos/skill/Python"
  },
  {
    title: "Candidatos con experiencia en Backend",
    description: "Candidatos con experiencia en Backend.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Candidatos",
    codeSnippet: `db.candidatos.find({ experiencia: "Backend" })`,
    endpoint: "/api/candidatos/experiencia/Backend"
  },
  {
    title: "Candidatos con seniority Senior",
    description: "Candidatos que tienen un seniority de 'Senior'.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Candidatos",
    codeSnippet: `db.candidatos.find({ seniority: "Senior" })`,
    endpoint: "/api/candidatos/seniority/Senior"
  },
  {
    title: "Actualizar Seniority de cand_007",
    description: "Actualiza el nivel de seniority del candidato 'cand_007' a 'Principal Engineer'. Requiere un cuerpo de Petición.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Candidatos",
    method: 'PUT',
    endpoint: "/api/candidatos/cand_007/seniority",
    body: { "seniority": "Principal Engineer" },
    codeSnippet: `
# Endpoint: PUT /api/candidatos/{candidato_id}/seniority
# Body: { "seniority": "Principal Engineer" }

# pymongo
db.candidatos.update_one(
  { "id": "cand_007" },
  { "$set": { "seniority": "Principal Engineer" } }
)
`
  },
  {
    title: "Eliminar Candidato cand_049",
    description: "Elimina al candidato con ID 'cand_049' de la base de datos.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Candidatos",
    method: 'DELETE',
    endpoint: "/api/candidatos/cand_049",
    codeSnippet: `
# Endpoint: DELETE /api/candidatos/cand_049

# pymongo
db.candidatos.delete_one({ "id": "cand_049" })
`
  },
  {
    title: "Todos los cursos",
    description: "Lista de todos los cursos disponibles.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Cursos",
    codeSnippet: `db.cursos.find({})`,
    endpoint: "/api/cursos"
  },
  {
    title: "Cursos tipo video",
    description: "Cursos cuyo tipo es 'video'.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Cursos",
    codeSnippet: `db.cursos.find({ tipo: "video" })`,
    endpoint: "/api/cursos/tipo/video"
  },
  {
    title: "Todas las búsquedas",
    description: "Todas las búsquedas laborales activas.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Búsquedas",
    codeSnippet: `db.busquedas.find({})`,
    endpoint: "/api/busquedas"
  },
  {
    title: "Búsquedas de la empresa TechSolutions",
    description: "Búsquedas publicadas por la empresa TechSolutions.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Búsquedas",
    codeSnippet: `db.busquedas.find({ empresa: "TechSolutions" })`,
    endpoint: "/api/busquedas/empresa/TechSolutions"
  },
  {
    title: "Procesos de selección",
    description: "Todos los procesos de selección documentados.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Procesos de Selección",
    codeSnippet: `db.procesos_seleccion.find({})`,
    endpoint: "/api/procesos_seleccion"
  },
  {
    title: "Procesos de selección de cand_001",
    description: "Procesos de selección en los que participó cand_001.",
    dbInfo: { name: "MongoDB", model: "Documental" },
    category: "Procesos de Selección",
    codeSnippet: `db.procesos_seleccion.find({ candidato_id: "cand_001" })`,
    endpoint: "/api/procesos_seleccion/candidato/cand_001"
  },
  // Grafo
  {
    title: "Cursos tomados por cand_001",
    description: "Cursos tomados por el candidato cand_001 (grafo).",
    dbInfo: { name: "Neo4j", model: "Grafo" },
    category: "Cursos y Candidatos",
    codeSnippet: `MATCH (c:Candidato {id: "cand_001"})-[:TOMO]->(cu:Curso) RETURN cu`,
    endpoint: "/api/candidatos/cand_001/cursos"
  },
  {
    title: "Candidatos que tomaron curso_001",
    description: "Candidatos que tomaron el curso curso_001.",
    dbInfo: { name: "Neo4j", model: "Grafo" },
    category: "Cursos y Candidatos",
    codeSnippet: `MATCH (c:Candidato)-[:TOMO]->(cu:Curso {id: "curso_001"}) RETURN c`,
    endpoint: "/api/cursos/curso_001/candidatos"
  },
  {
    title: "Red de contactos de cand_001",
    description: "Contactos directos de cand_001.",
    dbInfo: { name: "Neo4j", model: "Grafo" },
    category: "Red de Contactos",
    codeSnippet: `MATCH (c:Candidato {id: "cand_001"})-[:CONTACTO]->(otro:Candidato) RETURN otro`,
    endpoint: "/api/candidatos/cand_001/contactos"
  },
  {
    title: "Contactos de 2do Grado de cand_001",
    description: "Contactos de los contactos de cand_001 (grafo).",
    dbInfo: { name: "Neo4j", model: "Grafo" },
    category: "Red de Contactos",
    codeSnippet: `MATCH (c:Candidato {id: "cand_001"})-[:CONTACTO*2..2]->(coc:Candidato) WHERE NOT (c)-[:CONTACTO]->(coc) AND c <> coc RETURN DISTINCT coc`,
    endpoint: "/api/candidatos/cand_001/contactos-de-contactos"
  },
  {
    title: "Búsquedas a las que aplicó cand_001",
    description: "Búsquedas laborales a las que aplicó cand_001.",
    dbInfo: { name: "Neo4j", model: "Grafo" },
    category: "Búsquedas y Aplicaciones",
    codeSnippet: `MATCH (c:Candidato {id: "cand_001"})-[:APLICA_A]->(b:Busqueda) RETURN b`,
    endpoint: "/api/candidatos/cand_001/busquedas"
  },
  {
    title: "Empresas y sus búsquedas",
    description: "Empresas y las búsquedas que publicaron.",
    dbInfo: { name: "Neo4j", model: "Grafo" },
    category: "Búsquedas y Aplicaciones",
    codeSnippet: `MATCH (e:Empresa)-[:PUBLICA]->(b:Busqueda) RETURN e, b`,
    endpoint: "/api/empresas/busquedas"
  },
  {
    title: "Matching Inteligente para Búsqueda",
    description: "Encuentra los 10 mejores candidatos para la búsqueda 'busq_005'. Los resultados se cachean en Redis por 5 minutos. La primera ejecución consulta la BD (lento), las siguientes leen del caché (rápido).",
    dbInfo: { name: "Neo4j / Redis", model: "Grafo / Caché" },
    category: "Matching Inteligente",
    endpoint: "/api/busquedas/busq_005/match-candidatos",
    codeSnippet: `
# api.py
@app.get("/api/busquedas/{id}/match-candidatos")
def get_matching_candidatos(busqueda_id: str):
    cache_key = f"cache:matching:{busqueda_id}"
    cached_result = redis_client.get(cache_key)

    if cached_result:
        return { "source": "cache", ... }

    # ... Si no, consultar Neo4j ...
    
    redis_client.setex(cache_key, 300, result_json)
    return { "source": "database", ... }
`
  },
  // Clave-Valor
  {
    title: "Todas las Sesiones",
    description: "Obtiene todas las claves de sesión y sus datos desde Redis.",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Sesiones (Clave-Valor)",
    endpoint: "/sesiones",
    codeSnippet: `
# FastAPI Endpoint
@app.get("/sesiones")
def get_todas_sesiones():
    all_sessions = []
    # Usamos SCAN para no bloquear el servidor
    for key in redis_client.scan_iter("session:*"):
        session_data = redis_client.get(key)
        # ...
    return all_sessions
`
  },
  {
    title: "Sesión del Candidato cand_001",
    description: "Obtiene los datos de sesión para un candidato específico desde Redis.",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Sesiones (Clave-Valor)",
    endpoint: "/sesion/cand_001",
    codeSnippet: `
# FastAPI Endpoint
@app.get("/sesion/{candidato_id}")
def get_sesion_candidato(candidato_id: str):
    session_data = redis_client.get(f"session:{candidato_id}")
    if session_data is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return json.loads(session_data)
`
  },
  {
    title: "Logout Candidato (Borrar Sesión)",
    description: "Elimina la clave de sesión de un candidato en Redis. Esto también registrará una acción en la lista de acciones recientes.",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Sesiones (Clave-Valor)",
    method: 'DELETE',
    endpoint: "/sesion/cand_001",
    codeSnippet: `
# api.py
@app.delete("/sesion/{candidato_id}")
def delete_sesion_candidato(candidato_id: str):
    session_key = f"session:{candidato_id}"
    deleted_count = redis_client.delete(session_key)
    # ...
    log_recent_action(...)
    return {"message": "Sesión eliminada."}
`
  },
  {
    title: "Añadir Acción a Sesión",
    description: "Añade una acción a la lista de 'recent_actions' para la sesión del 'cand_001'. Requiere un cuerpo de petición.",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Sesiones (Clave-Valor)",
    method: 'POST',
    endpoint: "/sesion/cand_001/action",
    body: { action_name: "reviewed_job_offer" },
    codeSnippet: `
# Endpoint: POST /sesion/cand_001/action
# Body: { "action_name": "reviewed_job_offer" }

# api.py
@app.post("/sesion/{id}/action")
def add_action_a_sesion(candidato_id: str, action: Action):
    # ...
    session_data["recent_actions"].append(...)
    redis_client.set(session_key, json.dumps(session_data))
    # ...
`
  },
  {
    title: "Ver Acciones Globales Recientes",
    description: "Obtiene una lista de las últimas 10 acciones importantes que han ocurrido en la plataforma (ej: updates, deletes, logins).",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Acciones Recientes (Cache)",
    endpoint: "/api/actions/recent",
    codeSnippet: `
# api.py
@app.get("/api/actions/recent")
def get_recent_actions():
    key = "global:recent_actions"
    recent_actions = redis_client.lrange(key, 0, 9)
    return {"recent_actions": recent_actions}
`
  }
];

export default consultas;