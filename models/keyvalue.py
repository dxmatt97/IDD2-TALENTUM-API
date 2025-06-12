from datetime import datetime, timedelta

def generar_sesiones(n=10):
    return {
        f"session_cand_{i:03d}": {
            "token": f"token_{i:06d}",
            "expira": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        for i in range(n)
    }

def obtener_sesion(sesiones, candidato_id):
    return sesiones.get(f'session_{candidato_id}') 