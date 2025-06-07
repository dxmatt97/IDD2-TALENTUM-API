from visualizations.neo4j_viz import (
    visualizar_candidatos_cursos,
    visualizar_empresas_busquedas,
    visualizar_red_contactos,
    graficar_red_contactos_neo4j
)

print("\n--- Visualización de datos reales desde Neo4j ---")
visualizar_candidatos_cursos()
visualizar_empresas_busquedas()
visualizar_red_contactos()
graficar_red_contactos_neo4j()