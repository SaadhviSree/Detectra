from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    path = data.get('path')
    case_id = data.get('case_id', None)

    if not path or not os.path.exists(path):
        return jsonify({"error": "Invalid path"}), 400

    cmd = ["python", "detectra-app/src/backend/main.py", path]
    if case_id:
        cmd.extend(["--case-id", case_id])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return jsonify({"message": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

if __name__ == '__main__':
    app.run(debug=True)
