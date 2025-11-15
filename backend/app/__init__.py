from flask import Flask
from flask import jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.tareas_routes import tareas_bp
    from app.database import get_connection # Importar aquí para test_db

    app.register_blueprint(tareas_bp, url_prefix="/api/tareas")

    @app.route("/")
    def home():
        return jsonify({"messages": "API del Sistema de Gestión de Tareas en ejecución"})

    @app.route("/test-db")
    def test_db():
        conn = get_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "No se pudo conectar a la base de datos"}), 500
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"status": "ok", "database": db_name[0]})

    return app
