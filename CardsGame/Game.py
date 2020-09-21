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
        self._card_A_tag (str): String colored tag for card A
        self._card_B_tag (str): String colored tag for card B
        self._tie_tag (str): String colored tag for tie
        self._winner_tag(str): String colored tag for the winner
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], tag_player_A: str, tag_player_B: str):
        self.deck_A, self.deck_B = self.build(num_ranks, suits, special_ranks)
        self.num_turns = 0
        self._tag_player_A = tag_player_A
        self._tag_player_B = tag_player_B
        self.cards_discarted: Dict[int, Tuple[Card, Card]] = dict()
        self._card_A_tag = colored(
            f"{self._tag_player_A}'s Card", constants.COLOR_A)
        self._card_B_tag = colored(
            f"{self._tag_player_B}'s Card", constants.COLOR_B)
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

    def _getWinner(self, min_num_cards=1) -> Union[str, None]:
        '''
        Returns the winner player if there is

        Args:
            min_num_cards (int): Minimun number of cards to have

        Returns:
            winner (str): Colored string with the name of the winner
        '''
        colored_attrs = ['bold']
        size_A = len(self.deck_A)
        size_B = len(self.deck_B)
        if((self.num_turns >= constants.MAX_NUM_TURNS) or (size_A < min_num_cards and size_B < min_num_cards)):
            return colored('Tie', constants.COLOR_TIE, attrs=colored_attrs)
        elif(size_A < min_num_cards):
            return colored(self._tag_player_B, constants.COLOR_B, attrs=colored_attrs)
        elif(size_B < min_num_cards):
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
