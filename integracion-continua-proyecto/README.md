# 🚀 Proyecto de Integración Continua – Entrega 1

## 📖 Descripción
Este proyecto implementa un **sistema de gestión de tareas** utilizando una arquitectura basada en **contenedores Docker**.  
Incluye tres servicios principales:
- **Frontend:** Aplicación web simple (HTML o Angular).  
- **Backend:** API REST desarrollada en Flask (Python).  
- **Base de datos:** MySQL.

El objetivo es demostrar la comunicación entre contenedores dentro del entorno Docker como parte de la **Entrega 1** del módulo *Énfasis Profesional I - Integración Continua* del Politécnico Grancolombiano.

## 🧱 Estructura del proyecto
```
integracion-continua-proyecto/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
├── frontend/
│   ├── Dockerfile
│   └── src/
│       └── index.html
└── README.md
```

## ⚙️ Ejecución del proyecto
1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Sulay2549/integracion-continua-proyecto.git
   cd integracion-continua-proyecto
   ```

2. **Ejecutar los contenedores**
   ```bash
   docker-compose up
   ```

3. **Verificar funcionamiento**
   - Frontend → [http://localhost:4200](http://localhost:4200)
   - Backend → [http://localhost:5000](http://localhost:5000)
   - Base de datos → Puerto `3306`

## 👨‍💻 Autor
**Román Mauricio Hernández**  
Politécnico Grancolombiano – 2025  
Módulo: Integración Continua  

## 📸 Evidencias sugeridas
- Captura del comando `docker ps` mostrando los tres contenedores activos.  
- Captura del navegador con el mensaje del frontend y backend.  
- Captura del repositorio en GitHub con la estructura del proyecto.
