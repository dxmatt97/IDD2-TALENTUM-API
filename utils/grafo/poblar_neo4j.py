#!/usr/bin/env python3

import sys
import os
import json
from neo4j import GraphDatabase
from decouple import config

# Add project root to path to allow imports from other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from models.documental import generar_candidatos, generar_cursos, generar_busquedas

def load_data_from_json(data_dir):
    """Carga los datos desde los archivos JSON."""
    with open(os.path.join(data_dir, 'candidatos.json'), 'r', encoding='utf-8') as f:
        candidatos = json.load(f)
    with open(os.path.join(data_dir, 'cursos.json'), 'r', encoding='utf-8') as f:
        cursos = json.load(f)
    with open(os.path.join(data_dir, 'busquedas.json'), 'r', encoding='utf-8') as f:
        busquedas = json.load(f)
    return candidatos, cursos, busquedas

def poblar_neo4j():
    """
    Limpia la BD de Neo4j y la puebla usando datos consistentes desde archivos JSON,
    siguiendo un modelo de grafos enriquecido.
    """
    log = {
        "status": "in_progress",
        "operations": [],
        "counts": {
            "candidatos": 0, "cursos": 0, "busquedas": 0, "empresas": 0,
            "tecnologias": 0, "idiomas": 0, "beneficios": 0,
            "rel_tomo_curso": 0, "rel_aplica_busqueda": 0, "rel_contacto": 0,
            "rel_publica": 0, "rel_tiene_skill": 0, "rel_requiere_skill": 0
        }
    }

    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        candidatos, cursos, busquedas = load_data_from_json(data_dir)
        log["operations"].append({"step": "Carga de datos JSON", "status": "success", "details": f"Cargados {len(candidatos)} candidatos, {len(cursos)} cursos, {len(busquedas)} búsquedas."})
    except FileNotFoundError as e:
        log["status"] = "error"
        log["operations"].append({"step": "Carga de datos JSON", "status": "error", "details": f"Archivo no encontrado: {e}. Por favor, ejecute primero la población de MongoDB para generar los archivos."})
        return log

    try:
        NEO4J_URI = config("NEO4J_URI")
        NEO4J_USER = config("NEO4J_USER")
        NEO4J_PASSWORD = config("NEO4J_PASSWORD")
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        log["operations"].append({"step": "Conexión a Neo4j", "status": "success", "details": f"Conectado a {NEO4J_URI}"})
    except Exception as e:
        log["status"] = "error"
        log["operations"].append({"step": "Conexión a Neo4j", "status": "error", "details": str(e)})
        return log

    with driver.session() as session:
        try:
            session.run("MATCH (n) DETACH DELETE n")
            log["operations"].append({"step": "Limpieza de BD", "status": "success"})

            # --- Creación de Nodos Entidad Unicos (Tecnologia, Idioma, etc.) ---
            all_skills = set(skill for c in candidatos for skill in c.get('skills_tecnicos', []))
            all_skills.update(skill for b in busquedas for skill in b.get('requisitos_skills', []))
            
            for skill in all_skills:
                session.run("MERGE (:Tecnologia {nombre: $skill})", skill=skill)
            log['counts']['tecnologias'] = len(all_skills)
            
            # (Aquí se podrían añadir más nodos únicos como Idioma, Beneficio si estuvieran en los datos)

            # --- Creación de Nodos Principales (Candidato, Curso, Busqueda, Empresa) ---
            for c in candidatos:
                session.run(
                    "CREATE (c:Candidato {id: $id, nombre: $nombre, experiencia: $experiencia, seniority: $seniority})",
                    **c
                )
            log['counts']['candidatos'] = len(candidatos)

            for curso in cursos:
                session.run("CREATE (cu:Curso {id: $id, titulo: $titulo, tipo: $tipo})", **curso)
            log['counts']['cursos'] = len(cursos)

            empresas_creadas = set()
            for b in busquedas:
                if b["empresa"] not in empresas_creadas:
                    session.run("MERGE (e:Empresa {nombre: $empresa})", empresa=b["empresa"])
                    empresas_creadas.add(b["empresa"])
                session.run("CREATE (b:Busqueda {id: $id, puesto: $puesto, fecha_publicacion: $fecha_publicacion})", **b)
            log['counts']['busquedas'] = len(busquedas)
            log['counts']['empresas'] = len(empresas_creadas)
            log["operations"].append({"step": "Creación de Nodos", "status": "success"})

            # --- Creación de Relaciones ---
            # Candidato -> TIENE_SKILL -> Tecnologia
            for c in candidatos:
                for skill in c.get('skills_tecnicos', []):
                    session.run("""
                        MATCH (cand:Candidato {id: $cid}), (tech:Tecnologia {nombre: $skill})
                        CREATE (cand)-[:TIENE_SKILL]->(tech)
                    """, cid=c['id'], skill=skill)
                    log['counts']['rel_tiene_skill'] += 1

            # Busqueda -> REQUIERE_TECNOLOGIA -> Tecnologia
            for b in busquedas:
                for skill in b.get('requisitos_skills', []):
                    session.run("""
                        MATCH (busq:Busqueda {id: $bid}), (tech:Tecnologia {nombre: $skill})
                        CREATE (busq)-[:REQUIERE_TECNOLOGIA]->(tech)
                    """, bid=b['id'], skill=skill)
                    log['counts']['rel_requiere_skill'] += 1

            # Empresa -> PUBLICA -> Busqueda
            for b in busquedas:
                session.run("""
                    MATCH (e:Empresa {nombre: $empresa}), (busq:Busqueda {id: $id})
                    CREATE (e)-[:PUBLICA]->(busq)
                """, empresa=b["empresa"], id=b["id"])
                log['counts']['rel_publica'] += 1

            # Candidato -> TOMO -> Curso
            for i, c in enumerate(candidatos):
                if not cursos: continue
                curso_a_tomar = cursos[i % len(cursos)]
                session.run("""
                    MATCH (cand:Candidato {id: $cid}), (cu:Curso {id: $cuid})
                    CREATE (cand)-[:TOMO]->(cu)
                """, cid=c['id'], cuid=curso_a_tomar['id'])
                log['counts']['rel_tomo_curso'] += 1
            
            # Candidato -> APLICA_A -> Busqueda
            for i, c in enumerate(candidatos):
                 if not busquedas: continue
                 busqueda_a_aplicar = busquedas[i % len(busquedas)]
                 session.run("""
                    MATCH (cand:Candidato {id: $cid}), (busq:Busqueda {id: $bid})
                    CREATE (cand)-[:APLICA_A]->(busq)
                 """, cid=c['id'], bid=busqueda_a_aplicar['id'])
                 log['counts']['rel_aplica_busqueda'] += 1

            # Candidato -> CONTACTO -> Candidato
            for i in range(len(candidatos)):
                contacto_idx = (i + 5) % len(candidatos) # Evitar que todos contacten al siguiente
                if i == contacto_idx: continue
                session.run("""
                    MATCH (a:Candidato {id: $id_a}), (b:Candidato {id: $id_b})
                    CREATE (a)-[:CONTACTO]->(b)
                """, id_a=candidatos[i]['id'], id_b=candidatos[contacto_idx]['id'])
                log['counts']['rel_contacto'] += 1

            log["operations"].append({"step": "Creación de Relaciones", "status": "success"})
            log["status"] = "success"

        except Exception as e:
            log["status"] = "error"
            log["operations"].append({"step": "Ejecución de Cypher", "status": "error", "details": str(e)})

    driver.close()
    return log

if __name__ == "__main__":
    resultado = poblar_neo4j()
    print(json.dumps(resultado, indent=4)) 