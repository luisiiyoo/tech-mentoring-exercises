import numpy as np
from termcolor import cprint
import math
from Deck import Deck

SPECIAL_RANKS: dict = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
}
SUITS: dict = {
    'club': '♣',
    'diamond': '♦',
    'heart': '♥',
    'spade': '♠'
}
NUM_CARDS = 20  # 52
NUM_SUITS = len(SUITS)  # 4
NUM_RANKS = math.floor(NUM_CARDS / NUM_SUITS)  # 13

"""

"""
deck = Deck(NUM_RANKS, SUITS, SPECIAL_RANKS)
deck_1, deck_2 = deck.splitRandomly()
cprint('Deck1: {}'.format(deck.getPrettyDeck(deck_1)), 'yellow')
cprint('Deck2: {}'.format(deck.getPrettyDeck(deck_2)), 'green')
