# database.py
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",        # change if using remote server
        user="root",             # your MySQL username
        password="Dsec@123", # your MySQL password
        database="construction_safety"
    )
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            worker_id VARCHAR(50) NOT NULL,
            phone VARCHAR(15) NOT NULL,
            address TEXT,
            image_path VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

def insert_worker(name, worker_id, phone, address, image_path):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO workers (name, worker_id, phone, address, image_path)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, worker_id, phone, address, image_path))
    conn.commit()
    conn.close()

def get_worker_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workers WHERE name = %s", (name,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_workers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, worker_id, phone, address, image_path FROM workers")
    rows = cursor.fetchall()
    conn.close()
    return rows
