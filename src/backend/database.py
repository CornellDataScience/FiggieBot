from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_uri)
db = client.get_database("FiggieBotData")
db_games = db.get_collection('Games')
db_rounds = db.get_collection('Rounds')
db_orders = db.get_collection('Orders')


def write_games():
    """Add a game to games database
    """
    # need to somehow get games id from database and add it to the rounds/order database
    # add players as they join (max out at 4)


def write_rounds():
    """Add a round to rounds database
    """
    # need to somehow get games id from database and add it to the order database


def write_orders():
    """Add orders to orders database
    """
