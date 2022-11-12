import cardcounting 
import controller
import asyncio
import websockets
from util import constants, classes

uri = "ws://127.0.0.1:8000/ws"

class CardCounter(classes.Player):
    def __init__(self, player_id, websocket, balance, count):
        super().__init__(player_id, websocket, balance)
        count = {}

    async def run(self):
        async with websockets.connect(uri) as websocket:
            await controller.add_player(websocket, self.player_id)
            await controller.start_round(websocket)
            while True:
                request = await websocket.receive_json()

                if request['type'] == 'accept_order':
                    self.count = cardcounting.count_cards(self.count, request)
