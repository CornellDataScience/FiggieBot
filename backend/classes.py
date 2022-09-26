class Player:
  def __init__(self, player_id, num_hearts, num_diamonds, num_clubs, num_spades, balance, orders):
    self.player_id = player_id
    self.orders = orders
    self.balance = balance
    self.num_hearts = num_hearts
    self.num_diamonds = num_diamonds
    self.num_clubs = num_clubs
    self.num_spades = num_spades

class Order:
  def __init__(order_id, player, is_bid, suit, price, time_stamp):
    self.order_id = order_id
    self.player = player
    self.is_bid = is_bid
    self.suit = suit
    self.price = price
    self.time_stamp = time_stamp

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