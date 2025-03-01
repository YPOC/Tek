from collections import deque
import random
from .Card import Card, Suit, Rank, BackColor

class Deck():
    def __init__(self, back_color: BackColor) -> None:
        self.back_color = back_color
        self.cards: deque[Card] = self.generate_deck(back_color)

    def generate_deck(self, back_color) -> deque[Card]:
        cards = deque()
        for suit in Suit:
            for rank in Rank:
                card = Card(suit=suit, rank=rank, back=back_color)
                if card.is_valid_rank_suit_combo:
                    cards.append(card)
        return cards


if __name__ == "__main__":

    print("Generating a deck...")
    deck = Deck(BackColor.BLUE)
    print("The deck has", len(deck.cards), "cards")

    total_value = 0
    for card in deck.cards:
        total_value += card.value
    print("Total points value of all cards in the deck is", total_value)

    print("Drawing 7 random cards:")
    for i in range(7):
        card = deck.cards[random.randint(0, len(deck.cards)-1)]
        print(card)
