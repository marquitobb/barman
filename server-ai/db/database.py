import sqlite3
import os
from contextlib import contextmanager

# Ruta del archivo de base de datos
DB_PATH = "motors.db"

# Inicialización de la base de datos
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Crear tabla de motores si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS motors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            device TEXT NOT NULL,
            capacity REAL NOT NULL,
            current_level REAL NOT NULL
        )
        ''')
        
        # Insertar datos iniciales si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM motors")
        if cursor.fetchone()[0] == 0:
            default_motors = [
                (1, "Motor 1", "Tequila", "relay_one", 1000.0, 1000.0),
                (2, "Motor 2", "Soda (Squirt)", "relay_two", 1000.0, 1000.0)
            ]
            cursor.executemany(
                "INSERT INTO motors (id, name, content, device, capacity, current_level) VALUES (?, ?, ?, ?, ?, ?)",
                default_motors
            )
        
        conn.commit()

@contextmanager
def get_connection():
    """Contexto para manejar conexiones a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()