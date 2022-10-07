import asyncio
from classes import Player, Order, OrderBook 

"""
Begins a timer that will end the round after the given number of seconds.
At each second, broadcasts a message to each player to update them on the
game state. When the timer ends, redistribute pot accordingly.
"""
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
        await end_round()

    def cancel(self):
        self._task.cancel()

"""
Broadcasts a given json_message to all players in the game.
"""
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

"""
Function to call when a round ends. Distributes money to players based
on their number of cards of the goal suit. Then, resets the order book.
Broadcasts a message to all players that the round has ended.
"""
async def end_round():
  for player in players.values():
    if goal_suit == "diamonds":
      player.balance += player.num_diamonds * 10
    if goal_suit == "hearts":
      player.balance += player.num_hearts * 10
    if goal_suit == "spades":
      player.balance += player.num_spades * 10
    if goal_suit == "clubs":
      player.balance += player.num_clubs * 10
  round_number += 1
  goal_suit = ""
  # reset order book (Eric's clear order book func)
  await broadcast({"type": "end_round"})

"""
Function to call when game ends. Calculates winner based on balances
and broadcasts to all players who the winner is.
"""
async def end_game():
  winner = max(players, key=lambda player_id: players[player_id].balance)
  await broadcast({"type": "end_game", "data": {"winner": winner}})

# place order
# cancel order
# accept order

players = {} # map of (player_id, Player)
round_number = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0