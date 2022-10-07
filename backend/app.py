from fastapi import FastAPI, WebSocket
import json
import game

app = FastAPI(title="FiggieBot Game Engine")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Connecting client...')
    await websocket.accept()
    while True:
        try:
            request = await websocket.receive_json()
            data = request['data']

            if request['type'] == 'add_player':
              print("Adding player...")
              await game.add_player(data['player_id'], websocket)

            if request['type'] == 'start_game':
              print("Starting game...")
              await game.start_game()

            if request['type'] == 'start_game':
              print("Ending game...")
              await game.end_game()

            if request['type'] == 'place_order':
              print("Placing order...")
            
            if request['type'] == 'cancel order':
              print("Cancelling order...")

            if request['type'] == 'accept_order':
              print("Accepting order...")

        except Exception as e:
            print('error:', e)
            break
    print('Disconnecting client...')