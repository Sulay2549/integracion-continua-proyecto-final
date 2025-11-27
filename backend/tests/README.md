# Tests - Backend

Este directorio contiene todas las pruebas automatizadas del backend.

## Estructura

```
tests/
├── conftest.py              # Fixtures compartidas
├── unit/                    # Pruebas unitarias
│   ├── test_tareas_model.py
│   └── test_database.py
├── integration/             # Pruebas de integración
│   ├── test_tareas_api.py
│   └── test_system_routes.py
└── functional/              # Pruebas funcionales
    └── test_tareas_workflow.py
```

## Tipos de Pruebas

### Pruebas Unitarias (`unit/`)
- Prueban funciones individuales de forma aislada
- Usan mocks para la base de datos
- Rápidas de ejecutar
- **29 tests** cubriendo modelos y utilidades de base de datos

### Pruebas de Integración (`integration/`)
- Prueban endpoints de la API completos
- Verifican validaciones de datos
- Prueban respuestas HTTP
- **28 tests** cubriendo todos los endpoints de tareas y sistema

### Pruebas Funcionales (`functional/`)
- Prueban flujos de trabajo completos
- Simulan escenarios de usuario real
- Verifican comportamiento end-to-end
- **8 tests** cubriendo flujos CRUD completos

---
## Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Solo unitarias
```bash
pytest tests/unit/
```

### Solo integración
```bash
pytest tests/integration/
```

### Solo funcionales
```bash
pytest tests/functional/
```

### Con reporte HTML
```bash
pytest --html=reports/test-report.html --self-contained-html
```

### Con cobertura
```bash
pytest --cov=app --cov-report=html --cov-report=term
```

### Modo verbose
```bash
pytest -v
```

### Con logs
```bash
pytest -v --log-cli-level=INFO
```

## Reportes

### Reporte HTML
Se genera en `reports/test-report.html`
- Resumen de tests pasados/fallidos
- Detalles de cada test
- Stack traces de errores
- Tiempo de ejecución

### Reporte de Cobertura
Se genera en `htmlcov/index.html`
- Porcentaje de cobertura por archivo
- Líneas cubiertas/no cubiertas
- Visualización interactiva

## Fixtures Disponibles

Definidas en `conftest.py`:

- `app`: Instancia de la aplicación Flask
- `client`: Cliente de prueba HTTP
- `mock_db_connection`: Mock de conexión a BD
- `sample_tarea_data`: Datos de ejemplo para crear tarea
- `sample_tarea_response`: Respuesta de ejemplo de la BD

## Marcadores

Los tests están marcados por tipo:

- `@pytest.mark.unit`: Pruebas unitarias
- `@pytest.mark.integration`: Pruebas de integración
- `@pytest.mark.functional`: Pruebas funcionales
- `@pytest.mark.slow`: Pruebas que tardan más tiempo

### Ejecutar por marcador
```bash
pytest -m unit          # Solo unitarias
pytest -m integration   # Solo integración
pytest -m functional    # Solo funcionales
```

## Notas

- Los tests usan mocks para aislar la lógica de la BD
- Cada test es independiente
