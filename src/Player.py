from .Card import Card
from .Stack import Stack, TooFewCardsError
from .PlayerStrategy import PlayerStrategy


class Player():
    def __init__(self, name, strategy):
        self.name: str = name
        self.strategy: PlayerStrategy = strategy
        self.score: int = 0
        self.hand: list[Card] = []
        self.n_plays_to_skip: int = 0


    def __repr__(self):
        return self.name


    def draw_card(self, stack: Stack) -> None:
        try:
            card = stack.draw()
            self.hand.append(card)
            return card
        except TooFewCardsError:
            self.n_plays_to_skip += 1


    def play_card(self, previous_card: Card, legal_moves: list[Card]) -> Card:
        if legal_moves:
            return self.strategy.play(hand=self.hand, top_card=previous_card, legal_moves=legal_moves)
        return None


    def has_card(self, card: Card) -> bool:
        return card in self.hand


    def remove_card(self, card: Card) -> None:
        self.hand.remove(card)


    def tally_points(self) -> int:
        self.score += sum(card.value for card in self.hand)