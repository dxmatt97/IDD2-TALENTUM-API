from pymongo import MongoClient
from decouple import config
import sys
import os
import json

# Agrega el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from models.documental import generar_candidatos, generar_cursos, generar_busquedas, generar_procesos_seleccion_documental

# --- Configuración de la Conexión ---
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["talentum_demo"]

def poblar_mongodb():
    """
    Limpia y puebla las colecciones, devolviendo un log estructurado.
    """
    logs = {"pasos": [], "summary": {}}
    
    # --- Limpieza de Colecciones ---
    colecciones = ["candidatos", "cursos", "busquedas", "procesos_seleccion"]
    for col in colecciones:
        db[col].delete_many({})
        logs["pasos"].append({"paso": f"Limpieza de colección '{col}'", "status": "completado"})

    # --- Generación de Datos ---
    candidatos = generar_candidatos(50)
    cursos = generar_cursos(15)
    busquedas = generar_busquedas(20)
    procesos = generar_procesos_seleccion_documental(50)
    logs["pasos"].append({"paso": "Generación de datos de prueba", "status": "completado"})

    # --- Guardar datos generados a archivos JSON ---
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, 'candidatos.json'), 'w', encoding='utf-8') as f:
        json.dump(candidatos, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, 'cursos.json'), 'w', encoding='utf-8') as f:
        json.dump(cursos, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, 'busquedas.json'), 'w', encoding='utf-8') as f:
        json.dump(busquedas, f, ensure_ascii=False, indent=2)
    logs["pasos"].append({"paso": "Guardado de datos en archivos JSON", "status": "completado"})

    # --- Inserción de Datos ---
    db.candidatos.insert_many(candidatos)
    logs["pasos"].append({"paso": "Inserción en 'candidatos'", "documentos": len(candidatos)})
    
    db.cursos.insert_many(cursos)
    logs["pasos"].append({"paso": "Inserción en 'cursos'", "documentos": len(cursos)})

    db.busquedas.insert_many(busquedas)
    logs["pasos"].append({"paso": "Inserción en 'busquedas'", "documentos": len(busquedas)})

    db.procesos_seleccion.insert_many(procesos)
    logs["pasos"].append({"paso": "Inserción en 'procesos_seleccion'", "documentos": len(procesos)})

    # --- Resumen ---
    logs["summary"] = {
        "candidatos": len(candidatos),
        "cursos": len(cursos),
        "busquedas": len(busquedas),
        "procesos_seleccion": len(procesos),
        "total_documentos": len(candidatos) + len(cursos) + len(busquedas) + len(procesos)
    }
    
    return logs

if __name__ == "__main__":
    try:
        resultado = poblar_mongodb()
        # Imprime el JSON a stdout para que el subprocess lo pueda capturar
        print(json.dumps(resultado, indent=2))
    except Exception as e:
        error_msg = {"error": True, "message": str(e)}
        print(json.dumps(error_msg, indent=2))
        sys.exit(1) 