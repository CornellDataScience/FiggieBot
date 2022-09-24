# FiggieBot

Creating a game to play Figgie &amp; Train an agent to play against

## Run Backend

- cd backend
- python3 -m venv my_venv
- source my_venv/Scripts/activate
- pip install fastapi "uvicorn[standard]"
- uvicorn app:app --reload
- Websocket available at: ws://127.0.0.1:8000/ws
