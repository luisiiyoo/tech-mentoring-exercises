from termcolor import colored, cprint
from Card import Card
from Deck import Deck
import constants
from typing import Tuple, Union, Dict


class Game:
    '''
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
        cards_discarted (Dict[int, Tuple[Card, Card]]): Dictionary that contains the discarted cards by turn (if there were turns)
        __tag_p1 (str): Player 1 name
        __tag_p2 (str): Player 2 name
        __num_turns (int): Counter of turns
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], tag_p1: str, tag_p2: str):
        self.deck_p1, self.deck_p2 = self.__build(
            num_ranks, suits, special_ranks)
        self.cards_discarted: Dict[int, Tuple[Card, Card]] = dict()
        self.__num_turns = 0
        self.__tag_p1 = tag_p1
        self.__tag_p2 = tag_p2

    def getTagPlayer1(self) -> str:
        '''
        Gets the name of the player 1

        Args:
            None

        Returns:
            tag_name (str): Name for the player 1
        '''
        return self.__tag_p1

    def getTagPlayer2(self) -> str:
        '''
        Gets the name of the player 2

        Args:
            None

        Returns:
            tag_name (str): Name for the player 2
        '''
        return self.__tag_p2

    def getNumTurns(self) -> int:
        '''
        Gets current turn

        Args:
            None

        Returns:
            turn (int): Current turn
        '''
        return self.__num_turns

    def incrementNumTurn(self) -> None:
        '''
        Increments the turn_number variable by 1

        Args:
            None

        Returns:
            None
        '''
        self.__num_turns += 1

    def __build(self, num_ranks, suits, special_ranks) -> Tuple[Deck, Deck]:
        '''
        Generates the shuffled decks for the player A and B

        Args:
            num_ranks (int): Number of ranks by suit
            suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
            special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'

        Returns:
            deck_p1 (Deck): Deck object that contains the player 1's cards
            deck_p2 (Deck): Deck object that cosntains the player 2's cards
        '''
        deck = Deck(num_ranks, suits, special_ranks)
        deck.shuffle()
        return deck.split()

    def printDecks(self) -> None:
        '''
        Prints a pretty colored Deck presentation for the Player A and B

        Args:
            None

        Returns:
            None
        '''
        cprint(f'{self.getTagPlayer1()}:\n  {self.deck_p1}',
               constants.COLOR_P1)
        cprint(f'{self.getTagPlayer2()}:\n  {self.deck_p2}',
               constants.COLOR_P2)

    def getWinner(self, min_num_cards) -> Union[str, None]:
        '''
        Returns the winner player if there is

        Args:
            min_num_cards (int): Minimun number of cards to have

        Returns:
            winner (str): Colored string with the name of the winner
        '''
        colored_attrs = ['bold']
        size_p1 = len(self.deck_p1)
        size_p2 = len(self.deck_p2)
        if((self.getNumTurns() >= constants.MAX_NUM_TURNS) or (size_p1 < min_num_cards and size_p2 < min_num_cards)):
            return colored('Tie', constants.COLOR_TIE, attrs=colored_attrs)
        elif(size_p1 < min_num_cards):
            return colored(self.getTagPlayer2(), constants.COLOR_P2, attrs=colored_attrs)
        elif(size_p2 < min_num_cards):
            return colored(self.getTagPlayer1(), constants.COLOR_P1, attrs=colored_attrs)
        else:
            return None
