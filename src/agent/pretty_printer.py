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


def print_state(state: dict):
    '''
    Prints a message based on the game state received from the server.
    '''
    if (("type" not in state.keys()) or ("data" not in state.keys())):
        print(state)
    elif (state["type"] == "error"):
        print(state["data"]["message"])
    else:
        order_book = None
        if ("order_book" in state["data"].keys()):
            order_book = state["data"]["order_book"]
            state["data"].pop("order_book")
        print(state)
        print_order_book(order_book)
