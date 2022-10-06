import asyncio
from classes import Player, Order, OrderBook 
import random
class Timer:
    def __init__(self, timeout):
        self._timeout = timeout
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while(self._timeout > 0):
          await asyncio.sleep(1)
          self._timeout -= 1
          # should this broadcast be personalized to player? only send player their own info
          # maybe include numPlayers in broadcast
          await broadcast({
            "type": "update_game",
            "data": {
              "round_number": round_number,
              "time": self._timeout,
              "players": [vars(players[player_id]) for player_id in players], # make sure individual order objects are converted to dicts
              "order_book": vars(order_book) # make sure individual order objects are converted to dicts
            }
          })
        await broadcast({"type": "end_game"}) # call some sort of end game function to distribute money and reset game state

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
  # make sure we have enough players
  # randomize cards and deal to players
  await broadcast({"type": "start_game"})

# place order
# cancel order
# accept order

""" Helper function: Counts the number of each suit in a deck of cards
"""
def countCards(deck):
  counter = {}
  for card in deck:
    if card not in counter:
      counter[card] = 1
    else:
      counter[card] += 1
  print(counter)

"""Generate a random deck of 40 cards with the proper specifications for a game of Figgie
"""
def randomizeSuit():
  #generate random goal suit, append 8 cards to cardArray of the goal suit
  cardArray = []
  suits = ["diamond","club","heart","spade"]
  goalSuitInt = random.randint(0,3)
  print(goalSuitInt)
  for i in range(8):
    cardArray.append(suits[goalSuitInt])
 
  #randomize whether the suit opposite the goal suit is 10 or 12 cards
  numberOppositeCards = random.randint(0,1)
  for i in range(4):
    print(i)
    if i != goalSuitInt and i%2 == goalSuitInt%2:
      if numberOppositeCards==0:
        for j in range(10):
          cardArray.append(suits[i])
      else:
        for j in range(12):
          cardArray.append(suits[i])
      suits.pop(i)
      suits.remove(cardArray[0])

  #if opposite goal suit has 12 cards, just append 10 of each remaining suit
  #if opposite goal suit has 10 cards, randomize which of remaining suits 
  #gets 12 cards and the other will get 10

  if numberOppositeCards == 1:
    for i in range(10):
      cardArray.append(suits[0])
      cardArray.append(suits[1])
  elif numberOppositeCards == 0:
    numCards = random.randint(0,1)
    for i in range(10):
      cardArray.append(suits[numCards])
    for i in range(12):
      cardArray.append(suits[1-numCards])
  countCards(cardArray)
  return cardArray

#shuffle deck and then distribute cards to each player 
def dealCards(deck):

  return 



clients = {} # map of (player_id, websocket)
players = {} # map of (player_id, Player)
round_number = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0

randomizeSuit()