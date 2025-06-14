import networkx as nx
import random
from neo4j import GraphDatabase
from models.documental import generar_candidatos, generar_cursos, generar_busquedas

def construir_grafo(candidatos, cursos, n_tomas=10, n_contactos=5):

    G = nx.DiGraph()
    for c in candidatos:
        G.add_node(c['id'], label='candidato')
    for curso in cursos:
        G.add_node(curso['id'], label='curso')
    for i in range(n_tomas):
        G.add_edge(f"cand_{i%len(candidatos):03d}", f"curso_{random.randint(0,len(cursos)-1):03d}", type='tomo')
    for i in range(n_contactos):
        origen = f"cand_{i%len(candidatos):03d}"
        destino = f"cand_{random.randint(0,len(candidatos)-1):03d}"
        if origen != destino:
            G.add_edge(origen, destino, type='contacto')
    return G

def cursos_tomados_por(G, candidato_id):
    """Devuelve los cursos tomados por un candidato (lista de nodos)."""
    return [n for n in G.successors(candidato_id) if G[candidato_id][n]['type'] == 'tomo']

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

candidatos = generar_candidatos(10)
cursos = generar_cursos(5)
busquedas = generar_busquedas(5)

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

    for c in candidatos:
        session.run(
            "CREATE (c:Candidato {id: $id, nombre: $nombre, experiencia: $experiencia, skills_tecnicos: $skills_tecnicos, skills_soft: $skills_soft})",
            id=c["id"], nombre=c["nombre"], experiencia=c["experiencia"],
            skills_tecnicos=c["skills_tecnicos"], skills_soft=c["skills_soft"]
        )

    for curso in cursos:
        session.run(
            "CREATE (cu:Curso {id: $id, titulo: $titulo, tipo: $tipo})",
            id=curso["id"], titulo=curso["titulo"], tipo=curso["tipo"]
        )

    for b in busquedas:
        session.run(
            "MERGE (e:Empresa {nombre: $empresa})", empresa=b["empresa"]
        )
        session.run(
            "CREATE (b:Busqueda {id: $id, requisitos_skills: $skills, requisitos_experiencia: $experiencia, fecha: $fecha})",
            id=b["id"], skills=b["requisitos_skills"], experiencia=b["requisitos_experiencia"], fecha=b["fecha_publicacion"]
        )
        session.run(
            "MATCH (e:Empresa {nombre: $empresa}), (b:Busqueda {id: $id}) "
            "CREATE (e)-[:PUBLICA]->(b)",
            empresa=b["empresa"], id=b["id"]
        )

    for c in candidatos:
        for curso in cursos[:2]:
            session.run(
                "MATCH (cand:Candidato {id: $cid}), (cu:Curso {id: $cuid}) "
                "CREATE (cand)-[:TOMO]->(cu)",
                cid=c["id"], cuid=curso["id"]
            )
        for b in busquedas[:2]:
            session.run(
                "MATCH (cand:Candidato {id: $cid}), (busq:Busqueda {id: $bid}) "
                "CREATE (cand)-[:APLICA_A]->(busq)",
                cid=c["id"], bid=b["id"]
            )
    for i in range(len(candidatos)-1):
        session.run(
            "MATCH (a:Candidato {id: $a}), (b:Candidato {id: $b}) "
            "CREATE (a)-[:CONTACTO]->(b)",
            a=candidatos[i]["id"], b=candidatos[i+1]["id"]
        )

print("Neo4j poblado con datos de ejemplo.") 