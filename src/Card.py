from enum import Enum
from dataclasses import dataclass
import random


class Suit(Enum):
    DIAMONDS = "Diamonds"   # ♦
    CLUBS = "Clubs"         # ♣
    HEARTS = "Hearts"       # ♥
    SPADES = "Spades"       # ♠
    JOKER = "Joker"         # J


class Rank(Enum):
    ACE = "Ace"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    BLACK_JOKER = "Black Joker"
    RED_JOKER = "Red Joker"


class BackColor(Enum):
    BLUE = "blue"
    RED = "red"


@dataclass(frozen=True)
class Card():
    suit: Suit
    rank: Rank
    back: BackColor = None

    def __repr__(self) -> str:
        if self.suit == Suit.JOKER:
            s = f"{self.rank.value}"
        else:
            s = f"{self.rank.value} of {self.suit.value}"

        if self.back is not None:
            s += f" with {self.back.value} back"
        return s


    @property
    def value(self) -> int:
        if self.rank in {Rank.QUEEN, Rank.KING, Rank.ACE}:
            return 10
        elif self.rank == Rank.JACK:
            return 25
        elif self.rank in {Rank.RED_JOKER, Rank.BLACK_JOKER}:
            return 100
        else:
            return int(self.rank.value)


    @property
    def is_joker(self) -> bool:
        return self.suit is Suit.JOKER and self.rank in {Rank.RED_JOKER, Rank.BLACK_JOKER}


    @property
    def is_valid_rank_suit_combo(self) -> bool:
        # used to determine if the pair of rank and suit form a valid card, e.g. a suit of JOKER and a
        # rank of THREE aren't valid.
        return (
            (self.suit is not Suit.JOKER and self.rank not in {Rank.RED_JOKER, Rank.BLACK_JOKER}) or
            self.is_joker
        )


    @property
    def is_special(self):
        # For determining which GameState to choose
        rank = self.rank in {Rank.SEVEN, Rank.TEN, Rank.JACK, Rank.ACE}
        suit = self.suit is Suit.JOKER
        return rank or suit


    @property
    def is_significant(self):
        # For initial drawing of cards
        return self.is_special or self.suit is Suit.CLUBS




if __name__ == "__main__":
    print("Generating a random card:")
    while True:
        suit = list(Suit)[random.randint(0, len(Suit)-1)]
        rank = list(Rank)[random.randint(0, len(Rank)-1)]
        color = list(BackColor)[random.randint(0, len(BackColor)-1)]
        card = Card(suit, rank, color)
        if card.is_valid_rank_suit_combo:
            print(card)
            print(f"This card {'is' if card.is_significant else 'isn\'t'} significant")
            break