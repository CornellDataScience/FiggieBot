'''
Helper functions for pretty-printing game states.
'''


def print_order_book(order_book: dict):
    '''
    Pretty-prints the order book.
    '''
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


def print_state(state: dict):
    '''
    Prints a message based on the game state received from the server.
    '''
    if (state["type"] == "error"):
        print(state["data"]["message"])
    elif (state["type"] in ["new_order", "cancel_order", "accept_order", "update_game"]):
        order_book = state["data"]["order_book"]
        state["data"].pop("order_book")
        print(state)
        print_order_book(order_book)
    else:
        print(state)
