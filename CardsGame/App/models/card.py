from __future__ import annotations
from App.util.constants import SPECIAL_RANKS


class Card:
    """
    Card class representing the rank and suit

    Args:
        rank (int): Value that receives the card
        suit (str): Special character of the card, e.g. '♣'

    Attributes:
        rank (int): Value that receives the card
        suit (str): Special character of the card, e.g. '♣'
    """

    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit

    def get_rank(self) -> int:
        return self.rank

    def get_suit(self) -> str:
        return self.suit

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
        rank = SPECIAL_RANKS.get(self.rank) if (
                self.rank in SPECIAL_RANKS) else str(self.rank)
        return f'{rank:>2s}{self.suit}'
