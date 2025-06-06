from neo4j import GraphDatabase
import pandas as pd

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