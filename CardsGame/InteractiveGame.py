from termcolor import colored, cprint
from typing import Dict, List, Tuple
from Game import Game
from Card import Card
from Deck import Deck
import constants
import uuid
import random


class InteractiveGame(Game):
    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], player_name: str):
        super().__init__(num_ranks, suits, special_ranks, player_name, 'PC')
        self.id_game = uuid.uuid1()
        self.num_cards_take = 3
        self.num_cards_use = self.num_cards_take - 1
        self.__start_random = 0
        self.__stop_random = constants.NUM_RANKS * (self.num_cards_use)
        self.target_number = self.__getRandomNumber()
        self.options_cards_p1: List[Card] = []
        self.options_cards_p2: List[Card] = []

    def __popNCards(self) -> Tuple[List[Card], List[Card]]:
        poped_cards_p1: List[Card] = []
        poped_cards_p2: List[Card] = []
        count = 0
        while(count < self.num_cards_take):
            poped_cards_p1.append(self.deck_p1.popCard())
            poped_cards_p2.append(self.deck_p2.popCard())
            count += 1
        return (poped_cards_p1, poped_cards_p2)

    def __getRandomNumber(self) -> int:
        return random.randint(self.__start_random, self.__stop_random)

    def startGame(self):
        print('ID Game:', self.id_game)
        if(self.num_turns == 0):
            print('Starting the game')
        else:
            print('The game was already started')

    def play(self):
        winner = self._getWinner()
        if(winner is None):
            if(len(self.options_cards_p1) != 0 and len(self.options_cards_p2) != 0):
                print("Waiting for your Cards")
            else:
                print("Getting cards")
                self.options_cards_p1, self.options_cards_p2 = self.__popNCards()

            print("Game ID: ", self.id_game)
