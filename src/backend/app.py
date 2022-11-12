from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

            if request['type'] == 'start_round':
                await game.start_round()

            if request['type'] == 'end_game':
                await game.end_game()

            if request['type'] == 'add_player':
                await game.add_player(data['player_id'], websocket)

            if request['type'] == 'place_order':
                await game.place_order(data['player_id'], data['is_bid'], data['suit'], data['price'])

            if request['type'] == 'cancel_order':
                await game.cancel_order(data['player_id'], data['is_bid'], data['suit'])

            if request['type'] == 'accept_order':
                print("Accepting order...")
                await game.accept_order(data['accepter_id'], data['is_bid'], data['suit'])

        except WebSocketDisconnect:
            print('Disconnecting client...')
            break

        except Exception as e:
            print('error:', e)

    print('Disconnecting client...')
