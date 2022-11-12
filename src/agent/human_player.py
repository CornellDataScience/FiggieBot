# fmt: off
import asyncio
import websockets
import controller
import random
import sys
sys.path.insert(0, "../")
from util import constants
# fmt: on

'''
A human player.
'''

uri = "ws://127.0.0.1:8000/ws"


class HumanPlayer:
    def __init__(self):
        self.player_id = "Human Player"

    def print_help(self):
        print("Commands:")
        print("help (h)")
        print("bid (b): bid <suit> <price> OR b <suit> <price>")
        print("offer (o): offer <suit> <price> OR o <suit> <price>")
        print("accept bid (ab): accept bid <suit> OR ab <suit>")
        print("accept offer (ao): accept offer <suit> OR ao <suit>")
        print("cancel bid (cb): cancel bid <suit> OR cb <suit>")
        print("cancel offer (co): cancel offer <suit> OR co <suit>")
        print("suits: hearts (h), clubs (c), spades (s), diamonds (d)")

    def parse_suit(self, suit_str: str) -> str:
        '''
        Parses a string representing a suit.
        Requires: suit_str has no leading or trailing commas
        Returns: one of ["h", "c", "s", "d"] if successful, "" if unsuccessful.
        '''
        if (suit_str == "hearts" or suit_str == "h"):
            return "h"
        if (suit_str == "clubs" or suit_str == "c"):
            return "c"
        if (suit_str == "spades" or suit_str == "s"):
            return "s"
        if (suit_str == "diamonds" or suit_str == "d"):
            return "d"
        return ""

    async def parse(self, websocket, cmd_str: str) -> bool:
        '''
        Parses the command string and performs actions
        if the command is well-formed.
        Returns: false if the command is malformed,
        true if the command is well-formed.
        '''
        suits = ["h", "c", "s", "d"]
        cmd_str = cmd_str.strip().lower()
        cmd_lst = cmd_str.split()
        if (cmd_lst.len() < 1):
            return False
        if (cmd_lst[0] == "help" or cmd_lst[0] == "h"):
            self.print_help()
            return True
        if (cmd_lst[0] == "bid" or cmd_lst[0] == "b"):
            suit = self.parse_suit(cmd_lst[1])
            price = int(cmd_lst[2])
            await controller.place_bid(
                websocket,
                self.player_id,
                suit,
                price)
            game_state = await controller.get_game_update(websocket)
            print(game_state)
            return True
        if (cmd_lst[0] == "offer" or cmd_lst[0] == "o"):
            suit = self.parse_suit(cmd_lst[1])
            price = int(cmd_lst[2])
            await controller.place_offer(
                websocket,
                self.player_id,
                suit,
                price)
            game_state = await controller.get_game_update(websocket)
            print(game_state)
            return True
        print("Unimplemented/Malformed")
        return False

    async def run(self):
        async with websockets.connect(uri) as websocket:
            name = input("Enter your username: ")
            self.player_id += (" " + name)
            await controller.add_player(websocket, self.player_id)
            await controller.start_round(websocket)
            self.print_help()
            while True:
                game_state = await controller.get_game_update(websocket)
                print("Current game state:")
                print(game_state)
                cmd_str = input("Make an action (type h or help for help): ")
                parse_ok = await self.parse(websocket, cmd_str)
                while (not parse_ok):
                    print("The command you entered is malformed.")
                    cmd_str = input(
                        "Make an action (type h or help for help): ")
                    parse_ok = await self.parse(cmd_str)


human_player = HumanPlayer()
asyncio.get_event_loop().run_until_complete(human_player.run())
