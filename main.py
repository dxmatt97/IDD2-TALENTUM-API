# -----------------------------
# Talentum+ Data Architecture Demo (Modularizado)
# -----------------------------
# Este script orquesta la generación, consulta y visualización de los modelos:
# - Documental
# - Tabular
# - Grafo
# - Clave-Valor

from models.documental import generar_candidatos, generar_cursos, generar_busquedas, candidatos_con_skill
from models.tabular import generar_procesos_seleccion, filtrar_por_estado
from models.grafo import construir_grafo, cursos_tomados_por
from models.keyvalue import generar_sesiones, obtener_sesion
from visualizations.documental_viz import mostrar_candidatos_con_skill
from visualizations.tabular_viz import mostrar_procesos_filtrados
from visualizations.grafo_viz import mostrar_cursos_tomados
from visualizations.keyvalue_viz import mostrar_sesion

# -----------------------------
# 1. Documental
# -----------------------------
candidatos = generar_candidatos()
cursos = generar_cursos()
busquedas = generar_busquedas()
candidatos_python = candidatos_con_skill(candidatos, 'Python')
mostrar_candidatos_con_skill(candidatos_python, 'Python')

# -----------------------------
# 2. Tabular
# -----------------------------
procesos = generar_procesos_seleccion()
entrevista_df = filtrar_por_estado(procesos, 'entrevista')
mostrar_procesos_filtrados(entrevista_df, 'entrevista')

# -----------------------------
# 3. Grafo
# -----------------------------
G = construir_grafo(candidatos, cursos)
cursos_cand_001 = cursos_tomados_por(G, 'cand_001')
mostrar_cursos_tomados(G, 'cand_001', cursos_cand_001)

# -----------------------------
# 4. Clave-Valor
# -----------------------------
sesiones = generar_sesiones()
sesion_cand_001 = obtener_sesion(sesiones, 'cand_001')
mostrar_sesion(sesion_cand_001, 'cand_001')

