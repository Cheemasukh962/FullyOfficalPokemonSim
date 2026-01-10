# FullyOfficialPokemonSim
**https://fullyofficalpokemonsim-production.up.railway.app/index.html**

A Flask + SQLAlchemy web app that lets users fetch Pokémon data and simulate simple battles based on attack stats. Frontend is served from `public/` and backend exposes a small REST API. Deployed on Railway with PostgreSQL.

## Stack
- Python (Flask, SQLAlchemy)
- PostgreSQL (Railway)
- Gunicorn (Prod server)
- Frontend: HTML/CSS/JS in `public/`

## Project Structure
- `api/app.py` — platform entrypoint for Gunicorn
- `source/api/server.py` — Flask app + routes
- `source/api/database.py` — SQLAlchemy `Battle` model and `init_db()`
- `public/` — frontend assets (index, scripts, styles)
- `Procfile` — start command for Railway (`gunicorn api.app:app`)
- `requirements.txt` — Python dependencies

## Environment
- `DATABASE_URL` (required in production): PostgreSQL connection string provided by Railway.
  - Example: `postgresql://USER:PASS@HOST:PORT/DBNAME`
  - If a provider gives `postgres://...`, the app will auto-convert to `postgresql://...`.
- Local fallback: when `DATABASE_URL` is not set, the app uses SQLite at `pokemon_battle.db`.

## Run Locally (Windows PowerShell)
```powershell
cd "C:\Users\cheem\Python workspace"
# Option A: SQLite (no env vars)
.venv\Scripts\python.exe source\api\server.py

# Option B: PostgreSQL (set your DB URL)
$env:DATABASE_URL = 'postgresql://USER:PASS@HOST:5432/DBNAME'
.venv\Scripts\python.exe source\api\server.py
```
- App runs at http://localhost:8000

## Deploy on Railway(for me to remember)
1. Create a Railway project and add PostgreSQL (free tier available).
2. Copy the Postgres connection string and set it as a Variable:
   - Key: `DATABASE_URL`
   - Value: `<your Postgres URL>`
3. Connect this GitHub repo to Railway and deploy.
4. Railway detects `Procfile` and runs:
   - `web: gunicorn api.app:app --bind 0.0.0.0:$PORT --workers 2`

## API Endpoints
- `GET /api/pokemon/<name>` — fetch Pokémon JSON from PokeAPI.
- `POST /api/battle` — run a battle and persist result.
  - Body: `{ "pokemon1": "pikachu", "pokemon2": "charizard" }`
  - Response: `{ "winner": "pikachu", "loser": "charizard", "winner_attack": 100, ... }`
- `GET /api/stats?limit=50&pokemon=pikachu` — recent battles with simple aggregates.

## Notes
- Persistence: battles are stored in PostgreSQL in production; SQLite locally.
- Ephemeral storage: don’t rely on local files in hosted environments.
- The app supports both `Apitry.py` and `Logic.py` as the battle logic module via a fallback import.

## Troubleshooting
- Import errors on Railway: ensure `api/app.py` adds the project root to `sys.path` and `DATABASE_URL` is set.
- DB errors: verify `DATABASE_URL` and network access; on boot, `init_db(app)` runs `db.create_all()`.
- Start issues: confirm `Procfile` is present and that Railway shows Gunicorn binding to `0.0.0.0:$PORT` in logs.
