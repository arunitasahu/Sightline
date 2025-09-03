import sqlite3
import os

# Use in-memory database for Render deployment to avoid filesystem issues
DB_PATH = ':memory:'  # In-memory database for cloud deployment

# Global connection to keep in-memory database alive
_conn = None

def get_connection():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        # Initialize table
        c = _conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS faces (
            name TEXT PRIMARY KEY,
            image_data BLOB NOT NULL,
            image_format TEXT NOT NULL DEFAULT 'jpg'
        )''')
        _conn.commit()
    return _conn

# Initialize database and create table if not exists
def init_db():
    get_connection()  # This will create the table

# Add a face to the database (store image as BLOB)
def add_face(name, image_data, image_format='jpg'):
    conn = get_connection()
    c = conn.cursor()
    c.execute('REPLACE INTO faces (name, image_data, image_format) VALUES (?, ?, ?)', 
              (name, image_data, image_format))
    conn.commit()

# Get all faces from the database
def get_all_faces():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT name FROM faces')
    faces = c.fetchall()
    return [face[0] for face in faces]

# Get face image data by name
def get_face_data(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT image_data, image_format FROM faces WHERE name = ?', (name,))
    result = c.fetchone()
    return result if result else None

# Get all face data (for recognition)
def get_all_face_data():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT name, image_data, image_format FROM faces')
    return c.fetchall()

# Get image path for a given name (backward compatibility)
def get_face_path(name):
    # This function is for backward compatibility
    # In the new system, we don't use file paths
    return f"memory://{name}"
