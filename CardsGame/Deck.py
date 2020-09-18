from __future__ import annotations
import math
import numpy
from typing import Dict, List, Tuple
from Card import Card
import constants


class Deck:
    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], cards: List[Card] = []):
        self.__num_ranks = num_ranks
        self.__suits = suits
        self.__special_ranks = special_ranks
        self.__cards: List[Card] = cards if (
            len(cards) > 0) else self.__createListOfCards()

    def __createListOfCards(self):
        cards: List[Card] = []
        for suit_key in self.__suits:
            for rank in range(1, self.__num_ranks + 1):
                card = Card(rank, self.__suits.get(suit_key))
                cards.append(card)
        return cards

    def __len__(self):
        return len(self.__cards)

    def __str__(self) -> str:
        pretty = self.getPrettyDeck()
        return ','.join(pretty)

    def getPrettyDeck(self) -> List[str]:
        return [card.getPrettyCard() for card in self.__cards]

    def addCards(self, new_cards: List[Card]) -> None:
        self.__cards = self.__cards + new_cards

    def popCard(self) -> Card:
        return self.__cards.pop(0)

    def shuffleDeck(self) -> None:
        num_cards = len(self.__cards)
        idx_ranperm = list(numpy.random.permutation(num_cards))
        shuffled_cards = [self.__cards[idx] for idx in idx_ranperm]
        # print(list(map(lambda card: str(card.rank)+card.suit, shuffled_cards)))
        self.__cards = shuffled_cards

    def splitDeck(self) -> Tuple[Deck, Deck]:
        num_cards = len(self.__cards)
        split_idx = math.floor(num_cards / constants.NUM_SPLITS)

        cards_1 = self.__cards[0:split_idx]
        cards_2 = self.__cards[split_idx:]

        deck_1 = Deck(self.__num_ranks, self.__suits,
                      self.__special_ranks, cards_1)
        deck_2 = Deck(self.__num_ranks, self.__suits,
                      self.__special_ranks, cards_2)
        return (deck_1, deck_2)
