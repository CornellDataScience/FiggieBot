'''
Helper functions for pretty-printing game states.
'''


def print_order_book(order_book: dict):
    '''
    Pretty-prints the order book.
    '''
    if (order_book == None):
        return
    print("Current Order Book:")
    for suit in order_book["bids"].keys():
        order = order_book["bids"][suit]
        if order["order_id"] == -1:
            continue
        print(order["player_id"], "bids",
              order["suit"], "at price", order["price"])

    for suit in order_book["offers"].keys():
        order = order_book["offers"][suit]
        if order["order_id"] == -1:
            continue
        print(order["player_id"], "offers",
              order["suit"], "at price", order["price"])


def print_hand(hand: dict):
    print("Your current hand:")
    for suit in hand.keys():
        print("- ", suit, ": ", hand[suit], sep="")


def print_players(players: list[dict]):
    print("Current players:")
    for player in players:
        print("- ", player["player_id"],
              ", balance: ", player["balance"], sep="")


def print_state(state: dict):
    '''
    Prints a message based on the game state received from the server.
    '''
    if (("type" not in state.keys()) or ("data" not in state.keys())):
        print(state)
    elif (state["type"] == "error"):
        print("Error:", state["data"]["message"])
    elif (state["type"] == "place_order"):
        print("New order:", state["data"]["message"])
        order_book = state["data"].pop("order_book")
        print_order_book(order_book)
    elif (state["type"] == "update_game"):
        round_no = player_info = state["data"].pop("round_number")
        # print("Round", round_no + 1)
        time = state["data"].pop("time")
        print("Time remaining:", time)
        player_info = state["data"].pop("player")
        print_hand(hand=player_info["hand"])
        players = state["data"].pop("players")
        print_players(players)
        order_book = state["data"].pop("order_book")
        print_order_book(order_book)
    else:
        order_book = None
        if ("order_book" in state["data"].keys()):
            order_book = state["data"].pop("order_book")
        print(state)
        print_order_book(order_book)
