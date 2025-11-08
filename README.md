# David Tutor

Quick setup and run instructions for local development (macOS / zsh).

Prerequisites
- Python 3.11+ installed (we create a project virtualenv; system Python won't be used).

Create and activate the virtual environment (already created by the dev tooling in this repo):

```bash
# create (if not created):
python3 -m venv .venv

# activate (zsh)
source .venv/bin/activate

# install dependencies for backend and frontend
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

Run backend (FastAPI + Uvicorn):

```bash
# from project root, with .venv activated
uvicorn backend.app.main:app --reload --port 8000
```

Run frontend (Streamlit):

```bash
# from project root, with .venv activated
streamlit run frontend/app.py
```

VS Code
- The repository includes a recommended workspace setting at `.vscode/settings.json` which points the Python interpreter to `${workspaceFolder}/.venv/bin/python`. Open the Command Palette → "Python: Select Interpreter" to confirm, then reload the window.

Notes
- Don't commit virtual environments. `.venv/` is in `.gitignore`.

Environment variables (important for deployments)
- `ANTHROPIC_API_KEY` (backend) — din Anthropic API-nyckel.
- `APP_API_KEY` (backend + frontend) — server-till-server API-nyckel som frontend skickar i headeren `X-API-KEY`. Sätt detta i både backend- och frontend-deploy för att autentisera anrop.
- `DAVID_PASSWORD` (frontend) — ett enkelt lösenord som endast David känner till; Streamlit-frontend kräver detta innan chattgränssnittet visas.

When deploying to Render (or similar), add the three env vars to the service settings. `APP_API_KEY` must match between frontend and backend so only authenticated requests succeed.
# David Tutor Cloud
