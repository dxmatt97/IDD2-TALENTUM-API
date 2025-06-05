import random
from datetime import datetime, timedelta
import pandas as pd

# -----------------------------
# Modelo Tabular: Procesos de Selección
# -----------------------------
def generar_procesos_seleccion(n=10):
    return [
        {
            "proceso_id": f"proc_{i:03d}",
            "candidato_id": f"cand_{i:03d}",
            "estado_actual": random.choice(["preselección", "entrevista", "técnica", "propuesta", "rechazo"]),
            "fecha_ultima_accion": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            "notas_confidenciales": random.choice(["Confidencial", "Buen desempeño", "Faltó experiencia"])
        }
        for i in range(n)
    ]

def filtrar_por_estado(procesos, estado):
    """Devuelve un DataFrame con los procesos en el estado dado."""
    df = pd.DataFrame(procesos)
    return df[df['estado_actual'] == estado] 