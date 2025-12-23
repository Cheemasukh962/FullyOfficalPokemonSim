import requests
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

CWD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUBLIC_DIR = os.path.join(CWD, "public")

app = Flask(__name__, static_folder=PUBLIC_DIR, static_url_path="")
CORS(app)

BASE_URL = "https://pokeapi.co/api/v2/"

@app.route("/")
def index():
    """Serve the homepage."""
    return app.send_static_file("index.html")

@app.route("/api/pokemon/<pokemon_name>")
def get_pokemon(pokemon_name):
    """Fetch Pokémon data from pokeapi.co"""
    url = f"{BASE_URL}pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return jsonify({"error": "Pokémon not found"}), 404
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": "network error", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)