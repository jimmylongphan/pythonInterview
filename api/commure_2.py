import dataclasses
import typing

import requests


@dataclasses.dataclass()
class Card:
    code: str
    image: str
    images: typing.Dict
    value: str
    suit: str

    def _get_true_value(self, value: str) -> int:
        match value:
            case "ACE":
                return 14
            case "KING":
                return 13
            case "QUEEN":
                return 12
            case "JACK":
                return 11
            case _:
                return int(value)

    def __lt__(self, other):
        if self._get_true_value(self.value) < self._get_true_value(other.value):
            return True

        if self._get_true_value(self.value) == self._get_true_value(other.value):
            return self.suit < other.suit

        if self._get_true_value(self.value) > self._get_true_value(other.value):
            return False

    def __str__(self):
        return f"{self.value} of {self.suit}"


@dataclasses.dataclass()
class Deck:
    deck_id: str
    shuffled: bool
    remaining: int

# need / at end for urljoin to work
BASE_URL = "https://www.deckofcardsapi.com/api/"


def get_new_deck() -> Deck:
    API = "/deck/new/shuffle/?deck_count=1"

    response = requests.get(f"{BASE_URL}{API}")
    data = response.json()
    deck = Deck(data["deck_id"], shuffled=data["shuffled"], remaining=data["remaining"])

    return deck


def get_cards(deck: Deck, number: int = 1) -> typing.List[int]:
    API = f"/deck/{deck.deck_id}/draw/?count={number}"

    response = requests.get(f"{BASE_URL}{API}")
    data = response.json()

    deck.remaining = data["remaining"]

    cards = []
    for card in data["cards"]:
        cards.append(Card(**card))

    return cards


def main():
    deck_id = get_new_deck()

    cards = get_cards(deck_id, 5)

    sorted_cards = sorted(cards)

    for card in sorted_cards:
        print(card)


if __name__ == "__main__":
    main()
