import asyncio
import websockets
import controller
import random
import json

'''
A player that places random bids in the range [1, 10], and random offers in the range [5, 15]
'''

uri = "ws://127.0.0.1:8000/ws"


class RandomPlayer:
    def __init__(self):
        self.player_id = "Random Player" + str(random.random())

    async def run(self):
        async with websockets.connect(uri) as websocket:
            await controller.add_player(websocket, self.player_id)
            await controller.start_game(websocket)
            while True:
                await controller.place_bid(
                    websocket, player_id=self.player_id, suit="hearts", price=random.randint(1, 10))
                await asyncio.sleep(1)
                msg_json = await websocket.recv()
                print(msg_json)


random_player = RandomPlayer()
asyncio.get_event_loop().run_until_complete(random_player.run())
