class Player:
    def __init__(self, player_id, hand, balance, orders):
        self.player_id = player_id
        self.orders = orders
        self.balance = balance
        self.hand = {"hearts": int, "diamonds": int,
                     "clubs": int, "spades": int}


class Order:
    def __init__(self, order_id, player_id, is_bid, suit, price):
        self.order_id = order_id
        self.player_id = player_id
        self.is_bid = is_bid
        self.suit = suit
        self.price = price


class OrderBook:
    def __init__(self, hearts_bid, hearts_offer, diamonds_bid, diamonds_offer, clubs_bid, clubs_offer, spades_bid, spades_offer):
        self.hearts_bid = hearts_bid
        self.hearts_offer = hearts_offer
        self.diamonds_bid = diamonds_bid
        self.diamonds_offer = diamonds_offer
        self.clubs_bid = clubs_bid
        self.clubs_offer = clubs_offer
        self.spades_bid = spades_bid
        self.spades_offer = spades_offer
