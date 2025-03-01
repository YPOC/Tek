from collections import deque
from .Card import Card
from .Deck import Deck, BackColor
from .ShufflingStrategy import RandomShufflingStrategy


class TooFewCardsError(Exception):
    pass


class Stack():
    def __init__(
            self,
            decks: list[Deck],
            shuffling_strategy = RandomShufflingStrategy
        ) -> None:
        # self.cards: deque = self.generate_stack(*decks)
        self.cards: deque = self.generate_stack(*decks)
        self._shuffling_strategy = shuffling_strategy

    def generate_stack(self, *args: Deck) -> deque:
        cards = deque()
        for deck in args:
            cards.extend(deck.cards)
        return cards

    def shuffle(self, strategy: RandomShufflingStrategy = None) -> None:
        if strategy is not None:
            strategy.shuffle(self.cards)
        else:
            self._shuffling_strategy.shuffle(self.cards)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise TooFewCardsError("You're trying to draw more cards than what is available")
        return self.cards.popleft()
    
    # def draw_multiple(self, n_cards) -> list[Card]:
    #     if n_cards > len(self.cards):
    #         raise TooFewCardsError("You're trying to draw more cards than what is available")
    #     cards = self.cards[:n_cards]
    #     self.cards = self.cards[n_cards:]
    #     return cards

    def cut(at: int):
        raise NotImplementedError()
        # It should be possible to cut the deck in two parts such that you can peek at the lowest card
        # of the upper part and draw up to 7 significant cards

    @property
    def size(self):
        return len(self.cards)


if __name__ == "__main__":
    print("Generating a draw stack from 2 decks...")
    stack = Stack(decks = [Deck(BackColor.BLUE), Deck(BackColor.RED)])
    stack.shuffle()
    print("Drawing 7 random cards:")
    for i in range(7):
        print(stack.draw())