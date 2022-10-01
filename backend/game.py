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
          all_player_data = [players[player_id].publicToDict() for player_id in players]
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
        await broadcast({"type": "end_game"}) # call some sort of end game function to distribute money and reset game state

    def cancel(self):
        self._task.cancel()

async def broadcast(json_message):
  for player in players.values():
    await player.websocket.send_json(json_message)

async def add_player(player_id, websocket):
  players[player_id] = Player(player_id, websocket, 0, 0, 0, 0, 350, [])
  # make sure no repeat names (override other players)

async def start_game():
  Timer(240)
  # make sure we have enough players
  # randomize cards and deal to players
  await broadcast({"type": "start_game"})

# place order
# cancel order
# accept order

players = {} # map of (player_id, Player)
round_number = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0