# FiggieBot

Creating a game to play Figgie &amp; Train an agent to play against

## How to Run the Backend Locally

- cd backend
- python3 -m venv my_venv (only must do on first time setup)
- Activate virtual environment
  - Windows Git Bash: source my_venv/Scripts/activate
  - Mac: source ". my_venv/bin/activate"
- pip install fastapi "uvicorn[standard]" (only must do on first time setup)
- uvicorn app:app --reload
- Websocket available at: ws://127.0.0.1:8000/ws

## Backend WebSocket Inputs/Outputs Examples
### Inputs
- Add players: `{"type": "add_player", "data": {"player_id": "Connor"}}`
- Start Game: `{"type": "start_game", "data": {}}`
- End Game: `{"type": "end_game", "data": {}}`
- Place Order: `{"type": "place_order", "data": {"player_id": "Connor", "is_bid": true, "suit": "clubs", "price": 5}}`
- Cancel Order: `{"type": "cancel_order", "data": {"player_id": "Connor", "is_bid": true, "suit": "clubs"}}`
- Accept Order: `{"type": "accept_order", "data": {"accepter_id": "Pun", "is_bid": true, "suit": "clubs"}}`

### Output
- Game State (broadcasted every second during round): 
```
{
  "type": "update_game",
  "data": {
    "round_number": 0,
    "time": 181,
    "player": {
      "player_id": "Pun",
      "balance": 355,
      "hand": {
        "hearts": 2,
        "diamonds": 3,
        "clubs": 1,
        "spades": 3
        }
       },
    "players": [
      {"player_id": "Connor", "balance": 345},
      {"player_id": "Pun", "balance": 355},
      {"player_id": "Iram", "balance": 345},
      {"player_id": "Eric", "balance": 355}
      ],
    "order_book": {
      "bids": {"hearts": {"order_id": -1, "player_id": "", "suit": "", "price": 0},
      "diamonds": {"order_id": -1, "player_id": "", "suit": "", "price": 0},
      "clubs": {"order_id": 0, "player_id": "Connor", "suit": "clubs", "price": 5},
      "spades": {"order_id": -1, "player_id": "", "suit": "", "price": 0}
      },
    "offers": {
      "hearts": {"order_id": -1, "player_id": "", "suit": "", "price": 0},
      "diamonds": {"order_id": -1, "player_id": "", "suit": "", "price": 0},
      "clubs": {"order_id": -1, "player_id": "", "suit": "", "price": 0},
      "spades": {"order_id": -1, "player_id": "", "suit": "", "price": 0}
      }
     }
  }
}
```
