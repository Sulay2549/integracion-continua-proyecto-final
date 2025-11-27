"""
Pruebas de integración para la API de Tareas.

Estas pruebas verifican el comportamiento de los endpoints
de la API interactuando con todos los componentes.
"""
import pytest
import json


@pytest.mark.integration
class TestTareasAPIEndpoints:
    """Tests de integración para los endpoints de tareas."""
    
    def test_get_home_endpoint(self, client):
        """Test: GET / debe retornar mensaje de bienvenida."""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "messages" in data
        assert "Gestión de Tareas" in data["messages"]
    
    def test_get_tareas_endpoint(self, client, mock_db_connection, sample_tarea_response):
        """Test: GET /api/tareas/ debe retornar lista de tareas."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = [sample_tarea_response]
        
        response = client.get('/api/tareas/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        # Verificar estructura en lugar de valores exactos
        assert "titulo" in data[0]
        assert "idTarea" in data[0]
    
    def test_get_tareas_con_filtro(self, client, mock_db_connection):
        """Test: GET /api/tareas/?titulo=test debe filtrar por título."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = []
        
        response = client.get('/api/tareas/?titulo=test')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_post_tarea_valida(self, client, mock_db_connection):
        """Test: POST /api/tareas/ con datos válidos debe crear tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 789
        
        tarea_data = {
            "titulo": "Nueva tarea",
            "descripcion": "Descripción de prueba",
            "estado": "Pendiente",
            "prioridad": "Alta"
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert "id" in data
        assert isinstance(data["id"], int)
        assert data["id"] > 0
        assert "mensaje" in data
    
    def test_post_tarea_sin_datos(self, client):
        """Test: POST con JSON vacío debe retornar error 400."""
        response = client.post(
            '/api/tareas/',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "No se recibieron datos" in data["error"]
    
    def test_post_tarea_sin_titulo(self, client):
        """Test: POST sin título debe retornar error 400."""
        tarea_data = {
            "descripcion": "Sin título"
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "titulo" in data["error"].lower()
    
    def test_post_tarea_titulo_vacio(self, client):
        """Test: POST con título vacío debe retornar error 400."""
        tarea_data = {
            "titulo": ""
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_post_tarea_titulo_muy_largo(self, client):
        """Test: POST con título > 100 caracteres debe retornar error."""
        tarea_data = {
            "titulo": "a" * 101
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "100" in data["error"]
    
    def test_post_tarea_estado_invalido(self, client):
        """Test: POST con estado inválido debe retornar error."""
        tarea_data = {
            "titulo": "Test",
            "estado": "EstadoInvalido"
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "estado" in data["error"].lower()
    
    def test_post_tarea_prioridad_invalida(self, client):
        """Test: POST con prioridad inválida debe retornar error."""
        tarea_data = {
            "titulo": "Test",
            "prioridad": "PrioridadInvalida"
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "prioridad" in data["error"].lower()
    
    def test_put_tarea_existente(self, client, mock_db_connection):
        """Test: PUT /api/tareas/<id> debe actualizar tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        update_data = {
            "estado": "Completada",
            "prioridad": "Baja"
        }
        
        tarea_id = 500
        response = client.put(
            f'/api/tareas/{tarea_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "mensaje" in data
        assert "actualizada" in data["mensaje"].lower()
    
    def test_put_tarea_sin_datos(self, client):
        """Test: PUT sin datos debe retornar error 400."""
        response = client.put(
            '/api/tareas/1',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_put_tarea_no_encontrada(self, client, mock_db_connection):
        """Test: PUT a tarea inexistente debe retornar 404."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 0
        
        update_data = {"estado": "Completada"}
        
        tarea_id = 99999
        response = client.put(
            f'/api/tareas/{tarea_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "mensaje" in data
    
    def test_delete_tarea_existente(self, client, mock_db_connection):
        """Test: DELETE /api/tareas/<id> debe eliminar tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        tarea_id = 600
        response = client.delete(f'/api/tareas/{tarea_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "mensaje" in data
        assert "eliminada" in data["mensaje"].lower()
    
    def test_delete_tarea_no_encontrada(self, client, mock_db_connection):
        """Test: DELETE a tarea inexistente debe retornar 404."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 0
        
        tarea_id = 99999
        response = client.delete(f'/api/tareas/{tarea_id}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "mensaje" in data


@pytest.mark.integration
class TestTareasAPIValidaciones:
    """Tests específicos de validaciones de la API."""
    
    def test_validacion_descripcion_muy_larga(self, client):
        """Test: Descripción > 250 caracteres debe retornar error."""
        tarea_data = {
            "titulo": "Test",
            "descripcion": "a" * 251
        }
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "250" in data["error"]
    
    def test_validacion_estados_permitidos(self, client, mock_db_connection):
        """Test: Solo estados válidos deben ser aceptados."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 1
        
        estados_validos = ["Pendiente", "En progreso", "Completada", "Cancelada"]
        
        for estado in estados_validos:
            tarea_data = {
                "titulo": f"Test {estado}",
                "estado": estado
            }
            
            response = client.post(
                '/api/tareas/',
                data=json.dumps(tarea_data),
                content_type='application/json'
            )
            
            assert response.status_code == 201
    
    def test_validacion_prioridades_permitidas(self, client, mock_db_connection):
        """Test: Solo prioridades válidas deben ser aceptadas."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 1
        
        prioridades_validas = ["Baja", "Media", "Alta"]
        
        for prioridad in prioridades_validas:
            tarea_data = {
                "titulo": f"Test {prioridad}",
                "prioridad": prioridad
            }
            
            response = client.post(
                '/api/tareas/',
                data=json.dumps(tarea_data),
                content_type='application/json'
            )
            
            assert response.status_code == 201

@pytest.mark.integration
class TestTareasAPIErrores:
    """Tests para casos de error en los endpoints."""
    
    def test_get_tareas_error_bd(self, client, mocker):
        """Test: GET /api/tareas/ con error de BD debe retornar 500."""
        mocker.patch('app.routes.tareas_routes.Tarea.listar', 
                     return_value=(None, "Error de base de datos"))
        
        response = client.get('/api/tareas/')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        assert "base de datos" in data["error"].lower()
    
    def test_post_tarea_sin_json(self, client):
        """Test: POST sin Content-Type JSON debe retornar 415."""
        response = client.post(
            '/api/tareas/',
            data="no es json"
        )
        
        # Flask retorna 415 (Unsupported Media Type) cuando no es JSON
        assert response.status_code == 415
    
    def test_post_tarea_error_bd(self, client, mocker):
        """Test: POST con error de BD debe retornar 500."""
        mocker.patch('app.routes.tareas_routes.Tarea.crear',
                     return_value=(None, "Error al insertar en BD"))
        
        tarea_data = {"titulo": "Test"}
        
        response = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
        assert "insertar" in data["error"].lower()
    
    def test_put_titulo_muy_largo(self, client):
        """Test: PUT con título > 100 caracteres debe retornar 400."""
        update_data = {
            "titulo": "a" * 101
        }
        
        response = client.put(
            '/api/tareas/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "100" in data["error"]
    
    def test_put_descripcion_muy_larga(self, client):
        """Test: PUT con descripción > 250 caracteres debe retornar 400."""
        update_data = {
            "descripcion": "a" * 251
        }
        
        response = client.put(
            '/api/tareas/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "250" in data["error"]
    
    def test_put_estado_invalido(self, client):
        """Test: PUT con estado inválido debe retornar 400."""
        update_data = {
            "estado": "EstadoNoValido"
        }
        
        response = client.put(
            '/api/tareas/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "estado" in data["error"].lower()
    
    def test_put_prioridad_invalida(self, client):
        """Test: PUT con prioridad inválida debe retornar 400."""
        update_data = {
            "prioridad": "PrioridadNoValida"
        }
        
        response = client.put(
            '/api/tareas/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "prioridad" in data["error"].lower()
    
    def test_put_tarea_error_bd(self, client, mocker):
        """Test: PUT con error de BD debe retornar 500."""
        mocker.patch('app.routes.tareas_routes.Tarea.actualizar',
                     return_value=(False, "Error al actualizar en BD"))
        
        update_data = {"estado": "Completada"}
        
        response = client.put(
            '/api/tareas/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
    
    def test_delete_tarea_error_bd(self, client, mocker):
        """Test: DELETE con error de BD debe retornar 500."""
        mocker.patch('app.routes.tareas_routes.Tarea.eliminar',
                     return_value=(False, "Error al eliminar de BD"))
        
        response = client.delete('/api/tareas/1')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data
