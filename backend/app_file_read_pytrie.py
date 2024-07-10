from flask import Flask, request, jsonify
from flask_cors import CORS
import pytrie

app = Flask(__name__)
CORS(app)

PASSWORD_FILE = 'rockyou2024.txt'

# Passwörter einmalig in einen Trie laden
trie = pytrie.StringTrie()
with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
    for line in file:
        trie[line.strip()] = True

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')

    if password in trie:
        return jsonify({"status": "unsafe"})
    else:
        return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
