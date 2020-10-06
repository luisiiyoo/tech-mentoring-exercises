import random
import uuid
from typing import List, Tuple
from numpy.random import permutation
from numpy import sort, argsort
from App.Game.card import Card


def getRandomString(len_str: int = 12) -> str:
    """
    Returns a random string

    Args:
        len_str (int): Random string length desired (Default: 12)

    Returns:
        random_str (str): Random string
    """
    random_str = str(uuid.uuid4()).replace('-', '')
    return random_str[-len_str:]


def getRandomNumInRange(start, stop) -> int:
    """
    Returns a random integer between a range

    Args:
        start (int): Star range
        stop (int): Stop range

    Returns:
        random_int (int): Random integer
    """
    return random.randint(start, stop)


def getRandomIndexes(size_perm: int, num_indxs: int) -> List[int]:
    """
    Returns a list of n-random indexes

    Args:
        size_perm (int): Last possible index (starting in 0)
        num_indxs (int): Number of random indexes wanted

    Returns:
        list_indexes (int): List of n-random indexes
      """
    return list(permutation(size_perm))[0:num_indxs]


def getIndexClosestNumber(sorted_nums: List[int], original_indxs: List[int], target: int) -> Tuple[int, int]:
    """
    Returns the index of the clostest number according to a target

    Args:
        sorted_nums (List[int]): Sorted candidates numbers
        original_indxs (List[int]): Original indexes of the sorted candidates
        target (int): Target number

    Returns:
        indexes (Tuple[int,int]) -> Tuple of the sorted index and the original index that is equal or close value to the target
    """
    first_indx = 0
    last_indx = len(sorted_nums) - 1

    if target <= sorted_nums[first_indx]:
        original_indx = original_indxs[first_indx]
        return (first_indx, original_indx)
    elif target >= sorted_nums[last_indx]:
        original_indx = original_indxs[last_indx]
        return (last_indx, original_indx)
    else:
        best_indx = -1
        best_original_indx = -1
        best_diffence = 999999
        for indx, ele in enumerate(zip(sorted_nums, original_indxs), 0):
            num, original_indx = ele
            diffence = abs(num - target)
            if(diffence < best_diffence):
                best_diffence = diffence
                best_indx = indx
                best_original_indx = original_indx
        return (best_indx, best_original_indx)


def getClosestIndexCards(hand: List[Card], target_rank: int, num_cards_to_use: int) -> List[int]:
    """
    Returns the indexes of the values that approximate to a target value

    Args:
        hand (List[Card]): List of candidate Cards to be used
        target_rank (int): Target to approximate with the Card ranks
        target (int): Target number

    Returns:
        indexes (List[int]) -> List of indexes
    """
    ranks = [card.getRank() for card in hand]
    indx_to_use: List[int] = []

    sorted_ranks = sort(ranks).tolist()
    original_indxs = argsort(ranks).tolist()

    print(f'Hand ranks: {ranks}')
    print(f'Target: {target_rank}')
    for i in range(0, num_cards_to_use):
        indx,  true_indx = getIndexClosestNumber(
            sorted_ranks, original_indxs, target_rank)
        # Remove indx
        sorted_ranks = sorted_ranks[:indx] + sorted_ranks[indx+1:]
        original_indxs = original_indxs[:indx] + original_indxs[indx+1:]
        # Change target
        target_rank = target_rank - ranks[true_indx]

        print(
            f"Card {i+1} : Using rank '{ranks[true_indx]}' (indx: {true_indx})")
        indx_to_use.append(true_indx)
    print(f"Indexes to use: {indx_to_use}")
    return indx_to_use
