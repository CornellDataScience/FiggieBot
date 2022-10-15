# FiggieBot

Creating a game to play Figgie &amp; Train an agent to play against

## Run Backend

### Mac

- cd backend
- python3 -m venv my_venv
- source my_venv/Scripts/activate (may be source ". my_venv/bin/activate" on Mac)
- pip install fastapi "uvicorn[standard]"
- uvicorn app:app --reload
- Websocket available at: ws://127.0.0.1:8000/ws

### Windows Powershell

May need to run `Set-ExecutionPolicy Unrestricted -Scope Process` (allow running scripts for the current PowerShell session) or `Set-ExecutionPolicy Unrestricted -Force` (less safe) if execution policy is restricted.

- cd backend
- python -m venv my_venv
- my_venv\Scripts\Activate.ps1
- pip install fastapi "uvicorn[standard]"
- uvicorn app:app --reload
- Websocket available at: ws://127.0.0.1:8000/ws
