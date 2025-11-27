"""
Pruebas unitarias para el módulo de base de datos.
"""
import pytest
from app.database import get_connection
import mysql.connector

@pytest.mark.unit
def test_get_connection_error(mocker):
    """Test: get_connection debe manejar errores de conexión y retornar None."""
    # Importar la clase Error real que usa el módulo
    from mysql.connector import Error
    
    # Simular error de conexión
    mocker.patch('mysql.connector.connect', side_effect=Error("Error de conexión simulado"))
    
    # Capturar el print
    mock_print = mocker.patch('builtins.print')
    
    connection = get_connection()
    
    assert connection is None
    # Verificar que se imprimió el mensaje de error (línea 16)
    mock_print.assert_called_with("Error conectando a la base de datos: Error de conexión simulado")

@pytest.mark.unit
def test_get_connection_success(mocker):
    """Test: get_connection debe retornar conexión si es exitosa."""
    # Mockear mysql.connector.connect
    mock_connect = mocker.patch('mysql.connector.connect')
    mock_connection = mocker.Mock()
    mock_connect.return_value = mock_connection
    
    # Simular que está conectado
    mock_connection.is_connected.return_value = True
    
    connection = get_connection()
    
    assert connection == mock_connection
    assert connection.is_connected() is True
