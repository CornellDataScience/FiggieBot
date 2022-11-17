# fmt: off
import asyncio
from typing import Tuple
import websockets
import controller
import random
from enum import Enum, auto
import sys
sys.path.insert(0, "../")
from util import constants
# fmt: on

'''
A human player.
'''

uri = "ws://127.0.0.1:8000/ws"


class CmdType(Enum):
    NONE = auto()
    HELP = auto()
    BID = auto()
    OFFER = auto()
    ACCEPT_BID = auto()
    ACCEPT_OFFER = auto()
    CANCEL_BID = auto()
    CANCEL_OFFER = auto()


class Command:
    def __init__(self, command_type=CmdType.NONE, suit="", price=-1):
        self.command_type = command_type
        self.suit = suit
        self.price = price


class HumanPlayer:
    def __init__(self):
        self.player_id = "Human Player"

    def print_help(self):
        print("Commands:")
        print("help (h)")
        print("bid (b): bid <suit> <price> OR b <suit> <price>")
        print("offer (o): offer <suit> <price> OR o <suit> <price>")
        print("accept_bid (ab): accept_bid <suit> OR ab <suit>")
        print("accept_offer (ao): accept_offer <suit> OR ao <suit>")
        print("cancel_bid (cb): cancel_bid <suit> OR cb <suit>")
        print("cancel_offer (co): cancel_offer <suit> OR co <suit>")
        print("suits: hearts (h), clubs (c), spades (s), diamonds (d)")

    def pp_order_book(self, order_book: dict):
        '''
        Pretty-prints the order book.
        '''
        print("Current Order Book:")
        for suit in order_book["bids"].keys():
            order = order_book["bids"][suit]
            if order["order_id"] == -1:
                continue
            print(order["player_id"], "bids",
                  order["suit"], "at price", order["price"])

        for suit in order_book["offers"].keys():
            order = order_book["offers"][suit]
            if order["order_id"] == -1:
                continue
            print(order["player_id"], "offers",
                  order["suit"], "at price", order["price"])

    def print_state(self, state: dict):
        '''
        Prints a message based on the game state received from the server.
        '''
        if (state["type"] == "error"):
            print(state["data"]["message"])
        elif (state["type"] in ["new_order", "cancel_order", "accept_order", "update_game"]):
            order_book = state["data"]["order_book"]
            state["data"].pop("order_book")
            print(state)
            self.pp_order_book(order_book)
        else:
            print(state)

    def parse_suit(self, suit_str: str) -> Tuple[bool, str]:
        '''
        Parses a string representing a suit.
        Requires: suit_str has no leading or trailing commas
        Returns: (True, suit) if successful, (False, _) otherwise
        '''
        if (suit_str == "hearts" or suit_str == "h"):
            return (True, constants.HEARTS)
        if (suit_str == "clubs" or suit_str == "c"):
            return (True, constants.CLUBS)
        if (suit_str == "spades" or suit_str == "s"):
            return (True, constants.SPADES)
        if (suit_str == "diamonds" or suit_str == "d"):
            return (True, constants.DIAMONDS)
        return (False, constants.HEARTS)

    def parse_cmd(self, cmd_str: str) -> Tuple[bool, Command]:
        '''
        Parses the command string.
        Returns: (False, _) if the command is malformed,
        (True, command) if the command is well-formed.
        '''
        cmd_str = cmd_str.strip().lower()
        cmd_lst = cmd_str.split()
        if (len(cmd_lst) < 1):
            return (False, Command())

        if (cmd_lst[0] == "help" or cmd_lst[0] == "h"):
            return (True, Command(CmdType.HELP))

        if (cmd_lst[0] == "bid" or cmd_lst[0] == "b"):
            if (len(cmd_lst) != 3):
                return (False, Command())
            suit_ok, suit = self.parse_suit(cmd_lst[1])
            price = int(cmd_lst[2])
            return (suit_ok, Command(CmdType.BID, suit, price))

        if (cmd_lst[0] == "offer" or cmd_lst[0] == "o"):
            if (len(cmd_lst) != 3):
                return (False, Command())
            suit_ok, suit = self.parse_suit(cmd_lst[1])
            price = int(cmd_lst[2])
            return (suit_ok, Command(CmdType.OFFER, suit, price))

        if (cmd_lst[0] == "accept_bid" or cmd_lst[0] == "ab"):
            if (len(cmd_lst) != 2):
                return (False, Command())
            suit_ok, suit = self.parse_suit(cmd_lst[1])
            return (suit_ok, Command(CmdType.ACCEPT_BID, suit))

        if (cmd_lst[0] == "accept_offer" or cmd_lst[0] == "ao"):
            if (len(cmd_lst) != 2):
                return (False, Command())
            suit_ok, suit = self.parse_suit(cmd_lst[1])
            return (suit_ok, Command(CmdType.ACCEPT_OFFER, suit))

        if (cmd_lst[0] == "cancel_bid" or cmd_lst[0] == "cb"):
            if (len(cmd_lst) != 2):
                return (False, Command())
            suit_ok, suit = self.parse_suit(cmd_lst[1])
            return (suit_ok, Command(CmdType.CANCEL_BID, suit))

        if (cmd_lst[0] == "cancel_offer" or cmd_lst[0] == "co"):
            if (len(cmd_lst) != 2):
                return (False, Command())
            suit_ok, suit = self.parse_suit(cmd_lst[1])
            return (suit_ok, Command(CmdType.CANCEL_OFFER, suit))

        return (False, Command())

    async def run_cmd(self, websocket, cmd: Command):
        if (cmd.command_type == CmdType.HELP):
            self.print_help()
        if (cmd.command_type == CmdType.BID):
            await controller.place_bid(
                websocket,
                self.player_id,
                cmd.suit,
                cmd.price)
        if (cmd.command_type == CmdType.OFFER):
            await controller.place_offer(
                websocket,
                self.player_id,
                cmd.suit,
                cmd.price
            )
        if (cmd.command_type == CmdType.ACCEPT_BID):
            await controller.accept_bid(
                websocket,
                self.player_id,
                cmd.suit,
            )
        if (cmd.command_type == CmdType.ACCEPT_OFFER):
            await controller.accept_offer(
                websocket,
                self.player_id,
                cmd.suit,
            )
        if (cmd.command_type == CmdType.CANCEL_BID):
            await controller.cancel_bid(
                websocket,
                self.player_id,
                cmd.suit,
            )
        if (cmd.command_type == CmdType.CANCEL_OFFER):
            await controller.cancel_offer(
                websocket,
                self.player_id,
                cmd.suit,
            )

        print()
        game_state = await controller.get_game_update(websocket)
        self.print_state(game_state)

    async def run(self):
        async with websockets.connect(uri) as websocket:
            name = input("Enter your username: ")
            self.player_id += (" " + name)
            await controller.add_player(websocket, self.player_id)
            await controller.start_round(websocket)
            self.print_help()
            while True:
                # game_state = await controller.get_game_update(websocket)
                # print("Current game state:")
                # self.print_state(game_state)
                cmd_str = input("Make an action (type h or help for help): ")
                cmd_ok, cmd = self.parse_cmd(cmd_str)
                while (not cmd_ok):
                    print("The command you entered is malformed.")
                    cmd_str = input(
                        "Make an action (type h or help for help): ")
                    cmd_ok, cmd = self.parse_cmd(cmd_str)
                await self.run_cmd(websocket, cmd)


human_player = HumanPlayer()
asyncio.get_event_loop().run_until_complete(human_player.run())
