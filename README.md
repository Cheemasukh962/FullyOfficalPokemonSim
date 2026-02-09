# FullyOfficialPokemonSim

A Flask + SQLAlchemy web app that lets users fetch Pokémon data and simulate simple battles based on attack stats. Frontend is served from `public/` and backend exposes a small REST API. Can be deployed on Railway or Vercel with PostgreSQL.

## Stack
- Python (Flask, SQLAlchemy)
- PostgreSQL (Railway/Vercel)
- Gunicorn (Railway) / WSGI (Vercel)
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



## Deploy on Railway
1. Create a Railway project and add PostgreSQL (free tier available).
2. Copy the Postgres connection string and set it as a Variable:
   - Key: `DATABASE_URL`
   - Value: `<your Postgres URL>`
3. Connect this GitHub repo to Railway and deploy.
4. Railway detects `Procfile` and runs:
   - `web: gunicorn api.app:app --bind 0.0.0.0:$PORT --workers 2`

## Deploy on Vercel
1. Install the Vercel CLI: `npm i -g vercel`
2. Link your project: `vercel link` (or connect via Vercel dashboard)
3. Set up a PostgreSQL database:
   - Option A: Use Vercel Postgres (add from Vercel dashboard Storage tab)
   - Option B: Use external PostgreSQL (Railway, Neon, Supabase, etc.)
4. Set environment variables in Vercel:
   - Key: `DATABASE_URL`
   - Value: `postgresql://user:password@host:5432/dbname` (your Postgres URL)
   - Key: `FLASK_ENV`
   - Value: `production`
5. Deploy: `vercel --prod` or push to connected GitHub branch
6. Vercel will:
   - Detect `vercel.json` configuration
   - Install dependencies from `requirements.txt`
   - Deploy the Flask app as serverless functions
   - Serve static files from `public/` directory

### Important Notes for Vercel:
- Vercel runs Flask as serverless functions (stateless)
- Database connections should be managed efficiently (connection pooling recommended)
- Static files are served from the `public/` directory
- The `vercel.json` configuration handles routing between API and static files
- Environment variables must be set in Vercel dashboard or via CLI

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

### Railway
- Import errors on Railway: ensure `api/app.py` adds the project root to `sys.path` and `DATABASE_URL` is set.
- DB errors: verify `DATABASE_URL` and network access; on boot, `init_db(app)` runs `db.create_all()`.
- Start issues: confirm `Procfile` is present and that Railway shows Gunicorn binding to `0.0.0.0:$PORT` in logs.

### Vercel
- Function timeout: Vercel has a 10s timeout for hobby tier, 60s for Pro. Ensure API calls complete within limits.
- Cold starts: First request after inactivity may be slower due to serverless function initialization.
- Static files: Ensure static assets are in the `public/` directory and referenced correctly.
- Database connections: Use connection pooling to avoid exhausting database connections (e.g., `pool_pre_ping=True` in SQLAlchemy).
- Build errors: Check Vercel deployment logs for Python dependency issues.
- Environment variables: Verify `DATABASE_URL` and `FLASK_ENV` are set in Vercel project settings.
