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
        tag_player_A (str): Player A name
        tag_player_B (str): Player B name

    Attributes:
        deck_A (Deck): Deck object that contains the player A's cards
        deck_B (Deck): Deck object that cosntains the player B's cards
        _tag_player_A (str): Player A name
        _tag_player_B (str): Player B name
        num_turns (int): Counter of turns
        cards_discarted (Dict[int, Tuple[Card, Card]]): Dictionary that contains the discarted cards by turn (if there were turns)
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], tag_player_A: str, tag_player_B: str):
        self.deck_A, self.deck_B = self.build(num_ranks, suits, special_ranks)
        self.num_turns = 0
        self._tag_player_A = tag_player_A
        self._tag_player_B = tag_player_B
        self.cards_discarted: Dict[int, Tuple[Card, Card]] = dict()

    def build(self, num_ranks, suits, special_ranks) -> Tuple[Deck, Deck]:
        '''
        Generates the shuffled decks for the player A and B

        Args:
            num_ranks (int): Number of ranks by suit
            suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
            special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'

        Returns:
            deck_A (Deck): Deck object that contains the player A's cards
            deck_B (Deck): Deck object that cosntains the player B's cards
        '''
        deck = Deck(num_ranks, suits, special_ranks)
        deck.shuffleDeck()
        return deck.splitDeck()

    def printDecks(self) -> None:
        '''
        Prints a pretty colored Deck presentation for the Player A and B

        Args:
            None

        Returns:
            None
        '''
        cprint(f'{self._tag_player_A}:\n  {self.deck_A}',
               constants.COLOR_A)
        cprint(f'{self._tag_player_B}:\n  {self.deck_B}',
               constants.COLOR_B)

    def _getWinner(self) -> Union[str, None]:
        '''
        Returns the winner player if there is

        Args:
            None

        Returns:
            winner (str): Colored string with the name of the winner
        '''
        colored_attrs = ['bold']
        size_A = len(self.deck_A)
        size_B = len(self.deck_B)
        if((self.num_turns >= constants.MAX_NUM_TURNS) or (size_A == 0 and size_B == 0)):
            return colored('Tie', constants.COLOR_TIE, attrs=colored_attrs)
        elif(size_A <= 0):
            return colored(self._tag_player_B, constants.COLOR_B, attrs=colored_attrs)
        elif(size_B <= 0):
            return colored(self._tag_player_A, constants.COLOR_A, attrs=colored_attrs)
        else:
            return None

    def getColoredTurnStatusGame(self, card_A, card_B, best_tag) -> str:
        '''
        Returns the winner player if there is

        Args:
            card_A (Card): Card object obtained on the current turn for the player A
            card_B (Card): Card object obtained on the current turn for the player B
            best_tag (str): Message about the best Card between the two Cards passed as argument

        Returns:
            status (str): Colored string with the status message
        '''
        len_A = f'{len(self.deck_A)+1:2}'
        len_B = f'{len(self.deck_B)+1:2}'

        turn_msj = f'Turn: {self.num_turns:>3}'
        card_A_msj = colored('{}({}) - {}'.format(self._tag_player_A,
                                                  len_A, card_A.getPrettyCard()), constants.COLOR_A)
        card_B_msj = colored('{} - {}({})'.format(card_B.getPrettyCard(),
                                                  self._tag_player_B, len_B), constants.COLOR_B)

        return '{} => {} ... {} => {}'.format(
            turn_msj, card_A_msj, card_B_msj, best_tag)