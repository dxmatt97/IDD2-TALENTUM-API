import redis
import json

def mostrar_sesiones_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    print("\nSesiones en Redis:")
    for key in r.scan_iter("session_cand_*"):
        value = r.get(key)
        print(f"{key.decode()}: {json.loads(value)}")

def mostrar_sesion(sesion, candidato_id=None):
    if sesion:
        if candidato_id:
            print(f"\n[Key-Value] Sesión de {candidato_id}:")
        else:
            print("\n[Key-Value] Sesión:")
        print(json.dumps(sesion, indent=2))
    else:
        print("No se encontró la sesión.")