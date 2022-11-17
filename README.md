# FiggieBot

Creating a game to play Figgie &amp; Train an agent to play against

## How to Run the Backend Locally

### Mac

- Enter backend folder: `cd backend`
- Create virtual env called my_venv (only must do on first time setup): `python -m venv my_venv`
- Activate virtual environment: `source ". my_venv/bin/activate"`
- Install fastapi (only must do on first time setup): `pip install fastapi "uvicorn[standard]"`
- Install pymongo (only must do on first time setup): `pip install pymongo"`
- Start application: `uvicorn app:app --reload`
- Websocket available at: ws://127.0.0.1:8000/ws

### Windows Powershell

May need to run `Set-ExecutionPolicy Unrestricted -Scope Process` (allow running scripts for the current PowerShell session) or `Set-ExecutionPolicy Unrestricted -Force` (less safe) if execution policy is restricted.

- Enter backend folder: `cd backend`
- Create virtual env called my_venv (only must do on first time setup): `python -m venv my_venv`
- Activate virtual environment `my_venv\Scripts\Activate.ps1`
- Install fastapi (only must do on first time setup): `pip install fastapi "uvicorn[standard]"`
- Install pymongo (only must do on first time setup): `pip install pymongo"`
- Start application: `uvicorn app:app --reload`
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

Place Order:

- If successful: order is added to the order book; broadcast to everyone

```json
{
  "type": "new_order", 
  "data": {
    "new_order": {
      "player_id": "Eric", 
      "price": 5, 
      "is_bid": false, 
      "suit": "diamonds"
     }, 
     "message": "Player Eric offers 5 for diamonds.",
     "order_book":{
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": {
          "order_id": 1,
          "player_id": "Eric",
          "suit": "diamonds",
          "price": 5
        },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

- If not: order book is not changed; broadcast to specific player

```json
{
  "type": "error", 
  "data": {
    "message": "Your offer for diamonds is not low enough to update the order book.",
    "order_book":{
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

Cancel Order:

- If successful: order is removed from order book; broadcast to every player

```json
{
  "type": "cancel_order", 
  "data": {
    "order_canceled": {
      "player_id": "Eric", 
      "price": 5, 
      "is_bid": false, 
      "suit": "diamonds"
    }, 
    "message": "Player Eric canceled offer for diamonds.",
    "order_book":{
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

- If not: order remains in the order book; broadcast to specific player

```json
{
  "type": "error", 
  "data": {
    "message": "You cannot cancel this offer.",
    "order_book": {
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": {
          "order_id": 1,
          "player_id": "Connor",
          "suit": "diamonds",
          "price": 5
        },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

Accept Order:

- If successful: order book is empty; broadcast to every player

```json
{
  "type": "accept_order", 
  "data": {
    "accepted_order": {
      "buyer_id": "Pun", 
      "seller_id": "Connor", 
      "price": 5, 
      "is_bid": true, 
      "suit": "clubs"
    }, 
    "message": "Player Connor sold clubs to Player Pun for 5.", 
    "order_book":{
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

- If not: both orders remain in the order book; broadcast to specific player

```json
{
  "type": "error", 
  "data": {
    "message": "Order could not be fulfilled.",
    "order_book":{
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": {
          "order_id": 0,
          "player_id": "Pun",
          "suit": "clubs",
          "price": 5
        },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": {
          "order_id": 1,
          "player_id": "Connor",
          "suit": "clubs",
          "price": 6
        },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

Game State (broadcasted every second during round):

```json
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
      { "player_id": "Connor", "balance": 345 },
      { "player_id": "Pun", "balance": 355 },
      { "player_id": "Iram", "balance": 345 },
      { "player_id": "Eric", "balance": 355 }
    ],
    "order_book": {
      "bids": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": {
          "order_id": 0,
          "player_id": "Connor",
          "suit": "clubs",
          "price": 5
        },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      },
      "offers": {
        "hearts": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "diamonds": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "clubs": { "order_id": -1, "player_id": "", "suit": "", "price": 0 },
        "spades": { "order_id": -1, "player_id": "", "suit": "", "price": 0 }
      }
    }
  }
}
```

## How to Run Tests

- Enter backend folder: `cd backend`
- Run test file: `python test.py`
