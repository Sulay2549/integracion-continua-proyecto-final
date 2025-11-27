"""
Tests para rutas del sistema y utilidades.
"""
import pytest
import json

@pytest.mark.integration
class TestSystemRoutes:
    """Tests para endpoints del sistema como /test-db."""
    
    def test_test_db_success(self, mocker):
        """Test: /test-db debe retornar ok si hay conexión."""
        # Mockear get_connection ANTES de crear la app
        mock_conn = mocker.Mock()
        mock_cursor = mocker.Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test_db',)
        
        # Parchear en app.database
        mocker.patch('app.database.get_connection', return_value=mock_conn)
        
        # Crear app fresca para que tome el mock
        from app import create_app
        app = create_app()
        client = app.test_client()
        
        response = client.get('/test-db')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"
        assert data["database"] == "test_db"
    
    def test_test_db_failure(self, mocker):
        """Test: /test-db debe retornar error si no hay conexión."""
        # Parchear get_connection para retornar None
        mocker.patch('app.database.get_connection', return_value=None)
        
        # Crear app fresca
        from app import create_app
        app = create_app()
        client = app.test_client()
        
        response = client.get('/test-db')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["status"] == "error"
