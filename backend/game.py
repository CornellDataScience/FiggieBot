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
  players[player_id] = Player(player_id, websocket, 350, 0, 0, 0, 0)
  print(players)
  # make sure no repeat names (override other players)

async def start_game():
  dealCards(randomizeSuit())
  Timer(240)
  # make sure we have enough players
  # randomize cards and deal to players
  await broadcast({"type": "start_game"})
# place order
# cancel order
# accept order

#Goal Suit
goalSuitInt = random.randint(0,3)
suits = ["diamond","club","heart","spade"]
goalSuit = suits[goalSuitInt]

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
  for i in range(8):
    cardArray.append(suits[goalSuitInt])
 
  #randomize whether the suit opposite the goal suit is 10 or 12 cards
  numberOppositeCards = random.randint(0,1)
  for i in range(4):
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


"""Requires: 4 players already added to game
shuffle deck and then distribute cards to each player
"""
#40 cards deal 0,4,8...36
#then deal 1, 5, 9...37
#then deal 2, 6, 10...38
#           3,7,11...39
def dealCards(deck):
  random.shuffle(deck)
  counter = 0
  for playerid in players:
    playerHand = players[playerid]
    for i in range(10):
      if deck[counter + i*4]=="diamond":
        playerHand.num_diamonds += 1
      elif deck[counter + i*4] =="club":
        playerHand.num_clubs += 1
      elif deck[counter + i*4] =="heart":
        playerHand.num_hearts += 1
      elif deck[counter + i*4] =="spade":
        playerHand.num_spades += 1
    counter += 1
    playerHand.printHand()
  return 

players = {} # map of (player_id, Player)
round_number = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0

