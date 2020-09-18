import constants


class Card:
    '''
    Card class representing the rank and suit

    Args:
        rank (int): Value that recieves the card 
        suit (str): Special character of the card, e.g. '♣'

    Attributes:
        rank (int): Value that recieves the card 
        suit (str): Special character of the card, e.g. '♣'
    '''

    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return 'rank: {}, suitType: {}'.format(self.rank, self.suit)

    def getPrettyCard(self) -> str:
        '''
        Converts the Card object to a string, e.g. 'K♣'

        Args:
            None

        Returns:
            pretty_card(str): String with the card value and suit 
        '''
        suit = self.suit
        rank = constants.SPECIAL_RANKS.get(self.rank) if (
            self.rank in constants.SPECIAL_RANKS) else str(self.rank)
        return f'{rank:>2s}{suit}'
