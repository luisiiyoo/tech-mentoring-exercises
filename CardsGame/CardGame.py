import math
from termcolor import colored, cprint
from Deck import Deck

SPECIAL_RANKS: dict = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
}
SUITS: dict = {
    'club': '♣',
    'diamond': '♦',
    'heart': '♥',
    'spade': '♠'
}
NUM_CARDS = 52  # 52
NUM_SUITS = len(SUITS)  # 4
NUM_RANKS = math.floor(NUM_CARDS / NUM_SUITS)  # 13


def getPrettyCard(card):
    suit = card.suitType
    rank = SPECIAL_RANKS.get(card.rank) if (
        card.rank in SPECIAL_RANKS) else str(card.rank)
    return rank + suit


def getPrettyDeck(deck: list):
    return list(map(getPrettyCard, deck))


class CardGame:
    def __init__(self, deck_A: list, deck_B: list):
        self.color_A = 'yellow'
        self.color_B = 'green'
        self.color_tie = 'red'
        self.color_winner = 'blue'
        self.deck_A = deck_A
        self.deck_B = deck_B
        self.num_turns = 0
        self.cards_discarted = []
        self.printDecks()

    def printDecks(self):
        cprint('Deck_A: {}'.format(getPrettyDeck(self.deck_A)), self.color_A)
        cprint('Deck_B: {}'.format(getPrettyDeck(self.deck_B)), self.color_B)

    def __getWinner(self):
        colored_attrs = ['bold']
        size_A = len(self.deck_A)
        size_B = len(self.deck_B)
        if(size_A == 0 and size_B == 0):
            return colored('Tie', self.color_tie, attrs=colored_attrs)
        elif(size_A <= 0):
            return colored('Deck_B', self.color_B, attrs=colored_attrs)
        elif(size_B <= 0):
            return colored('Deck_A', self.color_A, attrs=colored_attrs)
        else:
            return None

    def getColoredTurnStatusGame(self, card_A, card_B, best_tag):
        len_A = str(len(self.deck_A)+1)
        len_B = str(len(self.deck_B)+1)

        turn_msj = 'Turn: ' + str(self.num_turns)
        card_A_msj = colored('Deck_A({}) - {}'.format(
            len_A, getPrettyCard(card_A)), self.color_A)
        card_B_msj = colored('{} - Deck_B({})'.format(
            getPrettyCard(card_B), len_B), self.color_B)

        return '{} => {} ... {} => {}'.format(
            turn_msj, card_A_msj, card_B_msj, best_tag)

    def play(self):
        card_A_tag = colored('Card_A', self.color_A)
        card_B_tag = colored('Card_B', self.color_B)
        tie_tag = colored('TIE', self.color_tie)
        winner_tag = colored('Winner:', self.color_winner, attrs=[
                             'reverse', 'blink', 'bold'])

        winner = self.__getWinner()
        while(winner is None):
            self.num_turns += 1
            card_A = self.deck_A.pop(0)
            card_B = self.deck_B.pop(0)
            turn_msj = ''
            if (card_A.rank > card_B.rank):
                turn_msj = self.getColoredTurnStatusGame(
                    card_A, card_B, card_A_tag)
                self.deck_A = [*self.deck_A, card_B, card_A]
            elif (card_B.rank > card_A.rank):

                turn_msj = self.getColoredTurnStatusGame(
                    card_A, card_B, card_B_tag)
                self.deck_B = self.deck_B + [card_A, card_B]
            else:
                turn_msj = self.getColoredTurnStatusGame(
                    card_A, card_B, tie_tag)
                self.cards_discarted.append([card_B, card_A])
            print(turn_msj)
            winner = self.__getWinner()
            # self.printDecks()
        print('{} {}'.format(winner_tag, winner))


# %% MAIN
deck = Deck(NUM_RANKS, SUITS, SPECIAL_RANKS)
deck_A, deck_B = deck.splitRandomly()
game = CardGame(deck_A, deck_B)
game.play()
