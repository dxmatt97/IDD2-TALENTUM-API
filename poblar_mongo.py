from pymongo import MongoClient
from models.documental import generar_candidatos, generar_cursos, generar_busquedas

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["talentum_demo"]

# Colecciones
candidatos_col = db["candidatos"]
cursos_col = db["cursos"]
busquedas_col = db["busquedas"]

# Limpia las colecciones (opcional, para evitar duplicados en pruebas)
candidatos_col.delete_many({})
cursos_col.delete_many({})
busquedas_col.delete_many({})

# Genera datos de ejemplo
datos_candidatos = generar_candidatos(10)
datos_cursos = generar_cursos(5)
datos_busquedas = generar_busquedas(5)

# Inserta los datos en MongoDB
candidatos_col.insert_many(datos_candidatos)
cursos_col.insert_many(datos_cursos)
busquedas_col.insert_many(datos_busquedas)

# Consulta de ejemplo: mostrar todos los candidatos con 'Python' como skill técnico
result = list(candidatos_col.find({"skills.tecnicos": "Python"}))
print("Candidatos con skill Python:")
for cand in result:
    print(f"- {cand['nombre']} ({cand['id']})")

# Consulta de ejemplo: mostrar todos los cursos
print("\nCursos:")
for curso in cursos_col.find():
    print(f"- {curso['titulo']} ({curso['tipo']})")

# Consulta de ejemplo: mostrar todas las búsquedas
print("\nBúsquedas:")
for busq in busquedas_col.find():
    print(f"- {busq['empresa']} busca {busq['requisitos']}") 