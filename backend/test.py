import unittest
import asyncio
from game import players, add_player, get_book, EMPTY_BID, EMPTY_OFFER, EMPTY_ORDER_BOOK, place_order, clear_book, cancel_order, accept_order, order_book_to_dict

class UnitTests(unittest.TestCase):
    def setUp(self):
      players.clear()
      clear_book()

    def test_add_player(self):
      self.assertEqual(len(players), 0)
      asyncio.run(add_player("1", None))
      self.assertEqual(len(players), 1)
      self.assertEqual(players["1"].player_id, "1")

    def test_place_order(self):
      # successful bid
      self.assertEqual(get_book()["bids"]["clubs"].order_id, EMPTY_BID.order_id)
      place_order("1", True, "clubs", 5)
      self.assertEqual(get_book()["bids"]["clubs"].player_id, "1")

      # unsuccessful bid
      place_order("2", True, "clubs", 1)
      self.assertEqual(get_book()["bids"]["clubs"].player_id, "1")

      # successful offer
      self.assertEqual(get_book()["offers"]["clubs"].order_id, EMPTY_OFFER.order_id)
      place_order("1", False, "clubs", 5)
      self.assertEqual(get_book()["offers"]["clubs"].player_id, "1")

      # unsuccessful offer
      place_order("2", False, "clubs", 7)
      self.assertEqual(get_book()["offers"]["clubs"].player_id, "1")

    def test_cancel_order(self):
      self.assertEqual(get_book()["bids"]["clubs"].order_id, EMPTY_BID.order_id)
      place_order("1", True, "clubs", 5)
      self.assertEqual(get_book()["bids"]["clubs"].player_id, "1")
      cancel_order("1", True, "clubs")
      self.assertEqual(get_book()["bids"]["clubs"].order_id, EMPTY_BID.order_id)

    def test_accept_order(self):
      asyncio.run(add_player("1", None))
      asyncio.run(add_player("2", None))
      self.assertEqual(players["1"].balance, 350)
      self.assertEqual(players["2"].balance, 350)
      players["2"].hand["clubs"] += 1
      self.assertEqual(players["1"].hand["clubs"], 0)
      self.assertEqual(players["2"].hand["clubs"], 1)
      place_order("1", True, "clubs", 5)
      accept_order("2", True, "clubs")
      self.assertEqual(players["1"].balance, 345)
      self.assertEqual(players["2"].balance, 355)
      self.assertEqual(players["1"].hand["clubs"], 1)
      self.assertEqual(players["2"].hand["clubs"], 0)


if __name__ == '__main__':
  unittest.main()
