'''
A helper class for deciding what order to send.
Implements Algorithm 2 in the paper.
'''

# fmt: off
import random
import math
import controller
from enum import Enum, auto
import sys
sys.path.insert(0, "../")
from util import constants
# fmt: on


class OrderType(Enum):
    BID = auto()
    OFFER = auto()
    ACCEPT_BID = auto()
    ACCEPT_OFFER = auto()


class Order:
    def __init__(self, order_type, price):
        self.order_type = order_type
        self.price = price


async def propose_and_send(ws, player_id, suit, expected_buy, expected_sell,
                           market_buy=math.inf, market_sell=-math.inf) -> Order:
    '''
    Propose and send a new order based on Algorithm 2.
    '''
    if (random.random() > 0.5):
        # Buying
        price = random.randint(0, expected_buy + 1)
        if (price < market_buy):
            # Place a new bid
            await controller.place_bid(ws, player_id, suit, price)
            return Order(OrderType.BID, price)
        else:
            # Accept current bid
            await controller.accept_bid(ws, player_id, suit)
            return Order(OrderType.ACCEPT_BID, -1)
    else:
        # Selling
        price = random.randint(expected_sell, 2 * expected_sell + 1)
        if (price > market_sell):
            # Place a new offer
            await controller.place_offer(ws, player_id, suit, price)
            return Order(OrderType.OFFER, price)
        else:
            # Accept current offer
            await controller.accept_offer(ws, player_id, suit)
            return Order(OrderType.ACCEPT_OFFER, -1)
