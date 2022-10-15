import asyncio
import websockets
import controller
import random

'''
A player that places random bids in the range [1, 10], and random offers in the range [5, 15]
'''

uri = "ws://127.0.0.1:8000/ws"


class RandomPlayer:
    def __init__(self):
        self.player_id = "Random Player"

    async def run(self):
        async with websockets.connect(uri) as ws:
            controller.add_player(ws, self.player_id)
            while True:
                await controller.place_bid(
                    ws, player_id=self.player_id, suit="hearts", price=random.randint(1, 10))


random_player = RandomPlayer()
asyncio.get_event_loop().run_until_complete(random_player.run())
