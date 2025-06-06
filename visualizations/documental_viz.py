import pandas as pd
from pymongo import MongoClient

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

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["talentum_demo"]

# Recuperar datos reales de cada colección
candidatos = list(db["candidatos"].find())
cursos = list(db["cursos"].find())
busquedas = list(db["busquedas"].find())

# Mostrar candidatos con skill 'Python'
candidatos_python = [c for c in candidatos if 'Python' in c['skills']['tecnicos']]
mostrar_candidatos_con_skill(candidatos_python, 'Python')

# Mostrar todos los cursos
mostrar_cursos(cursos)

# Mostrar todas las búsquedas
mostrar_busquedas(busquedas)
