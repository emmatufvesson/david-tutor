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
# David Tutor Cloud
