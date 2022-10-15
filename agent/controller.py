import json


async def add_player(ws, player_id):
    add_json = {"type": "add_player", "data": {"player_id": player_id}}
    await ws.send(json.dumps(add_json))


async def start_game(ws):
    start_json = {"type": "start_game", "data": {}}
    await ws.send(json.dumps(start_json))

cancel_json = {"type": "cancel_order", "data": {
    "player_id": "Connor", "is_bid": "true", "suit": "clubs"}}
accept_json = {"type": "accept_order", "data": {
    "buyer_id": "Connor", "seller_id": "Pun", "is_bid": "true", "suit": "clubs"}}


async def _place_order(player_id):
    pass


async def cancel_order(order_json):
    pass


async def place_bid(ws, player_id, suit, price):
    place_json = {"type": "place_order", "data": {
        "player_id": player_id, "is_bid": "true", "suit": suit, "price": price}}
    await ws.send(json.dumps(place_json))


async def place_offer(suit, price):
    pass


async def fetch_order():
    pass


async def fetch_msg():
    pass
