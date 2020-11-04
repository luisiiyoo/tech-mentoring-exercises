import json
import random
import uuid
from typing import Any, Dict, List, Tuple
from numpy.random import permutation
from numpy import sort, argsort
from App.models.card import Card
from termcolor import cprint
from .constants import COLOR_P2, COLOR_TIE


def str_to_bool(cad: str) -> bool:
    """
    Converts an string to boolean

    Args:
        cad (str): string

    Returns:
        bool: string converted to boolean
    """
    return not (cad.lower() in ['false', '0'])


def to_dict(obj: Any) -> Dict:
    """
    Converts an instance to a dictionary

    Args:
        obj (Any): Object instance

    Returns:
        Dict: Instance converted to a dictionary
    """
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def get_random_string(len_str: int = 12) -> str:
    """
    Returns a random string

    Args:
        len_str (int): Random string length desired (Default: 12)

    Returns:
        random_str (str): Random string
    """
    random_str = str(uuid.uuid4()).replace('-', '')
    return random_str[-len_str:]


def get_random_num_in_range(start, stop) -> int:
    """
    Returns a random integer between a range

    Args:
        start (int): Star range
        stop (int): Stop range

    Returns:
        random_int (int): Random integer
    """
    return random.randint(start, stop)


def get_random_indexes(size_perm: int, num_idx: int) -> List[int]:
    """
    Returns a list of n-random indexes

    Args:
        size_perm (int): Last possible index (starting in 0)
        num_idx (int): Number of random indexes wanted

    Returns:
        list_indexes (int): List of n-random indexes
      """
    return list(permutation(size_perm))[0:num_idx]


def get_index_closest_number(sorted_nums: List[int], original_idx: List[int], target: int) -> Tuple[int, int]:
    """
    Returns the index of the closest number according to a target

    Args:
        sorted_nums (List[int]): Sorted candidates numbers
        original_idx (List[int]): Original indexes of the sorted candidates
        target (int): Target number

    Returns:
        indexes (Tuple[int,int]) -> Tuple of the sorted index and the original index that is equal or close value to the target
    """
    first_idx = 0
    last_idx = len(sorted_nums) - 1

    if target <= sorted_nums[first_idx]:
        original_idx = original_idx[first_idx]
        return first_idx, original_idx
    elif target >= sorted_nums[last_idx]:
        original_idx = original_idx[last_idx]
        return last_idx, original_idx
    else:
        best_idx = -1
        best_original_idx = -1
        best_difference = 999999
        for idx, ele in enumerate(zip(sorted_nums, original_idx), 0):
            num, original_idx = ele
            difference = abs(num - target)
            if difference < best_difference:
                best_difference = difference
                best_idx = idx
                best_original_idx = original_idx
        return best_idx, best_original_idx


def get_closest_index_cards(hand: List[Card], target_rank: int, num_cards_to_use: int) -> List[int]:
    """
    Returns the indexes of the values that approximate to a target value

    Args:
        hand (List[Card]): List of candidate Cards to be used
        target_rank (int): Target to approximate with the Card ranks
        num_cards_to_use (int): Cards allowed to use

    Returns:
        indexes (List[int]) -> List of indexes
    """
    ranks = [card.get_rank() for card in hand]
    idx_to_use: List[int] = []

    sorted_ranks = sort(ranks).tolist()
    original_idx = argsort(ranks).tolist()

    for i in range(0, num_cards_to_use):
        idx, true_idx = get_index_closest_number(
            sorted_ranks, original_idx, target_rank)
        # Remove idx
        sorted_ranks = sorted_ranks[:idx] + sorted_ranks[idx + 1:]
        original_idx = original_idx[:idx] + original_idx[idx + 1:]
        # Change target
        target_rank = target_rank - ranks[true_idx]
        idx_to_use.append(true_idx)
    return idx_to_use
