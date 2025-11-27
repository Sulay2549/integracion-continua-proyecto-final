from app.database import get_connection
import datetime
import logging

logger = logging.getLogger(__name__)

class Tarea:
    def __init__(self, id=None, titulo=None, descripcion=None, estado=None, prioridad=None, fechaCreacion=None, fechaLimite=None, idProyecto=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.prioridad = prioridad
        self.fechaCreacion = fechaCreacion
        self.fechaLimite = fechaLimite
        self.idProyecto = idProyecto

    # -------------------------
    # Crear tarea
    # -------------------------
    @staticmethod
    def crear(data):
        conn = get_connection()
        if conn is None:
            logger.error("No se pudo conectar a la base de datos")
            return None, "No se pudo conectar a la base de datos"
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO tareas (titulo, descripcion, estado, prioridad, fechaCreacion, fechaLimite, idProyecto)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data.get("titulo"),
                data.get("descripcion"),
                data.get("estado", "Pendiente"),
                data.get("prioridad", "Media"),
                datetime.date.today(),
                data.get("fechaLimite"),
                data.get("idProyecto")
            ))
            conn.commit()
            logger.info(f"Tarea creada exitosamente con ID: {cursor.lastrowid}")
            return cursor.lastrowid, None
        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            return None, str(e)
        finally:
            cursor.close()
            conn.close()

    # -------------------------
    # Listar tareas (todas o filtradas)
    # -------------------------
    @staticmethod
    def listar(filtros=None):
        conn = get_connection()
        if conn is None:
            logger.error("No se pudo conectar a la base de datos")
            return None, "No se pudo conectar a la base de datos"

        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tareas WHERE 1=1"
            params = []

            if filtros:
                if "id" in filtros:
                    sql += " AND idTarea = %s"
                    params.append(filtros["id"])
                if "titulo" in filtros:
                    sql += " AND titulo LIKE %s"
                    params.append(f"%{filtros['titulo']}%")
                if "descripcion" in filtros:
                    sql += " AND descripcion LIKE %s"
                    params.append(f"%{filtros['descripcion']}%")

            logger.info(f"Ejecutando consulta SQL: {sql}")
            logger.debug(f"Parámetros: {params}")

            cursor.execute(sql, tuple(params))
            tareas = cursor.fetchall()
            logger.info(f"Se encontraron {len(tareas)} tareas")
            return tareas, None
        except Exception as e:
            logger.error(f"Error al listar tareas: {str(e)}")
            return None, str(e)
        finally:
            cursor.close()
            conn.close()

    # -------------------------
    # Actualizar tarea
    # -------------------------
    @staticmethod
    def actualizar(id_tarea, data):
        conn = get_connection()
        if conn is None:
            logger.error("No se pudo conectar a la base de datos")
            return False, "No se pudo conectar a la base de datos"
        try:
            cursor = conn.cursor()
            updates = []
            params = []

            if "titulo" in data:
                updates.append("titulo = %s")
                params.append(data["titulo"])
            if "descripcion" in data:
                updates.append("descripcion = %s")
                params.append(data["descripcion"])
            if "estado" in data:
                updates.append("estado = %s")
                params.append(data["estado"])
            if "prioridad" in data:
                updates.append("prioridad = %s")
                params.append(data["prioridad"])
            if "fechaLimite" in data:
                updates.append("fechaLimite = %s")
                params.append(data["fechaLimite"])
            if "idProyecto" in data:
                updates.append("idProyecto = %s")
                params.append(data["idProyecto"])
            
            if not updates:
                logger.warning(f"Intento de actualizar tarea {id_tarea} sin datos")
                return False, "No hay datos para actualizar"

            sql = f"UPDATE tareas SET {', '.join(updates)} WHERE idTarea = %s"
            params.append(id_tarea)

            cursor.execute(sql, tuple(params))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Tarea {id_tarea} actualizada exitosamente")
            else:
                logger.warning(f"No se encontró la tarea {id_tarea} para actualizar")
            
            return cursor.rowcount > 0, None
        except Exception as e:
            logger.error(f"Error al actualizar tarea {id_tarea}: {str(e)}")
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    # -------------------------
    # Eliminar tarea
    # -------------------------
    @staticmethod
    def eliminar(id_tarea):
        conn = get_connection()
        if conn is None:
            logger.error("No se pudo conectar a la base de datos")
            return False, "No se pudo conectar a la base de datos"
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM tareas WHERE idTarea = %s"
            cursor.execute(sql, (id_tarea,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Tarea {id_tarea} eliminada exitosamente")
            else:
                logger.warning(f"No se encontró la tarea {id_tarea} para eliminar")
            
            return cursor.rowcount > 0, None
        except Exception as e:
            logger.error(f"Error al eliminar tarea {id_tarea}: {str(e)}")
            return False, str(e)
        finally:
            cursor.close()
            conn.close()