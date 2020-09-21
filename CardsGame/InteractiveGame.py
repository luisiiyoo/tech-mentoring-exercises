from termcolor import colored, cprint
from typing import Dict
from Game import Game
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

    def __getRandomNumber(self):
        return random.randint(self.__start_random, self.__stop_random)
