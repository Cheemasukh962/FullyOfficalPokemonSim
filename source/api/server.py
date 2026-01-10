import requests
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

CWD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUBLIC_DIR = os.path.join(CWD, "public")

# Add root to path so we can import project modules
sys.path.insert(0, CWD)

# Import database via absolute or local module name
try:
    from source.api.database import init_db, db, Battle
except ModuleNotFoundError:
    from database import init_db, db, Battle

# Support both old `Apitry.py` name and the renamed `Logic.py` on GitHub.
try:
    import Apitry
except ModuleNotFoundError:
    try:
        import Logic as Apitry
    except Exception:
        # Re-raise original import error for visibility
        raise

app = Flask(__name__, static_folder=PUBLIC_DIR, static_url_path="")
CORS(app)

# Database configuration - use PostgreSQL in production, SQLite locally
if os.getenv('DATABASE_URL'):
    # Vercel/Production: use PostgreSQL
    database_url = os.getenv('DATABASE_URL')
    # Fix PostgreSQL URL scheme if needed (postgres:// -> postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development: use SQLite
    db_path = os.path.join(CWD, "pokemon_battle.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

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


@app.route("/api/battle", methods=["POST"])
def battle():
    """Execute a battle between two Pokémon using Apitry logic (attack comparison).
    Stores result in database.
    
    Request JSON:
        {
            "pokemon1": "pokemon-name",
            "pokemon2": "pokemon-name"
        }
    
    Response:
        {
            "winner": "pokemon-name",
            "loser": "pokemon-name",
            "winner_attack": 100,
            "loser_attack": 80,
            "battle_id": 1
        }
    """
    from flask import request
    
    data = request.get_json()
    if not data or "pokemon1" not in data or "pokemon2" not in data:
        return jsonify({"error": "Missing pokemon1 or pokemon2"}), 400
    
    pokemon1 = data["pokemon1"].lower().strip()
    pokemon2 = data["pokemon2"].lower().strip()
    
    # Use Apitry battle logic (attack-based)
    result = Apitry.battle_pokemon_logic(pokemon1, pokemon2)
    
    if "error" in result:
        return jsonify(result), 409 if "tie" in result.get("error", "").lower() else 400
    
    # Store battle in database
    battle = Battle(
        winner=result["winner"],
        loser=result["loser"],
        winner_stats=result["winner_attack"],
        loser_stats=result["loser_attack"]
    )
    db.session.add(battle)
    db.session.commit()
    
    return jsonify({
        "winner": result["winner"],
        "loser": result["loser"],
        "winner_attack": result["winner_attack"],
        "loser_attack": result["loser_attack"],
        "battle_id": battle.id
    })


@app.route("/api/stats")
def get_stats():
    """Retrieve battle statistics and history.
    
    Query parameters:
        ?pokemon=name : Filter by Pokémon (as winner or loser)
        ?limit=10 : Limit number of results (default: 50)
    """
    from flask import request
    
    limit = min(int(request.args.get("limit", 50)), 100)
    pokemon_filter = request.args.get("pokemon", "").lower()
    
    query = Battle.query.order_by(Battle.created_at.desc()).limit(limit)
    
    battles = query.all()
    
    if pokemon_filter:
        battles = [b for b in battles if pokemon_filter in b.winner.lower() or pokemon_filter in b.loser.lower()]
    
    # Calculate aggregate stats
    total_battles = len(battles)
    pokemon_wins = {}
    
    for battle in battles:
        if battle.winner not in pokemon_wins:
            pokemon_wins[battle.winner] = 0
        pokemon_wins[battle.winner] += 1
    
    return jsonify({
        "total_battles": total_battles,
        "pokemon_wins": pokemon_wins,
        "recent_battles": [b.to_dict() for b in battles[:10]]
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)