# fmt: off
import asyncio
import websockets
import controller
import random
import pretty_printer as pp
import sys
sys.path.insert(0, "../")
from util import constants
# fmt: on

'''
A player that places random bids in the range [bid_low, bid_high], and random offers in the range [offer_low, offer_high]
'''

uri = "ws://127.0.0.1:8000/ws"


class RandomPlayer:
    def __init__(self, bid_low, bid_high, offer_low, offer_high, order_period, start_round):
        self.player_id = "Random Player"  # + str(random.random())
        self.bid_low = bid_low
        self.bid_high = bid_high
        self.offer_low = offer_low
        self.offer_high = offer_high
        self.order_period = order_period
        self.start_round = start_round

    async def run(self):
        async with websockets.connect(uri) as websocket:
            await controller.add_player(websocket, self.player_id)
            if (self.start_round):
                await controller.start_round(websocket)
            request = await controller.get_game_update(websocket)
            # request should either be add_player
            # or an error saying that player already exists
            pp.print_state(request)
            while (not await controller.round_started(websocket)):
                # Wait until round starts
                pass
            while True:
                if (random.random() > 0.5):
                    await controller.place_bid(
                        websocket,
                        self.player_id,
                        suit=random.choice(constants.SUITS),
                        price=random.randint(self.bid_low, self.bid_high))
                else:
                    await controller.place_offer(
                        websocket,
                        self.player_id,
                        suit=random.choice(constants.SUITS),
                        price=random.randint(self.offer_low, self.offer_high))
                await asyncio.sleep(self.order_period)
                game_state = await controller.get_game_update(websocket)
                pp.print_state(game_state)


random_player = RandomPlayer(
    bid_low=1, bid_high=10, offer_low=5, offer_high=15, order_period=3, start_round=True)
asyncio.get_event_loop().run_until_complete(random_player.run())
