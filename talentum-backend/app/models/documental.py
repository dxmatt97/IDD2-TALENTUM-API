import random
from datetime import datetime, timedelta

# --- Listas de datos ampliadas para mayor variedad ---
NOMBRES = [
    "Juan Pérez", "María García", "Carlos López", "Ana Fernández", "Lucía Martínez",
    "Pedro Gómez", "Sofía Díaz", "Martín Torres", "Valentina Romero", "Diego Ruiz",
    "Javier Hernández", "Laura Sánchez", "Miguel González", "Elena Ramírez", "David Castillo",
    "Paula Núñez", "Marcos Alonso", "Isabel Vidal", "Daniel Vega", "Clara Moreno"
]

CURSOS = [
    "Python para Data Science", "Java Spring Boot Masterclass", "Desarrollo Web Fullstack", "SQL y Optimización de Consultas",
    "Docker & Kubernetes: Guía Completa", "Machine Learning con Scikit-Learn", "React: De Cero a Experto", "Backend con Go y Gin",
    "Introducción a la Inteligencia Artificial", "Metodologías Ágiles y Scrum", "Ciberseguridad Defensiva", "Bases de Datos NoSQL",
    "Desarrollo de APIS con FastAPI", "Microservicios con .NET Core", "Flutter para Desarrollo Móvil"
]

EMPRESAS = [
    "TechSolutions", "InnovaSoft", "DataCorp", "CloudNet", "VisionIT",
    "NextGenApps", "SoftWorks", "DigitalMind", "CodeFactory", "SmartSystems",
    "QuantumLeap", "DataDriven", "AgileInnovations", "NexusTech", "ByteForge"
]

SKILLS = [
    "Python", "Java", "JavaScript", "SQL", "Docker", "AWS", "React", "Node.js", "Go", "C#", 
    "TypeScript", "PostgreSQL", "MongoDB", "Kubernetes", "Terraform", "FastAPI"
]

EXPERIENCIA = ["Backend", "Frontend", "Data Science", "DevOps", "Mobile", "Cybersecurity", "QA Automation", "Cloud Engineering"]

SENIORITY = ["Junior", "Junior Avanzado", "Semi-Senior", "Senior", "Staff Engineer", "Principal Engineer"]

IDIOMAS = ["Inglés B2", "Inglés C1", "Español Nativo", "Portugués B1", "Alemán A2", "Inglés A2"]

BENEFICIOS = [
    "Home office", "Capacitaciones pagas", "Bono anual por desempeño", "Gimnasio", 
    "Horario flexible", "Clases de inglés", "OSDE 310", "Vacaciones extendidas"
]

# -----------------------------
# Modelo Documental: Candidatos, Cursos, Búsquedas
# -----------------------------
def generar_candidatos(n=50):
    return [
        {
            "id": f"cand_{i:03d}",
            "nombre": random.choice(NOMBRES),
            "experiencia": random.sample(EXPERIENCIA, k=random.randint(1, 3)),
            "skills_tecnicos": random.sample(SKILLS, k=random.randint(3, 6)),
            "skills_soft": random.sample(["Comunicación", "Liderazgo", "Resolución de problemas", "Trabajo en equipo", "Adaptabilidad"], k=2),
            "idiomas": random.sample(IDIOMAS, k=random.randint(1, 2)),
            "seniority": random.choice(SENIORITY),
            "procesos_seleccion": [],
            "historial_cambios": []
        }
        for i in range(n)
    ]

def generar_cursos(n=15):
    return [
        {
            "id": f"curso_{i:03d}",
            "titulo": random.choice(CURSOS),
            "tipo": random.choice(["PDF", "video", "clase online", "tutorial interactivo"]),
            "contenido": f"Contenido detallado y práctico del curso {i}...",
        }
        for i in range(n)
    ]

def generar_busquedas(n=20):
    puestos = ["Desarrollador Backend", "Frontend Developer", "Data Scientist", "DevOps Engineer", "Project Manager", "Cloud Architect", "QA Tester"]
    return [
        {
            "id": f"busq_{i:03d}",
            "empresa": random.choice(EMPRESAS),
            "puesto": random.choice(puestos),
            "requisitos_skills": random.sample(SKILLS, k=random.randint(2, 4)),
            "requisitos_experiencia": random.choice(EXPERIENCIA),
            "requisitos_idioma": random.sample(IDIOMAS[:3], k=random.randint(1, 2)),
            "beneficios": random.sample(BENEFICIOS, k=random.randint(2, 4)),
            "seniority_requerido": random.choice(SENIORITY[:4]), # Enfocado en roles hasta Senior
            "fecha_publicacion": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
        }
        for i in range(n)
    ]

def candidatos_con_skill(candidatos, skill):
    """Devuelve candidatos que tengan el skill técnico dado."""
    return [c for c in candidatos if skill in c['skills_tecnicos']]

def generar_procesos_seleccion_documental(n=50):
    procesos = []
    estados = ["preselección", "entrevista", "técnica", "propuesta", "rechazo", "contratado"]
    for i in range(n):
        historial = []
        fecha_base = datetime.now() - timedelta(days=random.randint(10, 60))
        num_estados = random.randint(1, len(estados))
        for j in range(num_estados):
            historial.append({
                "estado": estados[j],
                "fecha": (fecha_base + timedelta(days=j*3)).strftime('%Y-%m-%d')
            })
        entrevistas = [
            {
                "fecha": (fecha_base + timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d'),
                "evaluador": f"Evaluador_{random.randint(1,5)}",
                "notas_confidenciales": random.choice(["Excelente desempeño técnico.", "Faltó profundidad en el área de sistemas distribuidos.", "Perfil cultural muy bueno."])
            }
            for _ in range(random.randint(0, 3))
        ]
        feedback = [
            {
                "autor": random.choice(["RRHH", "Manager", "Tech Lead", "Peer Interviewer"]),
                "comentario": random.choice(["Candidato altamente recomendado.", "Requiere desarrollo en habilidades de liderazgo.", "Sólido perfil técnico."]),
                "fecha": (fecha_base + timedelta(days=random.randint(1, 15))).strftime('%Y-%m-%d')
            }
            for _ in range(random.randint(0, 3))
        ]
        procesos.append({
            "id": f"proc_{i:03d}",
            "candidato_id": f"cand_{i:03d}",
            "busqueda_id": f"busq_{random.randint(0, 19):03d}",
            "estado_actual": historial[-1]['estado'],
            "fecha_ultima_accion": historial[-1]['fecha'],
            "historial_estados": historial,
            "entrevistas": entrevistas,
            "feedback": feedback
        })
    return procesos 