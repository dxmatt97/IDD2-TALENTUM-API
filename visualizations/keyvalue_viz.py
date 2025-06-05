import json

def mostrar_sesion(sesion, candidato_id):
    if sesion:
        print(f"\n[Key-Value] Sesión de {candidato_id}:")
        print(json.dumps(sesion, indent=2))
