from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PASSWORD_FILE = 'rockyou2024.txt'  # Dein Dateiname hier

# Passwörter einmalig in ein Set laden
with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
    unsafe_passwords = set(line.strip() for line in file)

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')

    if password in unsafe_passwords:
        return jsonify({"status": "unsafe"})
    else:
        return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
