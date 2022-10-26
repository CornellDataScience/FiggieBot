import random
import asyncio
from src.util.constants import SUITS, EMPTY_ORDER_BOOK, HEARTS, SPADES, CLUBS, DIAMONDS, EMPTY_BID, EMPTY_OFFER
from src.util.classes import Player, Bid, Offer
import json

players = {}  # map of (player_id, Player)
round_number = 0
next_order_id = 0
order_book = EMPTY_ORDER_BOOK.copy()
goal_suit = SUITS[random.randint(0, 3)]


class Timer:
    """
    Begins a timer that will end the round after the given number of seconds.
    At each second, broadcasts a message to each player to update them on the
    game state. When the timer ends, redistribute pot accordingly.
    """

    def __init__(self, timeout):
        self._timeout = timeout
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while (self._timeout > 0):
            await asyncio.sleep(1)
            self._timeout -= 1
            all_player_data = [players[player_id].publicToDict()
                               for player_id in players]
            for player in players.values():
                await player.websocket.send_json({
                    "type": "update_game",
                    "data": {
                        "round_number": round_number,
                        "time": self._timeout,
                        "player": player.privateToDict(),
                        "players": all_player_data,
                        "order_book": order_book_to_dict(order_book)
                    }
                })
        await end_round()

    def cancel(self):
        self._task.cancel()


async def broadcast(json_message):
    """
    Broadcasts a given json_message to all players in the game.
    """
    for player in players.values():
        await player.websocket.send_json(json_message)


async def start_game():
    """
    Starts the game timer and randomizes the cards for each player.
    """
    goal_suit = SUITS[random.randint(0, 3)]
    deal_cards()
    Timer(240)
    await broadcast({"type": "start_game"})


async def end_game():
    """
    Function to call when game ends. Calculates winner based on balances
    and broadcasts to all players who the winner is.
    """
    winner = max(players, key=lambda player_id: players[player_id].balance)
    await broadcast({"type": "end_game", "data": {"winner": winner}})


async def end_round():
    """
    Function to call when a round ends. Distributes money to players based
    on their number of cards of the goal suit. Then, resets the order book.
    Broadcasts a message to all players that the round has ended.
    """
    for player in players.values():
        player.balance += player.hand[goal_suit] * 10
    round_number += 1
    goal_suit = SUITS[random.randint(0, 3)]
    clear_book()
    await broadcast({"type": "end_round"})


async def add_player(player_id, websocket):
    """
    Adds a player to the game. If a player with this name already exists, send
    an error message to the client.
    """
    if player_id in players:
        await websocket.send_json(
            {"type": "error", "data": {"message": "Player already exists"}})
        return
    players[player_id] = Player(player_id, websocket, 350)


def place_order(player_id, is_bid, suit, price):
    """
    PLACE ORDER:
    - if a player overrides a bid/offer (i.e. places a strictly higher bid or lower offer
    than what's shown on the order book), then update the order book with newest
    (and better) bid/offer
    - if a player places a strictly lower bid or higher offer than what's shown on the current
    order book, don't change the order book (e.g. instead show the player an error
    message and/or return void or just the current order book unchanged)
    """
    global next_order_id

    if is_bid:
        new_order = Bid(next_order_id, player_id, suit, price)
    else:
        new_order = Offer(next_order_id, player_id, suit, price)

    order_type, _, prev_order = determine_order(player_id, is_bid, suit)

    if (order_type == "bids" and prev_order.price < price) or (order_type == "offers" and prev_order.price > price):
        order_book[order_type][suit] = new_order
        next_order_id += 1


def cancel_order(player_id, is_bid, suit):
    """
    CANCEL ORDER:
    - update the order book with an empty bid/offer
    """
    order_type, empty_order, prev_order = determine_order(
        player_id, is_bid, suit)

    if prev_order.player_id == player_id:
        order_book[order_type][suit] = empty_order


def accept_order(accepter_id, is_bid, suit):
    """
    ACCEPT ORDER:
    - check if an order can and should be accepted
    - update the order book by removing all current bids/offers
    - update the money and hand (i.e. count, kind) of cards for the two players involved
    """
    order = order_book["bids" if is_bid else "offers"][suit]

    if order.player_id == accepter_id:
        return

    if is_bid:
        buyer = players[order.player_id]
        seller = players[accepter_id]
    else:
        buyer = players[accepter_id]
        seller = players[order.player_id]

    if (seller.hand[suit] > 0) and (buyer.balance >= order.price):
        buyer.hand[suit] += 1
        seller.hand[suit] -= 1
        buyer.balance -= order.price
        seller.balance += order.price
        clear_book()


def clear_book():
    """
    CLEAR BOOK:
    - clear the entire order book of bids/offers
    """
    order_book = EMPTY_ORDER_BOOK.copy()


def determine_order(player_id, is_bid, suit):
    """
    DETERMINE ORDER (helper):
    - determines if the order is a bid/offer
    - returns a list [order_type, empty_order, prev_order]
      - order_type either denotes "bids" or "offers"
      - empty_order is the corresponding empty bid or offer (type Order)
      - prev_order is the corresponding previous bid or offer (type Order)
      in the order book corresponding to the suit
    """
    if is_bid:
        order_type = "bids"
        empty_order = EMPTY_BID
    else:
        order_type = "offers"
        empty_order = EMPTY_OFFER

    prev_order = order_book[order_type][suit]

    return [order_type, empty_order, prev_order]


def order_book_to_dict(order_book):
    """
    Converts the order book to a dictionary.
    """
    return {
        "bids": {
            suit: order_book["bids"][suit].toDict()
            for suit in SUITS
        },
        "offers": {
            suit: order_book["offers"][suit].toDict()
            for suit in SUITS
        }
    }


def deal_cards():
    """
    Generate a random deck of 40 cards with 8 or 10 of the goal suit, 12 of the
    opposite suit, and 10 or 12 of the remaining two suits.

    Requires: 4 players already added to game
    shuffles deck and then distribute cards to each player
    """
    deck = []
    suits = SUITS.copy()

    # same color but not goal suit gets 12
    if goal_suit == HEARTS:
        deck.extend([DIAMONDS] * 12)
    elif goal_suit == DIAMONDS:
        deck.extend([HEARTS] * 12)
    elif goal_suit == SPADES:
        deck.extend([CLUBS] * 12)
    elif goal_suit == CLUBS:
        deck.extend([SPADES] * 12)

    # goal suit gets 8 or 10
    num_of_goal_suit = random.choice([8, 10])
    deck.extend([goal_suit] * num_of_goal_suit)

    # one of opposite color gets 10 and other gets rest of cards (8 or 10)
    if goal_suit == HEARTS or goal_suit == DIAMONDS:
        suit_with_10 = random.choice([SPADES, CLUBS])
        deck.extend([suit_with_10] * 10)
        if suit_with_10 == SPADES:
            deck.extend([CLUBS] * (40 - len(deck)))
        else:
            deck.extend([SPADES] * (40 - len(deck)))
    else:
        suit_with_10 = random.choice([HEARTS, DIAMONDS])
        deck.extend([suit_with_10] * 10)
        if suit_with_10 == HEARTS:
            deck.extend([DIAMONDS] * (40 - len(deck)))
        else:
            deck.extend([HEARTS] * (40 - len(deck)))

    # nth player gets card at 4i + n where n is 0 through 10
    random.shuffle(deck)
    counter = 0
    for player_id in players:
        for i in range(10):
            players[player_id].hand[deck[counter + i*4]] += 1
        counter += 1
