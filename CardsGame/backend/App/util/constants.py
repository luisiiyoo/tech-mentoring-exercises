import math
from typing import Dict

SPECIAL_RANKS: Dict[int, str] = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
}
SUITS: Dict[str, str] = {
    'club': '♣',
    'diamond': '♦',
    'heart': '♥',
    'spade': '♠'
}
NUM_CARDS = 52  # 52
NUM_SUITS = len(SUITS)  # 4
NUM_RANKS = math.floor(NUM_CARDS / NUM_SUITS)  # 13

COLOR_P1 = 'yellow'
COLOR_P2 = 'green'
COLOR_TIE = 'red'
COLOR_WINNER = 'blue'

NUM_SPLITS = 2
MAX_NUM_TURNS = 500

MIN_NUM_CARDS_CLASSIC_GAME = 1

CARDS_BY_HAND = 3
CARDS_TO_USE = CARDS_BY_HAND - 1
IDX_CARD_OPTIONS = range(0, CARDS_BY_HAND)
START_TARGET_RANGE = 0
STOP_TARGET_RANGE = NUM_RANKS * CARDS_TO_USE
