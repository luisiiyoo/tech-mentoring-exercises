import math
import numpy as np
from Card import Card

NUM_SPLITS = 2


class Deck:
    def __init__(self, num_ranks: int, suits: dict, special_ranks: dict):
        self.__num_ranks = num_ranks
        self.__suits = suits
        self.__special_ranks = special_ranks
        self.deck: list = []

        for suit_key in self.__suits:
            for rank in range(1, self.__num_ranks + 1):
                card = Card(rank, self.__suits.get(suit_key))
                self.deck.append(card)

    def splitRandomly(self):
        num_cards = len(self.deck)
        idx_ranperm = list(np.random.permutation(num_cards))
        split_idx = math.floor(num_cards / NUM_SPLITS)

        rnd_range_1 = idx_ranperm[0:split_idx]
        rnd_range_2 = idx_ranperm[split_idx:]

        deck_1 = [self.deck[idx] for idx in rnd_range_1]
        deck_2 = [self.deck[idx] for idx in rnd_range_2]
        return (deck_1, deck_2)
