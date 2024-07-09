from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # CORS-Unterstützung hinzufügen

DATABASE = 'passwords.db'
PASSWORD_FILE = 'rockyou2024.txt'  # Dein Dateiname hier
BATCH_SIZE = 20000  # Anzahl der Passwörter pro Batch

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
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany('INSERT OR IGNORE INTO passwords (password) VALUES (?)', batch)
    conn.commit()
    conn.close()

def load_passwords_to_db():
    batch = []
    with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            password = line.strip()
            batch.append((password,))
            if len(batch) >= BATCH_SIZE:
                insert_passwords(batch)
                batch = []
        
        if batch:
            insert_passwords(batch)

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
