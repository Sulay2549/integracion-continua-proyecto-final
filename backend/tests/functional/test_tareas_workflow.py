"""
Pruebas funcionales para flujos completos de trabajo.

Estas pruebas verifican escenarios de uso real del sistema,
probando flujos completos desde la perspectiva del usuario.
"""
import pytest
import json


@pytest.mark.functional
class TestTareasWorkflowCompleto:
    """Tests de flujos de trabajo completos con tareas."""
    
    def test_flujo_crear_listar_actualizar_eliminar(self, client, mock_db_connection, sample_tarea_response):
        """
        Test: Flujo completo de CRUD de una tarea.
        1. Crear tarea
        2. Listar y verificar que existe
        3. Actualizar estado
        4. Eliminar tarea
        """
        mock_conn, mock_cursor = mock_db_connection
        
        # 1. Crear tarea - El ID puede ser cualquiera
        mock_cursor.lastrowid = 1001
        tarea_data = {
            "titulo": "Tarea de flujo completo",
            "descripcion": "Testing workflow",
            "prioridad": "Alta"
        }
        
        response_crear = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response_crear.status_code == 201
        data_crear = json.loads(response_crear.data)
        # Capturar el ID que retorna la creación
        tarea_id = data_crear["id"]
        assert isinstance(tarea_id, int)
        assert tarea_id > 0
        
        # 2. Listar tareas
        mock_cursor.fetchall.return_value = [sample_tarea_response]
        response_listar = client.get('/api/tareas/')
        
        assert response_listar.status_code == 200
        data_listar = json.loads(response_listar.data)
        assert len(data_listar) > 0
        
        # 3. Actualizar tarea - Usar el ID capturado
        mock_cursor.rowcount = 1
        update_data = {"estado": "Completada"}
        response_actualizar = client.put(
            f'/api/tareas/{tarea_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response_actualizar.status_code == 200
        
        # 4. Eliminar tarea - Usar el ID capturado
        response_eliminar = client.delete(f'/api/tareas/{tarea_id}')
        
        assert response_eliminar.status_code == 200
        data_eliminar = json.loads(response_eliminar.data)
        assert "eliminada" in data_eliminar["mensaje"].lower()
    
    def test_flujo_crear_multiples_tareas(self, client, mock_db_connection):
        """Test: Crear múltiples tareas y listarlas."""
        mock_conn, mock_cursor = mock_db_connection
        
        tareas = [
            {"titulo": "Tarea 1", "prioridad": "Alta"},
            {"titulo": "Tarea 2", "prioridad": "Media"},
            {"titulo": "Tarea 3", "prioridad": "Baja"}
        ]
        
        ids_creados = []
        
        # Crear múltiples tareas - IDs dinámicos
        for i, tarea in enumerate(tareas, 1):
            # Simular IDs que podrían venir de la BD
            mock_cursor.lastrowid = 2000 + i
            response = client.post(
                '/api/tareas/',
                data=json.dumps(tarea),
                content_type='application/json'
            )
            
            assert response.status_code == 201
            data = json.loads(response.data)
            ids_creados.append(data["id"])
        
        # Verificar que se crearon 3 tareas con IDs válidos
        assert len(ids_creados) == 3
        for id_tarea in ids_creados:
            assert isinstance(id_tarea, int)
            assert id_tarea > 0
    
    def test_flujo_busqueda_por_titulo(self, client, mock_db_connection):
        """Test: Crear tarea y buscarla por título."""
        mock_conn, mock_cursor = mock_db_connection
        
        # Crear tarea - ID dinámico
        mock_cursor.lastrowid = 3001
        tarea_data = {"titulo": "Implementar login"}
        
        response_crear = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response_crear.status_code == 201
        
        # Buscar por título
        mock_cursor.fetchall.return_value = [{
            "idTarea": 3001,
            "titulo": "Implementar login",
            "estado": "Pendiente",
            "prioridad": "Media"
        }]
        
        response_buscar = client.get('/api/tareas/?titulo=login')
        
        assert response_buscar.status_code == 200
        data = json.loads(response_buscar.data)
        assert len(data) > 0
    
    def test_flujo_cambio_de_estado_progresivo(self, client, mock_db_connection):
        """Test: Cambiar estado de tarea progresivamente."""
        mock_conn, mock_cursor = mock_db_connection
        
        # Crear tarea - ID dinámico
        mock_cursor.lastrowid = 4001
        tarea_data = {"titulo": "Tarea con estados"}
        
        response_crear = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_data),
            content_type='application/json'
        )
        
        assert response_crear.status_code == 201
        # Capturar el ID retornado
        tarea_id = json.loads(response_crear.data)["id"]
        
        # Cambiar estados progresivamente - Usar el ID capturado
        estados = ["En progreso", "Completada"]
        mock_cursor.rowcount = 1
        
        for estado in estados:
            response = client.put(
                f'/api/tareas/{tarea_id}',
                data=json.dumps({"estado": estado}),
                content_type='application/json'
            )
            
            assert response.status_code == 200


@pytest.mark.functional
class TestTareasWorkflowValidaciones:
    """Tests de flujos con validaciones y manejo de errores."""
    
    def test_flujo_intentar_actualizar_tarea_inexistente(self, client, mock_db_connection):
        """Test: Intentar actualizar tarea que no existe."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 0
        
        update_data = {"estado": "Completada"}
        # Usar un ID que claramente no existe
        tarea_id = 99999
        response = client.put(
            f'/api/tareas/{tarea_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "no encontrada" in data["mensaje"].lower() or "no hubo cambios" in data["mensaje"].lower()
    
    def test_flujo_intentar_eliminar_tarea_inexistente(self, client, mock_db_connection):
        """Test: Intentar eliminar tarea que no existe."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 0
        
        # Usar un ID que claramente no existe
        tarea_id = 99999
        response = client.delete(f'/api/tareas/{tarea_id}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "no encontrada" in data["mensaje"].lower()
    
    def test_flujo_crear_con_datos_invalidos_y_corregir(self, client, mock_db_connection):
        """Test: Intentar crear con datos inválidos, luego corregir."""
        mock_conn, mock_cursor = mock_db_connection
        
        # Intento 1: Sin título (debe fallar)
        tarea_invalida = {"descripcion": "Sin título"}
        response1 = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_invalida),
            content_type='application/json'
        )
        
        assert response1.status_code == 400
        
        # Intento 2: Con título (debe funcionar)
        mock_cursor.lastrowid = 1
        tarea_valida = {
            "titulo": "Tarea corregida",
            "descripcion": "Ahora con título"
        }
        response2 = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_valida),
            content_type='application/json'
        )
        
        assert response2.status_code == 201
    
    def test_flujo_validacion_longitud_campos(self, client):
        """Test: Validar límites de longitud en campos."""
        # Título muy largo
        tarea_titulo_largo = {"titulo": "a" * 101}
        response1 = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_titulo_largo),
            content_type='application/json'
        )
        
        assert response1.status_code == 400
        
        # Descripción muy larga
        tarea_desc_larga = {
            "titulo": "Test",
            "descripcion": "a" * 251
        }
        response2 = client.post(
            '/api/tareas/',
            data=json.dumps(tarea_desc_larga),
            content_type='application/json'
        )
        
        assert response2.status_code == 400


@pytest.mark.functional
@pytest.mark.slow
class TestTareasWorkflowComplejo:
    """Tests de flujos complejos y escenarios avanzados."""
    
    def test_flujo_gestion_completa_proyecto(self, client, mock_db_connection):
        """
        Test: Simular gestión completa de tareas de un proyecto.
        - Crear varias tareas
        - Actualizar algunas
        - Eliminar otras
        - Verificar estado final
        """
        mock_conn, mock_cursor = mock_db_connection
        
        ids_creados = []
        
        # Crear 5 tareas con IDs dinámicos
        for i in range(1, 6):
            # Simular IDs que podrían venir de la BD
            mock_cursor.lastrowid = 5000 + i
            tarea = {
                "titulo": f"Tarea {i}",
                "prioridad": ["Baja", "Media", "Alta"][i % 3]
            }
            
            response = client.post(
                '/api/tareas/',
                data=json.dumps(tarea),
                content_type='application/json'
            )
            
            assert response.status_code == 201
            data = json.loads(response.data)
            ids_creados.append(data["id"])
        
        # Verificar que se crearon 5 tareas
        assert len(ids_creados) == 5
        
        # Actualizar las primeras 3 tareas a "Completada"
        mock_cursor.rowcount = 1
        for tarea_id in ids_creados[:3]:
            response = client.put(
                f'/api/tareas/{tarea_id}',
                data=json.dumps({"estado": "Completada"}),
                content_type='application/json'
            )
            
            assert response.status_code == 200
        
        # Eliminar la cuarta tarea
        response = client.delete(f'/api/tareas/{ids_creados[3]}')
        assert response.status_code == 200
        
        # Verificar que quedan tareas
        mock_cursor.fetchall.return_value = [
            {"idTarea": ids_creados[0], "titulo": "Tarea 1", "estado": "Completada"},
            {"idTarea": ids_creados[1], "titulo": "Tarea 2", "estado": "Completada"},
            {"idTarea": ids_creados[2], "titulo": "Tarea 3", "estado": "Completada"},
            {"idTarea": ids_creados[4], "titulo": "Tarea 5", "estado": "Pendiente"}
        ]
        
        response = client.get('/api/tareas/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 4
