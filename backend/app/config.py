import os

class Config:
    # Configuración general
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

    # Configuración de la base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
    DB_NAME = os.getenv('DB_NAME', 'integracion_continua_db')
