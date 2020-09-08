class Card:
    def __init__(self, rank: int, suitType: str):
        self.rank = rank
        self.suitType = suitType

    def __str__(self):
        return 'rank: {}, suitType: {}'.format(self.rank, self.suitType)
