import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import redis
import json
from models.keyvalue import generar_sesiones

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Limpia todas las claves de sesiones (opcional para demo)
for key in r.scan_iter("session_cand_*"):
    r.delete(key)

# Genera sesiones de ejemplo
sesiones = generar_sesiones(10)

# Inserta las sesiones en Redis
for key, value in sesiones.items():
    r.set(key, json.dumps(value))

print("Redis poblado con sesiones de ejemplo.")