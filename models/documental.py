import random
from datetime import datetime, timedelta

# Lista de nombres y apellidos ficticios realistas
NOMBRES = [
    "Juan Pérez", "María García", "Carlos López", "Ana Fernández", "Lucía Martínez",
    "Pedro Gómez", "Sofía Díaz", "Martín Torres", "Valentina Romero", "Diego Ruiz"
]

# Lista de nombres de cursos ficticios realistas
CURSOS = [
    "Python para Principiantes", "Java Avanzado", "Desarrollo Web con JavaScript", "SQL y Bases de Datos",
    "Docker y DevOps", "Machine Learning Básico", "Frontend con React", "Backend con Node.js",
    "Introducción a la Ciencia de Datos", "Metodologías Ágiles"
]

# Lista de empresas ficticias realistas
EMPRESAS = [
    "TechSolutions", "InnovaSoft", "DataCorp", "CloudNet", "VisionIT",
    "NextGenApps", "SoftWorks", "DigitalMind", "CodeFactory", "SmartSystems"
]

# -----------------------------
# Modelo Documental: Candidatos, Cursos, Búsquedas
# -----------------------------
def generar_candidatos(n=10):
    return [
        {
            "id": f"cand_{i:03d}",
            "nombre": NOMBRES[i % len(NOMBRES)],
            "experiencia": random.sample(["Backend", "Frontend", "Data Science", "DevOps", "Mobile"], 2),
            "skills": {
                "tecnicos": random.sample(["Python", "Java", "JavaScript", "SQL", "Docker"], 3),
                "soft": random.sample(["Comunicación", "Liderazgo", "Resolución de problemas", "Trabajo en equipo"], 2)
            },
            "procesos_seleccion": [],
            "historial_cambios": []
        }
        for i in range(n)
    ]

def generar_cursos(n=5):
    return [
        {
            "id": f"curso_{i:03d}",
            "titulo": CURSOS[i % len(CURSOS)],
            "tipo": random.choice(["PDF", "video", "clase"]),
            "contenido": f"Contenido del curso {i}",
        }
        for i in range(n)
    ]

def generar_busquedas(n=5):
    return [
        {
            "id": f"busq_{i:03d}",
            "empresa": EMPRESAS[i % len(EMPRESAS)],
            "requisitos": {
                "skills": random.sample(["Python", "Java", "Docker", "SQL"], 2),
                "experiencia": random.choice(["Backend", "Frontend", "Data Science"])
            },
            "fecha_publicacion": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        }
        for i in range(n)
    ]

def candidatos_con_skill(candidatos, skill):
    """Devuelve candidatos que tengan el skill técnico dado."""
    return [c for c in candidatos if skill in c['skills']['tecnicos']] 