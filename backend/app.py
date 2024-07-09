from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import threading
from queue import Queue

app = Flask(__name__)
CORS(app)  # CORS-Unterstützung hinzufügen

DATABASE = 'passwords.db'
PASSWORD_FILE = 'rockyou2024.txt'  # Dein Dateiname hier
BATCH_SIZE = 1000  # Anzahl der Passwörter pro Batch
NUM_THREADS = 4  # Anzahl der Threads für parallele Verarbeitung
queue = Queue()
lock = threading.Lock()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA journal_mode=WAL;')  # Aktivieren des WAL-Modus
        cursor.execute('PRAGMA synchronous=OFF;')  # Deaktivieren der Synchronisation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                password TEXT PRIMARY KEY
            )
        ''')
        conn.commit()

def insert_passwords(batch):
    with lock:  # Synchronisiere den Schreibzugriff
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.executemany('INSERT OR IGNORE INTO passwords (password) VALUES (?)', batch)
        conn.commit()
        conn.close()

def worker():
    while True:
        lines = queue.get()
        if lines is None:
            break
        process_lines(lines)
        queue.task_done()

def process_lines(lines):
    batch = []
    for line in lines:
        password = line.strip()
        batch.append((password,))
        if len(batch) >= BATCH_SIZE:
            insert_passwords(batch)
            batch = []
    
    if batch:
        insert_passwords(batch)

def load_passwords_to_db():
    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
        while True:
            lines = file.readlines(1024 * 1024)  # Lese 1 MB auf einmal
            if not lines:
                break
            queue.put(lines)

    queue.join()

    for _ in range(NUM_THREADS):
        queue.put(None)

    for thread in threads:
        thread.join()

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
