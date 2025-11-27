"""
Pruebas unitarias para el modelo de Tareas.

Estas pruebas verifican el comportamiento de los métodos del modelo
de forma aislada usando mocks de la base de datos.
"""
import pytest
from app.models.tareas_model import Tarea
import datetime


@pytest.mark.unit
class TestTareaConstructor:
    """Tests para el constructor de la clase Tarea."""
    
    def test_constructor_con_todos_los_parametros(self):
        """Test: Constructor con todos los parámetros debe asignarlos correctamente."""
        tarea = Tarea(
            id=1,
            titulo="Tarea de prueba",
            descripcion="Descripción de prueba",
            estado="Pendiente",
            prioridad="Alta",
            fechaCreacion="2025-11-26",
            fechaLimite="2025-12-31",
            idProyecto=1
        )
        
        assert tarea.id == 1
        assert tarea.titulo == "Tarea de prueba"
        assert tarea.descripcion == "Descripción de prueba"
        assert tarea.estado == "Pendiente"
        assert tarea.prioridad == "Alta"
        assert tarea.fechaCreacion == "2025-11-26"
        assert tarea.fechaLimite == "2025-12-31"
        assert tarea.idProyecto == 1
    
    def test_constructor_sin_parametros(self):
        """Test: Constructor sin parámetros debe usar valores None."""
        tarea = Tarea()
        
        assert tarea.id is None
        assert tarea.titulo is None
        assert tarea.descripcion is None
        assert tarea.estado is None
        assert tarea.prioridad is None
        assert tarea.fechaCreacion is None
        assert tarea.fechaLimite is None
        assert tarea.idProyecto is None
    
    def test_constructor_con_parametros_parciales(self):
        """Test: Constructor con algunos parámetros debe asignar solo esos."""
        tarea = Tarea(
            id=2,
            titulo="Tarea parcial",
            estado="En progreso"
        )
        
        assert tarea.id == 2
        assert tarea.titulo == "Tarea parcial"
        assert tarea.estado == "En progreso"
        assert tarea.descripcion is None
        assert tarea.prioridad is None


@pytest.mark.unit
class TestTareaCrear:
    """Tests para el método crear() del modelo Tarea."""
    
    def test_crear_tarea_exitosa(self, mock_db_connection, sample_tarea_data):
        """Test: Crear una tarea con datos válidos debe retornar un ID."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 123
        
        id_tarea, error = Tarea.crear(sample_tarea_data)
        
        # Verificar que retorna un ID
        assert id_tarea is not None
        assert isinstance(id_tarea, int)
        assert id_tarea > 0
        assert error is None
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    def test_crear_tarea_con_valores_por_defecto(self, mock_db_connection):
        """Test: Crear tarea sin estado ni prioridad usa valores por defecto."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 456
        
        data = {"titulo": "Tarea mínima"}
        id_tarea, error = Tarea.crear(data)
        
        # Verificar que retorna un ID válido
        assert id_tarea is not None
        assert isinstance(id_tarea, int)
        assert id_tarea > 0
        assert error is None
        
        # Verificar que se llamó execute con los valores por defecto
        call_args = mock_cursor.execute.call_args[0]
        assert "Pendiente" in str(call_args)  # Estado por defecto
        assert "Media" in str(call_args)  # Prioridad por defecto
    
    def test_crear_tarea_error_bd(self, mock_db_connection):
        """Test: Error en BD debe retornar None y mensaje de error."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.execute.side_effect = Exception("Error de BD")
        
        data = {"titulo": "Test"}
        id_tarea, error = Tarea.crear(data)
        
        assert id_tarea is None
        assert error == "Error de BD"
    
    def test_crear_tarea_sin_conexion(self, mocker):
        """Test: Sin conexión a BD debe retornar error."""
        mocker.patch('app.models.tareas_model.get_connection', return_value=None)
        
        data = {"titulo": "Test"}
        id_tarea, error = Tarea.crear(data)
        
        assert id_tarea is None
        assert "No se pudo conectar" in error


@pytest.mark.unit
class TestTareaListar:
    """Tests para el método listar() del modelo Tarea."""
    
    def test_listar_todas_las_tareas(self, mock_db_connection, sample_tarea_response):
        """Test: Listar sin filtros debe retornar todas las tareas."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = [sample_tarea_response]
        
        tareas, error = Tarea.listar()
        
        assert len(tareas) == 1
        assert error is None
        # Verificar estructura
        assert "titulo" in tareas[0]
        assert "idTarea" in tareas[0]
    
    def test_listar_con_filtro_id(self, mock_db_connection, sample_tarea_response):
        """Test: Filtrar por ID debe incluir condición WHERE."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = [sample_tarea_response]
        
        # Usar el ID de la tarea de ejemplo
        filtros = {"id": sample_tarea_response["idTarea"]}
        tareas, error = Tarea.listar(filtros)
        
        assert len(tareas) == 1
        assert error is None
        
        # Verificar que se usó el filtro
        call_args = str(mock_cursor.execute.call_args)
        assert "idTarea" in call_args
    
    def test_listar_con_filtro_titulo(self, mock_db_connection):
        """Test: Filtrar por título debe usar LIKE."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = []
        
        filtros = {"titulo": "prueba"}
        tareas, error = Tarea.listar(filtros)
        
        assert tareas == []
        assert error is None
        
        # Verificar que se usó LIKE
        call_args = str(mock_cursor.execute.call_args)
        assert "LIKE" in call_args or "titulo" in call_args
    
    def test_listar_con_filtro_descripcion(self, mock_db_connection):
        """Test: Filtrar por descripción debe incluir condición WHERE."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = [{
            "idTarea": 1,
            "titulo": "Tarea test",
            "descripcion": "Descripción de prueba"
        }]
        
        filtros = {"descripcion": "prueba"}
        tareas, error = Tarea.listar(filtros)
        
        assert len(tareas) == 1
        assert error is None
        
        # Verificar que se usó el filtro
        call_args = str(mock_cursor.execute.call_args)
        assert "descripcion" in call_args.lower()
    
    def test_listar_con_filtros_combinados(self, mock_db_connection):
        """Test: Filtrar por múltiples campos simultáneamente."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = []
        
        filtros = {
            "titulo": "test",
            "descripcion": "descripción"
        }
        tareas, error = Tarea.listar(filtros)
        
        assert tareas == []
        assert error is None
    
    def test_listar_error_bd(self, mock_db_connection):
        """Test: Error en BD debe retornar None y mensaje."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.execute.side_effect = Exception("Error de consulta")
        
        tareas, error = Tarea.listar()
        
        assert tareas is None
        assert "Error de consulta" in error
    
    def test_listar_sin_conexion(self, mocker):
        """Test: Sin conexión debe retornar error."""
        mocker.patch('app.models.tareas_model.get_connection', return_value=None)
        
        tareas, error = Tarea.listar()
        
        assert tareas is None
        assert "No se pudo conectar" in error


@pytest.mark.unit
class TestTareaActualizar:
    """Tests para el método actualizar() del modelo Tarea."""
    
    def test_actualizar_tarea_exitosa(self, mock_db_connection):
        """Test: Actualizar tarea existente debe retornar True."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        data = {"estado": "Completada", "prioridad": "Alta"}
        tarea_id = 2
        actualizada, error = Tarea.actualizar(tarea_id, data)
        
        assert actualizada is True
        assert error is None
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    def test_actualizar_tarea_no_encontrada(self, mock_db_connection):
        """Test: Actualizar tarea inexistente debe retornar False."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 0
        
        data = {"estado": "Completada"}
        tarea_id = 99999
        actualizada, error = Tarea.actualizar(tarea_id, data)
        
        assert actualizada is False
        assert error is None
    
    def test_actualizar_sin_datos(self, mock_db_connection):
        """Test: Actualizar sin datos debe retornar False y error."""
        mock_conn, mock_cursor = mock_db_connection
        
        data = {}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is False
        assert "No hay datos para actualizar" in error
    
    def test_actualizar_error_bd(self, mock_db_connection):
        """Test: Error en BD debe retornar False y mensaje."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.execute.side_effect = Exception("Error de actualización")
        
        data = {"estado": "Completada"}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is False
        assert "Error de actualización" in error
    
    def test_actualizar_titulo(self, mock_db_connection):
        """Test: Actualizar solo el título de una tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        data = {"titulo": "Nuevo título"}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is True
        assert error is None
    
    def test_actualizar_descripcion(self, mock_db_connection):
        """Test: Actualizar solo la descripción de una tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        data = {"descripcion": "Nueva descripción"}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is True
        assert error is None
    
    def test_actualizar_fecha_limite(self, mock_db_connection):
        """Test: Actualizar solo la fecha límite de una tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        data = {"fechaLimite": "2025-12-31"}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is True
        assert error is None
    
    def test_actualizar_id_proyecto(self, mock_db_connection):
        """Test: Actualizar solo el ID de proyecto de una tarea."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        data = {"idProyecto": 5}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is True
        assert error is None
    
    def test_actualizar_sin_conexion(self, mocker):
        """Test: Actualizar sin conexión debe retornar error."""
        mocker.patch('app.models.tareas_model.get_connection', return_value=None)
        
        data = {"estado": "Completada"}
        actualizada, error = Tarea.actualizar(1, data)
        
        assert actualizada is False
        assert "No se pudo conectar" in error


@pytest.mark.unit
class TestTareaEliminar:
    """Tests para el método eliminar() del modelo Tarea."""
    
    def test_eliminar_tarea_exitosa(self, mock_db_connection):
        """Test: Eliminar tarea existente debe retornar True."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 1
        
        tarea_id = 200
        eliminada, error = Tarea.eliminar(tarea_id)
        
        assert eliminada is True
        assert error is None
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    def test_eliminar_tarea_no_encontrada(self, mock_db_connection):
        """Test: Eliminar tarea inexistente debe retornar False."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.rowcount = 0
        
        tarea_id = 99999
        eliminada, error = Tarea.eliminar(tarea_id)
        
        assert eliminada is False
        assert error is None
    
    def test_eliminar_error_bd(self, mock_db_connection):
        """Test: Error en BD debe retornar False y mensaje."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.execute.side_effect = Exception("Error de eliminación")
        
        eliminada, error = Tarea.eliminar(1)
        
        assert eliminada is False
        assert "Error de eliminación" in error
    
    def test_eliminar_sin_conexion(self, mocker):
        """Test: Sin conexión debe retornar error."""
        mocker.patch('app.models.tareas_model.get_connection', return_value=None)
        
        eliminada, error = Tarea.eliminar(1)
        
        assert eliminada is False
        assert "No se pudo conectar" in error
