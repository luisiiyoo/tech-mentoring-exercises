from termcolor import colored, cprint
from Deck import Deck
import Constants as cg


def getPrettyCard(card):
    suit = card.suitType
    rank = cg.SPECIAL_RANKS.get(card.rank) if (
        card.rank in cg.SPECIAL_RANKS) else str(card.rank)
    return rank + suit


def getPrettyDeck(deck: list):
    return list(map(getPrettyCard, deck))


class CardGame:
    def __init__(self, num_ranks: int, suits: dict, special_ranks: dict):
        deck = Deck(num_ranks, suits, special_ranks)
        self.deck_A, self.deck_B = deck.splitRandomly()
        self.num_turns = 0
        self.cards_discarted = []
        self.printDecks()

    def printDecks(self):
        cprint('Deck_A: {}'.format(getPrettyDeck(self.deck_A)), cg.COLOR_A)
        cprint('Deck_B: {}'.format(getPrettyDeck(self.deck_B)), cg.COLOR_B)

    def __getWinner(self):
        colored_attrs = ['bold']
        size_A = len(self.deck_A)
        size_B = len(self.deck_B)
        if(size_A == 0 and size_B == 0):
            return colored('Tie', cg.COLOR_TIE, attrs=colored_attrs)
        elif(size_A <= 0):
            return colored('Deck_B', cg.COLOR_B, attrs=colored_attrs)
        elif(size_B <= 0):
            return colored('Deck_A', cg.COLOR_A, attrs=colored_attrs)
        else:
            return None

    def getColoredTurnStatusGame(self, card_A, card_B, best_tag):
        len_A = str(len(self.deck_A)+1)
        len_B = str(len(self.deck_B)+1)

        turn_msj = 'Turn: ' + str(self.num_turns)
        card_A_msj = colored('Deck_A({}) - {}'.format(
            len_A, getPrettyCard(card_A)), cg.COLOR_A)
        card_B_msj = colored('{} - Deck_B({})'.format(
            getPrettyCard(card_B), len_B), cg.COLOR_B)

        return '{} => {} ... {} => {}'.format(
            turn_msj, card_A_msj, card_B_msj, best_tag)

    def play(self):
        card_A_tag = colored('Card_A', cg.COLOR_A)
        card_B_tag = colored('Card_B', cg.COLOR_B)
        tie_tag = colored('TIE', cg.COLOR_TIE)
        winner_tag = colored('Winner:', cg.COLOR_WINNER, attrs=[
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
game = CardGame(cg.NUM_RANKS, cg.SUITS, cg.SPECIAL_RANKS)
game.play()
