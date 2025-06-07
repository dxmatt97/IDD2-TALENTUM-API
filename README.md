# Talentum+ Data Architecture Demo

Este proyecto es una demo interactiva de una arquitectura de datos para una plataforma de gestión de talento IT, utilizando MongoDB, Neo4j y un backend de FastAPI con una interfaz en React.

## Requisitos
- Python 3.8+
- Node.js 16+
- Docker (recomendado para bases de datos)

## 1. Levantar las bases de datos (con Docker)

Abre una terminal y ejecuta los siguientes comandos para iniciar los contenedores de las bases de datos:

### MongoDB
```bash
docker run -d --name mongodb -p 27017:27017 mongo:6
```

### Neo4j
```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5
```
- **Interfaz web:** http://localhost:7474 (usuario: `neo4j`, contraseña: `password`)
- **Conexión Bolt:** bolt://localhost:7687 

## 2. Configurar el Backend (API)

### a. Crear y activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### b. Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

### c. Crear archivo de entorno
Crea un archivo llamado `.env` en la raíz del proyecto con las siguientes variables:
```
MONGO_URI="mongodb://localhost:27017/"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"
```

### d. Iniciar el servidor de la API
```bash
uvicorn api:app --reload
```
La API estará disponible en `http://localhost:8000`.

## 3. Configurar el Frontend

### a. Navegar a la carpeta del frontend
```bash
cd talentum-frontend
```

### b. Instalar dependencias de Node.js
```bash
npm install
```

### c. Iniciar la aplicación de React
```bash
npm start
```
La aplicación se abrirá automáticamente en `http://localhost:3000`.

## 4. Usar la Demo

Una vez que el frontend y el backend estén en ejecución, abre tu navegador en `http://localhost:3000`.

Desde la interfaz web, podrás:
- **Poblar las bases de datos:** Usa las tarjetas en la sección "Administración" para limpiar y llenar MongoDB y Neo4j con datos de prueba consistentes.
- **Ejecutar consultas:** Explora las diferentes tarjetas para realizar consultas GET, PUT, POST y DELETE a la API, viendo los resultados en tiempo real.
- **Entender la arquitectura:** Cada tarjeta muestra el modelo de datos, la consulta y el endpoint de la API que se está utilizando.