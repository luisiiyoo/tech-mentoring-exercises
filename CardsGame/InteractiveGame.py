from termcolor import colored, cprint
from typing import Dict, List, Tuple, Union
from datetime import datetime
from Game import Game
from Card import Card, getPrettyHandCard
from Deck import Deck
import Util
from termcolor import colored, cprint
import constants


class InteractiveGame(Game):
    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], player_name: str):
        super().__init__(num_ranks, suits, special_ranks, player_name, 'PC')
        self.__id_game = Util.getRandomString()
        self.__target_rank = None
        self.__hand_p1: List[Card] = []
        self.__hand_p2: List[Card] = []
        self.createdAt: int = datetime.timestamp(datetime.now())

    def getID(self) -> str:
        return self.__id_game

    def getTargetRank(self) -> int:
        return self.__target_rank

    def setTargetRank(self, val: int) -> int:
        self.__target_rank = val

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

    def __determineCardsToDraw(self, len_deck):
        return constants.CARDS_BY_HAND if len_deck >= constants.CARDS_BY_HAND else constants.CARDS_TO_USE

    def __drawCards(self) -> Tuple[List[Card], List[Card]]:
        cards_to_draw_p1 = self.__determineCardsToDraw(len(self.deck_p1))
        drawed_cards_p1: List[Card] = [self.deck_p1.drawCard()
                                       for i in range(0, cards_to_draw_p1)]

        cards_to_draw_p2 = self.__determineCardsToDraw(len(self.deck_p2))
        drawed_cards_p2: List[Card] = [self.deck_p2.drawCard()
                                       for i in range(0, cards_to_draw_p2)]

        return (drawed_cards_p1, drawed_cards_p2)

    def takeHand(self) -> List[Card]:
        winner = self.getWinner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't take a hand because the game is over. Winner: {winner}")

        if not self.__hand_p1 or not self.__hand_p2:
            new_rank = Util.getRandomNumInRange(
                constants.START_TARGET_RANGE, constants.STOP_TARGET_RANGE)
            self.setTargetRank(new_rank)
            self.__hand_p1, self.__hand_p2 = self.__drawCards()

        return self.__hand_p1

    def __validateIndexesCardOptions(self, indx_cards: List[int]) -> bool:
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
                indx_cards = [f"{indx}:{card}" for indx, card in enumerate(
                    self.getPrettyHandPlayer1())]
                raise Exception(
                    f"{indx} is not a valid index. You can only select {constants.CARDS_TO_USE} of the following indices:{constants.INDX_CARD_OPTIONS} -> Your hand is: {indx_cards}")
        return True

    def getTurnWinner(self, indx_cards_p1: List[int], indx_cards_p2: List[int]) -> Union[str, None]:
        selected_cards_p1 = [self.__hand_p1[indx].getRank()
                             for indx in indx_cards_p1]
        selected_cards_p2 = [self.__hand_p2[indx].getRank()
                             for indx in indx_cards_p2]
        sum_p1 = sum(selected_cards_p1)
        sum_p2 = sum(selected_cards_p2)
        turn_winner = None

        difference_p1 = abs(self.getTargetRank() - sum_p1)
        difference_p2 = abs(self.getTargetRank() - sum_p2)

        if(difference_p1 < difference_p2):
            turn_winner = self.getTagPlayer1()
            self.deck_p1.addCards(self.__hand_p2)
        elif(difference_p2 < difference_p1):
            turn_winner = self.getTagPlayer2()
            self.deck_p2.addCards(self.__hand_p1)
        cprint(
            f"INDEX: {indx_cards_p1} ({difference_p1}) ->{self.getTargetRank()}<- ({difference_p2}) {indx_cards_p2}", 'yellow')
        cprint(
            f"RANKS: {selected_cards_p1} = ({sum_p1}) ->{self.getTargetRank()}<- ({sum_p2}) {selected_cards_p2}", 'blue')
        cprint(f"{turn_winner}", 'red')
        self.__hand_p1 = []
        self.__hand_p2 = []
        return turn_winner

    def play(self, indx_cards_p1: List[int]) -> Union[str, None]:
        winner = self.getWinner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't play any more because {winner} won this game.")
        if not self.__hand_p1 or not self.__hand_p2:
            raise Exception("You don't have a hand.")

        self.__validateIndexesCardOptions(indx_cards_p1)

        self.incrementNumTurn()
        indx_cards_p2 = Util.getClosestIndexCards(
            self.__hand_p2, self.getTargetRank(), constants.CARDS_TO_USE)

        return (self.getTurnWinner(indx_cards_p1, indx_cards_p2), indx_cards_p2)
