import json

class Player:
  def __init__(self, player_id, websocket, orders, balance, num_hearts, num_diamonds, num_clubs, num_spades):
    self.player_id = player_id
    self.websocket = websocket
    self.balance = balance
    self.num_hearts = num_hearts
    self.num_diamonds = num_diamonds
    self.num_clubs = num_clubs
    self.num_spades = num_spades

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

class Order:
  def __init__(self, order_id, player_id, is_bid, suit, price, time_stamp):
    self.order_id = order_id
    self.player_id = player_id
    self.is_bid = is_bid
    self.suit = suit
    self.price = price
    self.time_stamp = time_stamp

  def toDict(self):
    return self.__dict__

class OrderBook:
  def __init__(self, hearts_bids, hearts_offers, diamonds_bids, diamonds_offers, clubs_bids, clubs_offers, spades_bids, spades_offers):
    self.hearts_bids = hearts_bids
    self.hearts_offers = hearts_offers
    self.diamonds_bids = diamonds_bids
    self.diamonds_offers = diamonds_offers
    self.clubs_bids = clubs_bids
    self.clubs_offers = clubs_offers
    self.spades_bids = spades_bids
    self.spades_offers = spades_offers

  def toDict(self):
    return self.__dict__