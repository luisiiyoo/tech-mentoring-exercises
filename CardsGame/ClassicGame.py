from termcolor import colored, cprint
from Card import Card
from Deck import Deck
from Game import Game
import constants
from typing import Tuple, Union, Dict


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
        (inherited from Card)
    '''

    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], tag_p1='p1', tag_p2='p2'):
        super().__init__(num_ranks, suits, special_ranks, tag_p1, tag_p2)

    def playClasssicGameOnTerminal(self) -> None:
        '''
        Starts the game and shows the progress in each turn until the game ends

        Args:
            None

        Returns:
            None
        '''
        winner = self._getWinner()
        while not winner:
            self.num_turns += 1
            card_p1 = self.deck_p1.popCard()
            card_p2 = self.deck_p2.popCard()
            turn_msj = ''
            if (card_p1.rank > card_p2.rank):
                turn_msj = self.getColoredTurnStatusGame(
                    card_p1, card_p2, self._card_p1_tag)
                self.deck_p1.addCards([card_p2, card_p1])
            elif (card_p2.rank > card_p1.rank):
                turn_msj = self.getColoredTurnStatusGame(
                    card_p1, card_p2, self._card_p2_tag)
                self.deck_p2.addCards([card_p1, card_p2])
            else:
                turn_msj = self.getColoredTurnStatusGame(
                    card_p1, card_p2, self._tie_tag)
                self.cards_discarted[self.num_turns] = (card_p2, card_p1)
            print(turn_msj)
            winner = self._getWinner()
            # self.printDecks()
        print(f'{self._winner_tag} {winner}')
