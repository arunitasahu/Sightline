import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/faces.db')

# Initialize database and create table if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces (
        name TEXT PRIMARY KEY,
        image_path TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Add a face to the database
def add_face(name, image_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('REPLACE INTO faces (name, image_path) VALUES (?, ?)', (name, image_path))
    conn.commit()
    conn.close()

# Get all faces from the database
def get_all_faces():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, image_path FROM faces')
    faces = c.fetchall()
    conn.close()
    return faces

# Get image path for a given name
def get_face_path(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT image_path FROM faces WHERE name = ?', (name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
