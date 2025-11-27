from flask import Blueprint, jsonify, request
from app.models.tareas_model import Tarea
from app.database import get_connection
import logging

logger = logging.getLogger(__name__)

tareas_bp = Blueprint("tareas", __name__)

# ---------------------------------
# Metodos correspondientes a Tareas
# ---------------------------------

@tareas_bp.route("/", methods=["GET"])
def obtener_tareas():
    filtros = {
        "id": request.args.get("id"),
        "titulo": request.args.get("titulo"),
        "descripcion": request.args.get("descripcion")
    }

    # eliminar claves con None
    filtros = {k: v for k, v in filtros.items() if v}

    logger.info(f"Filtros recibidos: {filtros}")

    tareas, error = Tarea.listar(filtros)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(tareas), 200

@tareas_bp.route("/", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    
    # Validar que se recibió JSON
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400
    
    # Validar campos requeridos
    if "titulo" not in data or not data["titulo"]:
        return jsonify({"error": "El campo 'titulo' es requerido"}), 400
    
    # Validar longitud del título
    if len(data["titulo"]) > 100:
        return jsonify({"error": "El título no puede exceder 100 caracteres"}), 400
    
    # Validar descripción si existe
    if "descripcion" in data and data["descripcion"] and len(data["descripcion"]) > 250:
        return jsonify({"error": "La descripción no puede exceder 250 caracteres"}), 400
    
    # Validar estado si existe
    estados_validos = ["Pendiente", "En progreso", "Completada", "Cancelada"]
    if "estado" in data and data["estado"] not in estados_validos:
        return jsonify({"error": f"Estado inválido. Valores permitidos: {', '.join(estados_validos)}"}), 400
    
    # Validar prioridad si existe
    prioridades_validas = ["Baja", "Media", "Alta"]
    if "prioridad" in data and data["prioridad"] not in prioridades_validas:
        return jsonify({"error": f"Prioridad inválida. Valores permitidos: {', '.join(prioridades_validas)}"}), 400
    
    nuevo_id, error = Tarea.crear(data)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"mensaje": "Tarea creada exitosamente", "id": nuevo_id}), 201

@tareas_bp.route("/<int:id_tarea>", methods=["PUT"])
def actualizar_tarea(id_tarea):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400

    # Validar longitud del título si existe
    if "titulo" in data and len(data["titulo"]) > 100:
        return jsonify({"error": "El título no puede exceder 100 caracteres"}), 400
    
    # Validar descripción si existe
    if "descripcion" in data and len(data["descripcion"]) > 250:
        return jsonify({"error": "La descripción no puede exceder 250 caracteres"}), 400
    
    # Validar estado si existe
    estados_validos = ["Pendiente", "En progreso", "Completada", "Cancelada"]
    if "estado" in data and data["estado"] not in estados_validos:
        return jsonify({"error": f"Estado inválido. Valores permitidos: {', '.join(estados_validos)}"}), 400
    
    # Validar prioridad si existe
    prioridades_validas = ["Baja", "Media", "Alta"]
    if "prioridad" in data and data["prioridad"] not in prioridades_validas:
        return jsonify({"error": f"Prioridad inválida. Valores permitidos: {', '.join(prioridades_validas)}"}), 400

    actualizada, error = Tarea.actualizar(id_tarea, data)
    if error:
        return jsonify({"error": error}), 500
    if not actualizada:
        return jsonify({"mensaje": "Tarea no encontrada o no hubo cambios"}), 404
    
    return jsonify({"mensaje": f"Tarea con ID {id_tarea} actualizada exitosamente"}), 200

@tareas_bp.route("/<int:id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    eliminada, error = Tarea.eliminar(id_tarea)
    if error:
        return jsonify({"error": error}), 500
    if not eliminada:
        return jsonify({"mensaje": "Tarea no encontrada"}), 404
    return jsonify({"mensaje": f"Tarea con ID {id_tarea} eliminada exitosamente"}), 200
