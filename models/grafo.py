import networkx as nx
import random

def construir_grafo(candidatos, cursos, n_tomas=10, n_contactos=5):
    """
    Construye un grafo dirigido con:
    - Nodos: candidatos y cursos
    - Aristas: 'tomo' (candidato->curso), 'contacto' (candidato->candidato)
    """
    G = nx.DiGraph()
    for c in candidatos:
        G.add_node(c['id'], label='candidato')
    for curso in cursos:
        G.add_node(curso['id'], label='curso')
    # Relaciones 'tomo'
    for i in range(n_tomas):
        G.add_edge(f"cand_{i%len(candidatos):03d}", f"curso_{random.randint(0,len(cursos)-1):03d}", type='tomo')
    # Relaciones 'contacto'
    for i in range(n_contactos):
        origen = f"cand_{i%len(candidatos):03d}"
        destino = f"cand_{random.randint(0,len(candidatos)-1):03d}"
        if origen != destino:
            G.add_edge(origen, destino, type='contacto')
    return G

def cursos_tomados_por(G, candidato_id):
    """Devuelve los cursos tomados por un candidato (lista de nodos)."""
    return [n for n in G.successors(candidato_id) if G[candidato_id][n]['type'] == 'tomo'] 