from __future__ import annotations
import math
import numpy
from typing import Dict, List
from App.models.card import Card


class Deck:
    """
    Deck class that contains the collection of cards and methods like shuffle, pop a card, etc.

    Args:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'

    Attributes:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
        cards(List[Card]): List of Card objects
    """

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], cards: List[Card] = None):
        self.num_ranks = num_ranks
        self.suits = suits
        self.special_ranks = special_ranks
        self.cards: List[Card] = cards if cards is not None else self.__build()

    def __build(self):
        """
        Creates the collection of cards based on the suits and number of ranks provided at the Deck object creation

        Args:
            None

        Returns:
            cards(List[Card]): List of Card objects
        """
        cards: List[Card] = []
        for suit_key in self.suits:
            for rank in range(1, self.num_ranks + 1):
                card = Card(rank, self.suits.get(suit_key))
                cards.append(card)
        return cards

    def __len__(self):
        return len(self.cards)

    def __str__(self) -> str:
        pretty = self.get_pretty_deck()
        return ','.join(pretty)

    def get_pretty_deck(self) -> List[str]:
        """
        Maps the cards list to an array of pretty Cards (string Cards representation)

        Args:
            None

        Returns:
            cards(List[Card]): List of Card objects
        """
        return [card.get_pretty_card() for card in self.cards]

    def add_cards(self, new_cards: List[Card]) -> None:
        """
        Adds a list of cards to Decks bottom

        Args:
            new_cards(List[Card]): List of cards to add

        Returns:
            None
        """
        self.cards = self.cards + new_cards

    def return_cards(self, new_cards: List[Card]) -> None:
        """
        Adds a list of cards to Decks top

        Args:
            new_cards(List[Card]): List of cards to add

        Returns:
            None
        """
        self.cards = new_cards + self.cards

    def draw(self) -> Card:
        """
        Gets the above card from the deck

        Args:
            None

        Returns:
            card(Card): Card obtained from the deck's top
        """
        return self.cards.pop(0)

    def random_shuffle(self) -> None:
        """
        Shuffles the deck randomly

        Args:
            None

        Returns:
            None
        """
        num_cards = len(self)
        idx_random_perm = list(numpy.random.permutation(num_cards))
        shuffled_cards = [self.cards[idx] for idx in idx_random_perm]
        # print(list(map(lambda card: str(card.rank)+card.suit, shuffled_cards)))
        self.cards = shuffled_cards

    def smart_split(self, num_splits) -> List[Deck]:
        """
        Splits the Deck object into two Decks

        Args:
            num_splits (int): number of splits to divide the deck

        Raises:
            Exception: If num_splits is lower than the deck length or num_splits not divisible with the deck length

        Returns:
            decks_list(Deck): Deck list for the n players (num_splits)
        """
        deck_list: List[Deck] = []
        num_cards = len(self)
        if num_splits > num_cards:
            raise Exception(f"Invalid number of splits. It's not possible split {num_splits} times in a deck of {num_cards} cards")
        if not (num_cards % num_splits == 0):
            raise Exception(f'The result of {num_cards}/{num_splits} is not an exact division')
        split_idx = math.floor(num_cards / num_splits)

        for i, start_idx in enumerate(range(0, num_cards, split_idx)):
            end_idx = split_idx * (i + 1)
            list_cards = self.cards[start_idx:end_idx]
            deck = Deck(self.num_ranks, self.suits, self.special_ranks, list_cards)
            deck_list.append(deck)
        return deck_list
