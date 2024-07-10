from flask import Flask, request, jsonify
from flask_cors import CORS
from pybloom_live import BloomFilter

app = Flask(__name__)
CORS(app)

PASSWORD_FILE = 'rockyou2024.txt'

# Passwörter einmalig in einen Bloom-Filter laden
bloom_filter = BloomFilter(capacity=1000000, error_rate=0.001)
with open(PASSWORD_FILE, 'r', encoding='utf-8') as file:
    for line in file:
        bloom_filter.add(line.strip())

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')

    if password in bloom_filter:
        return jsonify({"status": "unsafe"})
    else:
        return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
