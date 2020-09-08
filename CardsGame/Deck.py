import numpy as np
from Card import Card
import math


class Deck:
    def __init__(self, num_ranks: int, suits: dict, special_ranks: dict):
        self.__num_ranks = num_ranks
        self.__suits = suits
        self.__special_ranks = special_ranks
        self.deck: list = []

        for suit_key in self.__suits:
            for rank in range(1, self.__num_ranks + 1):
                card = Card(int(rank), self.__suits.get(suit_key))
                self.deck.append(card)

    def __getPrettyCard(self, card):
        suit = card.suitType
        rank = self.__special_ranks.get(card.rank) if (
            card.rank in self.__special_ranks) else str(card.rank)
        return rank + suit

    def getPrettyDeck(self, deck: list):
        return list(map(self.__getPrettyCard, deck))

    def splitRandomly(self):
        num_cards = len(self.deck)
        idx_ranperm = list(np.random.permutation(num_cards))
        split_idx = math.floor(num_cards / 2)

        rnd_range_1 = idx_ranperm[0:split_idx]
        rnd_range_2 = idx_ranperm[split_idx:]

        deck_1 = [self.deck[idx] for idx in rnd_range_1]
        deck_2 = [self.deck[idx] for idx in rnd_range_2]
        return (deck_1, deck_2)
