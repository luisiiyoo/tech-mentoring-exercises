import constants


class Card:
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return 'rank: {}, suitType: {}'.format(self.rank, self.suit)

    def getPrettyCard(self) -> str:
        suit = self.suit
        rank = constants.SPECIAL_RANKS.get(self.rank) if (
            self.rank in constants.SPECIAL_RANKS) else str(self.rank)
        return f'{rank:>2s}{suit}'
