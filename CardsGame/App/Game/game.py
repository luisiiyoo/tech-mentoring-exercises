from typing import Tuple, List, Union, Dict
from termcolor import colored, cprint
from .card import Card
from .deck import Deck
from ..util import constants


class Game:
    """
    CardGame class to control the game

    Args:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
        tag_p1 (str): Player 1 name
        tag_p2 (str): Player 2 name

    Attributes:
        deck_p1 (Deck): Deck object that contains the player 1's cards
        deck_p2 (Deck): Deck object that cosntains the player 2's cards
        cards_discarded (Dict[int, Tuple[Card, Card]]): Dictionary that contains the discarted cards by turn (if there were turns)
        __tag_p1 (str): Player 1 name
        __tag_p2 (str): Player 2 name
        __num_turns (int): Counter of turns
    """

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], tag_p1: str, tag_p2: str):
        self.deck_p1, self.deck_p2, *_ = self.__build(
            num_ranks, suits, special_ranks, constants.NUM_SPLITS)
        self.cards_discarded: Dict[int, Tuple[Card, Card]] = dict()
        self.__num_turns = 0
        self.__tag_p1 = tag_p1
        self.__tag_p2 = tag_p2

    def get_tag_player(self, player) -> Union[str, None]:
        """
        Gets the name of a player

        Args:
            player (int): Player id

        Returns:
            tag_name (str): If exist returns the player's name else returns None
        """
        if player == 1:
            return self.__tag_p1
        elif player == 2:
            return self.__tag_p2
        return None

    def get_num_turns(self) -> int:
        """
        Gets current turn

        Args:
            None

        Returns:
            turn (int): Current turn
        """
        return self.__num_turns

    def increment_num_turn(self) -> None:
        """
        Increments the turn_number variable by 1

        Args:
            None

        Returns:
            None
        """
        self.__num_turns += 1

    def __build(self, num_ranks, suits, special_ranks,num_splits) -> List[Deck]:
        """
        Generates the shuffled decks for the player A and B

        Args:
            num_ranks (int): Number of ranks by suit
            suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
            special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
            num_splits (int): number of splits to divide the deck

        Returns:
            decks_list(Deck): Deck list for the n players (num_splits)
        """
        deck = Deck(num_ranks, suits, special_ranks)
        deck.random_shuffle()
        return deck.smart_split(num_splits)

    def print_decks(self) -> None:
        """
        Prints a pretty colored Deck presentation for the Player A and B

        Args:
            None

        Returns:
            None
        """
        cprint(f'{self.get_tag_player(1)}:\n  {self.deck_p1}',
               constants.COLOR_P1)
        cprint(f'{self.get_tag_player(2)}:\n  {self.deck_p2}',
               constants.COLOR_P2)

    def get_winner(self, min_num_cards) -> Union[str, None]:
        """
        Returns the winner player if there is

        Args:
            min_num_cards (int): Minimun number of cards to have

        Returns:
            winner (str): Colored string with the name of the winner
        """
        colored_attrs = ['bold']
        size_p1 = len(self.deck_p1)
        size_p2 = len(self.deck_p2)
        if (self.get_num_turns() >= constants.MAX_NUM_TURNS) or (size_p1 < min_num_cards and size_p2 < min_num_cards):
            return colored('Tie', constants.COLOR_TIE, attrs=colored_attrs)
        elif size_p1 < min_num_cards:
            return colored(self.get_tag_player(2), constants.COLOR_P2, attrs=colored_attrs)
        elif size_p2 < min_num_cards:
            return colored(self.get_tag_player(1), constants.COLOR_P1, attrs=colored_attrs)
        else:
            return None
