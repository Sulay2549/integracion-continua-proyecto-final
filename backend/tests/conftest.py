"""
Fixtures compartidas para todos los tests.
"""
import pytest
import sys
import os

# Agregar el directorio raíz al path para importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import get_connection
import mysql.connector


@pytest.fixture(scope='session')
def app():
    """
    Crea una instancia de la aplicación Flask para testing.
    """
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture(scope='function')
def client(app):
    """
    Cliente de prueba para hacer requests HTTP.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def mock_db_connection(mocker):
    """
    Mock de la conexión a la base de datos.
    """
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    
    # Configurar el mock
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.is_connected.return_value = True
    
    # Mockear la función get_connection
    mocker.patch('app.database.get_connection', return_value=mock_conn)
    mocker.patch('app.models.tareas_model.get_connection', return_value=mock_conn)
    
    return mock_conn, mock_cursor


@pytest.fixture(scope='function')
def sample_tarea_data():
    """
    Datos de ejemplo para crear una tarea.
    """
    return {
        "titulo": "Ejecutar Tareas automaticas de Backend",
        "descripcion": "Realiza pruebas de integracion continua (Unitarias, de integracion y funcionales)",
        "estado": "En Proceso",
        "prioridad": "Alta",
        "fechaLimite": "2025-12-31",
        "idProyecto": 1
    }


@pytest.fixture(scope='function')
def sample_tarea_response():
    """
    Respuesta de ejemplo de una tarea desde la BD.
    """
    return {
        "idTarea": 1,
        "titulo": "Ejecutar Tareas automaticas de Backend",
        "descripcion": "Realiza pruebas de integracion continua (Unitarias, de integracion y funcionales)",
        "estado": "En Proceso",
        "prioridad": "Alta",
        "fechaCreacion": "2025-11-25",
        "fechaLimite": "2025-12-31",
        "idProyecto": 1
    }


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """
    Configuración inicial del entorno de testing.
    """
    # Aquí puedes agregar configuración adicional si es necesaria
    yield
    # Limpieza después de todos los tests
