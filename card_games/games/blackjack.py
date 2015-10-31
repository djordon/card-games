from numpy import ones, array, zeros, round
from numpy.random import multinomial
from ..cards import Card, Deck

class Hand(object) :
    def __init__(self):
        self.cards = []
        
    def __str__(self ):
        allCards = '['
        for k in range(len(self.cards)) :
            if k < len(self.cards) - 1 :
                allCards += '%s, ' % ( self.cards[k].__repr__() )
            else :
                allCards += '%s' % ( self.cards[k].__repr__() )
        allCards += '] with value: %s' % ( self.value() )
        return allCards

    def __repr__(self) :
        allCards = '<Hand: ['
        for k in range(len(self.cards)) :
            if k < len(self.cards) - 1 :
                allCards += '%s, ' % ( self.cards[k].__repr__() )
            else :
                allCards += '%s' % ( self.cards[k].__repr__() )
        allCards += ']>'
        return allCards

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        if index < len(self.cards):
            return self.cards[index]
        raise IndexError

    def receiveCard(self, card):
        self.cards.append( card )

    def split(self):
        if len(self.cards) != 2:
            print( "Cannot split, must have 2 and only 2 cards")
        elif self.cards[0].value() != self.cards[1].value() :
            print( "Cannot split, cards must have the same value")
        else :
            newHand = Hand()
            newHand.receiveCard( self.cards.pop(0) )
            return newHand


    def sortCards(self) :
        new_cards = []
        aceCount = [0]
        for card in self.cards :
            if card.rank == 'Ace' :
                aceCount.append( card.suit )
                aceCount[0] += 1
            else :
                new_cards.append( card )
        for k in range( aceCount[0] ) :
            new_cards.append( Card('Ace', aceCount[1+k] ) )
        self.cards = new_cards


    def value(self) :
        handSum1    = 0
        handSum2    = 0
        self.sortCards()
        for k in range( len(self.cards) ) :
            if self.cards[k].rank != 'Ace' :
                handSum1   += self.cards[k].value()
                handSum2   += self.cards[k].value()
            else :         # We have an ace
                if handSum1 == handSum2 :
                    handSum1   += 1
                    handSum2   += 11
                else :     # There is more than one ace in the hand
                    handSum1   += 1
                    handSum2   += 1
        return (handSum1, handSum2)

    def discardHand(self) :
        self.cards = []
        
        
class GenericPlayer(object) :

    def __init__(self ) :
        self.hand = Hand()

    def __str__(self) :
        allCards = 'Hand total is %s.\nContains: %s '\
             % (self.hand.value(), str(self.hand) )
        return allCards

    def receiveCard(self, card) :
        self.hand.receiveCard( card )
        
    def discardHands(self) :
        for hand in self.hands :
            hand.discardHand()


class Player(GenericPlayer) :

    def __init__( self, n=1 ) :
        GenericPlayer.__init__(self)
        self.n              = n
        self.hands          = [self.hand]
        self.active_hand    = 0
        self.SPLITTING      = False
        
    def addHand(self, hand) :
        self.hands.append( hand )

    def activateHand(self, hand):
        for k in range( len(self.hands) ) :
            if self.hands[k] == hand :
                self.active_hand = k
                


    def decision(self, hand, known_cards, dealer_card) :
        current_total = self.hand.value()
        if len(hand) == 2 and hand[0].value() == hand[1].value() and self.SPLITTING :
            hitstay = 3
        elif dealerSum < 21:
            hitstay = 1
        else :
            hitstay = 0
        return hitstay


class Dealer(GenericPlayer):

    def __init__(self, soft17 = True ) :
        GenericPlayer.__init__(self)
        self._stand_soft17 = soft17

    def __str__(self) :
        if self._stand_soft17 :
            text = '(Dealer stands on soft 17): '
        else :
            text = '(Dealer does not stand on soft 17): '
        text += super(Dealer, self).__str__()
        return text
        
    def __repr__(self) :
        if self._stand_soft17 :
            answer = "<Dealer: (SoS17) Hand value is %s>" \
                % (self.hand.value() )
        else :
            answer = "<Dealer: (No SoS17) Hand value is %s>" \
                % ( self.hand.value() )
        return answer
        
    def hitOrStay(self) :
        dealerSum = self.hand.value()
        if dealerSum < 17:
            hitstay = 1
        else :
            hitstay = 0
        return hitstay

    def hand_value(self) :
        return self.hand.value()



class BlackJack(object) :
    """ A deck of cards. Can also be multiple decks or cards """
    def __init__(self, numberOfDecks = 1, numberOfPlayers = 1, soft17 = True, maxRsplt = 0 ) :

        self._players = [ Player(k) for k in range( numberOfPlayers ) ]
        self._dealer  = Dealer( soft17 )
        self._deck    = Deck( numberOfDecks )
        self._stats   = array( (numberOfPlayers, 3), int) # Cols: Win, Lose, Draw

        self._known_cards = numberOfDecks * ones( (13, 5), int)
        self._maxResplits = maxRsplt
        self._penetration = [.5, 1.5]

    def __str__(self) :
        return status

    def deal(self, HIDDEN = False) :
        card = self._deck.draw()
        if HIDDEN == False :
            self._known_cards  += card.index
        return card



    def playGame(self, nGames = 1) :
        for k in range(2) :
            for player in self._players :
                player.receiveCard( self.deal( HIDDEN = False ) )
            if k == 0 :
                self._dealer.receiveCard( self.deal( HIDDEN = True ) )
            else :
                self._dealer.receiveCard( self.deal( HIDDEN = False ) )
        for player in self._players :
            self.playHand( player, player.hand )

        self._known_cards  += self._dealer.hand[0].index
        self.playHand( self._dealer, self._dealer.hand )

        dealers_count   = self._dealer.hand_value()

        for player in self._players :
            for hand in player.hands :
                if dealers_count > 21 :
                    if hand.value()[0] < 22 :
                        hand.cards.pop()
                        if hand.value()[1] > 21 :
                            sblh    = hand.value()[0]
                        else :
                            sblh    = hand.value()[1]
                        player.add_data( win_loss_draw=(1,0,0), total=sblh, whatever=self._dealer.hand[1] )
                    else :
                        hand.cards.pop()
                        sblh    = hand.value()[0]
                        player.add_data( win_loss_draw=(0,1,0), total=sblh, whatever=self._dealer.hand[1] )


    def playHand(self, player, hand, splitCount = 0) :
        while player.decision( hand, self._known_cards, self._dealer.hand[1] ) != 0 :
            playerAction    = player.decision( hand, self._known_cards, self._dealer.hand[1] )
            if playerAction == 1 :
                hand.receiveCard( self.deal( HIDDEN = False ) )
            elif playerAction == 2 and splitCount < self._maxResplits :
                han2 = hand.split()
                player.addHand( han2 )
                
                hand.receiveCard( self._deck.draw() )
                han2.receiveCard( self._deck.draw() )
                
                splitCount += 1
                self.playHand(player, hand, splitCount )
                self.playHand(player, han2, splitCount )
            
