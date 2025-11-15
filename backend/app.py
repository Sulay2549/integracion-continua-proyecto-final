from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    try:
        db = mysql.connector.connect(
            host="db",
            user="usuario",
            password="12345",
            database="tareas_db"
        )
        cursor = db.cursor()
        cursor.execute("SHOW DATABASES;")
        return jsonify({"message": "Conexión exitosa a la base de datos", "databases": [dbs[0] for dbs in cursor]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
