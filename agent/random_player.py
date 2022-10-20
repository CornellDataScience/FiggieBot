import asyncio
import websockets
import controller
import random
import constants

'''
A player that places random bids in the range [bid_low, bid_high], and random offers in the range [offer_low, offer_high]
'''

uri = "ws://127.0.0.1:8000/ws"


class RandomPlayer:
    def __init__(self, bid_low, bid_high, offer_low, offer_high):
        self.player_id = "Random Player" + str(random.random())
        self.bid_low = bid_low
        self.bid_high = bid_high
        self.offer_low = offer_low
        self.offer_high = offer_high

    async def run(self):
        async with websockets.connect(uri) as websocket:
            await controller.add_player(websocket, self.player_id)
            await controller.start_game(websocket)
            while True:
                if (random.random() > 0.5):
                    await controller.place_bid(
                        websocket,
                        self.player_id,
                        suit=random.choice(constants.SUITS),
                        price=random.randint(self.bid_low, self.bid_high))
                else:
                    # TODO: Offer placement does not work - doesn't show up in order book
                    await controller.place_offer(
                        websocket,
                        self.player_id,
                        suit=random.choice(constants.SUITS),
                        price=random.randint(self.offer_low, self.offer_high))
                await asyncio.sleep(1)
                game_state = await controller.get_game_update(websocket)
                print(game_state)


random_player = RandomPlayer(
    bid_low=1, bid_high=10, offer_low=5, offer_high=15)
asyncio.get_event_loop().run_until_complete(random_player.run())
