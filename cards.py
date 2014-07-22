from numpy import ones, array, zeros, round, argmax
from numpy.random import multinomial

class Card :

	def __init__(self, rank, suit ) :
		self.__suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
		self.__rank_names = ['2', '3', '4', '5', '6', '7', '8', '9', '10',\
			'Jack', 'Queen', 'King', 'Ace']
		if isinstance(suit, int) :
			if suit >= 4:
				print('Suit should be a number less than 4 (or the name of suit)')
			else :
				self._suit = suit
		elif isinstance(suit, str) :
			for k in range(4) :
				if suit.upper() == self.__suit_names[k].upper() :
					self._suit = k
					
		if isinstance(rank, int) :
			if rank >= 13:
				print('Rank should be a number less than 13 (or the name of rank)')
			else :
				self._rank = rank
		elif isinstance(rank, str) :
			for k in range(13) :
				if rank.upper() == self.__rank_names[k].upper() :
					self._rank = k

		self.index = zeros( (13, 5), int)
		self.index[rank, 0] = 1
		self.index[rank, suit + 1] = 1
		
	def __str__(self) :
		return "%s of %s" % (self.rank, self.suit)

	def __repr__(self) :
		return "<Card: %s of %s>" % (self.rank, self.suit)

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
		return self.__suit_names[self._suit]
	@suit.deleter
	def suit(self):
		del self._suit
	@suit.setter
	def suit(self, new_suit):
		self._suit = new_suit

	@property
	def rank(self):
		return self.__rank_names[self._rank]
	@rank.deleter
	def rank(self):
		del self._rank
	@rank.setter
	def rank(self, new_rank):
		self._rank = new_rank

	@property
	def suit_names(self):
		return self.__suit_names
	@suit_names.deleter
	def suit_names(self):
		print( "Will not delete suit_names" )
	@suit_names.setter
	def suit_names(self, tmp):
		print( "Will not change suit_names" )

	@property
	def rank_names(self):
		return self.__rank_names
	@rank_names.deleter
	def rank_names(self):
		print( "Will not delete rank_names" )
	@rank_names.setter
	def rank_names(self, tmp):
		print( "Will not change rank_names" )




class Deck() :
	""" A deck of cards. Can also be multiple decks or cards """
	def __init__(self, numberOfDecks = 1 ) :
		self._nDecks = numberOfDecks
		self._cardsRemaining = self._nDecks * 52
		self.__deck_index = ones( (13, 5), int )
		self.__deck_index[:,0]  = 4 * self._nDecks
		self.__deck_index[:,1:] = self._nDecks

	def __repr__(self):
		return '<Deck: Contains %s 52-card deck(s)>' % (self._nDecks)

	def __str__(self) :
		if self._cardsRemaining == 0 :
			stats = zeros( 13 )
		else :
			stats = [self._cardsRemaining]
			#for k in range(13) :
			stats.append( round(self.__deck_index[:,0] / self._cardsRemaining, 4) )
		status = "Cards Remaining : %s \n2 : %s \n3 : %s \n4 : %s \n5 : %s \
			\n6 : %s \n7 : %s \n8 : %s \n9 : %s \n10: %s \nJ : %s \nQ : %s \
			\nK : %s \nA : %s" % tuple( [self._cardsRemaining] + list(self.__deck_index[:,0]))
		return status


	def shuffle(self) :
		self._cardsRemaining = self._nDecks * 52
		self.__deck_index = ones( (13, 5), int )
		self.__deck_index[:,0]  = 4 * self._nDecks
		self.__deck_index[:,1:] = self._nDecks
		return


	def draw(self, n=1) :
		cards = []
		for k in range(n) :
			if self._cardsRemaining == 0 :
				print( "No more cards in Deck, shuffling" )
				self.shuffle()

			rank    = multinomial(1, self.__deck_index[:,0] / self._cardsRemaining, 1)
			rank    = int( argmax( rank ) )
			suit    = multinomial(1, self.__deck_index[rank, 1:]/self.__deck_index[rank, 0])
			suit    = int( argmax( suit ) )
			self.__deck_index[rank,0]      -= 1
			self.__deck_index[rank,suit+1] -= 1

			self._cardsRemaining = self._cardsRemaining - 1
			cards.append( Card( rank, suit ) )
		if n == 1 :
			return cards[0]
		else :
			return cards


	def silentDeal(self, n=1) :
		for k in range(n) :
			if self._cardsRemaining == 0 :
				print( "No more cards in Deck, shuffling" )
				self.shuffle()

			rank    = multinomial(1, self.__deck_index[:,0] / self._cardsRemaining, 1)
			rank    = int( argmax( rank ) )
			suit    = multinomial(1, self.__deck_index[rank, 1:]/self.__deck_index[rank, 0])
			suit    = int( argmax( suit ) )
			self.__deck_index[rank,0]      -= 1
			self.__deck_index[rank,suit+1] -= 1

			self._cardsRemaining = self._cardsRemaining - 1


	def count(self) :
		hilo = (5 * 4 * self._nDecks - sum(self.__deck_index[0:5, 0]) ) - \
			(5 * 4 * self._nDecks - sum(self.__deck_index[8:, 0]) )
		return hilo


	@property
	def cardsRemaining(self):
		return self._cardsRemaining
	@cardsRemaining.deleter
	def cardsRemaining(self):
		print( "Will not delete cardsRemaining" )
	@cardsRemaining.setter
	def cardsRemaining(self, tmp):
		print( "Will not change cardsRemaining" )

	@property
	def nDecks(self) :
		return self._nDecks
	@nDecks.deleter
	def nDecks(self) :
		self.nDecks = 1
		self._cardsRemaining = self._nDecks * 52
		self._cardsDiscarded = 0
	@nDecks.setter
	def nDecks(self, numberOfDecks):
		self._nDecks = numberOfDecks
		self._cardsRemaining = self._nDecks * 52
		self._cardsDiscarded = 0


