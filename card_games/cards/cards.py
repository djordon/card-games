import numpy as np
import numbers

ALL_SUITS = {
    'clubs'    : 0,
    'diamonds' : 1,
    'hearts'   : 2,
    'spades'   : 3
}
ALL_CARDS = {
    '2'     : 0,
    '3'     : 1,
    '4'     : 2,
    '5'     : 3,
    '6'     : 4,
    '7'     : 5,
    '8'     : 6,
    '9'     : 7,
    '10'    : 8,
    'jack'  : 9,
    'queen' : 10,
    'king'  : 11,
    'ace'   : 12
}

ALL_SUITS_MAP = {val: key for key, val in ALL_SUITS.items()}
ALL_CARDS_MAP = {val: key for key, val in ALL_CARDS.items()}


class Card(object):

    def __init__(self, rank, suit):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return ALL_SUITS_MAP[self._suit]

    @property
    def rank(self):
        return ALL_CARDS_MAP[self._rank]

    @property
    def index(self):
        index = np.zeros((13, 5), int)
        index[self._rank, 0] = 1
        index[self._rank, self._suit + 1] = 1
        return index

    def __str__(self) :
        return "{0} of {1}".format(self.rank, self.suit)

    def __repr__(self) :
        return "<Card: {0} of {1}>".format(self.rank, self.suit)

    def value(self) :
        if self._rank <= 8:
            thevalue = self._rank + 2
        elif 8 < self._rank <= 11:
            thevalue = 10
        else :
            thevalue = 1
        return thevalue

    def crazy_changes(self):
        pass

class Deck(object) :
    """ A deck of cards. Can also be multiple decks or cards """
    def __init__(self, num_decks=1):
        self.cards_remaining = num_decks * 52

        self.nDecks      = num_decks
        self._deck_index = np.ones((13, 5), int)

        self._deck_index[:, 0]  = 4 * num_decks
        self._deck_index[:, 1:] = num_decks

    def __repr__(self):
        return '<Deck: Contains {0} 52-card deck(s)>'.format(self.nDecks)

    def status(self):
        status = (
            'Cards Remaining : {0} \n'
            '2 : {1} \n'
            '3 : {2} \n'
            '4 : {3} \n'
            '5 : {4} \n'
            '6 : {5} \n'
            '7 : {6} \n'
            '8 : {7} \n'
            '9 : {8} \n'
            '10: {9} \n'
            'J : {10} \n'
            'Q : {11} \n'
            'K : {12} \n'
            'A : {13}')
        print(status.format(self.cards_remaining,  *self._deck_index[:, 0]))

    def shuffle(self):
        self.cards_remaining   = self.nDecks * 52
        self._deck_index        = np.ones((13, 5), int)
        self._deck_index[:, 0]  = self.nDecks * 4
        self._deck_index[:, 1:] = self.nDecks
        return

    def draw(self, n=1, quiet=False):
        cards = []

        for k in range(n):
            if self.cards_remaining == 0:
                print("No more cards in Deck, shuffling")
                self.shuffle()

            r_probs = self._deck_index[:, 0] / self.cards_remaining
            rank    = np.random.multinomial(1, r_probs)
            rank    = rank.argmax()

            s_probs = self._deck_index[rank, 1:] / self._deck_index[rank, 0]
            suit    = np.random.multinomial(1, s_probs)
            suit    = suit.argmax()

            self._deck_index[rank, 0]      -= 1
            self._deck_index[rank, suit+1] -= 1

            self.cards_remaining -= 1

            if not quiet:
                cards.append(Card(rank, suit))

        if not quiet:
            if n == 1 :
                return cards[0]
            else :
                return cards
