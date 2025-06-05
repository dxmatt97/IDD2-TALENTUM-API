import matplotlib.pyplot as plt
import networkx as nx

def mostrar_cursos_tomados(G, candidato_id, cursos_tomados):
    if cursos_tomados:
        plt.figure(figsize=(6,4))
        subG = G.subgraph([candidato_id] + cursos_tomados)
        pos = nx.spring_layout(subG)
        nx.draw(subG, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1200)
        plt.title(f"Cursos tomados por {candidato_id}")
        plt.show()
