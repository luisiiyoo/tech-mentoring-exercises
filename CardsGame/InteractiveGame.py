from termcolor import colored, cprint
from typing import Dict, List, Tuple, Union
from Game import Game
from Card import Card, getPrettyHandCard
from Deck import Deck
import Util
import constants


class InteractiveGame(Game):
    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], player_name: str):
        super().__init__(num_ranks, suits, special_ranks, player_name, 'PC')
        self.__id_game = Util.getRandomString()
        self.__target_rank = None
        self.__hand_p1: List[Card] = []
        self.__hand_p2: List[Card] = []

    def getID(self) -> str:
        return self.__id_game

    def getTargetRank(self) -> int:
        return self.__target_rank

    def deckLenPlayer1(self) -> int:
        return len(self.deck_p1)

    def deckLenPlayer2(self) -> int:
        return len(self.deck_p2)

    def getHandPlayer1(self) -> List[Card]:
        return self.__hand_p1

    def getHandPlayer2(self) -> List[Card]:
        return self.__hand_p2

    def getPrettyHandPlayer1(self) -> List[str]:
        return list(map(getPrettyHandCard, self.__hand_p1))

    def getPrettyHandPlayer2(self) -> List[str]:
        return list(map(getPrettyHandCard, self.__hand_p2))

    def determineCardsToDraw(self, len_deck):
        return constants.CARDS_BY_HAND if len_deck >= constants.CARDS_BY_HAND else constants.CARDS_TO_USE

    def __drawCards(self) -> Tuple[List[Card], List[Card]]:
        cards_to_draw_p1 = self.determineCardsToDraw(len(self.deck_p1))
        drawed_cards_p1: List[Card] = [self.deck_p1.drawCard()
                                       for i in range(0, cards_to_draw_p1)]

        cards_to_draw_p2 = self.determineCardsToDraw(len(self.deck_p2))
        drawed_cards_p2: List[Card] = [self.deck_p2.drawCard()
                                       for i in range(0, cards_to_draw_p2)]

        return (drawed_cards_p1, drawed_cards_p2)

    def takeHand(self) -> List[Card]:
        winner = self.getWinner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't take a hand because the game is over. Winner: {winner}")

        if self.__hand_p1 or self.__hand_p2:
            raise Exception(
                "You cann't take another hand of cards, you already have a hand!")
        else:
            self.__target_rank = Util.getRandomNumInRange(
                constants.START_TARGET_RANGE, constants.STOP_TARGET_RANGE)
            self.__hand_p1, self.__hand_p2 = self.__drawCards()

        return self.__hand_p1

    def validateIndexesCardOptions(self, indx_cards: List[int]) -> bool:
        # Check the len
        len_indxs = len(indx_cards)
        if len_indxs != constants.CARDS_TO_USE:
            raise Exception(f"You can only use {constants.CARDS_TO_USE} cards")

        # Check if there are not repeating elements
        if len(set(indx_cards)) != len_indxs:
            raise Exception('You must provide non-repeating indexes')

        # Check if the indexes are in the correct range
        for indx in indx_cards:
            if(indx not in constants.INDX_CARD_OPTIONS):
                raise Exception(
                    f"{indx} is not a valid index. You can only select {constants.CARDS_TO_USE} of the following indices:{constants.INDX_CARD_OPTIONS} -> Your hand is: {self.getPrettyHandPlayer1()}")
        return True

    def getRoundWinner(self, indx_cards_p1: List[int], indx_cards_p2: List[int]) -> Union[str, None]:
        sum_p1 = sum([self.__hand_p1[indx] for indx in indx_cards_p1])
        sum_p2 = sum([self.__hand_p2[indx] for indx in indx_cards_p2])
        round_winner = None

        difference_p1 = self.__target_rank - sum_p1
        difference_p2 = self.__target_rank - sum_p2

        if(difference_p1 < difference_p2):
            round_winner = self._tag_p1
            self.deck_p1.addCards(self.__hand_p2)
            self.cards_discarted = self.cards_discarted + self.__hand_p1
        elif(difference_p2 < difference_p1):
            round_winner = self._tag_p2
            self.deck_p2.addCards(self.__hand_p1)
            self.cards_discarted = self.cards_discarted + self.__hand_p2
        else:
            self.cards_discarted = self.cards_discarted + self.__hand_p1 + self.__hand_p2

        self.__hand_p1 = []
        self.__hand_p2 = []
        return round_winner

    def play(self, indx_cards_p1: List[int]) -> Union[str, None]:
        winner = self.getWinner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't play any more because {winner} won this game.")
        if not self.__hand_p1 or not self.__hand_p2:
            raise Exception("You don't have a hand.")

        self.validateIndexesCardOptions(indx_cards_p1)

        self.incrementNumTurn()
        indx_cards_p2 = Util.getClosestIndexCards(
            self.__hand_p2, self.__target_rank, constants.CARDS_TO_USE)

        self.getRoundWinner(indx_cards_p1, indx_cards_p2)
