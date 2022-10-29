from pymongo import MongoClient
import settings
from datetime import datetime, timezone

client = MongoClient(settings.mongodb_uri)
db = client.get_database("FiggieBotData")
db_games = db.get_collection('Games')
db_rounds = db.get_collection('Rounds')
db_orders = db.get_collection('Orders')

def write_games(players):
    """Add a game to games database once a game is started, perhaps write final balances of players at end game?
    """
    player_array = [str(player) for player in players]
    db_games.insert_one({
        #need to figure out what to do with the game rounds aka game id
        #"game_id" : game_id
        "players" : player_array
    })
    print("Successfully added the game to the database.")

def write_rounds(round_id,players):
    """Add a round to rounds database with starting balances?
    """
    #need to somehow get games id from database and add it to the order database

    db_rounds.insert_one({
        #need to figure out what to do with the game rounds aka game id
        #"game_id" : game_id
        "round_id" : round_id,
        "players": players
    })
    print("Successfully added the round to the database.")

def write_orders(round_id, is_bid, suit, price, buyer, seller, action):
    """Add orders to orders database
    """
    db_orders.insert_one(
        {
            #need to figure out what to do with the game rounds aka game id
            #"game_id" : game_id
            "round_id" : round_id,
            "timestamp" : datetime.now(),
            "is_bid" : is_bid,
            "suit" : suit,
            "price" : price,
            "buyer" : buyer,
            "seller" : seller,
            "action" : action
        }
    )
    print("Successfully added the order to the database.")
    
x = {
    "hello" : 1,
    "hello2" : 2,
}

write_rounds(2,x)