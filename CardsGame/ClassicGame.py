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

    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], tag_player_A='Player_A', tag_player_B='Player_B'):
        super().__init__(num_ranks, suits, special_ranks, tag_player_A, tag_player_B)

    def playClasssicGameOnTerminal(self) -> None:
        '''
        Starts the game and shows the progress in each turn until the game ends

        Args:
            None

        Returns:
            None
        '''
        card_A_tag = colored(f"{self._tag_player_A}'s Card", constants.COLOR_A)
        card_B_tag = colored(f"{self._tag_player_B}'s Card", constants.COLOR_B)
        tie_tag = colored('TIE', constants.COLOR_TIE)
        winner_tag = colored('Winner:', constants.COLOR_WINNER, attrs=[
                             'reverse', 'blink', 'bold'])

        winner = self._getWinner()
        while(winner is None):
            self.num_turns += 1
            card_A = self.deck_A.popCard()
            card_B = self.deck_B.popCard()
            turn_msj = ''
            if (card_A.rank > card_B.rank):
                turn_msj = self.getColoredTurnStatusGame(
                    card_A, card_B, card_A_tag)
                self.deck_A.addCards([card_B, card_A])
            elif (card_B.rank > card_A.rank):
                turn_msj = self.getColoredTurnStatusGame(
                    card_A, card_B, card_B_tag)
                self.deck_B.addCards([card_A, card_B])
            else:
                turn_msj = self.getColoredTurnStatusGame(
                    card_A, card_B, tie_tag)
                self.cards_discarted[self.num_turns] = (card_B, card_A)
            print(turn_msj)
            winner = self._getWinner()
            # self.printDecks()
        print('{} {}'.format(winner_tag, winner))
