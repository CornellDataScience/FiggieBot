import math 
import sys 
sys.path.insert(0, "../")
from util import constants
from util.constants import SPADES, CLUBS, HEARTS, DIAMONDS, EMPTY_DECK

SUIT_NUMS = {SPADES: 0, CLUBS: 1, HEARTS: 2, DIAMONDS: 3}

DECK0 = {SPADES: 12, CLUBS: 8, HEARTS: 10, DIAMONDS: 10}
DECK1 = {SPADES: 12, CLUBS: 10, HEARTS: 8, DIAMONDS: 10}
DECK2 = {SPADES: 12, CLUBS: 10, HEARTS: 10, DIAMONDS: 8}
DECK3 = {SPADES: 8, CLUBS: 12, HEARTS: 10, DIAMONDS: 10}
DECK4 = {SPADES: 10, CLUBS: 12, HEARTS: 8, DIAMONDS: 10}
DECK5 = {SPADES: 10, CLUBS: 12, HEARTS: 10, DIAMONDS: 8}
DECK6 = {SPADES: 8, CLUBS: 10, HEARTS: 12, DIAMONDS: 10}
DECK7 = {SPADES: 10, CLUBS: 8, HEARTS: 12, DIAMONDS: 10}
DECK8 = {SPADES: 10, CLUBS: 10, HEARTS: 12, DIAMONDS: 8}
DECK9 = {SPADES: 8, CLUBS: 10, HEARTS: 10, DIAMONDS: 12}
DECK10 = {SPADES: 10, CLUBS: 8, HEARTS: 10, DIAMONDS: 12}
DECK11 = {SPADES: 10, CLUBS: 10, HEARTS: 8, DIAMONDS: 12}

MAJORITIES = [5, 6, 6, 5, 6, 6, 6, 6, 5, 6, 6, 5]

PAYOUTS = [120, 100, 100, 120, 100, 100, 100, 100, 120, 100, 100, 120]

POSSIBLE_DECKS = [DECK0, DECK1, DECK2, DECK3, DECK4, DECK5, DECK6, DECK7, DECK8, DECK9, DECK10, DECK11]


def count_cards(count, trade): 
    """
    Update list of observed cards when new trade occurs. 
    """
    data = trade['data']
    buyer = data['buyer_id']
    seller = data['seller_id']
    suit = data['suit']

    if count[seller][suit] < 1:
        count[seller][suit] = 0
    else:
        count[seller][suit] -=1

    count[buyer][suit] +=1 

    return count
    

def deck_distribution(player_hands):
    """
    Return probability of being in each deck given the list of counted cards. 
    """
    total = EMPTY_DECK.copy()
    for hand in player_hands:
        for suit in hand: 
            total[suit] += hand[suit]

    m = [0] * 12
    for i in range(12):
        combs = 1 
        for suit in total: 
            combs *= math.comb(POSSIBLE_DECKS[i][suit], total[suit])
        m[i] = combs

    total_combs = sum(m) 
    for i in range(12):
        m[i] /= total_combs

    return m 


def expected_value_buy(suit, suit_count, m):
    """
    Return expected value for card being bought. 
    suit_count is # of cards of a suit in YOUR hand.
    """
    expected_value = 0 
    for i in range(12):
        expected_value += m[i] * value_card(i, suit, suit_count)
    return expected_value  


def expected_value_sell(suit, suit_count, m):
    """
    Return expected value for card being sold. 
    suit_count is # of cards of a suit in YOUR hand.
    """
    return expected_value_buy(suit, suit_count - 1, m)


def value_card(deck_index, suit, suit_count):
    """
    Return value of a given suit's card given the current deck. 
    """
    suit_num = SUIT_NUMS[suit] * 3
    if deck_index == suit_num or deck_index == suit_num + 1 or deck_index == suit_num + 2:
        return 10 + value_payout(deck_index, suit_count)
    return 0


def value_payout(deck_index, suit_count):
    """
    Return value of a given suit given a deck and the number of cards of that suit held. 
    """
    r = 3.5 # subject to change   
    if suit_count < MAJORITIES[deck_index]:
        payout = PAYOUTS[deck_index]
        value = payout * (1 - r) * (r ** suit_count) / (1 - r ** MAJORITIES[deck_index])
        return value 
    return 0 
    

    


        


