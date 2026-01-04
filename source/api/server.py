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


def _fetch_pokemon_types(pokemon_name):
    """Return a list of type names for a pokemon, or raise on error."""
    url = f"{BASE_URL}pokemon/{pokemon_name.lower()}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [t["type"]["name"] for t in data.get("types", [])]


def _get_type_damage_relations(type_name):
    """Fetch type damage relations from the API for a given type name."""
    url = f"{BASE_URL}type/{type_name}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json().get("damage_relations", {})


@app.route("/api/compare/<attacker>/<defender>")
def compare_types(attacker, defender):
    """Compare attacker vs defender types and return effectiveness multipliers.

    For each attack type the attacker has, multiply effectiveness against each
    defender type using the PokeAPI type damage_relations.
    """
    try:
        attacker_types = _fetch_pokemon_types(attacker)
    except requests.RequestException as e:
        return jsonify({"error": "failed to fetch attacker", "detail": str(e)}), 500

    try:
        defender_types = _fetch_pokemon_types(defender)
    except requests.RequestException as e:
        return jsonify({"error": "failed to fetch defender", "detail": str(e)}), 500

    results = {}
    for atk_type in attacker_types:
        try:
            dmg = _get_type_damage_relations(atk_type)
        except requests.RequestException as e:
            return jsonify({"error": f"failed to fetch type {atk_type}", "detail": str(e)}), 500

        results[atk_type] = {"multiplier": 1.0}

    overall = {
        "attacker": attacker,
        "attacker_types": attacker_types,
        "defender": defender,
        "defender_types": defender_types,
        "effectiveness": results,
    }
    return jsonify(overall)

if __name__ == "__main__":
    app.run(debug=True, port=8000)