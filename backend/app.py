from fastapi import FastAPI, WebSocket
import json
import asyncio

class Timer:
    def __init__(self, timeout):
        self._timeout = timeout
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while(self._timeout > 0):
          await asyncio.sleep(1)
          self._timeout -= 1
          # broadcast timer to all clients - should abstract broadcast function
          for websocket in clients.values():
            await websocket.send_json({"type": "timer", "data": self._timeout})
        # broadcast that game ended

    def cancel(self):
        self._task.cancel()

class Player:
  def __init__(self, player_id, num_hearts, num_diamonds, num_clubs, num_spades, balance, orders):
    self.player_id = player_id
    self.orders = orders
    self.balance = balance
    self.num_hearts = num_hearts
    self.num_diamonds = num_diamonds
    self.num_clubs = num_clubs
    self.num_spades = num_spades

class Order:
  def __init__(order_id, player, is_bid, suit, price, time_stamp):
    self.order_id = order_id
    self.player = player
    self.is_bid = is_bid
    self.suit = suit
    self.price = price
    self.time_stamp = time_stamp

class OrderBook:
  def __init__(self, hearts_bids, hearts_offers, diamonds_bids, diamonds_offers, clubs_bids, clubs_offers, spades_bids, spades_offers):
    self.hearts_bids = hearts_bids
    self.hearts_offers = hearts_offers
    self.diamonds_bids = diamonds_bids
    self.diamonds_offers = diamonds_offers
    self.clubs_bids = clubs_bids
    self.clubs_offers = clubs_offers
    self.spades_bids = spades_bids
    self.spades_offers = spades_offers

clients = {} # map of (player_id, websocket)
players = {} # map of (player_id, Player)
round_number = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0

app = FastAPI(title="FiggieBot Game Engine")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Connecting client...')
    await websocket.accept()
    while True:
        try:
            request = await websocket.receive_json()

            if request['action'] == 'add_player':
              print("Adding player...")
              player_id = request['player_id']
              clients[player_id] = websocket
              players[player_id] = Player(player_id, 13, 13, 13, 13, 100, [])

            if request['action'] == 'start_game':
              print("Starting game...")
              Timer(240)

            if request['action'] == 'place_order':
              print("Placing order...")
            
            if request['action'] == 'cancel order':
              print("Cancelling order...")

            if request['action'] == 'accept_order':
              print("Accepting order...")

        except Exception as e:
            print('error:', e)
            break
    print('Disconnecting client...')