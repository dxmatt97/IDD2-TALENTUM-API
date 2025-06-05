# Talentum+ Data Architecture Demo

Este proyecto es una demo modularizada de arquitectura de datos para una plataforma de gestión de talento IT, utilizando diferentes motores de bases de datos: MongoDB (documental), Neo4j (grafos), Redis (clave-valor) y un modelo tabular simulado.

## Requisitos
- Python 3.8+
- Docker (recomendado para bases de datos)

## 1. Levantar MongoDB con Docker

Si no tienes MongoDB instalado, puedes levantarlo fácilmente con Docker:

```bash
docker run -d --name mongodb -p 27017:27017 mongo:6
```

Esto iniciará un contenedor de MongoDB accesible en `localhost:27017`.

## 2. Crear y activar un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Poblar la base de datos MongoDB con datos de ejemplo

Ejecuta el script:

```bash
python poblar_mongo.py
```

Esto generará y cargará candidatos, cursos y búsquedas con datos ficticios realistas en la base de datos `talentum_demo`.

## 5. Ejecutar la demo principal

```bash
python main.py
```

Esto mostrará ejemplos de consultas y visualizaciones para cada modelo de datos.

## 6. (Opcional) Levantar Neo4j y Redis con Docker

Si quieres probar los otros motores:

```bash
# Neo4j
docker run -d --name neo4j -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5

# Redis
docker run -d --name redis -p 6379:6379 redis:7
```

---

**¡Listo!**
Puedes modificar los scripts y modelos para adaptarlos a tus necesidades o hacer pruebas con tus propios datos.