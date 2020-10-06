from __future__ import annotations
from ..util.constants import SPECIAL_RANKS


def get_pretty_hand_card(card: Card) -> str:
    """
      Returns the Card string representation

      Args:
          card (Card): Card object

      Returns:
          card_str (str): the Card string representation
    """
    return card.get_pretty_card()


class Card:
    """
    Card class representing the rank and suit

    Args:
        rank (int): Value that recieves the card 
        suit (str): Special character of the card, e.g. '♣'

    Attributes:
        rank (int): Value that recieves the card 
        suit (str): Special character of the card, e.g. '♣'
    """

    def __init__(self, rank: int, suit: str):
        self.__rank = rank
        self.__suit = suit

    def get_rank(self) -> int:
        return self.__rank

    def get_suit(self) -> str:
        return self.__suit

    def __str__(self) -> str:
        return self.get_pretty_card()

    def get_pretty_card(self) -> str:
        """
        Converts the Card object to a string, e.g. 'K♣'

        Args:
            None

        Returns:
            pretty_card(str): String with the card value and suit 
        """
        rank = SPECIAL_RANKS.get(self.__rank) if (
            self.__rank in SPECIAL_RANKS) else str(self.__rank)
        return f'{rank:>2s}{self.__suit}'
