
"""
deck of cards
draw 5 cards
return them in ascending order

j, 2, 3, 5 ,4
2,3,4,5, j

--------------------

https://www.deckofcardsapi.com/
### sample output

7 of HEARTS
8 of DIAMONDS
10 of CLUBS
JACK of DIAMONDS
JACK of SPADES
"""

from collections import deque
import json
import requests

from urllib.parse import urljoin

# need / at the end
BASE_URL = "https://www.deckofcardsapi.com/api/"

FACE_VALUES = {
    "JACK": 11,
    "QUEEN": 12,
    "KING": 13,
    "ACE": 14
}


class Card:
    def __init__(self, name: str, suit: str):
        self.suit = suit
        self.name = name

        if name in FACE_VALUES:
            self.value = FACE_VALUES[name]
        else:
            self.value = int(name)

    def __lt__(self, other):
        # ascending order
        return self.value > other.value

    def __repr__(self):
        return f"name: {self.name}\t\tsuit: {self.suit}\tvalue: {self.value}"

class Deck:
    def __init__(self, id: str):
        self.id = id
        self.cards = deque()

    def add_card(self, card: Card):
        self.cards.append(card)

    def add_cards(self, card: list[Card]):
        self.cards.extend(card)

    def sort_deck(self):
        self.cards = deque(sorted(self.cards))

    def draw_card(self) -> Card:
        if self.cards:
            return self.cards.popleft()

    def __repr__(self):
        output = ""
        for card in self.cards:
            output += repr(card) + "\n"
        return output


def get_new_deck() -> int:
    endpoint = "deck/new/shuffle/?deck_count=1"

    url = urljoin(BASE_URL, endpoint)
    response = requests.get(url=url)

    data_json = response.json()
    deck_id = data_json["deck_id"]
    return deck_id

def draw_cards(deck_id: str, count: int) -> list[Card]:
    endpoint = f"deck/{deck_id}/draw/?count={count}"

    url = urljoin(BASE_URL, endpoint)

    response = requests.get(url=url)
    data_json = response.json()

    cards = []
    json_cards = data_json["cards"]
    for c in json_cards:
        suit = c["suit"]
        value = c["value"]
        card = Card(suit=suit, name=value)
        cards.append(card)

    return cards


def main():
    deck_id = get_new_deck()
    deck = Deck(deck_id)
    print(f"New deck id: {deck_id}")

    cards = draw_cards(deck_id=deck_id, count=5)
    deck.add_cards(cards)

    deck.sort_deck()
    print(deck)



if __name__ == "__main__":
    main()
