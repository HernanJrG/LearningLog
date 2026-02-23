# LearningLog Project 2

This repository now includes all required layers for **CSCE 548 Project 2**:

- Data layer (existing DAOs + SQL schema)
- Business layer (service classes that wrap all DAO CRUD methods)
- Service layer (FastAPI endpoints that expose all business methods)
- Console client (invokes services over HTTP for end-to-end testing)

## Project Structure

- `app/daos/`: data layer (existing Project 1 CRUD)
- `app/business/`: business layer methods and validation/error handling
- `app/api/`: HTTP service layer (FastAPI app + routers + schemas)
- `app/client/`: console client that calls service endpoints
- `sql/schema.sql`: PostgreSQL schema
- `sql/seed.sql`: seed data

## Dependencies

Dependencies are in `requirements.txt` and are installed automatically by `run.sh`.

Configuration:

- Copy `.env.example` to `.env` and set your DB credentials.
- `run.sh` auto-loads `.env`.

## Run Modes

`run.sh` supports:

- `./run.sh api` (default): start FastAPI service on port `8000`
- `./run.sh client`: start console client (calls the service endpoints)
- `./run.sh legacy-cli`: run the old direct-DAO CLI

On Windows, use:

- `run.bat` (defaults to API mode)
- `run.bat client`
- `run.bat legacy-cli`

`run.bat` starts WSL and executes `run.sh` inside Ubuntu.

## Setup (WSL Ubuntu on Windows 11)

1. Install WSL Ubuntu (PowerShell as admin):
   - `wsl --install -d Ubuntu`
2. Reboot if prompted, then open Ubuntu and finish first-time setup.
3. In Ubuntu, install Python and build tools:
   - `sudo apt update`
   - `sudo apt install -y python3 python3-venv python3-pip build-essential libpq-dev`
4. Install PostgreSQL (or connect to an existing instance):
   - `sudo apt install -y postgresql postgresql-contrib`
5. Start PostgreSQL:
   - `sudo service postgresql start`
6. Create database:
   - `sudo -u postgres psql -c "CREATE DATABASE learninglog;"`
7. From project root, apply schema and seed:
   - `sudo -u postgres psql -d learninglog -f sql/schema.sql`
   - `sudo -u postgres psql -d learninglog -f sql/seed.sql`
8. Set DB connection (if needed) and run API:
   - `export DATABASE_URL='postgresql://postgres@localhost:5432/learninglog'`
   - `./run.sh api`
9. In a second terminal, run client:
   - `./run.sh client`
10. In client menu, run **full CRUD smoke test**.

### PostgreSQL Auth Troubleshooting (`fe_sendauth: no password supplied`)

If you see this error, PostgreSQL requires a password for TCP (`localhost`) connections.

1. Set password for postgres role:
   - `sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"`
2. Create `.env` in project root:
   - `cp .env.example .env`
   - Edit `.env` and set `DB_PASSWORD=postgres`
3. Restart API:
   - `./run.sh api`

### WSL Permission Note

If your project directory is mounted read-only or without write permissions (for example, under `/mnt/...`), `run.sh` automatically falls back to a writable virtualenv path in:

- `$HOME/.cache/learninglog/.venv`

You can also force a specific venv location:

- `export VENV_DIR="$HOME/.venvs/learninglog"`
- `./run.sh api`

## API Endpoints

### Users
- `POST /users`
- `GET /users`
- `GET /users/by-email?email=...`
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

### Topics
- `POST /topics`
- `GET /topics`
- `GET /topics?user_id=...`
- `GET /topics/{topic_id}`
- `PUT /topics/{topic_id}`
- `DELETE /topics/{topic_id}`

### Resources
- `POST /resources`
- `GET /resources?topic_id=...`
- `GET /resources/{resource_id}`
- `PUT /resources/{resource_id}`
- `DELETE /resources/{resource_id}`

### Sessions
- `POST /sessions`
- `GET /sessions?user_id=...`
- `GET /sessions?topic_id=...`
- `GET /sessions/{session_id}`
- `PUT /sessions/{session_id}`
- `DELETE /sessions/{session_id}`

### Reflections
- `POST /reflections`
- `GET /reflections?session_id=...`
- `GET /reflections?topic_id=...`
- `GET /reflections/{reflection_id}`
- `PUT /reflections/{reflection_id}`
- `DELETE /reflections/{reflection_id}`

## Hosting Notes (Render)

1. Push this repo to GitHub.
2. Create Render Web Service from the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.api.main:app --host 0.0.0.0 --port $PORT`
5. Set `DATABASE_URL` environment variable.
6. Use `/health` endpoint to verify deployment.


