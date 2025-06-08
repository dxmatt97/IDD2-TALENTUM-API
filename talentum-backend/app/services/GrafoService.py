from app.config.db import neo4j_driver

def run_neo4j_query(query: str, params: dict = {}) -> list[dict]:
    with neo4j_driver.session() as session:
        result = session.run(query, **params)
        return [record.data() for record in result]

def get_cursos_de_candidato(candidato_id: str):
    query = """
        MATCH (c:Candidato {id: $candidato_id})-[:TOMO]->(curso:Curso)
        RETURN curso.id AS id, curso.titulo AS titulo, curso.tipo as tipo
    """
    return run_neo4j_query(query, {"candidato_id": candidato_id})

def get_candidatos_de_curso(curso_id: str):
    query = """
        MATCH (c:Candidato)-[:TOMO]->(cu:Curso {id: $curso_id})
        RETURN c.id AS id, c.nombre AS nombre
    """
    return run_neo4j_query(query, {"curso_id": curso_id})

def get_contactos_directos(candidato_id: str):
    query = """
        MATCH (c:Candidato {id: $candidato_id})-[:CONTACTO]->(otro:Candidato)
        RETURN otro.id AS id, otro.nombre AS nombre
    """
    return run_neo4j_query(query, {"candidato_id": candidato_id})

def get_contactos_indirectos(candidato_id: str):
    query = """
        MATCH (c:Candidato {id: $candidato_id})-[:CONTACTO*2..2]->(coc:Candidato)
        WHERE NOT (c)-[:CONTACTO]->(coc) AND c <> coc
        RETURN DISTINCT coc.id AS id, coc.nombre AS nombre
    """
    return run_neo4j_query(query, {"candidato_id": candidato_id})

def get_busquedas_aplicadas(candidato_id: str):
    query = """
        MATCH (c:Candidato {id: $candidato_id})-[:APLICA_A]->(b:Busqueda)
        RETURN b.id AS id, b.fecha AS fecha
    """
    return run_neo4j_query(query, {"candidato_id": candidato_id})

def get_empresas_y_busquedas():
    query = """
        MATCH (e:Empresa)-[:PUBLICA]->(b:Busqueda)
        RETURN e.nombre AS empresa, b.id AS busqueda_id, b.fecha AS fecha
    """
    return run_neo4j_query(query)

def get_candidatos_matcheados(busqueda_id: str):
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
        WHERE skill_matches > 0
        RETURN
            c.id AS candidato_id,
            c.nombre AS nombre,
            skill_matches,
            lang_matches,
            (skill_score * 0.75) + (lang_score * 0.25) AS match_score
        ORDER BY match_score DESC
        LIMIT 10
    """
    return run_neo4j_query(query, {"busqueda_id": busqueda_id})
