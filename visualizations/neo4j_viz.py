from neo4j import GraphDatabase
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def visualizar_candidatos_skills():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Candidato) RETURN c.nombre AS nombre, c.skills_tecnicos AS skills_tecnicos, c.skills_soft AS skills_soft"
        )
        df = pd.DataFrame([r.data() for r in result])
        print("\nCandidatos y sus skills (Neo4j):")
        print(df)

def visualizar_candidatos_cursos():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Candidato)-[:TOMO]->(cu:Curso) "
            "RETURN c.nombre AS candidato, cu.titulo AS curso"
        )
        df = pd.DataFrame([r.data() for r in result])
        print("\nCandidatos y cursos tomados (Neo4j):")
        print(df)

def visualizar_empresas_busquedas():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(
            "MATCH (e:Empresa)-[:PUBLICA]->(b:Busqueda) "
            "RETURN e.nombre AS empresa, b.id AS busqueda_id, b.requisitos_skills AS requisitos_skills, b.requisitos_experiencia AS requisitos_experiencia"
        )
        df = pd.DataFrame([r.data() for r in result])
        print("\nEmpresas y búsquedas publicadas (Neo4j):")
        print(df)

def visualizar_busquedas():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(
            "MATCH (b:Busqueda) RETURN b.id AS id, b.requisitos_skills AS requisitos_skills, b.requisitos_experiencia AS requisitos_experiencia"
        )
        df = pd.DataFrame([r.data() for r in result])
        print("\nBúsquedas (Neo4j):")
        print(df)

def visualizar_red_contactos():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(
            "MATCH (a:Candidato)-[:CONTACTO]->(b:Candidato) "
            "RETURN a.nombre AS origen, b.nombre AS destino"
        )
        df = pd.DataFrame([r.data() for r in result])
        print("\nRed de contactos entre candidatos (Neo4j):")
        print(df)

def graficar_red_contactos_neo4j():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(
            "MATCH (a:Candidato)-[:CONTACTO]->(b:Candidato) "
            "RETURN a.nombre AS origen, b.nombre AS destino"
        )
        edges = [(r["origen"], r["destino"]) for r in result]
    G = nx.DiGraph()
    G.add_edges_from(edges)
    plt.figure(figsize=(8,6))
    nx.draw(G, with_labels=True, node_color='lightgreen', edge_color='gray', node_size=1200)
    plt.title("Red de contactos entre candidatos (Neo4j)")
    plt.show() 