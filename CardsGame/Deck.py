from __future__ import annotations
import math
import numpy
from typing import Dict, List, Tuple
from Card import Card
import constants


class Deck:
    '''
    Deck class that contains the collection of cards and methods like shuffle, pop a card, etc.

    Args:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'

    Attributes:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
        __cards(List[Card]): List of Card objects
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], cards: List[Card] = []):
        self.num_ranks = num_ranks
        self.suits = suits
        self.special_ranks = special_ranks
        self.__cards: List[Card] = cards if (
            len(cards) > 0) else self.__createListOfCards()

    def __createListOfCards(self):
        '''
        Creates the collection of cards based on the suits and number of ranks providen at the Deck object creation

        Args:
            None

        Returns:
            cards(List[Card]): List of Card objects
        '''
        cards: List[Card] = []
        for suit_key in self.suits:
            for rank in range(1, self.num_ranks + 1):
                card = Card(rank, self.suits.get(suit_key))
                cards.append(card)
        return cards

    def getCardsList(self):
        return self.__cards

    def __len__(self):
        return len(self.__cards)

    def __str__(self) -> str:
        pretty = self.getPrettyDeck()
        return ','.join(pretty)

    def getPrettyDeck(self) -> List[str]:
        '''
        Maps the cards list to an array of pretty Cards (string Cards representation)

        Args:
            None

        Returns:
            cards(List[Card]): List of Card objects
        '''
        return [card.getPrettyCard() for card in self.__cards]

    def addCards(self, new_cards: List[Card]) -> None:
        '''
        Adds a list of cards to Decks bottom

        Args:
            new_cards(List[Card]): List of cards to add

        Returns:
            None
        '''
        self.__cards = self.__cards + new_cards

    def putBackCards(self, new_cards: List[Card]) -> None:
        '''
        Adds a list of cards to Decks top

        Args:
            new_cards(List[Card]): List of cards to add

        Returns:
            None
        '''
        self.__cards = new_cards + self.__cards

    def popCard(self) -> Card:
        '''
        Gets the above card from the deck

        Args:
            None

        Returns:
            card(Card): Card obtained from the deck's top
        '''
        return self.__cards.pop(0)

    def shuffleDeck(self) -> None:
        '''
        Shuffles the deck randomly

        Args:
            None

        Returns:
            None
        '''
        num_cards = len(self.__cards)
        idx_ranperm = list(numpy.random.permutation(num_cards))
        shuffled_cards = [self.__cards[idx] for idx in idx_ranperm]
        # print(list(map(lambda card: str(card.rank)+card.suit, shuffled_cards)))
        self.__cards = shuffled_cards

    def splitDeck(self) -> Tuple[Deck, Deck]:
        '''
        Splits the Deck object into two Decks

        Args:
            None

        Returns:
            deck_A(Deck): Deck object for the player A
            deck_A(Deck): Deck object for the player A
        '''
        num_cards = len(self.__cards)
        split_idx = math.floor(num_cards / constants.NUM_SPLITS)

        cards_A = self.__cards[0:split_idx]
        cards_B = self.__cards[split_idx:]

        deck_A = Deck(self.num_ranks, self.suits,
                      self.special_ranks, cards_A)
        deck_B = Deck(self.num_ranks, self.suits,
                      self.special_ranks, cards_B)
        return (deck_A, deck_B)
