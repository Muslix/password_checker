from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS-Unterstützung hinzufügen

PASSWORD_FILE = 'rockyou2024.txt'  # Dein Dateiname hier

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')
    is_unsafe = False

    with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            if password == line.strip():
                is_unsafe = True
                break

    if is_unsafe:
        return jsonify({"status": "unsafe"})
    else:
        return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
