from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from multiprocessing import Pool, cpu_count

app = Flask(__name__)
CORS(app)  # CORS-Unterstützung hinzufügen

DATABASE = 'passwords.db'
PASSWORD_FILE = 'rockyou2024.txt'  # Dein Dateiname hier
BATCH_SIZE = 1000  # Anzahl der Passwörter pro Batch

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                password TEXT PRIMARY KEY
            )
        ''')
        conn.commit()

def insert_passwords(batch):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany('INSERT OR IGNORE INTO passwords (password) VALUES (?)', ((pw,) for pw in batch))
    conn.commit()
    conn.close()

def process_file_chunk(file_chunk):
    batch = []
    for line in file_chunk:
        password = line.strip()
        batch.append(password)
        if len(batch) >= BATCH_SIZE:
            insert_passwords(batch)
            batch = []
    if batch:
        insert_passwords(batch)

def read_file_in_chunks(file_path, chunk_size=1024*1024*10):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            lines = file.readlines(chunk_size)
            if not lines:
                break
            yield lines

def load_passwords_to_db():
    pool = Pool(cpu_count())
    for file_chunk in read_file_in_chunks(PASSWORD_FILE):
        pool.apply_async(process_file_chunk, args=(file_chunk,))
    pool.close()
    pool.join()

# Initialisiere die Datenbank und lade Passwörter beim Start
if not os.path.exists(DATABASE):
    init_db()
    load_passwords_to_db()

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM passwords WHERE password = ?', (password,))
        result = cursor.fetchone()
        if result:
            return jsonify({"status": "unsafe"})
        else:
            return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
