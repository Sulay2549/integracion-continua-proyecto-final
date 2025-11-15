from flask import Blueprint, jsonify, request
from app.models.tareas_model import Tarea
from app.database import get_connection

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

    print("Filtros recibidos:", filtros)

    tareas, error = Tarea.listar(filtros)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(tareas), 200

@tareas_bp.route("/", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    nuevo_id, error = Tarea.crear(data)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"mensaje": "Tarea creada exitosamente", "id": nuevo_id}), 201

@tareas_bp.route("/<int:id_tarea>", methods=["PUT"])
def actualizar_tarea(id_tarea):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400

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
