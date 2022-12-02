import json


async def add_player(ws, player_id):
    '''
    Add a player to the game.
    '''
    add_json = {"type": "add_player", "data": {"player_id": player_id}}
    await ws.send(json.dumps(add_json))


async def start_round(ws):
    '''
    Start the round.
    '''
    start_json = {"type": "start_round", "data": {}}
    await ws.send(json.dumps(start_json))


async def _place_order(ws, player_id, suit, price, is_bid):
    '''
    Place a bid or an offer with the given information.
    '''
    place_json = {"type": "place_order", "data": {
        "player_id": player_id, "is_bid": is_bid, "suit": suit, "price": price}}
    await ws.send(json.dumps(place_json))


async def place_bid(ws, player_id, suit, price):
    '''
    Place a bid with the given information.
    '''
    await _place_order(ws, player_id, suit, price, is_bid=True)


async def place_offer(ws, player_id, suit, price):
    '''
    Place an offer with the given information.
    '''
    await _place_order(ws, player_id, suit, price, is_bid=False)


async def _cancel_order(ws, player_id, suit, is_bid):
    '''
    Cancel an existing order placed by the player.
    '''
    cancel_json = {"type": "cancel_order", "data": {
        "player_id": player_id, "is_bid": is_bid, "suit": suit}}
    await ws.send(json.dumps(cancel_json))


async def cancel_bid(ws, player_id, suit):
    '''
    Cancel an existing bid placed by the player.
    '''
    await _cancel_order(ws, player_id, suit, is_bid=True)


async def cancel_offer(ws, player_id, suit):
    '''
    Cancel an existing offer placed by the player.
    '''
    await _cancel_order(ws, player_id, suit, is_bid=False)


async def _accept_order(ws, player_id, suit, is_bid):
    '''
    Accept an existing order with the given information.
    '''
    accept_json = {"type": "accept_order", "data": {
        "accepter_id": player_id, "is_bid": is_bid, "suit": suit}}
    await ws.send(json.dumps(accept_json))


async def accept_bid(ws, player_id, suit):
    '''
    Accept an existing bid with the given information.
    '''
    await _accept_order(ws, player_id, suit, is_bid=True)


async def accept_offer(ws, player_id, suit):
    '''
    Accept an existing offer with the given information.
    '''
    await _accept_order(ws, player_id, suit, is_bid=False)


async def get_game_update(ws) -> dict:
    '''
    Get updates from the game engine about the game state.
    '''
    msg_json = await ws.recv()
    return json.loads(msg_json)


async def round_started(ws) -> bool:
    '''
    Returns true if the next message received from the server
    is of type "start_round", false otherwise.
    '''
    game_state = await get_game_update(ws)
    return game_state["type"] == "start_round"
