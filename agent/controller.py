import json


async def add_player(ws, player_id):
    """
    Add a player to the game.
    """
    add_json = {"type": "add_player", "data": {"player_id": player_id}}
    await ws.send(json.dumps(add_json))


async def start_game(ws):
    """
    Start the game.
    """
    start_json = {"type": "start_game", "data": {}}
    await ws.send(json.dumps(start_json))


async def _place_order(ws, player_id, suit, price, is_bid):
    """
    Place a bid or an offer with the given information.
    """
    place_json = {"type": "place_order", "data": {
        "player_id": player_id, "is_bid": is_bid, "suit": suit, "price": price}}
    await ws.send(json.dumps(place_json))


async def cancel_order(ws, player_id, suit):
    """
    Cancel an existing order placed by the player.
    """
    cancel_json = {"type": "cancel_order", "data": {
        "player_id": player_id, "is_bid": "true", "suit": suit}}
    await ws.send(json.dumps(cancel_json))


async def place_bid(ws, player_id, suit, price):
    """
    Place a bid with the given information.
    """
    await _place_order(ws, player_id, suit, price, is_bid=True)


async def place_offer(ws, player_id, suit, price):
    """
    Place an offer with the given information.
    """
    await _place_order(ws, player_id, suit, price, is_bid=False)


async def accept_order(ws, player_id, suit):
    """
    Accept an existing order with the given information.
    """
    accept_json = {"type": "accept_order", "data": {
        "buyer_id": player_id, "seller_id": "TODO", "is_bid": "true", "suit": suit}}
    await ws.send(json.dumps(accept_json))


def _parse_msg(msg_json):
    """
    Parse the message received from the game engine.
    """
    return json.loads(msg_json)  # TODO: Implement


async def get_game_update(ws):
    """
    Get updates from the game engine about the game state.
    """
    msg_json = await ws.recv()
    return _parse_msg(msg_json)
