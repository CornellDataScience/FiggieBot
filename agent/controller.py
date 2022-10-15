import asyncio
import websockets
import json

uri = "ws://127.0.0.1:8000/ws"


async def add_player(player_id):
    async with websockets.connect(uri) as websocket:
        my_json = {"type": "add_player", "data": {"player_id": player_id}}
        await websocket.send(json.dumps(my_json))


place_json = {"type": "place_order", "data": {
    "player_id": "Connor", "is_bid": "true", "suit": "clubs", "price": 5}}
cancel_json = {"type": "cancel_order", "data": {
    "player_id": "Connor", "is_bid": "true", "suit": "clubs"}}
accept_json = {"type": "accept_order", "data": {
    "buyer_id": "Connor", "seller_id": "Pun", "is_bid": "true", "suit": "clubs"}}


async def _place_order(player_id):
    pass


async def cancel_order(order_json):
    pass


async def place_bid(suit, price):
    pass


async def place_offer(suit, price):
    pass


async def fetch_order():
    pass


async def fetch_msg():
    pass

asyncio.get_event_loop().run_until_complete(add_player("James"))
