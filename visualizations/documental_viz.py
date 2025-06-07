import pandas as pd
from pymongo import MongoClient
from models.documental import generar_procesos_seleccion_documental

def mostrar_candidatos_con_skill(candidatos, skill):
    df = pd.DataFrame(candidatos)
    if not df.empty:
        try:
            import ace_tools as tools
            tools.display_dataframe_to_user(name=f"Candidatos con skill {skill}", dataframe=df)
        except ImportError:
            print(f"Candidatos con skill {skill}:")
            print(df)

def mostrar_cursos(cursos):
    df = pd.DataFrame(cursos)
    if not df.empty:
        try:
            import ace_tools as tools
            tools.display_dataframe_to_user(name="Cursos", dataframe=df)
        except ImportError:
            print("Cursos:")
            print(df)

def mostrar_busquedas(busquedas):
    df = pd.DataFrame(busquedas)
    if not df.empty:
        try:
            import ace_tools as tools
            tools.display_dataframe_to_user(name="Búsquedas", dataframe=df)
        except ImportError:
            print("Búsquedas:")
            print(df)

def mostrar_procesos_filtrados(df, estado):
    if not df.empty:
        try:
            import ace_tools as tools
            tools.display_dataframe_to_user(name=f"Procesos en estado {estado}", dataframe=df)
        except ImportError:
            print(f"Procesos en estado {estado}:")
            print(df)

def mostrar_procesos_seleccion(procesos):
    df = pd.DataFrame(procesos)
    if not df.empty:
        try:
            import ace_tools as tools
            tools.display_dataframe_to_user(name="Procesos de Selección", dataframe=df)
        except ImportError:
            print("Procesos de Selección:")
            print(df)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["talentum_demo"]

# Recuperar datos reales de cada colección
candidatos = list(db["candidatos"].find())
cursos = list(db["cursos"].find())
busquedas = list(db["busquedas"].find())

# Mostrar candidatos con skill 'Python'
candidatos_python = [c for c in candidatos if 'skills_tecnicos' in c and 'Python' in c.get('skills_tecnicos', [])]
if not candidatos_python:
    print("No se encontraron candidatos con el campo 'skills_tecnicos' o con el skill 'Python'.")
mostrar_candidatos_con_skill(candidatos_python, 'Python')

# Mostrar todos los cursos
mostrar_cursos(cursos)

# Mostrar todas las búsquedas
mostrar_busquedas(busquedas)

# Clean MongoDB collections
db["candidatos"].delete_many({})
db["busquedas"].delete_many({})

# Poblar procesos de selección
procesos = generar_procesos_seleccion_documental(10)
db["procesos_seleccion"].delete_many({})
db["procesos_seleccion"].insert_many(procesos)

# Mostrar procesos de selección
procesos_mongo = list(db["procesos_seleccion"].find())
mostrar_procesos_seleccion(procesos_mongo)
 