import asyncio
from inspect import _void
from classes import Player, Order, OrderBook

clients = {}  # map of (player_id, websocket)
players = {}  # map of (player_id, Player)
round_number = 0
empty_bid = Order(-1, -1, True, 0, 0)
empty_offer = Order(-1, -1, False, 0, 0)
# order_book = OrderBook(empty_bid, empty_offer, empty_bid, empty_offer, empty_bid, empty_offer, empty_bid, empty_offer)
empty_bids = {"hearts": empty_bid, "diamonds": empty_bid,
              "clubs": empty_bid, "spades": empty_bid}
empty_offers = {"hearts": empty_offer, "diamonds": empty_offer,
                "clubs": empty_offer, "spades": empty_offer}
order_book = {"bids": empty_bids, "offers": empty_offers}

next_order_id = 0


class Timer:
    def __init__(self, timeout):
        self._timeout = timeout
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while(self._timeout > 0):
            await asyncio.sleep(1)
            self._timeout -= 1
            # should this broadcast be personalized to player? only send player their own info
            # maybe include numPlayers in broadcast
            await broadcast({
                "type": "update_game",
                "data": {
                    "round_number": round_number,
                    "time": self._timeout,
                    # make sure individual order objects are converted to dicts
                    "players": [vars(players[player_id]) for player_id in players],
                    # make sure individual order objects are converted to dicts
                    "order_book": vars(order_book)
                }
            })
        # call some sort of end game function to distribute money and reset game state
        await broadcast({"type": "end_game"})

    def cancel(self):
        self._task.cancel()


async def broadcast(json_message):
    for websocket in clients.values():
        await websocket.send_json(json_message)


async def add_player(player_id, websocket):
    clients[player_id] = websocket
    players[player_id] = Player(player_id, 0, 0, 0, 0, 350, [])
    # make sure no repeat names (override other players)


async def start_game():
    Timer(240)
    # make sure we have enough players
    # randomize cards and deal to players
    await broadcast({"type": "start_game"})


# MANAGING THE ORDER BOOK:
# - should only be updated whenever a player makes/updates a bid/offer
# - cancel ALL orders in the book when any bid/offer is fulfilled
# - at maximum, there is only one bid and one offer per suit on the order book at all times


async def place_order(player_id, is_bid, suit, price):
    """PLACE ORDER:
    - if a player overrides a bid/offer (i.e. places a strictly higher bid or lower offer
    than what's shown on the order book), then update the order book with newest
    (and better) bid/offer
    - if a player places a strictly lower bid or higher offer than what's shown on the current
    order book, don't change the order book (e.g. instead show the player an error
    message and/or return void or just the current order book unchanged)
    """
    new_order = Order(next_order_id, player_id, is_bid, suit, price)

    list = determine_order(player_id, is_bid, suit)
    order_type = list[0]
    prev_order = list[2]

    if (order_type == "bids" and prev_order.price < price) or (order_type == "offers" and prev_order.price > price):
        order_book[order_type][suit] = new_order
        next_order_id += 1


async def cancel_order(player_id, is_bid, suit):
    """ CANCEL ORDER:
    - update the order book with an empty bid/offer
    """
    list = determine_order(player_id, is_bid, suit)
    order_type = list[0]
    empty_order = list[1]
    prev_order = list[2]

    if prev_order.player_id == player_id:
        order_book[order_type][suit] = empty_order


async def clear_book():
    """ CLEAR BOOK:
    - clear the entire order book of bids/offers
    """
    order_book = {"bids": empty_bids, "offers": empty_offers}


async def accept_order(buyer_id, seller_id, suit, price):
    """ACCEPT ORDER:
    - check if an order can and should be accepted
    - update the order book by removing all current bids/offers
    - update the money and hand (i.e. count, kind) of cards for the two players involved
    """
    buyer = players[buyer_id]
    seller = players[seller_id]
    buyer_suit_hand = buyer.hand[suit]
    seller_suit_hand = seller.hand[suit]
    if (seller_suit_hand > 0) and (buyer.balance >= price):
        buyer_suit_hand[suit] += 1
        seller_suit_hand[suit] -= 1
        buyer.balance -= price
        seller.balance += price
        clear_book()


def determine_order(player_id, is_bid, suit):
    """DETERMINE ORDER (helper):
    - determines if the order is a bid/offer
    - returns a list [order_type, empty_order, prev_order]
      - order_type either denotes "bids" or "offers"
      - empty_order is the corresponding empty bid or offer (type Order)
      - prev_order is the corresponding previous bid or offer (type Order) 
      in the order book corresponding to the suit
    """
    if is_bid:
        order_type = "bids"
        empty_order = empty_bid
    else:
        order_type = "offers"
        empty_order = empty_offer

    prev_order = order_book[order_type][suit]

    return [order_type, empty_order, prev_order]
