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
        _tag_p1 (str): Player 1 name
        _tag_p2 (str): Player 2 name
        num_turns (int): Counter of turns
        cards_discarted (Dict[int, Tuple[Card, Card]]): Dictionary that contains the discarted cards by turn (if there were turns)
        self._card_p1_tag (str): String colored tag for player 1's card 
        self._card_p2_tag (str): String colored tag for player 2's card
        self._tie_tag (str): String colored tag for tie
        self._winner_tag(str): String colored tag for the winner
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], tag_p1: str, tag_p2: str):
        self.deck_p1, self.deck_p2 = self.build(
            num_ranks, suits, special_ranks)
        self.num_turns = 0
        self._tag_p1 = tag_p1
        self._tag_p2 = tag_p2
        self.cards_discarted: Dict[int, Tuple[Card, Card]] = dict()
        self._card_p1_tag = colored(
            f"{self._tag_p1}'s Card", constants.COLOR_P1)
        self._card_p2_tag = colored(
            f"{self._tag_p2}'s Card", constants.COLOR_P2)
        self._tie_tag = colored('TIE', constants.COLOR_TIE)
        self._winner_tag = colored('Winner:', constants.COLOR_WINNER, attrs=[
            'reverse', 'blink', 'bold'])

    def build(self, num_ranks, suits, special_ranks) -> Tuple[Deck, Deck]:
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
        cprint(f'{self._tag_p1}:\n  {self.deck_p1}',
               constants.COLOR_P1)
        cprint(f'{self._tag_p2}:\n  {self.deck_p2}',
               constants.COLOR_P2)

    def _getWinner(self, min_num_cards=1) -> Union[str, None]:
        '''
        Returns the winner player if there is

        Args:
            min_num_cards (int): Minimun number of cards to have

        Returns:
            winner (str): Colored string with the name of the winner
        '''
        colored_attrs = ['bold']
        size_A = len(self.deck_p1)
        size_B = len(self.deck_p2)
        if((self.num_turns >= constants.MAX_NUM_TURNS) or (size_A < min_num_cards and size_B < min_num_cards)):
            return colored('Tie', constants.COLOR_TIE, attrs=colored_attrs)
        elif(size_A < min_num_cards):
            return colored(self._tag_p2, constants.COLOR_P2, attrs=colored_attrs)
        elif(size_B < min_num_cards):
            return colored(self._tag_p1, constants.COLOR_P1, attrs=colored_attrs)
        else:
            return None

    def getColoredTurnStatusGame(self, card_p1, card_p2, best_tag) -> str:
        '''
        Returns the winner player if there is

        Args:
            card_p1 (Card): Card object obtained on the current turn for the player A
            card_p2 (Card): Card object obtained on the current turn for the player B
            best_tag (str): Message about the best Card between the two Cards passed as argument

        Returns:
            status (str): Colored string with the status message
        '''
        len_A = f'{len(self.deck_p1)+1:2}'
        len_B = f'{len(self.deck_p2)+1:2}'

        turn_msj = f'Turn: {self.num_turns:>3}'
        card_p1_msj = colored('{}({}) - {}'.format(self._tag_p1,
                                                   len_A, card_p1.getPrettyCard()), constants.COLOR_P1)
        card_p2_msj = colored('{} - {}({})'.format(card_p2.getPrettyCard(),
                                                   self._tag_p2, len_B), constants.COLOR_P2)

        return '{} => {} ... {} => {}'.format(
            turn_msj, card_p1_msj, card_p2_msj, best_tag)
