from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # CORS-Unterstützung hinzufügen

def load_passwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        passwords = set(line.strip() for line in file)
    return passwords

# Laden Sie die Passwörter beim Start der Anwendung
passwords = load_passwords("rockyou2024.txt")

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')
    if password in passwords:
        return jsonify({"status": "unsafe"})
    else:
        return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
