# Talentum+ Data Architecture Demo

Este proyecto es una demo modularizada de arquitectura de datos para una plataforma de gestión de talento IT, utilizando diferentes motores de bases de datos: MongoDB (documental), Neo4j (grafos), Redis (clave-valor).

## Requisitos
- Python 3.8+
- Docker (recomendado para bases de datos)

## 1. Levantar las bases de datos con Docker

### MongoDB
```bash
docker run -d --name mongodb -p 27017:27017 mongo:6
```
Esto iniciará un contenedor de MongoDB accesible en `localhost:27017`.

### Neo4j
```bash
docker run -d --name neo4j -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5
```
Esto iniciará Neo4j en:
- http://localhost:7474 (interfaz web, usuario: `neo4j`, contraseña: `password`)
- bolt://localhost:7687 (para conexión desde Python)

### Redis
```bash
docker run -d --name redis -p 6379:6379 redis:7
```
Esto iniciará Redis en `localhost:6379`.

## 2. Crear y activar un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Poblar y visualizar datos en MongoDB

Ejecuta el script:
```bash
python main.py
```
Esto generará y mostrará candidatos, cursos y búsquedas con datos ficticios realistas en la base de datos `talentum_demo`.

## 5. Poblar y visualizar datos en Neo4j

El script `models/grafo.py` pobla Neo4j automáticamente al ejecutarse como parte de la demo. Para visualizar los datos reales de Neo4j, puedes usar:
```bash
python -c "from visualizations.neo4j_viz import visualizar_candidatos_skills, visualizar_candidatos_cursos, visualizar_empresas_busquedas, visualizar_busquedas, visualizar_red_contactos, graficar_red_contactos_neo4j; visualizar_candidatos_skills(); visualizar_candidatos_cursos(); visualizar_empresas_busquedas(); visualizar_busquedas(); visualizar_red_contactos(); graficar_red_contactos_neo4j()"
```
O bien, llama a las funciones desde un script o notebook.

## 6. Poblar y visualizar datos en Redis

Para poblar Redis con sesiones de ejemplo:
```bash
python utils/clave_valor/poblar_redis.py
```
Para visualizar las sesiones almacenadas:
```bash
python utils/clave_valor/visualizar_redis.py
```