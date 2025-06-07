from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

with driver.session() as session:
    # Candidatos y sus cursos
    result = session.run(
        "MATCH (c:Candidato)-[:TOMO]->(cu:Curso) "
        "RETURN c.nombre AS candidato, cu.titulo AS curso"
    )
    df = pd.DataFrame([r.data() for r in result])
    print("\nCandidatos y cursos tomados:")
    print(df)

    # Empresas y búsquedas publicadas
    result = session.run(
        "MATCH (e:Empresa)-[:PUBLICA]->(b:Busqueda) "
        "RETURN e.nombre AS empresa, b.id AS busqueda_id, b.requisitos AS requisitos"
    )
    df = pd.DataFrame([r.data() for r in result])
    print("\nEmpresas y búsquedas publicadas:")
    print(df)

    # Red de contactos
    result = session.run(
        "MATCH (a:Candidato)-[:CONTACTO]->(b:Candidato) "
        "RETURN a.nombre AS origen, b.nombre AS destino"
    )
    df = pd.DataFrame([r.data() for r in result])
    print("\nRed de contactos entre candidatos:")
    print(df)

def mostrar_cursos_tomados(G, candidato_id, cursos_tomados):
    if cursos_tomados:
        plt.figure(figsize=(6,4))
        subG = G.subgraph([candidato_id] + cursos_tomados)
        pos = nx.spring_layout(subG)
        nx.draw(subG, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1200)
        plt.title(f"Cursos tomados por {candidato_id}")
        plt.show()