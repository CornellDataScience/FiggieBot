import asyncio
from classes import Player, Order, OrderBook 

class Timer:
    def __init__(self, timeout):
        self._timeout = timeout
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while(self._timeout > 0):
          await asyncio.sleep(1)
          self._timeout -= 1
          # should this broadcast be personalized to player?
          await broadcast({
            "type": "update_game",
            "data": {
              "round_number": round_number,
              "time": self._timeout,
              "players": [vars(players[player_id]) for player_id in players],
              "order_book": vars(order_book)
            }
          })
        await broadcast({"type": "end_game"})

    def cancel(self):
        self._task.cancel()

async def broadcast(json_message):
  for websocket in clients.values():
    await websocket.send_json(json_message)

async def add_player(player_id, websocket):
  clients[player_id] = websocket
  players[player_id] = Player(player_id, 0, 0, 0, 0, 350, [])
  # make sure no repeat names (override other players)

async def start_game():
  Timer(240)
  # randomize cards and deal to players
  await broadcast({"type": "start_game"})

clients = {} # map of (player_id, websocket)
players = {} # map of (player_id, Player)
round_number = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0