# fmt: off
import cardcounting 
import controller
import pretty_printer as pp
import asyncio
import json 
import sys
sys.path.insert(0, "../")
import websockets
from util import constants
# fmt: on

uri = "ws://127.0.0.1:8000/ws"


class CardCounter():
    def __init__(self):
        self.player_id = "Cardcounting bot"
        self.count = {}

    async def run(self):
        async with websockets.connect(uri) as websocket:
            await controller.add_player(websocket, self.player_id)
            await controller.start_round(websocket)
            while True:
                request = await controller.get_game_update(websocket)

                pp.print_state(request)
                if request['type'] == 'accept_order':
                    print("got accept order")
                    self.count = cardcounting.count_cards(self.count, request)
                    dist = cardcounting.deck_distribution(self.count)
                    for s in constants.SUITS:
                        print(
                            "Expected buy: " + str(cardcounting.expected_value_buy(s, self.hand[s], dist)))
                        print(
                            "Expected sell" + str(cardcounting.expected_value_sell(s, self.hand[s], dist)))


cardcounter = CardCounter(start_round=True)
asyncio.get_event_loop().run_until_complete(cardcounter.run())
