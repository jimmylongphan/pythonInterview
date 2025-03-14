"""
deck of cards
draw 5 cards
return them in ascending order

j, 2, 3, 5 ,4
2,3,4,5,j

init
1. call shuffle cards endpoint
2. draw cards - hardcode to 5
    takes in a count
3. 

deck - 
cards - class / object representing the cards
    2-10, j-a
        j, 11
        q, 12
        k, 13
        a, 14
    ignore suits for now
    __lt__ function
    compares the value
    
how to sort?

1. call the brand new deck endpoint (assumption)
    - deck not shuffled
    - call shuffle
2. 
--------------------

https://www.deckofcardsapi.com/
### sample output

7 of HEARTS
8 of DIAMONDS
10 of CLUBS
JACK of DIAMONDS
JACK of SPADES
"""

import json
import requests
from heapq import heapify, heappush, heappop

class Card:
    face_cards = ["JACK", "QUEEN", "KING", "ACE"]
    max_num_card = 10

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

        # converted the value to an int check if it is a face card, then assign a int value to it
        if value in self.face_cards:
            self.converted_value = self.max_num_card + self.face_cards.index(value) + 1
        else:
            self.converted_value = int (value)

    def __lt__(self, other):
        return self.converted_value < other.converted_value
    
class Deck:
    # min heap of cards
    def __init__(self):
        self.cards = []
        heapify(self.cards)

    def add_card(self, card: Card):
        heappush(self.cards, card)

    def draw_card(self) -> Card:
        return heappop(self.cards)

class SortCard:
    new_shuffle_endpoint = "https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
    draw_endpoint = "https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}"
    deck_id = -1

    def __init__(self):
        # create a new deck
        self.deck = Deck()

        # call the api to initialize and shuffle the deck
        response = requests.post(self.new_shuffle_endpoint)

        if response.status_code == 200:
            response_json = response.json()
            self.deck_id = response_json["deck_id"]

        # TODO handle errors cases


    def draw_cards(self, num_cards) -> list[Card]:
        # generate the url to make request
        draw_endpoint_url = self.draw_endpoint.format(deck_id=self.deck_id, count=num_cards)

        response = requests.get(draw_endpoint_url)

        # assumption handling success cases
        if response.status_code == 200:
            response_json = response.json()
            cards_json = response_json["cards"]
            for c_json in cards_json:
                card_object = Card(c_json["value"], c_json["suit"])
                self.deck.add_card(card_object)

            # print the cards
            for _ in range(num_cards):
                card_object = self.deck.draw_card()
                print(f"card value: {card_object.value}")

        # TODO handle error cases


sort_card = SortCard()
sort_card.draw_cards(5)
