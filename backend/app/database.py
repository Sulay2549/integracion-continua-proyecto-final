import mysql.connector
from mysql.connector import Error
from app.config import Config

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None
