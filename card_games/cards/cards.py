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



class Card(object):

    def __init__(self, rank, suit):
        if isinstance(suit, numbers.Integral):
            if suit >= 4:
                raise RuntimeError('Improper suit')
            else:
                self._suit = suit
        elif isinstance(suit, str):
            self._suit = ALL_SUITS[suit.lower()]
                    
        if isinstance(rank, numbers.Integral):
            if rank >= 13:
                raise RuntimeError('Improper rank')
            else :
                self._rank = rank
        elif isinstance(rank, str):
            self._rank = ALL_CARDS[rank.lower()]

        self.index = np.zeros((13, 5), int)
        self.index[rank, 0] = 1
        self.index[rank, suit + 1] = 1
        
    def __str__(self) :
        return "{0} of {1}".format(self.rank, self.suit)

    def __repr__(self) :
        return "<Card: {0} of {1}>".format(self.rank, self.suit)

    def value(self) :
        if self._rank <= 8:
            thevalue = self._rank + 2
        elif (self._rank > 8) and (self._rank <= 11) :
            thevalue = 10
        else :
            thevalue = 1
        return thevalue


    @property
    def suit(self):
        return list(ALL_SUITS.keys())[self._suit]

    @property
    def rank(self):
        return list(ALL_CARDS.keys())[self._rank]


class Deck(object) :
    """ A deck of cards. Can also be multiple decks or cards """
    def __init__(self, numberOfDecks=1):
        self._nDecks = numberOfDecks
        self._cardsRemaining = self._nDecks * 52
        self._deck_index = np.ones((13, 5), int)
        self._deck_index[:, 0]  = 4 * self._nDecks
        self._deck_index[:, 1:] = self._nDecks

    def __repr__(self):
        return '<Deck: Contains {0} 52-card deck(s)>'.format(self._nDecks)

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
        return status.format(self._cardsRemaining,  *self._deck_index[:, 0])

    def shuffle(self):
        self._cardsRemaining    = self._nDecks * 52
        self._deck_index 		= np.ones((13, 5), int)
        self._deck_index[:, 0]  = self._nDecks * 4
        self._deck_index[:, 1:] = self._nDecks
        return

    def draw(self, n=1, quiet=False):
        cards = []
        for k in range(n):
            if self._cardsRemaining == 0:
                print("No more cards in Deck, shuffling")
                self.shuffle()

            rank    = np.random.multinomial(1, self._deck_index[:, 0] / self._cardsRemaining, size=1)
            rank    = int( np.argmax(rank) )
            suit    = np.random.multinomial(1, self._deck_index[rank, 1:]/self._deck_index[rank, 0])
            suit    = int( np.argmax( suit ) )
            self._deck_index[rank, 0]      -= 1
            self._deck_index[rank, suit+1] -= 1

            self._cardsRemaining -= 1
			if not quiet:
            	cards.append(Card(rank, suit))
		if not quiet:
	        if n == 1 :
	            return cards[0]
	        else :
	            return cards

    def count(self):
        hilo = (5 * 4 * self._nDecks - sum(self._deck_index[0:5, 0]) ) - \
            (5 * 4 * self._nDecks - sum(self._deck_index[8:, 0]) )
        return hilo

    @property
    def cardsRemaining(self):
        return self._cardsRemaining

    @property
    def nDecks(self):
        return self._nDecks
