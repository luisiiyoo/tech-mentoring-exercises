from termcolor import colored, cprint
from card import Card
from deck import Deck
from .game import Game
from ..util import constants
from typing import Tuple, Dict


class ClassicGame(Game):
    '''
    CardGame class to control the game

    Args:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
        tag_p1 (str): Player 1 name
        tag_p2 (str): Player 2 name

    Attributes:
        (inherited from Game)
        __card_p1_tag (str): String colored tag for player 1's card 
        __card_p2_tag (str): String colored tag for player 2's card
        __tie_tag (str): String colored tag for tie
        __winner_tag(str): String colored tag for the winner
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], tag_p1='p1', tag_p2='p2'):
        super().__init__(num_ranks, suits, special_ranks, tag_p1, tag_p2)
        self.__card_p1_tag = colored(
            f"{self.getTagPlayer1()}'s Card", constants.COLOR_P1)
        self.__card_p2_tag = colored(
            f"{self.getTagPlayer2()}'s Card", constants.COLOR_P2)
        self.__tie_tag = colored('TIE', constants.COLOR_TIE)
        self.__winner_tag = colored('Winner:', constants.COLOR_WINNER, attrs=[
            'reverse', 'blink', 'bold'])

    def getColoredTurnStatusGame(self, card_p1, card_p2, best_tag) -> str:
        '''
        Returns the winner player if there is

        Args:
            card_p1 (Card): Card object obtained on the current turn for the player 1
            card_p2 (Card): Card object obtained on the current turn for the player 2
            best_tag (str): Message about the best Card between the two Cards passed as argument

        Returns:
            status (str): Colored string with the status message
        '''
        len_A = f'{len(self.deck_p1)+1:2}'
        len_B = f'{len(self.deck_p2)+1:2}'

        turn_msj = f'Turn: {self.getNumTurns():>3}'
        card_p1_msj = colored('{}({}) - {}'.format(self.getTagPlayer1(),
                                                   len_A, card_p1.getPrettyCard()), constants.COLOR_P1)
        card_p2_msj = colored('{} - {}({})'.format(card_p2.getPrettyCard(),
                                                   self.getTagPlayer2(), len_B), constants.COLOR_P2)

        return '{} => {} ... {} => {}'.format(
            turn_msj, card_p1_msj, card_p2_msj, best_tag)

    def playClasssicGameOnTerminal(self) -> None:
        '''
        Starts the game and shows the progress in each turn until the game ends

        Args:
            None

        Returns:
            None
        '''
        winner = self.getWinner(constants.MIN_NUM_CARDS_CLASSIC_GAME)
        while not winner:
            self.incrementNumTurn()
            card_p1 = self.deck_p1.drawCard()
            card_p2 = self.deck_p2.drawCard()
            turn_msj = ''
            rank_card_p1 = card_p1.getRank()
            rank_card_p2 = card_p2.getRank()
            if (rank_card_p1 > rank_card_p2):
                turn_msj = self.getColoredTurnStatusGame(
                    card_p1, card_p2, self.__card_p1_tag)
                self.deck_p1.addCards([card_p2, card_p1])
            elif (rank_card_p2 > rank_card_p1):
                turn_msj = self.getColoredTurnStatusGame(
                    card_p1, card_p2, self.__card_p2_tag)
                self.deck_p2.addCards([card_p1, card_p2])
            else:
                turn_msj = self.getColoredTurnStatusGame(
                    card_p1, card_p2, self.__tie_tag)
                self.cards_discarted[self.getNumTurns()] = (card_p2, card_p1)
            print(turn_msj)
            winner = self.getWinner(constants.MIN_NUM_CARDS_CLASSIC_GAME)
            # self.printDecks()
        print(f'{self.__winner_tag} {winner}')
