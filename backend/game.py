import asyncio
from classes import Player, Order, OrderBook 
import random

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

"""
Adds a player to the game. If a player with this name already exists, send
an error message to the client.
"""
async def add_player(player_id, websocket):
  if player_id in players:
    websocket.send_json({"type": "error", "data": {"message": "Player already exists"}})
  players[player_id] = Player(player_id, websocket, 350, 0, 0, 0, 0)

"""
Starts the game timer and randomizes the cards for each player.
"""
async def start_game():
  dealCards(randomizeSuit())
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

#Goal Suit
goalSuitInt = random.randint(0,3)
suits = ["diamond","club","heart","spade"]
goalSuit = suits[goalSuitInt]

"""
Helper function: Counts the number of each suit in a deck of cards
"""
def countCards(deck):
  counter = {}
  for card in deck:
    if card not in counter:
      counter[card] = 1
    else:
      counter[card] += 1
  print(counter)

"""
Generate a random deck of 40 cards with 8 of the goal suit, 10 or 12 of the
opposite suit, and 10 or 12 of the remaining two suits.
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


"""
Requires: 4 players already added to game
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

