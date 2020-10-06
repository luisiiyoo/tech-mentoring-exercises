from typing import Dict, List, Tuple, Union
from datetime import datetime
from .game import Game
from .card import Card, get_pretty_hand_card
from termcolor import cprint
from ..util import constants
from ..util.helpers import get_random_num_in_range, get_random_string, get_closest_index_cards


class InteractiveGame(Game):
    """
    Interactive card game class to control the game

    Args:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
        player_name (str): Player 1's name

    Attributes:
        (inherited from Game)
        __id_game (str): Random unique id
        __target_rank (int): target number to get close adding selected cards from the player's hand
        __hand_p1 (List[Card]): Player 1's hand
        __hand_p2 (List[Card]): Player 2's hand
        createdAt (int): Timestamp of the object creation
    """

    def __init__(self, num_ranks: int, suits: Dict[str, str],
                 special_ranks: Dict[int, str], player_name: str):
        super().__init__(num_ranks, suits, special_ranks, player_name, 'PC')
        self.__id_game = get_random_string()
        self.__target_rank = None
        self.__hand_p1: List[Card] = []
        self.__hand_p2: List[Card] = []
        self.createdAt: int = datetime.timestamp(datetime.now())

    def get_id(self) -> str:
        """
        Gets the id of the game

        Args:
            None

        Returns:
            id_game (str): Random unique string
        """
        return self.__id_game

    def get_target_rank(self) -> int:
        """
        Gets the current target rank

        Args:
            None

        Returns:
            target (int): Current target value
        """
        return self.__target_rank

    def set_target_rank(self, new_rank: int) -> int:
        """
        Sets the target rank

        Args:
            new_rank (int): New target value

        Returns:
            None
        """
        self.__target_rank = new_rank

    def deck_len_player1(self) -> int:
        """
        Gets the length of the player 1's deck

        Args:
            None

        Returns:
            deck_len (int): Player 1's deck's length
        """
        return len(self.deck_p1)

    def deck_len_player2(self) -> int:
        """
        Gets the length of the player 2's deck

        Args:
            None

        Returns:
            deck_len (int): Player 2's deck's length
        """
        return len(self.deck_p2)

    def get_pretty_hand_player1(self) -> List[str]:
        """
        Gets the players 1's hand as a list of strings

        Args:
            None

        Returns:
            prettr_hand (List[str]): Players 1's hand as a list of strings
        """
        return list(map(get_pretty_hand_card, self.__hand_p1))

    def get_pretty_hand_player2(self) -> List[str]:
        """
        Gets the players 2's hand as a list of strings

        Args:
            None

        Returns:
            prettr_hand (List[str]): Players 2's hand as a list of strings
        """
        return list(map(get_pretty_hand_card, self.__hand_p2))

    def __determine_cards_to_draw(self, len_deck) -> int:
        """
        Gets the number of cards to draw given the deck's length

        Args:
            len_deck (int): Deck's length

        Returns:
            num_cards (int): Number of cards to draw
        """
        return constants.CARDS_BY_HAND if len_deck >= constants.CARDS_BY_HAND else constants.CARDS_TO_USE

    def __draw_cards(self) -> Tuple[List[Card], List[Card]]:
        """
        Gets the hands for the player 1 and 2

        Args:
            None

        Returns:
            drawed_cards_p1 (List[Card]): List of drawed cards for the player 1
            drawed_cards_p2 (List[Card]): List of drawed cards for the player 2
        """
        cards_to_draw_p1 = self.__determine_cards_to_draw(len(self.deck_p1))
        drawed_cards_p1: List[Card] = [self.deck_p1.draw()
                                       for i in range(0, cards_to_draw_p1)]

        cards_to_draw_p2 = self.__determine_cards_to_draw(len(self.deck_p2))
        drawed_cards_p2: List[Card] = [self.deck_p2.draw()
                                       for i in range(0, cards_to_draw_p2)]

        return (drawed_cards_p1, drawed_cards_p2)

    def take_hand(self) -> List[Card]:
        """
        Gets the hands for the player 1 and 2 and validates the game status

        Args:
            None

        Raises:
            Exception: When the game is over

        Returns:
            hand_p1 (List[Card]): List of drawed cards for the player 1
        """
        winner = self.get_winner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't take a hand because the game is over. Winner: {winner}")

        if not self.__hand_p1 or not self.__hand_p2:
            new_rank = get_random_num_in_range(
                constants.START_TARGET_RANGE, constants.STOP_TARGET_RANGE)
            self.set_target_rank(new_rank)
            self.__hand_p1, self.__hand_p2 = self.__draw_cards()

        return self.__hand_p1

    def __validate_indexes_card_options(self, indx_cards: List[int]) -> bool:
        """
        Validates the provided indexes for the player 1

        Args:
            indx_cards (List[int]): List of indexes to use

        Raises:
            Exception: When the user provides more than N-defined indexes
            Exception: When the user provides repeating indexes
            Exception: When the user provides non-valid indexes 

        Returns:
            is_ok (bool): True if the list is contains valid indexes
        """
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
                    self.get_pretty_hand_player1())]
                raise Exception(
                    f"{indx} is not a valid index. You can only select {constants.CARDS_TO_USE} of the following indices:{constants.INDX_CARD_OPTIONS} -> Your hand is: {indx_cards}")
        return True

    def get_turn_winner(self, indx_cards_p1: List[int], indx_cards_p2: List[int]) -> Union[str, None]:
        """
        Gets the winner of the current turn

        Args:
            indx_cards_p1 (List[int]): List of player 1's indexes to use 
            indx_cards_p2 (List[int]): List of player 2's indexes to use

        Returns:
            turn_winner (str|None): The name of the turn's winner if there is
        """
        selected_cards_p1 = [self.__hand_p1[indx].get_rank()
                             for indx in indx_cards_p1]
        selected_cards_p2 = [self.__hand_p2[indx].get_rank()
                             for indx in indx_cards_p2]
        sum_p1 = sum(selected_cards_p1)
        sum_p2 = sum(selected_cards_p2)
        turn_winner = None

        difference_p1 = abs(self.get_target_rank() - sum_p1)
        difference_p2 = abs(self.get_target_rank() - sum_p2)

        if difference_p1 < difference_p2:
            turn_winner = self.get_tag_player1()
            self.deck_p1.add_cards(self.__hand_p2)
        elif difference_p2 < difference_p1:
            turn_winner = self.get_tag_player2()
            self.deck_p2.add_cards(self.__hand_p1)
        cprint(
            f"INDEX: {indx_cards_p1} ({difference_p1}) ->{self.get_target_rank()}<- ({difference_p2}) {indx_cards_p2}", 'yellow')
        cprint(
            f"RANKS: {selected_cards_p1} = ({sum_p1}) ->{self.get_target_rank()}<- ({sum_p2}) {selected_cards_p2}", 'blue')
        cprint(f"{turn_winner}", 'red')
        self.__hand_p1 = []
        self.__hand_p2 = []
        return turn_winner

    def play_turn(self, indx_cards_p1: List[int]) -> Tuple[Union[str, None], List[int]]:
        """
        Plays the turn and gets the turn winner 

        Args:
            indx_cards_p1 (List[int]): List of player 1's indexes to use 

        Raises:
            Exception: When the game is over
            Exception: When the player 1 don't have a hand

        Returns:
            turn_winner (str|None): The name of the turn's winner if there is
            indx_cards_p2 (List[int]): List of player 2's used indexes

        """
        winner = self.get_winner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't play any more because {winner} won this game.")
        if not self.__hand_p1 or not self.__hand_p2:
            raise Exception("You don't have a hand.")

        self.__validate_indexes_card_options(indx_cards_p1)

        self.increment_num_turn()
        indx_cards_p2 = get_closest_index_cards(
            self.__hand_p2, self.get_target_rank(), constants.CARDS_TO_USE)

        return self.get_turn_winner(indx_cards_p1, indx_cards_p2), indx_cards_p2
