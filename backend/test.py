import unittest
import asyncio
from game import players, add_player, order_book, EMPTY_BID, EMPTY_OFFER, place_order

class UnitTests(unittest.TestCase):
    def setUp(self):
      players.clear()

    def test_add_player(self):
      self.assertEqual(len(players), 0)
      asyncio.run(add_player("1", None))
      self.assertEqual(len(players), 1)
      self.assertEqual(players["1"].player_id, "1")

    def test_place_order(self):
      # successful bid
      self.assertEqual(order_book["bids"]["clubs"], EMPTY_BID)
      place_order("1", True, "clubs", 5)
      self.assertEqual(order_book["bids"]["clubs"].player_id, "1")

      # unsuccessful bid
      place_order("2", True, "clubs", 1)
      self.assertEqual(order_book["bids"]["clubs"].player_id, "1")

      # successful offer
      self.assertEqual(order_book["offers"]["clubs"], EMPTY_OFFER)
      place_order("1", False, "clubs", 5)
      self.assertEqual(order_book["offers"]["clubs"].player_id, "1")

      # unsuccessful offer
      place_order("2", False, "clubs", 7)
      self.assertEqual(order_book["offers"]["clubs"].player_id, "1")

    def test_cancel_order(self):
      print(players)

    def test_accept_order(self):
      print(players)

if __name__ == '__main__':
  unittest.main()
  # unittests = UnitTests()
  # print(aiounittest.helpers)
  # aiounittest.async_test(unittests.test_add_player)()
