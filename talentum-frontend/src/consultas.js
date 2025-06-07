const consultas = [
  // Administración
  {
    title: "Poblar MongoDB",
    description: "Ejecuta un script para limpiar y poblar la base de datos de MongoDB con datos de prueba. Devuelve el log de la operación.",
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
    description: "Ejecuta un script para limpiar y poblar la base de datos de Neo4j con un grafo de prueba. Devuelve el log de la operación.",
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
  // Clave-valor
  {
    title: "Sesión de cand_001",
    description: "Sesión almacenada para cand_001.",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Sesiones",
    codeSnippet: `GET cand_001`,
    endpoint: "/sesion/cand_001"
  },
  {
    title: "Todas las sesiones activas",
    description: "Lista de todas las sesiones activas.",
    dbInfo: { name: "Redis", model: "Clave-Valor" },
    category: "Sesiones",
    codeSnippet: `KEYS *`,
    endpoint: "/sesiones"
  }
];

export default consultas;