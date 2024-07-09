import sqlite3
import os

DATABASE = 'passwords_sample.db'
PASSWORD_FILE = 'rockyou2024.txt'  # Dein Dateiname hier
SAMPLE_SIZE = 100000  # Anzahl der Passwörter in der Teilmenge

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

def load_sample_passwords_to_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i >= SAMPLE_SIZE:
                    break
                password = line.strip()
                try:
                    cursor.execute('INSERT INTO passwords (password) VALUES (?)', (password,))
                except sqlite3.IntegrityError:
                    # Password already exists, skip it
                    pass
        conn.commit()

# Initialisiere die Datenbank und lade eine Teilmenge der Passwörter
if not os.path.exists(DATABASE):
    init_db()
    load_sample_passwords_to_db()

# Berechne die Größe der Datenbankdatei
db_size = os.path.getsize(DATABASE)
print(f'Die Größe der Datenbankdatei beträgt {db_size / (1024 ** 2):.2f} MB')

# Schätze die Gesamtgröße
total_size_estimate = (db_size / SAMPLE_SIZE) * 10_000_000_000  # Hochrechnung auf 10 Milliarden Passwörter
print(f'Die geschätzte Gesamtgröße der Datenbank beträgt {total_size_estimate / (1024 ** 3):.2f} GB')
