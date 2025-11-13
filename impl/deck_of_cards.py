
'''
Question: Deck of Cards Design and Implementation
Imagine you are given a task to design and implement a deck of cards used for a generic card game. A standard deck of 52 playing cards consists of four suits: hearts, diamonds, clubs, and spades. Each suit contains 13 cards, which are ranked from lowest to highest as follows: 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, and Ace.

Hence, 4 suits * 13 cards = 52 cards.

Order of cards values, from least to greatest: 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace

Order of card suits, from least to greatest: Hearts, Diamonds, Clubs, Spades.

Cards are compared by value first. If value is tied, then consider suit.

There are no duplicate cards.

Do not have to consider the special cases like Jokers, or Ace being valued as 1.

Part 1: Design
Class Design: Can you design classes to represent a Card, a Deck, and a Player? What attributes and methods would each class have? How would you represent the suits and ranks of the cards? Consider the usability and flexibility of your design, how could it be extended for different card games?
'''

'''

'''

from enum import Enum
import random

class Suit(Enum):
    Hearts = 1
    Diamonds = 2
    Clubs = 3
    Spades = 4

class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14
    
card_values = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    
class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit 
        
    def __lt__(self, other):
        # if rank equal
        if self.rank == other.rank:
            return self.suit < other.suit
        
        return self.rank < other.rank
        
    def __str__(self):
        # two of hearts
        return f"{self.rank.name} of {self.suit.name}"
        
            
class Player:
    def __init__(self):
        self.cards = []
        
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def __str__(self):
        output = ""
        for c in self.cards:
            output += c.__str__() + "\n"
            
        return output
        
class Deck:
    def __init__(self):
        self.cards = []
        # create cards in order
        for suit in range(Suit.Hearts.value, Suit.Spades.value + 1):
            for rank in range(Rank.Two.value, Rank.Ace.value + 1):
                card = Card(Rank(rank), Suit(suit))
                self.cards.append(card)
                
    def deal(self, num_cards, players):
        # negative numbers or empty players
        
        # assumption, enough cards for the players
        total_needed = num_cards * len(players)
        if total_needed > len(self.cards):
            raise "too many cards for each player"
        
        for n in range(num_cards):
            for p in players:
                # remove from cards
                p.add_card(self.cards.pop())
        

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0,i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]



deck = Deck()
players = []
for i in range(3):
    players.append(Player())
    
deck.shuffle()
deck.deal(5, players)

for i, p in enumerate(players):
    player_cards = p.__str__()
    print(f"player num: {i}, cards: \n{player_cards}")
    