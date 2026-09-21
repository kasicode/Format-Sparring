import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/proxy", methods=["POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response, 200

    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    data = request.get_json()
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        json=data,
        timeout=60,
    )
    response = jsonify(resp.json())
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response, resp.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
