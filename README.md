# FiggieBot

Creating a game to play Figgie &amp; Train an agent to play against

## Run Backend

- cd backend
- python3 -m venv websocket
- source websocket/Scripts/activate
- pip install fastapi "uvicorn[standard]"
- uvicorn app:app --reload
- will be available at: ws://127.0.0.1:8000/ws
