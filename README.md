#  Proyecto de Integración Continua – Sistema de Gestión de Tareas

## Descripción
Este proyecto implementa un **sistema de gestión de tareas** utilizando una arquitectura basada en **contenedores Docker**.  
Incluye tres servicios principales:
- **Frontend:** Aplicación web desarrollada en Angular 20
- **Backend:** API REST desarrollada en Flask (Python)
- **Base de datos:** MySQL 8.0

El objetivo es demostrar la comunicación entre contenedores dentro del entorno Docker y la implementación de CI/CD con Jenkins como parte del módulo *Énfasis Profesional I - Integración Continua* del Politécnico Grancolombiano.

---

## 🚀 Inicio Rápido

¿Quieres ejecutar el proyecto inmediatamente? Sigue estos pasos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Sulay2549/integracion-continua-proyecto-final.git
cd integracion-continua-proyecto-final

# 2. Ejecutar con Docker Compose
docker-compose up -d

# 3. Verificar que funciona
curl http://localhost:5000
curl http://localhost:5000/test-db
```

✅ **¡Listo!** El backend estará disponible en [http://localhost:5000](http://localhost:5000)

> 💡 El archivo `.env` ya está configurado con valores que funcionan. No necesitas configurar nada más.

---

##  Estructura del Proyecto

```
integracion-continua-proyecto-final/
├── .git/
├── .gitignore
├── .env                            # Variables de entorno
├── .env.example                    # Plantilla de variables de entorno
├── docker-compose.yml              # Orquestación de servicios
├── Jenkinsfile                     # Pipeline de CI/CD
├── README.md
│
├── backend/                        # API REST en Flask
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt        # Dependencias de testing
│   ├── pytest.ini                  # Configuración de pytest
│   ├── run.py                      # Punto de entrada
│   ├── app/
│   │   ├── __init__.py             # Configuración de Flask y logging
│   │   ├── config.py               # Variables de configuración
│   │   ├── database.py             # Conexión a MySQL
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── tareas_model.py     # Modelo de datos de Tareas
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── tareas_routes.py    # Endpoints de la API
│   ├── tests/                      # Pruebas automatizadas
│   │   ├── conftest.py             # Fixtures compartidas
│   │   ├── unit/                   # 29 pruebas unitarias
│   │   │   ├── test_tareas_model.py
│   │   │   └── test_database.py
│   │   ├── integration/            # 28 pruebas de integración
│   │   │   ├── test_tareas_api.py
│   │   │   └── test_system_routes.py
│   │   └── functional/             # 8 pruebas funcionales
│   │       └── test_tareas_workflow.py
│   └── reports/                    # Reportes de tests (generados)
│
├── frontend/                       # Aplicación Angular
│   ├── Dockerfile
│   ├── package.json
│   ├── angular.json
│   ├── tsconfig.json
│   ├── public/
│   └── src/
│       ├── index.html
│       ├── main.ts
│       ├── styles.scss
│       └── app/
│           ├── app.ts
│           ├── app.html
│           ├── app.routes.ts
│           └── services/
│               └── api.ts          # Servicio de comunicación con backend
│
└── database/                       # Scripts de base de datos
    └── init.sql                    # Esquema inicial de la BD
```

---

## 🗄️ Esquema de Base de Datos

El sistema cuenta con 4 tablas principales:

### **usuarios**
Gestión de usuarios del sistema con roles (usuario/administrador).

| Campo | Tipo | Descripción |
|-------|------|-------------|
| idusuario | INT | ID único del usuario |
| nombre | VARCHAR(100) | Nombre del usuario |
| correo | VARCHAR(100) | Correo electrónico |
| contraseña | VARCHAR(100) | Contraseña (debe hashearse en producción) |
| rol | ENUM | 'usuario' o 'administrador' |
| fechaCreacion | DATE | Fecha de creación del usuario |

### **proyectos**
Proyectos que agrupan tareas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| idproyecto | INT | ID único del proyecto |
| nombre | VARCHAR(100) | Nombre del proyecto |
| descripcion | VARCHAR(250) | Descripción del proyecto |
| fechaInicio | DATE | Fecha de inicio |
| fechaFin | DATE | Fecha de finalización |
| idLider | INT | ID del usuario líder (FK) |

### **tareas**
Tareas individuales con estado y prioridad.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| idTarea | INT | ID único de la tarea |
| titulo | VARCHAR(100) | Título de la tarea |
| descripcion | VARCHAR(250) | Descripción detallada |
| estado | ENUM | 'Pendiente', 'En progreso', 'Completada', 'Cancelada' |
| prioridad | ENUM | 'Baja', 'Media', 'Alta' |
| fechaCreacion | DATE | Fecha de creación |
| fechaLimite | DATE | Fecha límite |
| idProyecto | INT | ID del proyecto (FK) |

### **asignaciones**
Relación entre usuarios y tareas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| idasignaciones | INT | ID único de la asignación |
| idTarea | INT | ID de la tarea (FK) |
| idUsuario | INT | ID del usuario (FK) |
| fechaAsignacion | DATE | Fecha de asignación |

---

## 🚀 API REST - Endpoints

### Base URL
```
http://localhost:5000
```

### Endpoints Disponibles

#### 1. **GET /** - Verificar estado de la API
```bash
curl http://localhost:5000/
```
**Respuesta:**
```json
{
  "messages": "API del Sistema de Gestión de Tareas en ejecución"
}
```

#### 2. **GET /test-db** - Verificar conexión a base de datos
```bash
curl http://localhost:5000/test-db
```
**Respuesta:**
```json
{
  "status": "ok",
  "database": "integracion_continua_db"
}
```

#### 3. **GET /api/tareas/** - Listar todas las tareas
```bash
curl http://localhost:5000/api/tareas/
```
**Parámetros opcionales:**
- `id`: Filtrar por ID de tarea
- `titulo`: Buscar por título (búsqueda parcial)
- `descripcion`: Buscar por descripción (búsqueda parcial)

**Ejemplo con filtros:**
```bash
curl "http://localhost:5000/api/tareas/?titulo=Implementar"
```

**Respuesta exitosa:**
```json
[
  {
    "idTarea": 1,
    "titulo": "Implementar login",
    "descripcion": "Crear sistema de autenticación",
    "estado": "En progreso",
    "prioridad": "Alta",
    "fechaCreacion": "2025-11-25",
    "fechaLimite": "2025-12-01",
    "idProyecto": 1
  }
]
```

#### 4. **POST /api/tareas/** - Crear nueva tarea
```bash
curl -X POST http://localhost:5000/api/tareas/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Nueva tarea",
    "descripcion": "Descripción de la tarea",
    "estado": "Pendiente",
    "prioridad": "Alta",
    "fechaLimite": "2025-12-31",
    "idProyecto": 1
  }'
```

**Campos:**
- `titulo` ✅ **requerido** (max 100 caracteres)
- `descripcion` (opcional, max 250 caracteres)
- `estado` (opcional): `Pendiente`, `En progreso`, `Completada`, `Cancelada` (default: `Pendiente`)
- `prioridad` (opcional): `Baja`, `Media`, `Alta` (default: `Media`)
- `fechaLimite` (opcional, formato: YYYY-MM-DD)
- `idProyecto` (opcional)

**Validaciones implementadas:**
- ✅ Título es requerido
- ✅ Longitud máxima de campos
- ✅ Valores válidos para estado y prioridad
- ✅ Mensajes de error descriptivos

**Respuesta exitosa:**
```json
{
  "mensaje": "Tarea creada exitosamente",
  "id": 5
}
```

**Respuesta de error:**
```json
{
  "error": "El campo 'titulo' es requerido"
}
```

#### 5. **PUT /api/tareas/<id>** - Actualizar tarea existente
```bash
curl -X PUT http://localhost:5000/api/tareas/5 \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Completada",
    "prioridad": "Baja"
  }'
```

**Respuesta exitosa:**
```json
{
  "mensaje": "Tarea con ID 5 actualizada exitosamente"
}
```

#### 6. **DELETE /api/tareas/<id>** - Eliminar tarea
```bash
curl -X DELETE http://localhost:5000/api/tareas/5
```

**Respuesta exitosa:**
```json
{
  "mensaje": "Tarea con ID 5 eliminada exitosamente"
}
```

---

## ⚙️ Configuración de Variables de Entorno

El proyecto utiliza un archivo `.env` para gestionar las credenciales y configuración. Docker Compose lee automáticamente este archivo al ejecutar `docker-compose up`.

### Archivos de Configuración

**`.env`** (Archivo activo)
- Contiene las credenciales **reales** que usa el proyecto
- Ya está incluido en el repositorio con valores por defecto funcionales
- Es el archivo que Docker Compose lee automáticamente

**`.env.example`** (Plantilla)
- Contiene **placeholders** como ejemplo
- Sirve como referencia para saber qué variables configurar
- Útil para restaurar configuración o para otros desarrolladores

### Valores Actuales en `.env`

El archivo `.env` incluido tiene estos valores por defecto que **ya funcionan**:

```bash
# Configuración de MySQL (Servicio db)
MYSQL_ROOT_PASSWORD=12345
MYSQL_DATABASE=integracion_continua_db
MYSQL_USER=user
MYSQL_PASSWORD=12345

# Configuración de Backend (Servicio backend)
DB_HOST=db
DB_USER=root
DB_PASSWORD=12345
DB_NAME=integracion_continua_db
FLASK_ENV=development

# Configuración de Frontend (Servicio frontend)
CHOKIDAR_USEPOLLING=true
```

### Personalizar Credenciales (Opcional)

Si deseas cambiar las credenciales, edita directamente el archivo `.env`:

```bash
# Ejemplo de credenciales personalizadas
MYSQL_ROOT_PASSWORD=mi_password_seguro_2025
MYSQL_PASSWORD=otra_password_segura
DB_PASSWORD=mi_password_seguro_2025
```

### Restaurar Configuración

Si necesitas restaurar el archivo `.env` desde la plantilla:

```bash
# Linux/Mac
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Luego edita `.env` y reemplaza los placeholders con tus valores reales.

> 💡 **Nota:** El archivo `.env` ya existe con valores funcionales. Solo necesitas copiarlo desde `.env.example` si lo eliminaste o quieres empezar de cero.

---

##  Ejecución del Proyecto

### Requisitos Previos
- Docker y Docker Compose instalados
- Puertos 3306, 5000 y 4200 disponibles

### 1. Clonar el repositorio
```bash
git clone https://github.com/Sulay2549/integracion-continua-proyecto-final.git
cd integracion-continua-proyecto-final
```

### 2. Ejecutar los contenedores

El proyecto ya incluye el archivo `.env` configurado, así que puedes ejecutar directamente:

```bash
docker-compose up -d
```

> 💡 **Nota:** Docker Compose leerá automáticamente el archivo `.env` y configurará todos los servicios con las credenciales definidas.

### 3. Verificar que los servicios estén corriendo
```bash
docker-compose ps
```

Deberías ver algo como:
```
NAME        IMAGE                    STATUS
backend     backend                  Up
mysql_db    mysql:8.0                Up
```

### 4. Verificar funcionamiento
- **Backend API:** [http://localhost:5000](http://localhost:5000)
- **Test DB:** [http://localhost:5000/test-db](http://localhost:5000/test-db)
- **API Tareas:** [http://localhost:5000/api/tareas/](http://localhost:5000/api/tareas/)
- **Frontend:** [http://localhost:4200](http://localhost:4200) *(actualmente comentado en docker-compose.yml)*
- **Base de datos:** Puerto `3306`

---

## 🛠️ Comandos Útiles de Docker

### Ver logs de un servicio
```bash
docker-compose logs backend
docker-compose logs db
docker-compose logs -f backend  # Seguir logs en tiempo real
```

### Reiniciar un servicio específico
```bash
docker-compose restart backend
```

### Detener todos los servicios
```bash
docker-compose down
```

### Reconstruir imágenes
```bash
docker-compose up -d --build
```

### Acceder a la base de datos
```bash
docker exec -it mysql_db mysql -u root -p
# Ingresar contraseña: 12345 (o la configurada en .env)
```

### Ver tablas de la base de datos
```bash
docker exec -it mysql_db mysql -u root -p12345 -e "USE integracion_continua_db; SHOW TABLES;"
```

---

## 🔧 Desarrollo Local (sin Docker)

### Backend
```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python run.py
```

> **Nota:** Necesitarás tener MySQL corriendo localmente y configurar las variables de entorno en `backend/app/config.py`.

### Frontend
```bash
cd frontend
npm install
npm start
```

El frontend estará disponible en [http://localhost:4200](http://localhost:4200)

---

## 🧪 Pruebas Automatizadas

El proyecto incluye un sistema completo de pruebas automatizadas para el backend.

### Tipos de Pruebas

| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| **Unitarias** | 29 tests | Prueban modelos y utilidades (DB) |
| **Integración** | 28 tests | Prueban endpoints de API y sistema |
| **Funcionales** | 8 tests | Prueban flujos de trabajo completos |
| **TOTAL** | **65 tests** | **100% de cobertura de código** |

### Características de los Tests

✅ **Mocks de BD:** Aislamiento completo sin afectar datos reales  
✅ **Validaciones:** Cobertura del 100% en validaciones de datos  
✅ **Casos de Error:** Pruebas de manejo de errores y casos edge  
✅ **Flujos Completos:** Simulación de escenarios de usuario real  

> 📖 Ver documentación completa en [`backend/tests/README.md`](backend/tests/README.md)

---

## 🔄 CI/CD con Jenkins

El proyecto incluye un `Jenkinsfile` que automatiza:

### Pipeline Stages

1. **Build Backend**
   - Usa imagen `python:3.9-slim-buster`
   - Crea entorno virtual
   - Instala dependencias desde `requirements.txt`

2. **Deploy**
   - Detiene contenedores existentes
   - Reconstruye y despliega con `docker-compose up -d --build`

### Configuración en Jenkins

1. Crear un nuevo Pipeline Job
2. Configurar SCM: Git → `https://github.com/Sulay2549/integracion-continua-proyecto-final.git`
3. Script Path: `Jenkinsfile`
4. Ejecutar el pipeline

> **Nota:** El stage de Build Frontend está comentado en el Jenkinsfile actual.

---

## 📋 Características Implementadas

### Backend
✅ API REST completa con CRUD de tareas  
✅ Validación de datos en endpoints (POST y PUT)  
✅ Sistema de logging profesional con niveles (INFO, ERROR, WARNING)  
✅ Manejo de errores con mensajes descriptivos  
✅ Configuración mediante variables de entorno  
✅ Conexión a base de datos MySQL con pooling  
✅ CORS habilitado para comunicación con frontend  
✅ **65 tests automatizados con 100% de cobertura**  

### Base de Datos
✅ Esquema relacional con 4 tablas  
✅ Claves foráneas y relaciones definidas  
✅ Script de inicialización automática  
✅ Persistencia de datos con volúmenes Docker  

### DevOps
✅ Dockerización de todos los servicios  
✅ Docker Compose para orquestación  
✅ Variables de entorno para configuración  
✅ Pipeline de CI/CD con Jenkins  
✅ Logs centralizados  
✅ **Reportes HTML de tests y cobertura**  

### Frontend
✅ Aplicación Angular 20  
✅ Servicio API para comunicación con backend  
✅ Componente de validación de conexión  

### Testing
✅ **29 pruebas unitarias** del modelo y base de datos
✅ **28 pruebas de integración** de la API y sistema
✅ **8 pruebas funcionales** de flujos completos
✅ Reportes HTML interactivos
✅ Cobertura de código del **100%**
✅ Mocks de base de datos para aislamiento  

---

## 👨‍💻 Autores

**SubGrupo 7**  
Politécnico Grancolombiano – 2025  
Módulo: Integración Continua  

---

## 📚 Recursos Adicionales

- **Documentación de Docker Compose:** https://docs.docker.com/compose/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Angular Documentation:** https://angular.dev/
- **MySQL Documentation:** https://dev.mysql.com/doc/



