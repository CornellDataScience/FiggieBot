import random
import asyncio
from inspect import _void
from classes import Player, Order, OrderBook

clients = {}  # map of (player_id, websocket)
players = {}  # map of (player_id, Player)
round_number = 0
empty_bid = Order(-1, -1, True, 0, 0)
empty_offer = Order(-1, -1, False, 0, 0)
empty_bids = {"hearts": empty_bid, "diamonds": empty_bid,
              "clubs": empty_bid, "spades": empty_bid}
empty_offers = {"hearts": empty_offer, "diamonds": empty_offer,
                "clubs": empty_offer, "spades": empty_offer}
order_book = {"bids": empty_bids, "offers": empty_offers}

next_order_id = 0


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
        while(self._timeout > 0):
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
                        "order_book": order_book.toDict()
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


async def add_player(player_id, websocket):
    """
    Adds a player to the game. If a player with this name already exists, send
    an error message to the client.
    """
    if player_id in players:
        websocket.send_json(
            {"type": "error", "data": {"message": "Player already exists"}})
    players[player_id] = Player(player_id, websocket, 350, 0, 0, 0, 0)


async def start_game():
    """
    Starts the game timer and randomizes the cards for each player.
    """
    deal_cards(randomize_suit())
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


async def end_round():
    """
    Function to call when a round ends. Distributes money to players based
    on their number of cards of the goal suit. Then, resets the order book.
    Broadcasts a message to all players that the round has ended.
    """
    for player in players.values():
        if goal_suit == "diamonds":
            player.balance += player.num_diamonds * 10
        if goal_suit == "hearts":
            player.balance += player.num_hearts * 10
        if goal_suit == "spades":
            player.balance += player.num_spades * 10
        if goal_suit == "clubs":
            player.balance += player.num_clubs * 10
    round_number += 1
    goal_suit = ""
    clear_book()
    await broadcast({"type": "end_round"})


async def end_game():
    """
    Function to call when game ends. Calculates winner based on balances
    and broadcasts to all players who the winner is.
    """
    winner = max(players, key=lambda player_id: players[player_id].balance)
    await broadcast({"type": "end_game", "data": {"winner": winner}})

# Goal Suit
goal_suit_int = random.randint(0, 3)
suits = ["diamond", "club", "heart", "spade"]
goal_suit = suits[goal_suit_int]


def count_cards(deck):
    """
    Helper function: Counts the number of each suit in a deck of cards
    """
    counter = {}
    for card in deck:
        if card not in counter:
            counter[card] = 1
        else:
            counter[card] += 1
    print(counter)


def randomize_suit():
    """
    Generate a random deck of 40 cards with 8 of the goal suit, 10 or 12 of the
    opposite suit, and 10 or 12 of the remaining two suits.
    """
    # generate random goal suit, append 8 cards to cardArray of the goal suit
    card_array = []
    suits = ["diamond", "club", "heart", "spade"]
    for i in range(8):
        card_array.append(suits[goal_suit_int])

    # randomize whether the suit opposite the goal suit is 10 or 12 cards
    num_opposite_cards = random.randint(0, 1)
    for i in range(4):
        if i != goal_suit_int and i % 2 == goal_suit_int % 2:
            if num_opposite_cards == 0:
                for j in range(10):
                    card_array.append(suits[i])
            else:
                for j in range(12):
                    card_array.append(suits[i])
            suits.pop(i)
            suits.remove(card_array[0])

    # if opposite goal suit has 12 cards, just append 10 of each remaining suit
    # if opposite goal suit has 10 cards, randomize which of remaining suits
    # gets 12 cards and the other will get 10

    if num_opposite_cards == 1:
        for i in range(10):
            card_array.append(suits[0])
            card_array.append(suits[1])
    elif num_opposite_cards == 0:
        num_cards = random.randint(0, 1)
        for i in range(10):
            card_array.append(suits[num_cards])
        for i in range(12):
            card_array.append(suits[1-num_cards])
    count_cards(card_array)
    return card_array


def deal_cards(deck):
    """
    Requires: 4 players already added to game
    shuffle deck and then distribute cards to each player
    """
    # 40 cards deal 0,4,8...36
    # then deal 1, 5, 9...37
    # then deal 2, 6, 10...38
    #           3,7,11...39
    random.shuffle(deck)
    counter = 0
    for player_id in players:
        player_hand = players[player_id]
        for i in range(10):
            if deck[counter + i*4] == "diamond":
                player_hand.num_diamonds += 1
            elif deck[counter + i*4] == "club":
                player_hand.num_clubs += 1
            elif deck[counter + i*4] == "heart":
                player_hand.num_hearts += 1
            elif deck[counter + i*4] == "spade":
                player_hand.num_spades += 1
        counter += 1
        player_hand.printHand()
    return
