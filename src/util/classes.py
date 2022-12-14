import json
import datetime
from . import constants


class Player:
    def __init__(self, player_id, websocket, balance, is_ready):
        self.player_id = player_id
        self.websocket = websocket
        self.balance = balance
        self.hand = constants.EMPTY_DECK.copy()
        self.is_ready = is_ready

    def privateToDict(self):
        dict = self.__dict__.copy()
        dict.pop('websocket')
        return dict

    def publicToDict(self):
        dict = {
            "player_id": self.player_id,
            "balance": self.balance
        }
        return dict


class Bid:
    def __init__(self, order_id, player_id, suit, price):
        self.order_id = order_id
        self.player_id = player_id
        self.suit = suit
        self.price = price

    def toDict(self):
        return self.__dict__


class Offer:
    def __init__(self, order_id, player_id, suit, price):
        self.order_id = order_id
        self.player_id = player_id
        self.suit = suit
        self.price = price

    def toDict(self):
        return self.__dict__
