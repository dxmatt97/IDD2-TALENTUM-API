import redis
import json

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Recupera todas las sesiones
print("\nSesiones en Redis:")
for key in r.scan_iter("session_cand_*"):
    value = r.get(key)
    print(f"{key.decode()}: {json.loads(value)}")