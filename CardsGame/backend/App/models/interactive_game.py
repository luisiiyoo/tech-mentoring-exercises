from __future__ import annotations
from typing import Any, Dict, List, Tuple, Union
from datetime import datetime
from App.models.game import Game
from App.models.card import Card
from App.models.deck import Deck
from termcolor import cprint, colored
from App.util import constants
from App.util.helpers import get_random_num_in_range, get_random_string, get_closest_index_cards


class InteractiveGame(Game):
    """
    Interactive card game class to control the game

    Args:
        num_ranks (int): Number of ranks by suit
        suits (Dict[str, str]): Dictionary containing the suits, e.g. 'club': '♣'
        special_ranks (Dict[int, str]): Dictionary of special characters that receive a rank or value, e.g. 13: 'K'
        name_p1 (str): Player 1's name

    Attributes:
        (inherited from Game)
        _id (str): Random unique Game id
        _current_target (int): target number to get close adding selected cards from the player's hand
        _hand_p1 (List[Card]): Player 1's hand
        _hand_p2 (List[Card]): Player 2's hand
        _created_date (int): Timestamp of the object creation
        _history (Dict): Information for each turn
    """

    def __init__(self, num_ranks: int, suits: Dict[str, str], special_ranks: Dict[int, str], name_p1: str,
                 name_p2: str = 'PC', id_game: str = None, created_date: int = None, curr_target: int = None,
                 hand_p1: List[Card] = [], hand_p2: List[Card] = [], history: Dict = {},
                 deck_p1: Deck = None, deck_p2: Deck = None, num_turns: int = 0):
        # Calling parent constructor
        super().__init__(num_ranks, suits, special_ranks, name_p1, name_p2, deck_p1, deck_p2, num_turns)
        # Setup class attributes
        self._id = get_random_string() if not id_game else id_game
        self._created_date = datetime.timestamp(datetime.now()) if not created_date else created_date
        self._current_target = curr_target
        self._hand_p1: List[Card] = hand_p1
        self._hand_p2: List[Card] = hand_p2
        if not history:
            initial_turn = dict()
            initial_turn['DeckPlayer1'] = ','.join(map(str, self.get_deck_player(1).cards))
            initial_turn['DeckPlayer2'] = ','.join(map(str, self.get_deck_player(2).cards))
            self._history: Dict[int, Dict[str, Any]] = {0: initial_turn}
        else:
            self._history: Dict[int, Dict[str, Any]] = history

    def get_id(self) -> str:
        """
        Gets the id of the game

        Args:
            None

        Returns:
            id_game (str): Random unique string
        """
        return self._id

    def get_history(self) -> Dict[int, Dict[str, Any]]:
        """
        Gets each turn details from this InteractiveGame instance

        Args:
            None

        Returns:
            Dict[int, Dict[str, Any]]: Dictionary having details of each turn
        """
        return self._history

    def get_created_date(self) -> int:
        """
        Gets the creation date

        Args:
            None

        Returns:
            int: Time stamp
        """
        return self._created_date

    def get_created_date(self) -> int:
        """
        Gets the creation date

        Args:
            None

        Returns:
            int: Time stamp
        """
        return self._created_date

    def get_target_rank(self) -> int:
        """
        Gets the current target rank

        Args:
            None

        Returns:
            target (int): Current target value
        """
        return self._current_target

    def set_target_rank(self, new_rank: int) -> int:
        """
        Sets the target rank

        Args:
            new_rank (int): New target value

        Returns:
            None
        """
        self._current_target = new_rank

    def get_deck_player(self, player) -> Union[int, None]:
        """
        Gets the player's deck

        Args:
            player (int): Player id

        Returns:
            Deck: Player deck's
        """
        if player == 1:
            return self._deck_p1
        elif player == 2:
            return self._deck_p2
        return None

    def get_deck_len_player(self, player) -> Union[int, None]:
        """
        Gets the length of a player's deck

        Args:
            player (int): Player id

        Returns:
            deck_len (int): Player deck's length if exist else None
        """
        if player == 1:
            return len(self._deck_p1)
        elif player == 2:
            return len(self._deck_p2)
        return None

    def get_hand_player(self, player, pretty=True) -> Union[List[Union[str, Card]], None]:
        """
        Gets the players' hand as a list of strings

        Args:
            player (int): Player id
            pretty (bool): If it is True returns a list of cards as strings else returns a list of Card objects

        Returns:
            hand (List[str]): Players' hand as a list of strings or list of cards based on 'pretty' flag
        """
        hand = None
        if player == 1:
            hand = self._hand_p1
        elif player == 2:
            hand = self._hand_p2
        else:
            return hand
        if pretty:
            return list(map(str, hand))
        return hand

    def __determine_cards_to_draw(self, len_deck) -> int:
        """
        Gets the number of cards to draw given the deck's length

        Args:
            len_deck (int): Deck's length

        Returns:
            num_cards (int): Number of cards to draw
        """
        return constants.CARDS_BY_HAND if len_deck >= constants.CARDS_BY_HAND else constants.CARDS_TO_USE

    def __draw(self) -> Tuple[List[Card], List[Card]]:
        """
        Gets the hands for the player 1 and 2

        Args:
            None

        Returns:
            drawn_cards_p1 (List[Card]): List of drawn cards for the player 1
            drawn_cards_p2 (List[Card]): List of drawn cards for the player 2
        """
        cards_to_draw_p1 = self.__determine_cards_to_draw(self.get_deck_len_player(1))
        drawn_cards_p1: List[Card] = [self._deck_p1.draw() for i in range(0, cards_to_draw_p1)]

        cards_to_draw_p2 = self.__determine_cards_to_draw(self.get_deck_len_player(2))
        drawn_cards_p2: List[Card] = [self._deck_p2.draw() for i in range(0, cards_to_draw_p2)]
        return drawn_cards_p1, drawn_cards_p2

    def take_hand(self) -> bool:
        """
        Gets the hands for the player 1 and 2 and validates the game status

        Args:
            None

        Raises:
            Exception: When the game is over

        Returns:
            bool: Flag to indicate if takes a new hand or not
        """
        take_new_hand = False
        winner = self.get_winner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't take a hand because the game is over. Winner: {winner}")

        if not self._hand_p1 or not self._hand_p2:
            take_new_hand = True
            new_rank = get_random_num_in_range(
                constants.START_TARGET_RANGE, constants.STOP_TARGET_RANGE)
            self.set_target_rank(new_rank)
            self._hand_p1, self._hand_p2 = self.__draw()
        return take_new_hand

    def __validate_indexes_card_options(self, idx_cards: List[int], len_hand: int) -> bool:
        """
        Validates the provided indexes for the player 1

        Args:
            idx_cards (List[int]): List of indexes to use
            len_hand (int): Deck length

        Raises:
            Exception: When the user provides more than N-defined indexes
            Exception: When the user provides repeating indexes
            Exception: When the user provides non-valid indexes 

        Returns:
            is_ok (bool): True if the list is contains valid indexes
        """
        # Check the len
        len_indexes = len(idx_cards)
        if len_indexes != constants.CARDS_TO_USE:
            raise Exception(f"You can only use {constants.CARDS_TO_USE} cards")

        # Check if there are not repeating elements
        if len(set(idx_cards)) != len_indexes:
            raise Exception('You must provide non-repeating indexes')

        # Check if the indexes are in the correct range
        idx_cards_valid_options = constants.IDX_CARD_OPTIONS if len_hand > constants.CARDS_TO_USE \
            else list(range(0, len_hand))
        for idx in idx_cards:
            if idx not in idx_cards_valid_options:
                idx_cards = [f"{idx}:{card}" for idx, card in enumerate(self.get_hand_player(1))]
                raise Exception(
                    f"{idx} is not a valid index. You can only select {constants.CARDS_TO_USE} of the following "
                    f"indices: {list(idx_cards_valid_options)} -> Your hand is: {idx_cards}")
        return True

    def get_turn_winner(self, idx_cards_p1: List[int], idx_cards_p2: List[int]) -> Union[str, None]:
        """
        Gets the winner of the current turn

        Args:
            idx_cards_p1 (List[int]): List of player 1's indexes to use 
            idx_cards_p2 (List[int]): List of player 2's indexes to use

        Returns:
            turn_winner (str|None): The name of the turn's winner if there is
        """
        winner = self.get_winner(constants.CARDS_TO_USE)
        if winner:
            return winner

        selected_cards_p1 = [self._hand_p1[idx].get_rank() for idx in idx_cards_p1]
        selected_cards_p2 = [self._hand_p2[idx].get_rank() for idx in idx_cards_p2]
        sum_p1 = sum(selected_cards_p1)
        sum_p2 = sum(selected_cards_p2)
        turn_winner = None

        difference_p1 = abs(self.get_target_rank() - sum_p1)
        difference_p2 = abs(self.get_target_rank() - sum_p2)

        if difference_p1 < difference_p2:
            # Turn  Winner : Player 1
            turn_winner = self.get_name_player(1)
            cards_to_add = [self._hand_p2[idx] for idx in idx_cards_p2]
            self._deck_p1.add_cards(cards_to_add)
        elif difference_p2 < difference_p1:
            # Turn  Winner : Player 2
            turn_winner = self.get_name_player(2)
            cards_to_add = [self._hand_p1[idx] for idx in idx_cards_p1]
            self._deck_p2.add_cards(cards_to_add)

        aux_diff_p1 = colored(f'{idx_cards_p1} (dif:{difference_p1})', constants.COLOR_P1)
        aux_diff_p2 = colored(f'(dif:{difference_p2}) {idx_cards_p2}', constants.COLOR_P2)
        aux_sum_p1 = colored(f'{selected_cards_p1} (sum:{sum_p1})', constants.COLOR_P1)
        aux_sum_p2 = colored(f'(sum:{sum_p2}) {selected_cards_p2}', constants.COLOR_P2)
        len_deck_p1 = colored(f'Deck len {self.get_name_player(1)}: {self.get_deck_len_player(1)}', constants.COLOR_P1)
        len_deck_p2 = colored(f'Deck len {self.get_name_player(2)}: {self.get_deck_len_player(2)}', constants.COLOR_P2)
        target_colored = colored(f' Target: {self.get_target_rank()}', 'cyan')

        print(f"HAND: {colored(list(map(str,self._hand_p1)), constants.COLOR_P1)}   {colored(list(map(str, self._hand_p2)), constants.COLOR_P2)}")
        print(f"INDEX: {aux_diff_p1} -> {target_colored} <- {aux_diff_p2}")
        print(f"RANKS: {aux_sum_p1} -> {target_colored} <- {aux_sum_p2}")
        cprint(f"{turn_winner}, Turn: {self.get_num_turns()}", constants.COLOR_WINNER)
        print(f"{len_deck_p1}    {len_deck_p2}")

        self._hand_p1 = []
        self._hand_p2 = []
        return turn_winner

    def play_turn(self, idx_cards_p1: List[int]) -> Tuple[Union[str, None], List[int]]:
        """
        Plays the turn and gets the turn winner 

        Args:
            idx_cards_p1 (List[int]): List of player 1's indexes to use 

        Raises:
            Exception: When the game is over
            Exception: When the player 1 don't have a hand

        Returns:
            turn_winner (str|None): The name of the turn's winner if there is
            idx_cards_p2 (List[int]): List of player 2's used indexes
        """
        winner = self.get_winner(constants.CARDS_TO_USE)
        if winner:
            raise Exception(
                f"You cann't play any more because {winner} won this game.")
        if not self._hand_p1 or not self._hand_p2:
            raise Exception("You don't have a hand.")

        self.__validate_indexes_card_options(idx_cards_p1, len(self.get_hand_player(1)))
        self.increment_num_turn()

        idx_cards_p2 = get_closest_index_cards(self._hand_p2, self.get_target_rank(), constants.CARDS_TO_USE)
        turn_winner = self.get_turn_winner(idx_cards_p1, idx_cards_p2)

        # check again the winner
        self.get_winner(constants.CARDS_TO_USE)
        self.generate_history_turn(idx_cards_p1, idx_cards_p2, turn_winner)
        return turn_winner, idx_cards_p2

    def generate_history_turn(self, idx_cards_p1: List[int], idx_cards_p2: List[int],
                              turn_winner: Union[str, None]) -> None:
        """
        Gets a dictionary of relevant keys values about the current turn

        Args:
            idx_cards_p1 (List[int]): List of player 1's indexes to use
            idx_cards_p2 (List[int]): List of player 2's indexes to use
            turn_winner (Union[str, None]): Winner for the current turn

        Returns:
            None
        """
        select_cards_p1 = [card for idx, card in enumerate(self._hand_p1) if idx in idx_cards_p1]
        select_cards_p2 = [card for idx, card in enumerate(self._hand_p2) if idx in idx_cards_p2]
        sum_select_cards_p1 = sum([card.get_rank() for card in select_cards_p1])
        sum_select_cards_p2 = sum([card.get_rank() for card in select_cards_p2])

        curr_turn = self.get_num_turns()
        turn_dict = dict()
        turn_dict['cardsSelectedPlayer1'] = list(map(str, select_cards_p1))
        turn_dict['cardsSelectedPlayer2'] = list(map(str, select_cards_p2))
        turn_dict['sumCardsSelectedPlayer1'] = sum_select_cards_p1
        turn_dict['sumCardsSelectedPlayer2'] = sum_select_cards_p2
        turn_dict['lenDeckPlayer1'] = self.get_deck_len_player(1)
        turn_dict['lenDeckPlayer2'] = self.get_deck_len_player(2)
        turn_dict['target'] = self.get_target_rank()
        turn_dict['turn'] = curr_turn
        turn_dict['turnWinner'] = turn_winner if turn_winner else 'Tie'
        self._history[curr_turn] = turn_dict
