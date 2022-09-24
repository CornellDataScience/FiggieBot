from fastapi import FastAPI, WebSocket

class Player:
  def __init__(self, num_hearts, num_diamonds, num_clubs, num_spades, balance, orders):
    self.num_hearts = num_hearts
    self.num_diamonds = num_diamonds
    self.num_clubs = num_clubs
    self.num_spades = num_spades
    self.balance = balance
    self.orders = orders


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

players = []
round_number = 0
timer = 0
order_book = OrderBook([], [], [], [], [], [], [], [])
next_order_id = 0

app = FastAPI(title="FiggieBot Game Engine")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Connecting client...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            await websocket.receive_text()
            # Send message to the client
            await websocket.send_text("Received message")

            # When client sends message from UI like ({'action': 'place_order', data: {suit: 'hearts', price: 10, is_bid: false}})
            # We should be able to figure out what function to call based on action (should make constants file for these)
            # On each action, we do some internal logic and then websocket.send something back to client for updating UI
            # https://github.com/penumbragames/tankanarchy/blob/master/server.js pretty useful resource (but in JS)
        except Exception as e:
            print('error:', e)
            break
    print('Disconnecting client...')

# how to use:
# cd backend
# python3 -m venv websocket
# source websocket/Scripts/activate
# pip install fastapi "uvicorn[standard]"
# uvicorn app:app --reload

# will be available at: ws://127.0.0.1:8000/ws

# for repo, we should make .gitignore (SO WE DON'T COMMIT VENV OR _PYCACHE FILES), requirements.txt