import sqlite3
import os

def get_connection():

    db_path = os.path.join(os.path.dirname(__file__), 'votaciones.db')

    return sqlite3.connect(db_path, timeout=30, check_same_thread=False)

def init_database():
    """Inicializar la base de datos con las tablas necesarias"""
    conn = get_connection()
    cursor = conn.cursor()

    # Crear tabla de puestos de votación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS puestos_votacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lugar TEXT NOT NULL,
            direccion TEXT NOT NULL,
            mesa INTEGER NOT NULL,
            zona TEXT NOT NULL
        )
    ''')

    # Crear tabla de ciudadanos (incluye columna `mesa`)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ciudadanos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificacion TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            puesto_id INTEGER,
            mesa INTEGER,
            FOREIGN KEY (puesto_id) REFERENCES puestos_votacion(id)
        )
    ''')
    # si la tabla ya existía y no tiene columna mesa, añadirla
    cursor.execute("PRAGMA table_info(ciudadanos)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'mesa' not in cols:
        cursor.execute('ALTER TABLE ciudadanos ADD COLUMN mesa INTEGER')

    # Insertar datos de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM puestos_votacion")
    if cursor.fetchone()[0] == 0:
        puestos = [
            ('Escuela Nacional', 'Calle Principal 123', 1, 'Zona 1'),
            ('Colegio Central', 'Avenida Central 456', 2, 'Zona 2'),
            ('Instituto Técnico', 'Plaza Mayor 789', 3, 'Zona 3')
        ]
        cursor.executemany("INSERT INTO puestos_votacion (lugar, direccion, mesa, zona) VALUES (?, ?, ?, ?)", puestos)

    conn.commit()
    cursor.close()
    conn.close()
    