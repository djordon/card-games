from cards import *
from scipy.stats import bernoulli
from random import randint, shuffle

class Pile(object) :
    
    def __init__(self):
        self.cards = []
        self.owner = None

    def __getitem__(self, index):
        if index < len(self.cards) :
            return self.cards[-1 - index]
        raise IndexError

    def append(self, card, owner) :
        self.cards.append(card)
        if card._rank >= 9 :
            self.owner = owner
    
    def putUnder(self, card) :
        newCards = [card]
        for cards in self.cards :
            newCards.append( cards )
        self.cards = newCards
        
    def slapable(self) :
        if len(self.cards) < 2 :
            return False
        elif len(self.cards) == 2 :
            if self.cards[-1]._rank == self.cards[-2]._rank :
                return True
            else :
                return False
        elif len(self.cards) >= 3 :
            if self.cards[-1]._rank == self.cards[-2]._rank :
                return True
            elif self.cards[-1]._rank == self.cards[-3]._rank :
                return True
            else :
                return False
                
    def len(self):
        return len(self.cards)
        
    def give2owner(self):
        if self.owner == None :
            return False

        def cardxPlayed(x) :
            return len(self.cards) >= x-7 and self.cards[7-x]._rank == x
        def afterxNothing(x) :
            notFaceCard = True
            for k in range(1,x-7) :
                notFaceCard *= self.cards[-k]._rank < 9
            return notFaceCard

        for k in range(9,13) :
            if cardxPlayed(k) :
                if afterxNothing(k) :
                    return True
                else :
                    return False
        return False

class ErsPlayer(object) :
    
    def __init__(self, speed = 9) :
        self.speed = [1, speed % 11]
        self.pile  = Pile()
        self.name  = 'Player'
    
    def Slap(self, pile) :
        if pile.slapable() :
            return randint( self.speed[0], self.speed[1] )
        else :
            return 0
    
    def receiveCard(self, card):
        self.pile.append( card, None )
    
    def receivePile(self, pile):
        for card in pile.cards :
            self.pile.putUnder( card )
    
    def deal(self):
        return self.pile.cards.pop()
        


class ErsDummy(ErsPlayer) :
    
    def __init__(self, p = 1) :
        ErsPlayer.__init__(self)
        self.propensityToSlap = p
        self.name = 'Dummy'
    
    def Slap(self, pile) :
        if self.pile.len() == 0 or pile.len() < 2:
            return 0
        else :
            if bernoulli.rvs(self.propensityToSlap) :
                return 10
            else :
                return 0


class EgyptionRatScrew(object) :

    def __init__(self, numberOfPlayers = 1, numberOfDummies = 1, shuffleOrder = False) :
        self.nPlayers  = numberOfPlayers + numberOfDummies
        self._nPlayers = numberOfPlayers
        self._nDummies = numberOfDummies
        self._players  = [ErsPlayer() for k in range(numberOfPlayers)]
        self._players.extend( [ErsDummy() for k in range(numberOfDummies)] )
        if shuffleOrder :
            shuffle(self._players)
        self.__deck    = Deck()
        self._whoDeals = randint(0,self.nPlayers-1)
        self.pile = Pile()
        self.PRINTSTATUS = False
        while self.__deck._cardsRemaining > 0 :
            for player in self._players :
                if self.__deck._cardsRemaining > 0 :
                    player.receiveCard( self.__deck.deal() )
                else :
                    break

    
    def printStatus(self, n = 0, wonPile = None) :
        if self.PRINTSTATUS :
            if n == 0:
                for k in range(self._nPlayers):
                    print("Player has %s cards: %s" \
                        % (self._players[k].pile.len(), self._players[k].pile.cards[-3:] ) )
                for k in range(self.nPlayers-self._nDummies, self.nPlayers):
                    print("Dummy has %s cards: %s" \
                        % (self._players[k].pile.len(), self._players[k].pile.cards[-3:] ) )
            elif n == 1 :
                print("Person %s deals" % (self._whoDeals) )
            elif n == 2 :
                print("The pile has %s cards: %s" % (self.pile.len(), self.pile.cards[-6:]) )
            elif n == 3 :
                print("It was slapable and person %s won the pile!" % (wonPile) )
            elif n == 4 :
                print("The owner is %s" % (self.pile.owner) )
            elif n == 5 :
                print("Player %s wins the pile" % (self.pile.owner))


    def action(self, PRINTSTATUS = False) :
        while self._players[self._whoDeals].pile.len() == 0 :
            self.nPlayers -= 1
            if self.nPlayers == 1 :
                return True
            self._whoDeals = (self._whoDeals + 1) % self.nPlayers
        self.printStatus(0)
        self.printStatus(1)
        self.pile.append( self._players[self._whoDeals].deal(), self._whoDeals )
        self.printStatus(2)

        peopleSlap = self.peopleSlapping()
        if self.pile.slapable() :
            tmp = []
            for k in range( self.nPlayers ):
                if peopleSlap[k] == max(peopleSlap) :
                    tmp.append(k)
            if len(tmp) > 0 :
                k = tmp[randint(0, len(tmp) - 1 )]
                self.printStatus(3,k)
                self._players[k].receivePile( self.pile )
                self.pile = Pile()
                self._whoDeals = k
        else :
            for k in range(self.nPlayers) :
                if peopleSlap[k] > 0 :
                    self.pile.putUnder( self._players[k].deal() )
                    
        GIVEPILE = self.pile.give2owner()
        self.printStatus(2)
        self.printStatus(4)
        if GIVEPILE :
            self.printStatus(5)
            self._players[self.pile.owner].receivePile( self.pile )
            self._whoDeals = self.pile.owner
            self.pile = Pile()
        else :
            if self.pile.len() > 0 :
                if self.pile.cards[-1]._rank >= 9 :
                    self._whoDeals   = (self.pile.owner + 1) % self.nPlayers
                else :
                    if self.pile.owner != None :
                        self._whoDeals   = (self.pile.owner + 1) % self.nPlayers
                    else :
                        self._whoDeals   = (self._whoDeals + 1) % self.nPlayers


    def peopleSlapping(self) :
        myTuple = []
        for player in self._players :
            myTuple.append( player.Slap( self.pile ) )
        return tuple(myTuple)
